// Match the words we asked the voice to say with the words Whisper heard.
// Gives every script word a measured time, and reports the words nobody heard.
// Same approach as explainroo's src/align.js (MIT, Vincent Schmalbach), rewritten for this pipeline.

export const splitWords = s => String(s).split(/\s+/).filter(Boolean);
// Sidecar next to a voice clip. tts.mjs deletes it when it writes the clip again.
export const alignFile = clipFile => clipFile.replace(/\.\w+$/, ".align.json");
// Word matching needs spaces between words. These languages write without them.
export const canCheckSpeech = language => !/^(ja|zh|th)\b/i.test(language);

const ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"];
const TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"];
const SCALES = [[1e9, "billion"], [1e6, "million"], [1e3, "thousand"]];
const CURRENCY = { $: "dollars", "€": "euros", "£": "pounds" };
const NUMBER_WORDS = new Set([...ONES, ...TENS, "hundred", "thousand", "million", "billion"]);

function intWords(n) {
  if (n < 20) return [ONES[n]];
  if (n < 100) return [TENS[Math.floor(n / 10)], ...(n % 10 ? [ONES[n % 10]] : [])];
  if (n < 1000) return [ONES[Math.floor(n / 100)], "hundred", ...(n % 100 ? intWords(n % 100) : [])];
  for (const [size, name] of SCALES) if (n >= size) return [...intWords(Math.floor(n / size)), name, ...(n % size ? intWords(n % size) : [])];
  return [String(n)];
}
// Voices read a lone 1582 as "fifteen eighty two" and 1900 as "nineteen hundred". 2000 and 2005 stay cardinal.
function yearWords(n) {
  if (n < 1100 || n > 9999 || n % 1000 < 10) return null;
  const hi = Math.floor(n / 100), lo = n % 100;
  if (lo === 0) return [...intWords(hi), "hundred"];
  return [...intWords(hi), ...(lo < 10 ? ["oh"] : []), ...intWords(lo)];
}

// One written word → the tokens a voice would say. Both the script and the transcript go through this,
// so "$1,050" and "one thousand fifty dollars" compare equal.
export function spokenTokens(word, language = "en") {
  const raw = String(word).toLowerCase().normalize("NFC").replace(/^[^\p{L}\p{N}$€£.]+|[^\p{L}\p{N}%]+$/gu, "");
  if (language.toLowerCase().startsWith("en")) {
    const num = /^([$€£])?(\d[\d,]*)(?:\.(\d+))?(%)?$/.exec(raw);
    if (num) {
      const [, cur, digits, dec, pct] = num;
      const n = Number(digits.replace(/,/g, ""));
      if (n >= 1e12) return [digits];
      const year = !cur && dec === undefined && !pct && !digits.includes(",") && digits.length === 4 ? yearWords(n) : null;
      if (year) return year;
      const out = intWords(n);
      if (dec !== undefined) { if (cur) out.push(CURRENCY[cur], ...intWords(Number(dec)), "cents"); else out.push("point", ...[...dec].map(d => ONES[+d])); }
      else if (cur) out.push(CURRENCY[cur]);
      if (pct) out.push("percent");
      return out;
    }
    if (/[a-z0-9]\.[a-z0-9]/.test(raw)) return raw.split(".").filter(Boolean).flatMap((p, i) => (i ? ["dot", ...spokenTokens(p)] : spokenTokens(p)));
  }
  return raw.split(/[-–—/]+/).map(p => p.replace(/[^\p{L}\p{N}]/gu, "")).filter(Boolean);
}

function editDistance(a, b) {
  let prev = Array.from({ length: b.length + 1 }, (_, j) => j);
  for (let i = 1; i <= a.length; i++) {
    const cur = [i];
    for (let j = 1; j <= b.length; j++) cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    prev = cur;
  }
  return prev[b.length];
}
// Short words must match exactly. Longer ones may differ by about a third (a misspelled name).
function similar(a, b) {
  if (a === b) return true;
  const len = Math.max(a.length, b.length);
  return len > 3 && editDistance(a, b) / len <= 0.34;
}

// Whisper splits "$1,000" into "$1" + ",000" and "5%" into "5" + "%". Join them before comparing.
function joinSplitNumbers(heard) {
  const out = [];
  for (const h of heard) {
    const prev = out.at(-1), t = String(h.text).trim();
    if (prev && ((/^[,.]\d/.test(t) && /\d$/.test(prev.text)) || (t.startsWith("%") && /\d$/.test(prev.text)) || (/^\d/.test(t) && /^[$€£]$/.test(prev.text)))) { prev.text += t; prev.end = h.end; }
    else out.push({ ...h, text: t });
  }
  return out;
}

// words: script words in order. heard: [{text, start, end}] from Whisper. duration: seconds of audio.
// Returns { words: [{w, t, end, heard}], matchRate } with a time for every word: a word nobody heard
// gets a time spread between its heard neighbours.
export function alignWords(words, heard, duration, language = "en") {
  const tokens = [];
  words.forEach((w, wi) => {
    for (const norm of spokenTokens(w, language)) {
      // "and" inside a spoken number ("one thousand and fifty") is optional.
      const optional = norm === "and" && NUMBER_WORDS.has(tokens.at(-1)?.norm);
      tokens.push({ wi, norm, optional });
    }
  });
  const H = joinSplitNumbers(heard).flatMap(h => {
    const parts = spokenTokens(h.text, language), step = (h.end - h.start) / Math.max(1, parts.length);
    return parts.map((norm, k) => ({ norm, start: h.start + k * step, end: h.start + (k + 1) * step }));
  });

  // Edit distance over (token i, heard j). Moves: 1 match, 2 skip a token, 3 skip a heard word, 4 wrong word,
  // 5 two tokens to one heard word ("data base" / "database"), 6 one token to two heard words.
  const T = tokens.length, N = H.length;
  const cost = Array.from({ length: T + 1 }, () => new Float64Array(N + 1).fill(Infinity));
  const move = Array.from({ length: T + 1 }, () => new Int8Array(N + 1));
  const relax = (i, j, c, m) => { if (c < cost[i][j]) { cost[i][j] = c; move[i][j] = m; } };
  cost[0][0] = 0;
  for (let i = 0; i <= T; i++) for (let j = 0; j <= N; j++) {
    const c = cost[i][j];
    if (c === Infinity) continue;
    if (i < T) relax(i + 1, j, c + (tokens[i].optional ? 0 : 1), 2);
    if (j < N) relax(i, j + 1, c + 1, 3);
    if (i < T && j < N) { const ok = similar(tokens[i].norm, H[j].norm); relax(i + 1, j + 1, c + (ok ? 0 : 1.6), ok ? 1 : 4); }
    // Exact only: a loose match here lets "is blue" pass as "blue" and hides a wrong word.
    if (i + 1 < T && j < N && tokens[i].norm + tokens[i + 1].norm === H[j].norm) relax(i + 2, j + 1, c, 5);
    if (i < T && j + 1 < N && tokens[i].norm === H[j].norm + H[j + 1].norm) relax(i + 1, j + 2, c, 6);
  }

  const spans = words.map(() => null), hits = words.map(() => 0);
  const add = (wi, start, end) => { hits[wi]++; const s = spans[wi]; spans[wi] = s ? { start: Math.min(s.start, start), end: Math.max(s.end, end) } : { start, end }; };
  let matched = 0;
  for (let i = T, j = N; i > 0 || j > 0;) {
    const m = move[i][j];
    if (m === 1) { add(tokens[i - 1].wi, H[j - 1].start, H[j - 1].end); matched++; i--; j--; }
    else if (m === 2) i--;
    else if (m === 3) j--;
    else if (m === 4) { i--; j--; }
    else if (m === 5) { add(tokens[i - 1].wi, H[j - 1].start, H[j - 1].end); add(tokens[i - 2].wi, H[j - 1].start, H[j - 1].end); matched += 2; i -= 2; j--; }
    else { add(tokens[i - 1].wi, H[j - 2].start, H[j - 1].end); matched++; i--; j -= 2; }
  }

  const need = words.map((_, wi) => tokens.filter(t => t.wi === wi && !t.optional).length);
  const out = words.map((w, wi) => ({ w, t: spans[wi]?.start ?? 0, end: spans[wi]?.end ?? 0, heard: !!spans[wi] && hits[wi] >= need[wi] }));
  for (let k = 0; k < words.length;) {
    if (spans[k]) { k++; continue; }
    let e = k;
    while (e < words.length && !spans[e]) e++;
    const from = k > 0 ? out[k - 1].end : 0, to = e < words.length ? spans[e].start : duration;
    const total = words.slice(k, e).reduce((s, w) => s + Math.max(1, w.length), 0);
    let t = from;
    for (let q = k; q < e; q++) { const d = (to - from) * Math.max(1, words[q].length) / total; out[q].t = t; out[q].end = t + d; t += d; }
    k = e;
  }
  for (let q = 1; q < out.length; q++) out[q].t = Math.max(out[q].t, out[q - 1].t);
  for (const w of out) { w.t = +w.t.toFixed(3); w.end = +Math.max(w.end, w.t).toFixed(3); }
  const counted = tokens.filter(t => !t.optional).length;
  return { words: out, matchRate: counted ? Math.min(1, matched / counted) : 1 };
}

// A line's "say" can differ from its "text", but at() and captions use the text words.
// Words both share keep their measured time. The rest spread over the spoken words they stand for.
export function timesForText(text, timed, language = "en") {
  const shown = splitWords(text), said = timed.map(w => w.w);
  const key = w => spokenTokens(w, language).join(" ");
  const lcs = Array.from({ length: shown.length + 1 }, () => new Int32Array(said.length + 1));
  for (let i = shown.length - 1; i >= 0; i--) for (let j = said.length - 1; j >= 0; j--) {
    lcs[i][j] = key(shown[i]) === key(said[j]) ? lcs[i + 1][j + 1] + 1 : Math.max(lcs[i + 1][j], lcs[i][j + 1]);
  }
  const anchors = [];
  for (let i = 0, j = 0; i < shown.length && j < said.length;) {
    if (key(shown[i]) === key(said[j])) anchors.push([i++, j++]);
    else if (lcs[i + 1][j] >= lcs[i][j + 1]) i++;
    else j++;
  }
  anchors.push([shown.length, said.length]);
  const out = [];
  let i0 = 0, j0 = 0;
  for (const [i1, j1] of anchors) {
    // Words before this anchor have no exact match: spread them across the spoken words in the same gap.
    const from = timed[Math.min(j0, timed.length - 1)]?.t ?? 0, to = timed[j1]?.t ?? timed.at(-1)?.end ?? from;
    for (let i = i0; i < i1; i++) out.push({ w: shown[i], t: +(from + (to - from) * (i - i0) / (i1 - i0)).toFixed(3) });
    if (i1 < shown.length) out.push({ w: shown[i1], t: timed[j1].t });
    i0 = i1 + 1; j0 = j1 + 1;
  }
  return out;
}
