// Minimal OpenRouter client. Every paid call goes through here so the spend ledger
// (spend.json in the job dir) and EXPLAINER_BUDGET_USD are enforced in one place.
import { config, assertBudget, record, die, isStop } from "./config.mjs";

const OR = config.openrouter;

function headers(extra = {}) {
  if (!OR.apiKey) die("OPENROUTER_API_KEY is not set (add it to .env; see getting-started.md)", 2);
  return {
    Authorization: `Bearer ${OR.apiKey}`,
    "Content-Type": "application/json",
    "HTTP-Referer": OR.referer,
    "X-Title": OR.title,
    ...extra,
  };
}

async function request(path, body, { raw = false, retries = 3, timeoutMs = 180000 } = {}) {
  let last;
  for (let attempt = 1; attempt <= retries; attempt++) {
    const ctl = new AbortController();
    const timer = setTimeout(() => ctl.abort(), timeoutMs);
    try {
      const res = await fetch(OR.baseUrl + path, { method: "POST", headers: headers(), body: JSON.stringify(body), signal: ctl.signal });
      if (res.status === 402) die("OpenRouter returned 402 payment_required: the key's credit limit or account balance is exhausted", 3);
      if (!res.ok) {
        const text = await res.text();
        const err = new Error(`OpenRouter ${path} ${res.status}: ${text.slice(0, 600)}`);
        err.status = res.status;
        if (res.status === 429 || res.status >= 500) { last = err; await sleep(1500 * attempt ** 2); continue; }
        throw err;
      }
      return raw ? res : await res.json();
    } catch (e) {
      if (isStop(e)) throw e;
      if (e.status && e.status < 500 && e.status !== 429) throw e;
      last = e; await sleep(1500 * attempt ** 2);
    } finally { clearTimeout(timer); }
  }
  throw last;
}
const sleep = ms => new Promise(r => setTimeout(r, ms));

// Cost for endpoints that return raw bytes (TTS): look up the generation after the fact.
export async function generationCost(id) {
  if (!id) return null;
  for (let i = 0; i < 6; i++) {
    await sleep(1000 + i * 1000);
    try {
      const res = await fetch(`${OR.baseUrl}/generation?id=${encodeURIComponent(id)}`, { headers: headers() });
      if (res.ok) { const j = await res.json(); const c = j?.data?.total_cost; if (typeof c === "number") return c; }
    } catch {}
  }
  return null;
}

export async function keyInfo() {
  const res = await fetch(`${OR.baseUrl}/key`, { headers: headers() });
  if (!res.ok) throw new Error(`GET /key ${res.status}: ${(await res.text()).slice(0, 300)}`);
  return (await res.json()).data;
}

// ---------- images: POST /images ----------
// opts: {model, prompt, aspect, resolution, seed, references: [dataUrl], background}
export async function generateImage(o) {
  assertBudget(0.1);
  const body = {
    model: o.model, prompt: o.prompt, n: 1,
    aspect_ratio: o.aspect ?? "1:1",
    resolution: o.resolution ?? config.image.resolution,
    output_format: "png",
    ...(o.seed !== undefined ? { seed: o.seed } : {}),
    ...(o.background === "transparent" ? { background: "transparent" } : {}),
    ...(o.references?.length ? { input_references: o.references.map(url => ({ type: "image_url", image_url: { url } })) } : {}),
  };
  const j = await request("/images", body);
  const d = j?.data?.[0];
  if (!d?.b64_json) throw new Error(`no image in response: ${JSON.stringify(j).slice(0, 400)}`);
  const cost = +(j.usage?.cost ?? 0);
  const total = record({ kind: "image", model: o.model, id: o.id, cost });
  return { buffer: Buffer.from(d.b64_json, "base64"), mediaType: d.media_type ?? "image/png", cost, total };
}

// ---------- speech: POST /audio/speech (raw audio bytes back) ----------
export async function speech({ model, text, voice, style, speed, format = "mp3", id }) {
  assertBudget(0.05);
  const body = { model, input: text, voice, response_format: format };
  if (speed && speed !== 1) body.speed = speed;
  if (style) body.provider = { options: { "google-ai-studio": { speech_metadata: { style } }, "google-vertex": { speech_metadata: { style } } } };
  let res;
  try { res = await request("/audio/speech", body, { raw: true }); }
  catch (e) {
    // Some providers accept only one format (Gemini TTS: pcm only). Retry once with the format the error names.
    const want = e.status === 400 && String(e.message).match(/response_format=\\?"(\w+)\\?"/)?.[1];
    if (!want || want === format) throw e;
    body.response_format = want;
    res = await request("/audio/speech", body, { raw: true });
  }
  const buffer = Buffer.from(await res.arrayBuffer());
  const genId = res.headers.get("x-generation-id");
  let cost = await generationCost(genId);
  const estimated = cost === null;
  if (estimated) cost = 0.0004 * text.length / 25 + 0.002; // conservative fallback so the ledger never reads $0
  const total = record({ kind: "tts", model, id, cost, estimated, generation: genId });
  return { buffer, format: body.response_format, contentType: res.headers.get("content-type") ?? "", cost, total };
}

// ---------- streamed chat completion with audio output (Lyria music) ----------
export async function chatAudio({ model, prompt, format = "wav", id }) {
  assertBudget(0.1);
  const res = await request("/chat/completions", {
    model, stream: true, modalities: ["text", "audio"], audio: { format },
    messages: [{ role: "user", content: prompt }],
  }, { raw: true, retries: 2, timeoutMs: 300000 });
  const reader = res.body.getReader(), dec = new TextDecoder();
  let buf = "", b64 = "", transcript = "", usage = null;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += dec.decode(value, { stream: true });
    let nl;
    while ((nl = buf.indexOf("\n")) >= 0) {
      const line = buf.slice(0, nl).trim(); buf = buf.slice(nl + 1);
      if (!line.startsWith("data:")) continue;
      const data = line.slice(5).trim();
      if (data === "[DONE]") continue;
      let j;
      try { j = JSON.parse(data); } catch { continue; }
      if (j.error) throw new Error(`stream error: ${JSON.stringify(j.error).slice(0, 400)}`);
      const a = j.choices?.[0]?.delta?.audio;
      if (a?.data) b64 += a.data;
      if (a?.transcript) transcript += a.transcript;
      if (j.usage) usage = j.usage;
    }
  }
  if (!b64) throw new Error("no audio data in the streamed response");
  const cost = +(usage?.cost ?? 0.08);
  const total = record({ kind: "music", model, id, cost, estimated: usage?.cost === undefined });
  return { buffer: Buffer.from(b64, "base64"), transcript, cost, total };
}
