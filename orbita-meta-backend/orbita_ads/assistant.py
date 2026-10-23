"""Asistente de Meta Ads con Claude. Loop manual de herramientas: cada llamada pasa por tools.execute con permisos del backend."""
import json
import os
import re
import uuid
from . import tools, validation as v

MODEL = os.environ.get("ORBITA_AI_MODEL", "claude-opus-5-5")
MAX_STEPS = 12


def load_permissions():
    raw = os.environ.get("ORBITA_AI_PERMISSIONS")
    if raw is None:
        return tools.ALL_PERMISSIONS
    chosen = frozenset(x.strip() for x in raw.split(",") if x.strip())
    v.require(chosen <= tools.ALL_PERMISSIONS, "ORBITA_AI_PERMISSIONS contiene permisos desconocidos")
    return chosen


class Assistant:
    def __init__(self, service, client=None, permissions=None):
        self.service = service
        self._client = client
        self.permissions = load_permissions() if permissions is None else frozenset(permissions)

    def client(self):
        if self._client is not None:
            return self._client
        try:
            import anthropic
        except ImportError:
            raise v.Problem("Falta el paquete anthropic: volvé a ejecutar el iniciador", 503, "AI_UNAVAILABLE")
        key = self.service.secrets.get("anthropic_api_key")
        if not key:
            raise v.Problem("Cargá la API key de Anthropic en Conexión para usar el asistente", 409, "AI_KEY_MISSING")
        return anthropic.Anthropic(api_key=key)

    def create(self, client, messages):
        request = dict(model=MODEL, max_tokens=16000, system=tools.SYSTEM_PROMPT_ES, tools=tools.TOOLS, messages=messages,
                       output_config={"effort": "medium"}, cache_control={"type": "ephemeral"},
                       # Si un clasificador rechaza el pedido, la API lo reintenta en el modelo de respaldo recomendado.
                       betas=["server-side-fallback-2026-07-01"], fallbacks="default")
        try:
            import anthropic
        except ImportError:  # solo con un cliente inyectado (pruebas sin el paquete)
            return client.beta.messages.create(**request)
        try:
            return client.beta.messages.create(**request)
        except anthropic.AuthenticationError:
            raise v.Problem("La API key de Anthropic no es válida", 502, "AI_AUTH")
        except anthropic.PermissionDeniedError:
            raise v.Problem("La API key de Anthropic no tiene permiso para este modelo", 502, "AI_PERMISSION")
        except anthropic.RateLimitError:
            raise v.Problem("Anthropic limitó los pedidos; probá en un minuto", 503, "AI_RATE_LIMIT")
        except anthropic.APIStatusError as e:
            raise v.Problem(f"Anthropic respondió {e.status_code}; probá de nuevo", 502, "AI_ERROR")
        except anthropic.APIConnectionError:
            raise v.Problem("Sin conexión con Anthropic", 503, "AI_CONNECTION")

    def history(self, conversation):
        return {"conversation_id": conversation,
                "messages": [{"role": m["role"], "text": m["visible"]} for m in self.service.store.messages(conversation) if m["visible"]]}

    def send(self, conversation, text):
        v.text(text, "mensaje", 8000)
        if conversation is None:
            conversation = uuid.uuid4().hex
        v.require(isinstance(conversation, str) and bool(re.fullmatch(r"[a-f0-9]{32}", conversation)), "conversation_id inválido")
        client = self.client()
        store = self.service.store
        # Historial completo y sin editar (bloques de thinking incluidos): se agrega, nunca se reescribe.
        messages = [{"role": m["role"], "content": m["content"]} for m in store.messages(conversation)]
        messages.append({"role": "user", "content": text})
        store.append_message(conversation, "user", text, visible=text)
        actions, reply, stop = [], "", None
        for _ in range(MAX_STEPS):
            response = self.create(client, messages)
            content = [block.to_dict() for block in response.content]
            said = "\n".join(b.text for b in response.content if b.type == "text").strip()
            messages.append({"role": "assistant", "content": content})
            store.append_message(conversation, "assistant", content, visible=said or None)
            reply, stop = said or reply, response.stop_reason
            if stop == "pause_turn":
                continue
            if stop != "tool_use":
                break
            results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                out = tools.execute(self.service, block.name, block.input, self.permissions)
                actions.append({"tool": block.name, "ok": not out.get("is_error"), "error": out.get("error")})
                result = {"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(out, ensure_ascii=False, default=str)}
                if out.get("is_error"):
                    result["is_error"] = True
                results.append(result)
            messages.append({"role": "user", "content": results})
            store.append_message(conversation, "user", results)
        else:
            reply = (reply + "\n\n" if reply else "") + "Corté acá para no seguir en bucle. Decime cómo seguimos."
        if stop == "refusal":
            reply = "No puedo ayudar con ese pedido."
        elif stop == "max_tokens":
            reply += "\n\n(La respuesta quedó cortada.)"
        return {"conversation_id": conversation, "reply": reply, "actions": actions, "stop_reason": stop}
