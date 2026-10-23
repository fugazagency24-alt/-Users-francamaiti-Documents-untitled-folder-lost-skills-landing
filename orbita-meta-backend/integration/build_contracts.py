"""Genera contratos JSON estáticos; validación semántica autoritativa en validation.py."""
import copy
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
def obj(properties, required=()):
    return {"type": "object", "additionalProperties": False, "properties": properties, "required": list(required)}
def string(**kwargs):
    return {"type": "string", **kwargs}
def enum(*args):
    return string(enum=list(args))
money = {"type": "integer", "minimum": 1, "maximum": 1000000000, "description": "Unidades menores enteras. ARS/USD/BRL/EUR: 100 = 1 unidad monetaria."}
id32 = string(pattern="^[a-f0-9]{32}$")
hash64 = string(pattern="^[a-f0-9]{64}$")
url = string(format="uri", pattern="^https://", maxLength=4096)
copy_fields = obj({
    "primary_text": string(minLength=1,maxLength=5000), "headline": string(maxLength=255), "description": string(maxLength=255),
    "cta": enum("LEARN_MORE", "SHOP_NOW", "SIGN_UP", "BOOK_TRAVEL", "CONTACT_US", "DOWNLOAD", "GET_QUOTE", "SUBSCRIBE", "APPLY_NOW"),
    "destination_url": url, "display_url_mode": enum("AUTO", "CUSTOM", "OMIT_CUSTOM"), "display_url": string(maxLength=255),
    "utm_template": string(maxLength=2000, description="Parámetros sin ? inicial. Macros Meta se mantienen literales.")})
media = obj({"kind": enum("image","video"), "url": url, "image_hash": string(), "video_id": string(pattern="^[0-9]+$"),
             "thumbnail_url": url, "overrides": copy_fields}, ["kind"])
media["description"] = "Imagen: exactamente url o image_hash. Video: exactamente url o video_id, más thumbnail_url JPG/PNG. Reglas cruzadas validadas por backend."
request = obj({"name": string(minLength=1,maxLength=100), "structure": enum("BID_CAP_1_1_10","ABO_1_1_1"),
    "media": {"type":"array","items":media,"minItems":1,"maxItems":50}, "shared":copy_fields,
    "daily_budget_minor":money,"bid_cap_minor":money,"target_status":enum("PAUSED","ACTIVE")}, ["name","structure","media"])
request["description"] = "Bid Cap exige exactamente 10 creativos. ABO crea una campaña por creativo. Defaults del perfil; nunca inventar presupuestos."
profile_copy = copy.deepcopy(copy_fields)
profile_copy["required"] = ["primary_text","destination_url"]
profile = obj({"account_id": string(pattern="^act_[0-9]+$"), "page_id":string(pattern="^[0-9]+$"),
    "pixel_id":string(pattern="^[0-9]+$"), "instagram_user_id":string(pattern="^[0-9]+$"),
    "currency":enum("ARS","USD","EUR","BRL"),"countries":{"type":"array","items":string(pattern="^[A-Z]{2}$"),"minItems":1,"maxItems":25},
    "age_min":{"type":"integer","minimum":18,"maximum":65},"age_max":{"type":"integer","minimum":18,"maximum":65},
    "objective":enum("SALES","TRAFFIC"), "daily_budget_minor":money,"max_batch_daily_budget_minor":money,"bid_cap_minor":money,"defaults":profile_copy},
    ["account_id","page_id","currency","countries","objective","daily_budget_minor","max_batch_daily_budget_minor","defaults"])
link_props = {k:val for k,val in request["properties"].items() if k != "media"}
link_props.update({"source_url":url,"source_type":enum("image","video","manifest"),"thumbnail_url":url})
link = obj(link_props,["source_url","source_type"])
link["description"] = "Imagen/video: requiere name; video requiere thumbnail_url. Manifest: SOLO source_url y source_type; su JSON contiene CampaignRequest."
schemas = {"CampaignRequest":request,"Profile":profile,"FromLink":link,"Publish":obj({"plan_hash":hash64},["plan_hash"]),
           "Resolve":obj({"step_key":string(),"resolution":enum("ATTACH","NOT_CREATED"),"remote_id":string(pattern="^[0-9]+$"),"evidence":string(minLength=1,maxLength=500)},["step_key","resolution","evidence"])}
for name,schema in schemas.items():
    (root/f'integration/{name}.schema.json').write_text(json.dumps({"$schema":"https://json-schema.org/draft/2020-12/schema",**schema},ensure_ascii=False,indent=2)+'\n')

tools = [
    ("orbita_connection","Verifica la conexión configurada y moneda; mock no es conexión real.",obj({})),
    ("orbita_prepare_campaign","Prepara un borrador inmutable de campañas sin publicarlas en Meta.",obj({"request":request},["request"])),
    ("orbita_prepare_from_link","Prepara desde un enlace directo de archivo o manifiesto. No abre páginas ni carpetas privadas.",obj({"request":link},["request"])),
    ("orbita_publish_campaign","Crea la estructura del borrador en Meta. Puede activar/gastar si target_status=ACTIVE. Requiere instrucción del usuario o autorización vigente para ese plan y presupuesto.",obj({"draft_id":id32,"plan_hash":hash64},["draft_id","plan_hash"])),
    ("orbita_activate_campaign","Activa una estructura ya creada. Puede comenzar a gastar; requiere autorización para el plan y presupuesto.",obj({"job_id":id32,"plan_hash":hash64},["job_id","plan_hash"])),
    ("orbita_campaign_status","Consulta progreso local; SIMULATED nunca significa publicado en Meta.",obj({"job_id":id32},["job_id"])),
    ("orbita_campaign_remote","Lee status/effective_status actuales de campañas, conjuntos y anuncios en Meta.",obj({"job_id":id32},["job_id"])),
    ("orbita_pause_campaign","Solicita pausar todas las campañas de este trabajo; verificar respuesta y estado remoto.",obj({"job_id":id32},["job_id"])),
    ("orbita_campaign_insights","Lee métricas de hoy, en la zona horaria de la cuenta. No optimiza ni modifica campañas.",obj({"job_id":id32},["job_id"])),
]
(root/'integration/claude-tools.json').write_text(json.dumps([{"name":n,"description":d,"input_schema":s} for n,d,s in tools],ensure_ascii=False,indent=2)+'\n')

paths = {}
def route(path,method,operation,schema=None,status=200,description=""):
    entry = {"operationId":operation,"description":description,"responses":{str(status):{"description":"Respuesta JSON","content":{"application/json":{"schema":{"type":"object"}}}},"default":{"description":"Error JSON {error:{code,message}}"}}}
    params = []
    for name in ("draft_id","job_id"):
        if "{"+name+"}" in path:
            params.append({"name":name,"in":"path","required":True,"schema":id32})
    if operation == "publishCampaign":
        params.append({"name":"Idempotency-Key","in":"header","required":True,"schema":string(minLength=1,maxLength=128)})
    if params: entry["parameters"]=params
    if schema:
        entry["requestBody"]={"required":True,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/"+schema}}}}
    paths.setdefault(path,{})[method]=entry
route('/health','get','health')
paths['/health']['get']['security']=[]
route('/v1/profile','get','getProfile')
route('/v1/profile','put','saveProfile','Profile')
route('/v1/connection','get','connection')
route('/v1/preview','post','preview','CampaignRequest')
route('/v1/drafts','post','draft','CampaignRequest',201)
route('/v1/drafts/from-link','post','fromLink','FromLink',201)
route('/v1/drafts/{draft_id}','get','getDraft')
route('/v1/drafts/{draft_id}/publish','post','publishCampaign','Publish',202)
route('/v1/jobs/{job_id}','get','getJob')
for action in ('remote','insights','previews'): route('/v1/jobs/{job_id}/'+action,'get',action)
for action in ('pause','retry'): route('/v1/jobs/{job_id}/'+action,'post',action,status=202)
route('/v1/jobs/{job_id}/activate','post','activate','Publish',202)
route('/v1/jobs/{job_id}/resolve','post','resolve','Resolve')
api={"openapi":"3.1.0","info":{"title":"Orbita Meta Publisher","version":"1.0.0","description":"API interna mononegocio. Respuestas flexibles; reglas semánticas en validation.py y docs/API.md."},
     "servers":[{"url":"http://127.0.0.1:8787"}],"security":[{"ServiceKey":[]}],"paths":paths,
     "components":{"securitySchemes":{"ServiceKey":{"type":"http","scheme":"bearer"}},"schemas":schemas}}
(root/'integration/openapi.json').write_text(json.dumps(api,ensure_ascii=False,indent=2)+'\n')
print('Contratos generados.')
