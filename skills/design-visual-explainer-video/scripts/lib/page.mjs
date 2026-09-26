// Shared page assembly: player.html + engine.js + a scenes script, with fonts and images embedded.
// Used by build.mjs (the video) and storyboard.mjs (sketch frames).
import fs from "node:fs";
import path from "node:path";
import { config, ASSETS_DIR, jobPath, readJson, die } from "./config.mjs";

export const b64 = f => fs.readFileSync(jobPath(f)).toString("base64");
const MIME = { png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg", webp: "image/webp", svg: "image/svg+xml" };

export function fontFaces() {
  const fonts = readJson("fonts.json", []);
  const css = fonts.map(f => `@font-face{font-family:"${f.family}";font-weight:${f.weight};font-style:${f.style};font-display:block;src:url(data:font/woff2;base64,${b64(f.file)}) format("woff2");${f.unicodeRange ? `unicode-range:${f.unicodeRange};` : ""}}`).join("\n");
  return { css, families: [...new Set(fonts.map(f => f.family))] };
}

// Generated images (assets/<id>.png) and supplied ones (assets/extra/<id>.<ext>). `only` limits to a set of ids.
export function loadImages(only) {
  const images = {};
  const want = id => !only || only.has(id);
  const manifest = readJson("assets/manifest.json", {});
  for (const id of Object.keys(manifest)) {
    const f = `assets/${id}.png`;
    if (want(id) && fs.existsSync(jobPath(f))) images[id] = "data:image/png;base64," + b64(f);
  }
  if (fs.existsSync(jobPath("assets/extra"))) {
    for (const f of fs.readdirSync(jobPath("assets/extra"))) {
      const id = path.basename(f, path.extname(f)), mime = MIME[path.extname(f).slice(1).toLowerCase()];
      if (mime && want(id)) images[id] = `data:${mime};base64,` + b64(`assets/extra/${f}`);
    }
  }
  return images;
}

export const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
// JSON inside <script>: keep "</script>" and U+2028/9 from breaking the tag
export const safeJson = o => JSON.stringify(o).replace(/</g, "\\u003c").replace(/\u2028/g, "\\u2028").replace(/\u2029/g, "\\u2029");

// data: the window.EXPLAINER object (width/height/fps/dur/cues/images/audio/fontFamilies/...); scenesJs: the scenes source.
export function assemblePage({ data, scenesJs, faces }) {
  const { width, height } = config.video;
  const fill = (s, k, v) => { if (!s.includes(k)) die(`player.html is missing ${k}`); return s.split(k).join(v); };
  let html = fs.readFileSync(path.join(ASSETS_DIR, "player.html"), "utf8");
  html = fill(html, "{{TITLE}}", esc(data.title));
  html = fill(html, "{{ASPECT}}", `${width} / ${height}`);
  html = fill(html, "{{WIDTH}}", String(width));
  html = fill(html, "{{HEIGHT}}", String(height));
  html = fill(html, "/*{{FONT_FACES}}*/", faces);
  html = html.replace("/*{{DATA}}*/", () => safeJson(data));
  html = html.replace("/*{{ENGINE}}*/", () => fs.readFileSync(path.join(ASSETS_DIR, "engine.js"), "utf8"));
  html = html.replace("/*{{SCENES}}*/", () => scenesJs.replace(/<\/script/gi, "<\\/script"));
  return html;
}
