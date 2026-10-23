import copy
import re
from urllib.parse import urlsplit, parse_qsl


class Problem(Exception):
    def __init__(self, message, status=400, code="INVALID_REQUEST"):
        super().__init__(message)
        self.status, self.code = status, code


def require(ok, message):
    if not ok:
        raise Problem(message)


def obj(value, allowed, required=()):
    require(isinstance(value, dict), "Se esperaba un objeto JSON")
    require(not (set(value) - set(allowed)), "Campos desconocidos: " + ", ".join(sorted(set(value) - set(allowed))))
    require(set(required) <= set(value), "Faltan campos: " + ", ".join(sorted(set(required) - set(value))))
    return value


def text(value, label, maximum=2000, empty=False):
    require(isinstance(value, str) and (empty or bool(value.strip())) and len(value) <= maximum,
            f"{label}: texto requerido, máximo {maximum} caracteres")
    require(not any(ord(c) < 32 and c not in "\n\t" for c in value), f"{label}: caracteres de control")
    return value


def integer(value, label, low=1, high=1_000_000_000):
    require(type(value) is int and low <= value <= high, f"{label}: entero entre {low} y {high}")
    return value


def ident(value, label):
    require(isinstance(value, str) and bool(re.fullmatch(r"[0-9]{1,40}", value)), f"{label}: ID numérico como string")
    return value


def https(value, label="URL"):
    text(value, label, 4096)
    try:
        u = urlsplit(value)
        require(u.scheme == "https" and bool(u.hostname) and u.port in (None, 443)
                and not u.username and not u.password and not u.fragment
                and not any(c.isspace() for c in value), f"{label}: usá HTTPS sin credenciales ni fragmentos")
    except ValueError:
        raise Problem(f"{label}: URL inválida")
    return value


COPY_FIELDS = {"primary_text", "headline", "description", "cta", "destination_url", "display_url_mode", "display_url", "utm_template"}
CTAS = {"LEARN_MORE", "SHOP_NOW", "SIGN_UP", "BOOK_TRAVEL", "CONTACT_US", "DOWNLOAD", "GET_QUOTE", "SUBSCRIBE", "APPLY_NOW"}
DISPLAY_MODES = ("AUTO", "CUSTOM", "OMIT_CUSTOM")
MACROS = {"campaign.id", "adset.id", "ad.id", "campaign.name", "adset.name", "ad.name", "placement", "site_source_name"}


def normalize_utm(value):
    """Acepta lo que la gente suele pegar: '?a=b', una URL completa o macros codificadas."""
    if not isinstance(value, str):
        return value
    value = value.strip()
    if re.match(r"https?://", value, re.I):
        value = urlsplit(value).query
    value = value.lstrip("?&")
    return re.sub(r"%7B%7B", "{{", re.sub(r"%7D%7D", "}}", value, flags=re.I), flags=re.I)


def utm(value):
    text(value, "utm_template", 2000, empty=True)
    require(not value.startswith(("?", "&")) and "#" not in value and "\n" not in value,
            "UTM: pegá parámetros sin ? inicial, # ni saltos de línea")
    pairs = parse_qsl(value, keep_blank_values=True)
    require(not value or (len(pairs) > 0 and all("=" in x for x in value.split("&"))), "UTM: formato clave=valor&clave=valor")
    keys = [k for k, _ in pairs]
    require(len(keys) == len(set(keys)), "UTM: hay claves duplicadas")
    require(all(re.fullmatch(r"[A-Za-z0-9_.-]+", k) for k in keys), "UTM: clave inválida")
    require(all(m in MACROS for m in re.findall(r"\{\{([^{}]+)\}\}", value)), "UTM: macro no admitida")
    require(not re.search(r"[{}]", re.sub(r"\{\{[^{}]+\}\}", "", value)), "UTM: llaves inválidas")
    return value


def bare_host(url):
    host = (urlsplit(url).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def copy_fields(raw, complete=False):
    obj(raw, COPY_FIELDS, ("primary_text", "destination_url") if complete else ())
    d = copy.deepcopy(raw)
    if "utm_template" in d:
        d["utm_template"] = normalize_utm(d["utm_template"])
    if isinstance(d.get("display_url"), str) and d["display_url"].strip() and "://" not in d["display_url"]:
        d["display_url"] = "https://" + d["display_url"].strip()
    if complete:
        d = {"headline": "", "description": "", "cta": "LEARN_MORE", "display_url_mode": "AUTO",
             "display_url": "", "utm_template": "", **d}
    for k in ("primary_text", "headline", "description"):
        if k in d:
            text(d[k], k, {"primary_text": 5000, "headline": 255, "description": 255}[k], empty=k != "primary_text")
    if "cta" in d:
        require(d["cta"] in CTAS, "CTA no admitido")
    if "destination_url" in d:
        https(d["destination_url"], "destination_url")
    if "display_url_mode" in d:
        require(d["display_url_mode"] in DISPLAY_MODES, "display_url_mode inválido; ocultar siempre no está garantizado por Meta")
    if "display_url" in d:
        text(d["display_url"], "display_url", 255, empty=True)
    if "utm_template" in d:
        utm(d["utm_template"])
    if complete:
        if d["display_url_mode"] == "CUSTOM":
            https(d["display_url"], "display_url")
            require(bare_host(d["display_url"]) == bare_host(d["destination_url"]),
                    "El enlace visible debe usar el mismo dominio que el destino (www. opcional)")
        else:
            require(not d["display_url"], "Borrá display_url si el modo no es CUSTOM")
        dest_keys = {k for k, _ in parse_qsl(urlsplit(d["destination_url"]).query, keep_blank_values=True)}
        repeated = sorted(dest_keys.intersection(k for k, _ in parse_qsl(d["utm_template"], keep_blank_values=True)))
        require(not repeated, "Parámetros repetidos entre la URL de destino y el UTM: " + ", ".join(repeated)
                + ". Quitalos de la URL de destino; el UTM los agrega en url_tags.")
    return d


PROFILE_FIELDS = {"account_id", "page_id", "instagram_user_id", "pixel_id", "currency", "countries", "age_min", "age_max",
                  "advantage_audience", "objective", "daily_budget_minor", "max_batch_daily_budget_minor", "bid_cap_minor", "defaults"}


def profile(raw):
    obj(raw, PROFILE_FIELDS, ("account_id", "page_id", "currency", "countries", "objective", "daily_budget_minor", "max_batch_daily_budget_minor", "defaults"))
    p = {"age_min": 18, "age_max": 65, "advantage_audience": False, **copy.deepcopy(raw)}
    require(isinstance(p["account_id"], str) and bool(re.fullmatch(r"act_[0-9]{1,40}", p["account_id"])), "account_id debe ser act_123...")
    for k in ("page_id", "instagram_user_id", "pixel_id"):
        if k in p:
            ident(p[k], k)
    require(p["currency"] in ("ARS", "USD", "EUR", "BRL"), "Monedas soportadas: ARS, USD, EUR, BRL (100 unidades menores = 1 unidad)")
    require(isinstance(p["countries"], list) and 1 <= len(p["countries"]) <= 25, "countries: lista de países ISO de dos letras")
    require(all(isinstance(c, str) and re.fullmatch(r"[A-Z]{2}", c) for c in p["countries"]), "countries: códigos ISO en mayúsculas")
    integer(p["age_min"], "age_min", 18, 65)
    integer(p["age_max"], "age_max", p["age_min"], 65)
    require(type(p["advantage_audience"]) is bool, "advantage_audience: true o false")
    # Meta: con Advantage+ audience, age_min solo 18-25 y age_max fijo en 65.
    require(not p["advantage_audience"] or (p["age_min"] <= 25 and p["age_max"] == 65),
            "Con advantage_audience=true Meta solo admite age_min 18-25 y age_max 65")
    require(p["objective"] in ("SALES", "TRAFFIC"), "objective: SALES o TRAFFIC, destino sitio web")
    require(p["objective"] != "SALES" or bool(p.get("pixel_id")), "SALES necesita pixel_id y evento PURCHASE configurado en Meta")
    for k in ("daily_budget_minor", "max_batch_daily_budget_minor", "bid_cap_minor"):
        if k in p:
            integer(p[k], k)
    require(p["daily_budget_minor"] <= p["max_batch_daily_budget_minor"], "Presupuesto supera el máximo por lote")
    p["defaults"] = copy_fields(p["defaults"], complete=True)
    return p


REQUEST_FIELDS = {"name", "structure", "media", "shared", "daily_budget_minor", "bid_cap_minor", "target_status"}


def request(raw, p):
    obj(raw, REQUEST_FIELDS, ("name", "structure", "media"))
    r = {"target_status": "PAUSED", **copy.deepcopy(raw)}
    text(r["name"], "name", 100)
    require(r["structure"] in ("BID_CAP_1_1_10", "ABO_1_1_1"), "structure inválida")
    require(r["target_status"] in ("PAUSED", "ACTIVE"), "target_status inválido")
    require(isinstance(r["media"], list) and 1 <= len(r["media"]) <= 50, "Se requieren entre 1 y 50 creativos")
    require(r["structure"] != "BID_CAP_1_1_10" or len(r["media"]) == 10, "BID_CAP_1_1_10 requiere exactamente 10 creativos")
    r["daily_budget_minor"] = integer(r.get("daily_budget_minor", p["daily_budget_minor"]), "daily_budget_minor")
    count = 1 if r["structure"] == "BID_CAP_1_1_10" else len(r["media"])
    require(count * r["daily_budget_minor"] <= p["max_batch_daily_budget_minor"], "El presupuesto diario agregado del lote supera max_batch_daily_budget_minor")
    if r["structure"] == "BID_CAP_1_1_10":
        r["bid_cap_minor"] = integer(r.get("bid_cap_minor", p.get("bid_cap_minor")), "bid_cap_minor")
    else:
        require("bid_cap_minor" not in r, "ABO usa LOWEST_COST_WITHOUT_CAP; no acepta bid_cap_minor")
    shared = copy_fields(r.get("shared", {}))
    for m in r["media"]:
        obj(m, {"kind", "url", "image_hash", "video_id", "thumbnail_url", "overrides"}, ("kind",))
        require(m["kind"] in ("image", "video"), "kind: image o video")
        if m["kind"] == "image":
            require(("url" in m) != ("image_hash" in m), "Imagen: url o image_hash, exactamente uno")
            require(not ({"video_id", "thumbnail_url"} & set(m)), "Imagen: campos de video no válidos")
            if "image_hash" in m:
                require(isinstance(m["image_hash"], str) and bool(re.fullmatch(r"[A-Za-z0-9_-]{1,128}", m["image_hash"])), "image_hash inválido")
        else:
            require(("url" in m) != ("video_id" in m), "Video: url o video_id, exactamente uno")
            require("image_hash" not in m, "Video: image_hash no válido")
            # Sin portada propia se usa la miniatura preferida que Meta genera al procesar el video.
            if "thumbnail_url" in m:
                https(m["thumbnail_url"], "thumbnail_url")
            if "video_id" in m:
                ident(m["video_id"], "video_id")
        if "url" in m:
            https(m["url"], "media.url")
        m["copy"] = copy_fields({**p["defaults"], **shared, **copy_fields(m.pop("overrides", {}))}, complete=True)
    r.pop("shared", None)
    return r
