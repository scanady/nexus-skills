// Example scenes.js for the three-line example in lines.json.
// It shows the patterns every video uses: scene bounds from narration timing,
// entrances keyed to spoken words, one sound per visual event, and an overlay layer.
// Copy the patterns, not the content.

const INK = "#1f1a17", PAPER = "#f4ecd8", RED = "#d8452f", TEAL = "#2f8f8a";
const HAND = DATA.fontFamilies[0], BODY = DATA.fontFamilies[1] ?? DATA.fontFamilies[0];

music({ bpm: 96, key: "D", mood: "bright", level: 0.5 }); // used only when no music file is mixed in
FINISH.grain = 0.05;

// ---- Scene 1: hook (line 0) ----
// The hook holds into line 1 so "not the water" stays readable (lint.mjs checks reading time).
const S1 = { start: 0, end: at(1, "colour") };
const tWater = at(0, "water");
scene({
  name: "hook", ...S1, bg: PAPER, transition: "cut",
  draw(t) {
    const k = pop(t, 0.3, 0.6);
    text("Why is the sky blue?", W / 2, 300, { font: HAND, size: 110 * k, align: "center", color: INK });
    ink([[W / 2 - 360, 340], [W / 2 + 360, 332]], { t, reveal: ease.outCubic(seg(t, 0.9, 1.5)), color: RED, width: 7 });
    if (IMAGES.sun) img("sun", W / 2, 640, { h: 380, scale: pop(t, at(0, "sunlight"), 0.5), rot: noise(t * 0.5) * 0.05 });
    const wk = seg(t, tWater, tWater + 0.6);
    text("not the water", W / 2 + 420, 780, { font: HAND, size: 54, color: RED, alpha: wk, rot: -0.06, align: "center" });
  },
});
sfx(0.3, "pop"); sfx(0.9, "whoosh", { gain: 0.6 }); sfx(at(0, "sunlight"), "pop", { pitch: 1.2 }); sfx(tWater, "click");

// ---- Scene 2: mechanism (line 1) ----
const S2 = { start: S1.end - 0.65, end: lineEnd(1) + 0.4 };
const tScatter = at(1, "scatters");
scene({
  name: "scatter", ...S2, bg: "#e7f1f4", transition: "wipe", tlen: 0.65,
  draw(t) {
    text("Short blue waves bounce around the most", 140, 170, { font: BODY, size: 60, color: INK, reveal: seg(t, S2.start + 0.5, S2.start + 1.8) });
    const colors = ["#e04b3a", "#f0a33b", "#f1d54a", "#58b368", "#3b7dd8", "#6a4bc4"];
    colors.forEach((c, i) => {
      const y = 420 + i * 70, go = seg(t, S2.start + 0.8 + i * 0.12, tScatter);
      const bounce = i >= 4 && t > tScatter ? Math.sin((t - tScatter) * 9 + i) * 60 * seg(t, tScatter, tScatter + 0.4) : 0;
      ink([[160, y], [lerp(160, 1500, go), y + bounce]], { t, color: c, width: 10, wobble: 1.5, seed: i });
    });
    if (t > tScatter) circle(1500, 600, 90 * pop(t, tScatter, 0.5), { fill: "rgba(59,125,216,.25)", stroke: TEAL });
  },
});
sfx(S2.start, "swoosh"); sfx(tScatter, "sparkle"); shake(tScatter, 8);

// ---- Scene 3: recap (line 2) ----
const S3 = { start: S2.end - 0.6, end: DUR };
scene({
  name: "recap", ...S3, bg: PAPER, transition: "fade",
  draw(t) {
    // something on screen from the first frame: a viewer with blue light arriving from every side
    const cx = W / 2, cy = 420, tLook = at(2, "look");
    circle(cx, cy, 46 * pop(t, S3.start + 0.3), { stroke: INK, lineWidth: 6, fill: PAPER });
    circle(cx + 12, cy - 6, 10 * pop(t, S3.start + 0.5), { fill: INK }); // pupil: it's an eye
    for (let i = 0; i < 8; i++) {
      const ang = (i / 8) * Math.PI * 2 + 0.2, r0 = 290, r1 = 78;
      arrow(cx + Math.cos(ang) * r0, cy + Math.sin(ang) * r0 * 0.85, cx + Math.cos(ang) * r1, cy + Math.sin(ang) * r1,
        { t, reveal: ease.outCubic(seg(t, tLook + i * 0.06, tLook + 0.5 + i * 0.06)), color: "#3b7dd8", width: 5, seed: i, bend: 0.08 });
    }
    const tb = at(2, "blue"), k = pop(t, tb, 0.5);
    const tw = measure("Scattered light = blue sky", { font: HAND, size: 84 });
    highlight(cx - tw / 2 - 16, 790, (tw + 32) * seg(t, tb, tb + 0.5), 100, { color: "#bcd8ff" });
    text("Scattered light = blue sky", cx, 865, { font: HAND, size: 84 * k, align: "center", color: INK });
  },
});
sfx(S3.start + 0.3, "pop"); sfx(at(2, "look"), "whoosh", { gain: 0.5 }); sfx(at(2, "blue"), "chime"); sfx(END + 0.2, "ding");

// Captions over everything (remove this if the style uses on-screen labels instead).
overlay(t => captions(t, { size: 40 }));
