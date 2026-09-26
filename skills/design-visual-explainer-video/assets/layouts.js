// Storyboard sketch layouts: one still key frame per scene, drawn with the engine helpers in the
// video's own palette and fonts. storyboard.mjs prepends `const SB = {theme, frames, prompts}` and
// registers one scene per frame. A frame spec (storyboard.json → scenes[].frame):
//   layout     type | photo-card | photo-full | cards | list | quote | diagram | device
//   bg         "light" | "dark" | "#rrggbb"
//   kicker     small mono label ("01 · Arrival")      headline / headline2 (accent colour) / sub (serif line)
//   image      asset id; imageSide "left"|"right"; textSide "left"|"right"|"bottom"; focus [px, py]
//   items      short strings (chips, checks, cards, diagram sources)
//   quote      [{label, text}]  (quote layout)       target  diagram end node label
//   callouts   [{x, y, text}] with x, y in 0..1 of the frame: ember ring + label (a tap, a highlight)
"use strict";
const T = Object.assign({
  light: "#f6f5f2", dark: "#171614", ink: "#111110", inkOnDark: "#f5f3ee", accent: "#e07a2e",
  muted: "#55524d", mutedOnDark: "#a9a59d", card: "#ffffff", cardOnDark: "#201e1b", border: "#e6e3dd",
}, SB.theme || {});
const FF = DATA.fontFamilies;
T.display = T.display || FF[0] || "sans-serif";
T.serif = T.serif || FF.find(f => /serif|garamond|playfair|lora|merriweather/i.test(f)) || T.display;
T.mono = T.mono || FF.find(f => /mono|code/i.test(f)) || "monospace";
FINISH.fadeIn = 0; FINISH.fadeOut = 0; FINISH.grain = 0.02; FINISH.vignette = 0.1; CAM.drift = 0;

const isDarkHex = h => { const m = /^#?([0-9a-f]{6})$/i.exec(h || ""); if (!m) return false; const n = parseInt(m[1], 16); return ((n >> 16) * 299 + ((n >> 8) & 255) * 587 + (n & 255) * 114) / 1000 < 110; };
function ground(f) {
  const dark = f.bg === "dark" || isDarkHex(f.bg);
  bg(f.bg === "dark" ? T.dark : f.bg && f.bg.startsWith("#") ? f.bg : T.light);
  return { dark, fg: dark ? T.inkOnDark : T.ink, mute: dark ? T.mutedOnDark : T.muted, card: dark ? T.cardOnDark : T.card };
}
function kick(s, x, y, c, o = {}) {
  if (!s) return 0;
  circle(x + 7, y - 8, 7, { fill: T.accent });
  return tracked("3px", () => text(String(s).toUpperCase(), x + 26, y, { font: T.mono, size: o.size ?? 22, color: c, weight: 500 }));
}
function headBlock(f, x, y, c, o = {}) {
  const size = o.size ?? 92, mw = o.maxWidth ?? 820, align = o.align ?? "left";
  let yy = y;
  if (f.kicker) { kick(f.kicker, align === "center" ? x - measure(f.kicker.toUpperCase(), { font: T.mono, size: 22 }) / 2 - 20 : x, yy, c.mute); yy += 90; }
  if (f.headline) { const r = tracked(`${-size * 0.03}px`, () => text(f.headline, x, yy, { font: T.display, weight: 800, size, color: c.fg, maxWidth: mw, align, lineHeight: 1.08 })); yy += r.h + 6; }
  if (f.headline2) { const r = tracked(`${-size * 0.03}px`, () => text(f.headline2, x, yy, { font: T.display, weight: 800, size, color: T.accent, maxWidth: mw, align, lineHeight: 1.08 })); yy += r.h + 6; }
  if (f.sub) { yy += 24; const r = text(f.sub, x, yy, { font: T.serif, italic: true, size: 50, color: c.mute, maxWidth: mw, align, lineHeight: 1.2 }); yy += r.h; }
  return yy;
}
// image, or a hatched placeholder naming the image still to generate
function picture(id, x, y, w, h, o = {}) {
  if (id && IMAGES[id]) { cover(id, x, y, w, h, { r: o.r ?? 0, px: o.focus?.[0], py: o.focus?.[1], shadow: o.shadow, dim: o.dim }); return; }
  ctx.save(); ctx.beginPath(); ctx.roundRect(x, y, w, h, o.r ?? 0); ctx.clip();
  ctx.fillStyle = "#d9d5ce"; ctx.fillRect(x, y, w, h);
  ctx.strokeStyle = "rgba(0,0,0,.08)"; ctx.lineWidth = 14;
  for (let k = -h; k < w; k += 48) { ctx.beginPath(); ctx.moveTo(x + k, y + h); ctx.lineTo(x + k + h, y); ctx.stroke(); }
  ctx.restore();
  rrect(x, y, w, h, o.r ?? 0, { stroke: "#8b877f", lineWidth: 3 });
  const cx = x + w / 2, cy = y + h / 2;
  tracked("3px", () => text(`IMAGE TO GENERATE: ${id || "?"}`, cx, cy - 20, { font: T.mono, size: 22, color: "#3b3833", align: "center", maxWidth: w - 60 }));
  const p = (SB.prompts || {})[id];
  if (p) text(p.length > 140 ? p.slice(0, 137) + "…" : p, cx, cy + 30, { font: T.display, size: 24, color: "#55524d", align: "center", maxWidth: w - 80, lineHeight: 1.3 });
}
function chips(items, x, y, c, o = {}) {
  let xx = x;
  for (const s of items || []) {
    const w = measure(s, { font: T.display, size: 30, weight: 800 }) + 56;
    if (o.maxX && xx + w > o.maxX) break;
    rrect(xx, y, w, 72, 36, { fill: o.fill ?? c.card, stroke: c.dark ? "rgba(255,255,255,.12)" : T.border, lineWidth: 2 });
    text(s, xx + 28, y + 47, { font: T.display, weight: 800, size: 30, color: o.color ?? c.fg });
    xx += w + 16;
  }
}
function checks(items, x, y, c) {
  (items || []).forEach((s, i) => {
    circle(x + 20, y + i * 86 - 12, 20, { fill: T.accent });
    ink([[x + 11, y + i * 86 - 12], [x + 18, y + i * 86 - 5], [x + 30, y + i * 86 - 19]], { color: "#fff", width: 4.5, wobble: 0, passes: 1 });
    text(s, x + 60, y + i * 86, { font: T.display, weight: 800, size: 46, color: c.fg });
  });
}
function callouts(list) {
  for (const k of list || []) {
    const x = k.x * W, y = k.y * H;
    circle(x, y, 46, { stroke: T.accent, lineWidth: 5 }); circle(x, y, 74, { stroke: T.accent, lineWidth: 3, alpha: 0.5 }); circle(x, y, 10, { fill: T.accent });
    if (k.text) {
      const w = measure(k.text, { font: T.display, size: 28, weight: 800 }) + 40, lx = Math.min(W - w - 60, x + 90), ly = y - 30;
      rrect(lx, ly - 36, w, 56, 28, { fill: T.accent });
      text(k.text, lx + 20, ly + 2, { font: T.display, size: 28, weight: 800, color: "#fff" });
    }
  }
}

const LAYOUTS = {
  type(f) { const c = ground(f); headBlock(f, W / 2, H / 2 - 60, c, { size: 110, align: "center", maxWidth: 1500 }); chips(f.items, W / 2 - 400, H / 2 + 180, c); },
  "photo-card"(f) {
    const c = ground(f), left = f.imageSide === "left";
    picture(f.image, left ? 150 : 1010, 120, 760, 840, { r: 26, shadow: true, focus: f.focus });
    const x = left ? 1010 : 150, yy = headBlock(f, x, 330, c, { maxWidth: 780 });
    if (f.items?.length) chips(f.items, x, yy + 40, c, { maxX: left ? W - 100 : 960 });
  },
  "photo-full"(f) {
    const c0 = ground(f);
    picture(f.image, 0, 0, W, H, { focus: f.focus });
    const side = f.textSide || "left", tint = "17,17,16";
    const g = side === "bottom" ? ctx.createLinearGradient(0, H, 0, H * 0.35) : side === "left" ? ctx.createLinearGradient(0, 0, W * 0.62, 0) : ctx.createLinearGradient(W, 0, W * 0.38, 0);
    g.addColorStop(0, `rgba(${tint},.85)`); g.addColorStop(1, `rgba(${tint},0)`);
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    const c = { ...c0, dark: true, fg: "#fff", mute: T.mutedOnDark, card: "rgba(17,17,16,.6)" };
    if (side === "bottom") { const yy = headBlock(f, 150, 700, c, { size: 84, maxWidth: 1500 }); chips(f.items, 150, yy + 30, c, { color: "#fff" }); }
    else { const x = side === "left" ? 150 : 1060; const yy = headBlock(f, x, 380, c, { size: 76, maxWidth: 720 }); chips(f.items, x, yy + 40, c, { maxX: x + 740, color: "#fff" }); }
  },
  cards(f) {
    const c = ground(f); headBlock(f, 150, 260, c, { size: 80, maxWidth: 1600 });
    const n = Math.max(1, (f.items || []).length), gap = 30, w = (W - 300 - gap * (n - 1)) / n;
    (f.items || []).forEach((s, i) => {
      const x = 150 + i * (w + gap);
      rrect(x, 520, w, 300, 24, { fill: c.card, stroke: c.dark ? "rgba(255,255,255,.1)" : T.border, lineWidth: 2, shadow: !c.dark });
      tracked("2px", () => text(String(i + 1).padStart(2, "0"), x + 40, 590, { font: T.mono, size: 22, color: T.accent }));
      tracked("-1px", () => text(s, x + 40, 680, { font: T.display, weight: 800, size: 44, color: c.fg, maxWidth: w - 80 }));
    });
  },
  list(f) {
    const c = ground(f), hasImg = !!f.image;
    if (hasImg) picture(f.image, 1010, 120, 760, 840, { r: 26, shadow: true, focus: f.focus });
    const yy = headBlock(f, 150, 300, c, { maxWidth: hasImg ? 780 : 1500 });
    checks(f.items, 150, yy + 90, c);
  },
  quote(f) {
    const c = ground(f); picture(f.image, 150, 140, 700, 800, { r: 26, shadow: true, focus: f.focus });
    let y = 220; if (f.kicker) { kick(f.kicker, 960, y, c.mute, { size: 18 }); y += 80; }
    for (const q of f.quote || []) {
      tracked("3px", () => text(String(q.label || "").toUpperCase(), 960, y, { font: T.mono, size: 20, color: T.accent }));
      const r = text(q.text, 960, y + 66, { font: T.serif, italic: true, size: 50, color: c.fg, maxWidth: 820, lineHeight: 1.15 });
      y += 66 + r.h + 60;
    }
  },
  diagram(f) {
    const c = ground(f); const hy = headBlock(f, 150, 230, c, { size: 76, maxWidth: 1600 });
    const items = f.items || [], n = items.length, y0 = Math.max(470, hy + 90), step = Math.min(160, 440 / Math.max(1, n - 1 || 1));
    if (f.target) {
      const tx = 1450, ty = Math.max(650, y0 + ((n - 1) * step) / 2);
      items.forEach((s, i) => {
        const y = n === 1 ? ty : y0 + i * step;
        rrect(150, y - 50, 460, 100, 22, { fill: c.card, stroke: c.dark ? "rgba(255,255,255,.12)" : T.border, lineWidth: 2 });
        text(s, 190, y + 14, { font: T.display, weight: 800, size: 40, color: c.fg });
        arrow(630, y, tx - 190, ty, { color: T.accent, width: 5, bend: 0.1, wobble: 0.8 });
      });
      const g = ctx.createRadialGradient(tx, ty, 20, tx, ty, 300); g.addColorStop(0, "rgba(240,162,90,.45)"); g.addColorStop(1, "rgba(240,162,90,0)");
      ctx.fillStyle = g; ctx.fillRect(tx - 320, ty - 320, 640, 640);
      circle(tx, ty, 150, { fill: c.card, stroke: T.accent, lineWidth: 6 });
      text(f.target, tx, ty + 16, { font: T.display, weight: 800, size: 38, color: c.fg, align: "center", maxWidth: 260, lineHeight: 1.1 });
    } else {
      const w = (W - 300 - 80 * (n - 1)) / Math.max(1, n);
      items.forEach((s, i) => {
        const x = 150 + i * (w + 80);
        rrect(x, 560, w, 180, 22, { fill: c.card, stroke: c.dark ? "rgba(255,255,255,.12)" : T.border, lineWidth: 2 });
        text(s, x + w / 2, 665, { font: T.display, weight: 800, size: 38, color: c.fg, align: "center", maxWidth: w - 40 });
        if (i < n - 1) arrow(x + w + 10, 650, x + w + 70, 650, { color: T.accent, width: 5, bend: 0, wobble: 0.5, head: 20 });
      });
    }
  },
  // A constellation of labeled nodes (items) with a thread through `path` (labels in order) and an
  // optional "now asking"-style card (quote[0]). points: [[x, y], …] in 0..1 of the map area; when absent
  // the nodes are spread on rings. The last label in `path` is the active node.
  map(f) {
    const c = ground(f), items = f.items || [], n = items.length;
    const mx = 900, my = 110, mw = 900, mh = 860;
    const pts = items.map((_, i) => {
      if (f.points?.[i]) return [mx + f.points[i][0] * mw, my + f.points[i][1] * mh];
      const ring = i < 6 ? 0.22 : 0.45, k = i < 6 ? i / 6 : (i - 6) / Math.max(1, n - 6);
      return [mx + mw / 2 + Math.cos(k * Math.PI * 2 - 1.2) * ring * mw, my + mh / 2 + Math.sin(k * Math.PI * 2 - 1.2) * ring * mh];
    });
    const idx = l => items.indexOf(l), path = (f.path || []).map(idx).filter(i => i >= 0);
    for (let k = 1; k < path.length; k++) {
      const [ax, ay] = pts[path[k - 1]], [bx, by] = pts[path[k]], cx = mx + mw / 2, cy = my + mh / 2;
      const qx = (ax + bx) / 2 + (cx - (ax + bx) / 2) * 0.45, qy = (ay + by) / 2 + (cy - (ay + by) / 2) * 0.45;
      ctx.save(); ctx.strokeStyle = T.accent; ctx.lineWidth = k === path.length - 1 ? 5 : 3; ctx.globalAlpha = k === path.length - 1 ? 1 : 0.45;
      ctx.beginPath(); ctx.moveTo(ax, ay); ctx.quadraticCurveTo(qx, qy, bx, by); ctx.stroke(); ctx.restore();
    }
    const active = path.at(-1);
    items.forEach((s, i) => {
      const [x, y] = pts[i], on = i === active, visited = path.includes(i);
      if (on) circle(x, y, 26, { fill: "rgba(224,122,46,.25)" });
      circle(x, y, on ? 15 : 11, on ? { fill: T.accent } : { stroke: visited ? T.accent : c.dark ? "rgba(255,255,255,.35)" : "#b9b4ac", lineWidth: 3, fill: c.dark ? T.dark : T.light });
      text(s, x, y + 48, { font: T.display, weight: on ? 800 : 500, size: 26, color: on ? c.fg : c.mute, align: "center" });
    });
    let y = headBlock({ ...f, sub: undefined }, 150, 250, c, { size: 64, maxWidth: 680 });
    const q = (f.quote || [])[0];
    if (q) {
      y += 30;
      rrect(150, y, 680, 290, 20, { fill: c.dark ? T.cardOnDark : "#ffffff", stroke: c.dark ? "rgba(255,255,255,.1)" : T.border, lineWidth: 2 });
      tracked("3px", () => text(String(q.label || "").toUpperCase(), 190, y + 64, { font: T.mono, size: 20, weight: 500, color: c.fg }));
      text(q.text, 190, y + 140, { font: T.serif, italic: true, size: 50, color: c.fg, maxWidth: 600, lineHeight: 1.15 });
      y += 290;
    }
    if (f.sub) text(f.sub, 150, y + 90, { font: T.serif, italic: true, size: 44, color: T.accent, maxWidth: 700 });
  },
  device(f) {
    const c = ground({ ...f, bg: f.bg || "dark" });
    const cx = 1300, cy = 560;
    const g = ctx.createRadialGradient(cx, cy - 40, 40, cx, cy - 40, 520); g.addColorStop(0, "rgba(240,162,90,.35)"); g.addColorStop(1, "rgba(240,162,90,0)");
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    if (f.image && IMAGES[f.image]) img(f.image, cx, cy, { w: 700 }); else picture(f.image, cx - 350, cy - 350, 700, 700, { r: 30 });
    const yy = headBlock(f, 150, 380, c, { size: 72, maxWidth: 760 });
    (f.items || []).forEach((s, i) => text(s, 150, yy + 60 + i * 80, { font: T.display, weight: 800, size: 48, color: i ? c.mute : T.accent }));
  },
};

(SB.frames || []).forEach((f, i) => {
  scene({
    name: `frame${i}`, start: i, end: i + 1, transition: "cut", tlen: 0,
    draw() {
      if (!f) { ground({}); return; }
      const fn = LAYOUTS[f.layout] || LAYOUTS.type;
      fn(f);
      callouts(f.callouts);
    },
  });
});
