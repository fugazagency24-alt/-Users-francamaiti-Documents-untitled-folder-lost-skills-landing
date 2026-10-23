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
  url?: string; // archivo publicitario directo, no la landing
  image_hash?: string;
  video_id?: string;
  thumbnail_url?: string; // opcional en video: sin ella se usa la portada que genera Meta
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
export type Summary = {
  name: string; structure: Structure; objective: "SALES" | "TRAFFIC";
  campaigns: number; adsets: number; ads: number; currency: string;
  daily_budget_per_adset_minor: number; total_daily_budget_minor: number;
  bid_strategy: "LOWEST_COST_WITH_BID_CAP" | "LOWEST_COST_WITHOUT_CAP"; bid_cap_minor: number | null;
  target_status: "PAUSED" | "ACTIVE"; videos_with_meta_thumbnail: number;
};
export type Draft = {draft_id: string; plan_hash: string; summary: Summary; warnings: string[]};
export type JobState = "QUEUED" | "RUNNING" | "SIMULATED" | "CREATED_PAUSED" | "ACTIVATION_REQUESTED" | "FAILED"
  | "NEEDS_RECONCILIATION" | "STOPPED_PAUSED" | "PAUSE_INCOMPLETE";
export type Job = {id: string; draft_id: string; mode: "mock" | "live"; state: JobState; error: string | null; steps: unknown[]; events: unknown[]};
export type JobListItem = {id: string; draft_id: string; mode: "mock" | "live"; state: JobState; error: string | null;
  created: number; updated: number; plan_hash: string; summary: Summary};
export type AssetCheck = {ok: true; kind: "image" | "video"; format: string; width?: number | null; height?: number | null; note?: string};
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
    profile: () => call<Record<string, unknown>>("/v1/profile"),
    saveProfile: (profile: Record<string, unknown>) => call<Record<string, unknown>>("/v1/profile", "PUT", profile),
    saveDefaults: (defaults: CopyFields) => call<Record<string, unknown>>("/v1/profile/defaults", "PUT", defaults),
    verifySetup: () => call<Record<string, unknown>>("/v1/setup/verify", "POST", {}),
    discoverAssets: (accountId?: string) => call<Record<string, unknown>>(
      "/v1/setup/assets" + (accountId ? `?account_id=${encodeURIComponent(accountId)}` : "")),
    checkAsset: (url: string, kind: "image" | "video" | "thumbnail") => call<AssetCheck>("/v1/assets/check", "POST", {url, kind}),
    jobs: (limit = 50) => call<{mode: string; jobs: JobListItem[]}>(`/v1/jobs?limit=${limit}`),
    connection: () => call<Record<string, unknown>>("/v1/connection"),
    // clientKey: generado una vez por intento del usuario y conservado hasta el éxito (doble clic, recarga, timeout).
    draft: (request: CampaignRequest, clientKey?: string) => call<Draft>("/v1/drafts", "POST", request, clientKey),
    fromLink: (request: LinkRequest, clientKey?: string) => call<Draft>("/v1/drafts/from-link", "POST", request, clientKey),
    publish: (draft: Pick<Draft, "draft_id" | "plan_hash">) => call<Job>(
      `/v1/drafts/${id(draft.draft_id)}/publish`, "POST", {plan_hash: draft.plan_hash}, `orbita-${draft.draft_id}`),
    job: (jobId: string) => call<Job>(`/v1/jobs/${id(jobId)}`),
    pause: (jobId: string) => call<Job | {job_id: string; pause_requested: boolean}>(`/v1/jobs/${id(jobId)}/pause`, "POST", {}),
    activate: (jobId: string, planHash: string) => call<Job>(`/v1/jobs/${id(jobId)}/activate`, "POST", {plan_hash: planHash}),
    remote: (jobId: string) => call<Record<string, unknown>>(`/v1/jobs/${id(jobId)}/remote`),
    insights: (jobId: string) => call<Record<string, unknown>>(`/v1/jobs/${id(jobId)}/insights`),
    previews: (jobId: string, format = "DESKTOP_FEED_STANDARD") =>
      call<Record<string, unknown>>(`/v1/jobs/${id(jobId)}/previews?format=${encodeURIComponent(format)}`),
    retry: (jobId: string) => call<Job>(`/v1/jobs/${id(jobId)}/retry`, "POST", {}),
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
