// REVIEW.md: the plain-text record of the reviewed plan (storyboard.html is what the user reviews).
import { config } from "./config.mjs";
import { fmt } from "./plan.mjs";

const esc = s => String(s ?? "").replace(/\|/g, "\\|").replace(/\n/g, " ");

export function reviewMarkdown(P) {
  const d = P.sb.design ?? {}, L = [];
  L.push(`# Review record: ${P.brief.title || "explainer video"}`, "");
  L.push("The user reviews `storyboard.html`. This file records the same plan as text.", "");
  if (P.errors.length) { L.push("> **Plan errors:**"); P.errors.forEach(e => L.push(`> - ${e}`)); L.push(""); }
  if (P.sb.changes?.length) { L.push("## What changed in this version", ""); P.sb.changes.forEach(c => L.push(`- ${c}`)); L.push(""); }
  L.push("## Brief", "", "| | |", "|---|---|");
  for (const [k, label] of [["goal", "Goal"], ["audience", "Audience"], ["cta", "Call to action"], ["language", "Language"]]) if (P.brief[k]) L.push(`| ${label} | ${esc(P.brief[k])} |`);
  L.push(`| Length | ${fmt(P.end)} (${P.measured} of ${P.lines.length} lines measured from the voice)${P.brief.lengthSec ? `, target ${fmt(P.brief.lengthSec)}` : ""} |`);
  L.push(`| Words | ${P.totalWords}, ${Math.round(P.wpm)} wpm |`, "");
  L.push("## Design", "", "| | |", "|---|---|");
  if (d.summary) L.push(`| Look | ${esc(d.summary)} |`);
  if (d.palette) L.push(`| Palette | ${Object.entries(d.palette).map(([n, h]) => `${n} \`${h}\``).join(" · ")} |`);
  if (d.fonts) L.push(`| Fonts | ${esc([].concat(d.fonts).join(" · "))} |`);
  L.push(`| Image style | ${esc(d.imageStyle ?? P.assets.style ?? "")} |`);
  if (d.motion) L.push(`| Motion | ${esc(d.motion)} |`);
  L.push(`| Voice | ${esc(d.voice ?? `${P.voice.voice ?? config.tts.voice}: ${P.voice.style ?? ""}`)} |`);
  L.push(`| Music | ${esc(d.music ?? P.music?.prompt ?? config.music.provider)} |`, "");
  L.push("## Storyboard", "");
  for (const s of P.scenes) {
    L.push(`### ${s.n}. ${s.title ?? s.name}${s.chapter ? ` · ${s.chapter}` : ""}  (${fmt(s.a)}–${fmt(s.b)})${s.changed ? "  **changed**" : ""}`, "");
    for (const i of s.lines ?? []) L.push(`> ${P.lines[i]?.text ?? "?"}`);
    L.push("", `- **Picture:** ${s.visual ?? ""}`);
    if (s.onScreen?.length) L.push(`- **On screen:** ${s.onScreen.map(x => `"${x}"`).join(", ")}`);
    if (s.motion) L.push(`- **Motion and sound:** ${s.motion}`);
    if (s.assets?.length) L.push(`- **Images:** ${s.assets.map(id => `\`${id}\` (${P.assetStatus(id)})`).join(", ")}`);
    if (s.notes) L.push(`- **Note:** ${s.notes}`);
    L.push("");
  }
  if (P.toMake.length) { L.push("## Images to generate", "", "| Id | Prompt |", "|---|---|"); P.toMake.forEach(x => L.push(`| \`${x.id}\` | ${esc(x.prompt)} |`)); L.push(""); }
  L.push("## Sources", "", `${P.factCount} facts in \`facts.md\`.`, ""); P.sources.forEach(s => L.push(`- ${s}`));
  if (P.sb.userFacts?.length) { L.push("", "Facts from the user:"); P.sb.userFacts.forEach(f => L.push(`- ${f}`)); }
  L.push("", "## Estimate", "", `About $${P.costTotal.toFixed(2)} of API calls (images $${P.cost.image.toFixed(2)}, voice $${P.cost.tts.toFixed(2)}, music $${P.cost.music.toFixed(2)}); budget $${config.budgetUsd}.`, "");
  if (P.sb.questions?.length || P.notes.length) { L.push("## Open questions", ""); [...(P.sb.questions ?? []), ...P.notes].forEach(q => L.push(`- ${q}`)); L.push(""); }
  return L.join("\n");
}
