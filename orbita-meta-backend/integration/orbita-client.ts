/** SERVER ONLY. Importar en el backend/BFF de Orbita, nunca en el navegador. */
export type Structure = "BID_CAP_1_1_10" | "ABO_1_1_1";
export type CopyFields = {
  primary_text?: string;
  headline?: string;
  description?: string;
  cta?: "LEARN_MORE" | "SHOP_NOW" | "SIGN_UP" | "BOOK_TRAVEL" | "CONTACT_US" | "DOWNLOAD" | "GET_QUOTE" | "SUBSCRIBE" | "APPLY_NOW";
  destination_url?: string;
  display_url_mode?: "AUTO" | "CUSTOM" | "OMIT_CUSTOM";
  display_url?: string;
  utm_template?: string;
};
export type Media = {
  kind: "image" | "video";
  url?: string;
  image_hash?: string;
  video_id?: string;
  thumbnail_url?: string;
  overrides?: CopyFields;
};
export type CampaignRequest = {
  name: string;
  structure: Structure;
  media: Media[];
  shared?: CopyFields;
  daily_budget_minor?: number;
  bid_cap_minor?: number;
  target_status?: "PAUSED" | "ACTIVE";
};
export type Draft = {
  draft_id: string;
  plan_hash: string;
  summary: {campaigns: number; adsets: number; ads: number; currency: string; total_daily_budget_minor: number; target_status: string};
  warnings: string[];
};
export type Job = {id: string; draft_id: string; mode: "mock" | "live"; state: string; error: string | null; steps: unknown[]; events: unknown[]};
export type LinkRequest = {
  source_url: string;
  source_type: "image" | "video" | "manifest";
  name?: string;
  structure?: Structure;
  thumbnail_url?: string;
  shared?: CopyFields;
  target_status?: "PAUSED" | "ACTIVE";
  daily_budget_minor?: number;
  bid_cap_minor?: number;
};

export function createOrbitaPublisher(baseUrl: string, serviceKey: string) {
  const base = new URL(baseUrl);
  if (base.protocol !== "https:" && !["localhost", "127.0.0.1"].includes(base.hostname)) {
    throw new Error("Usar HTTPS o loopback; configurar red privada/TLS para despliegues separados");
  }
  async function call<T>(path: string, method = "GET", body?: unknown, idempotencyKey?: string): Promise<T> {
    const response = await fetch(new URL(path, base), {
      method,
      headers: {Authorization: `Bearer ${serviceKey}`, "Content-Type": "application/json",
        ...(idempotencyKey ? {"Idempotency-Key": idempotencyKey} : {})},
      body: body === undefined ? undefined : JSON.stringify(body),
      signal: AbortSignal.timeout(120_000),
      redirect: "error",
    });
    const value = await response.json();
    if (!response.ok) throw new Error(value?.error?.message || `Publisher HTTP ${response.status}`);
    return value as T;
  }
  const id = (x: string) => {
    if (!/^[a-f0-9]{32}$/.test(x)) throw new Error("ID Orbita inválido");
    return x;
  };
  return {
    connection: () => call<Record<string, unknown>>("/v1/connection"),
    draft: (request: CampaignRequest) => call<Draft>("/v1/drafts", "POST", request),
    fromLink: (request: LinkRequest) => call<Draft>("/v1/drafts/from-link", "POST", request),
    publish: (draft: Pick<Draft, "draft_id" | "plan_hash">) => call<Job>(
      `/v1/drafts/${id(draft.draft_id)}/publish`, "POST", {plan_hash: draft.plan_hash}, `orbita-${draft.draft_id}`),
    job: (jobId: string) => call<Job>(`/v1/jobs/${id(jobId)}`),
    pause: (jobId: string) => call<Job | {job_id: string; pause_requested: boolean}>(`/v1/jobs/${id(jobId)}/pause`, "POST", {}),
    activate: (jobId: string, planHash: string) => call<Job>(`/v1/jobs/${id(jobId)}/activate`, "POST", {plan_hash: planHash}),
    remote: (jobId: string) => call<Record<string, unknown>>(`/v1/jobs/${id(jobId)}/remote`),
    insights: (jobId: string) => call<Record<string, unknown>>(`/v1/jobs/${id(jobId)}/insights`),
    previews: (jobId: string) => call<Record<string, unknown>>(`/v1/jobs/${id(jobId)}/previews`),
  };
}

/* Integración típica (tras autenticar al usuario y verificar permisos en Orbita):
const publisher = createOrbitaPublisher(env.PUBLISHER_URL, env.ORBITA_SERVICE_KEY);
const draft = await publisher.draft(bodyValidado);
// Persistir draft_id + plan_hash en Orbita. Mostrar resumen o usar autorización ya dada.
const job = await publisher.publish(draft);
// Persistir job.id y consultar publisher.job(job.id); devolverlo al cliente.
// Nunca convertir SIMULATED o ACTIVATION_REQUESTED en "anuncios entregando".
*/
