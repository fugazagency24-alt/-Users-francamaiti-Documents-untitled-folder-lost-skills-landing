import hashlib
import json
from . import validation as v


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def ref(key, field="id"):
    return {"$ref": f"{key}.{field}"}


def display_link(c):
    """AUTO: dominio limpio del destino. CUSTOM: el del usuario. OMIT_CUSTOM: no se envía; Meta usa su valor por defecto."""
    if c["display_url_mode"] == "CUSTOM":
        return c["display_url"]
    if c["display_url_mode"] == "AUTO":
        return "https://" + v.bare_host(c["destination_url"])
    return None


def plan(raw, raw_profile):
    p = v.profile(raw_profile)
    r = v.request(raw, p)
    ops = []
    account = p["account_id"]
    def add(key, kind, path, body):
        ops.append({"key": key, "kind": kind, "path": path, "body": body})
    # Prepare ALL assets before creating campaigns. No local URL fetch on preview.
    for i, m in enumerate(r["media"]):
        k = f"media{i}"
        if "image_hash" in m:
            add(k, "existing", "", {"hash": m["image_hash"]})
        elif "video_id" in m:
            add(k, "existing", "", {"id": m["video_id"]})
        elif m["kind"] == "image":
            add(k, "image", f"{account}/adimages", {"url": m["url"]})
        else:
            add(k, "video", f"{account}/advideos", {"file_url": m["url"], "name": f"{r['name']} {i+1}"})
        if m["kind"] == "video":
            add(f"ready{i}", "video_ready", ref(k), {})
            if "thumbnail_url" in m:
                add(f"thumb{i}", "image", f"{account}/adimages", {"url": m["thumbnail_url"]})
            else:
                add(f"thumb{i}", "video_thumbnail", ref(k), {})
    groups = [list(range(10))] if r["structure"] == "BID_CAP_1_1_10" else [[i] for i in range(len(r["media"]))]
    for g, indices in enumerate(groups):
        name = f"{r['name']} | {r['structure']} | {g+1:02d}"
        add(f"campaign{g}", "campaign", f"{account}/campaigns", {
            "name": name, "objective": "OUTCOME_SALES" if p["objective"] == "SALES" else "OUTCOME_TRAFFIC",
            "buying_type": "AUCTION", "status": "PAUSED", "special_ad_categories": [],
            "is_adset_budget_sharing_enabled": False,
        })
        body = {"name": name + " | conjunto", "campaign_id": ref(f"campaign{g}"), "daily_budget": r["daily_budget_minor"],
                "billing_event": "IMPRESSIONS", "optimization_goal": "OFFSITE_CONVERSIONS" if p["objective"] == "SALES" else "LINK_CLICKS",
                "destination_type": "WEBSITE", "status": "PAUSED",
                "bid_strategy": "LOWEST_COST_WITH_BID_CAP" if r["structure"] == "BID_CAP_1_1_10" else "LOWEST_COST_WITHOUT_CAP",
                "targeting": {"geo_locations": {"countries": p["countries"]}, "age_min": p["age_min"], "age_max": p["age_max"],
                              # Desde v23 Meta exige declararlo al crear el conjunto; 0 respeta la segmentación configurada.
                              "targeting_automation": {"advantage_audience": int(p["advantage_audience"])}}}
        if r["structure"] == "BID_CAP_1_1_10":
            body["bid_amount"] = r["bid_cap_minor"]
        if p["objective"] == "SALES":
            body["promoted_object"] = {"pixel_id": p["pixel_id"], "custom_event_type": "PURCHASE"}
        add(f"adset{g}", "adset", f"{account}/adsets", body)
        for i in indices:
            m, c = r["media"][i], r["media"][i]["copy"]
            story = {"page_id": p["page_id"]}
            if p.get("instagram_user_id"):
                story["instagram_user_id"] = p["instagram_user_id"]
            cta = {"type": c["cta"], "value": {"link": c["destination_url"]}}
            shown = display_link(c)
            if m["kind"] == "image":
                data = {"link": c["destination_url"], "message": c["primary_text"], "name": c["headline"],
                        "description": c["description"], "image_hash": ref(f"media{i}", "hash"), "call_to_action": cta}
                if shown:
                    data["caption"] = shown
                story["link_data"] = data
            else:
                if shown:
                    cta["value"]["link_caption"] = shown
                cover = {"image_hash": ref(f"thumb{i}", "hash")} if "thumbnail_url" in m else {"image_url": ref(f"thumb{i}", "url")}
                story["video_data"] = {"video_id": ref(f"media{i}"), **cover,
                                       "message": c["primary_text"], "title": c["headline"],
                                       "link_description": c["description"], "call_to_action": cta}
            add(f"creative{i}", "creative", f"{account}/adcreatives", {
                "name": f"{name} | creativo {i+1:02d}", "object_story_spec": story, "url_tags": c["utm_template"]})
            add(f"ad{i}", "ad", f"{account}/ads", {"name": f"{name} | anuncio {i+1:02d}",
                "adset_id": ref(f"adset{g}"), "creative": {"creative_id": ref(f"creative{i}")}, "status": "PAUSED"})
    result = {"schema_version": 2, "profile": p, "request": r, "operations": ops,
              "summary": {"name": r["name"], "structure": r["structure"], "objective": p["objective"],
                          "campaigns": len(groups), "adsets": len(groups), "ads": len(r["media"]), "currency": p["currency"],
                          "daily_budget_per_adset_minor": r["daily_budget_minor"],
                          "total_daily_budget_minor": len(groups) * r["daily_budget_minor"],
                          "bid_strategy": "LOWEST_COST_WITH_BID_CAP" if r["structure"] == "BID_CAP_1_1_10" else "LOWEST_COST_WITHOUT_CAP",
                          "bid_cap_minor": r.get("bid_cap_minor"), "target_status": r["target_status"],
                          "videos_with_meta_thumbnail": sum(1 for m in r["media"] if m["kind"] == "video" and "thumbnail_url" not in m)},
              "warnings": ["El presupuesto diario agregado corresponde solo a este lote: no limita el gasto de otras campañas existentes.",
                           "El presupuesto diario de Meta no es un límite estricto de gasto por día.",
                           "El enlace visible no garantiza ocultar el dominio; Meta decide la presentación por ubicación y no lo usa en Instagram.",
                           "ACTIVE solicita activación; entrega y aprobación dependen de Meta.",
                           "Este módulo no admite categorías especiales/reguladas, WhatsApp, catálogo ni formularios de leads."]}
    result["plan_hash"] = digest(result)
    return result
