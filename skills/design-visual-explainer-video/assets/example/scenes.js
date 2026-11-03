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
const S1 = { start: 0, end: at(1, "holds") };
const tSun = at(0, "sunlight");
scene({
  name: "hook", ...S1, bg: PAPER, transition: "cut",
  draw(t) {
    // The hook is on screen from frame 0: that frame is the thumbnail, and a muted viewer reads it first.
    text("Why is the sky blue?", W / 2, 300, { font: HAND, size: 110, align: "center", color: INK });
    ink([[W / 2 - 360, 340], [W / 2 + 360, 332]], { t, reveal: ease.outCubic(seg(t, 0.9, 1.5)), color: RED, width: 7 });
    if (IMAGES.sun) img("sun", W / 2, 640, { h: 380, scale: pop(t, tSun, 0.5), rot: noise(t * 0.5) * 0.05 });
    text("not the water", W / 2 + 420, 780, { font: HAND, size: 72, color: RED, alpha: seg(t, tSun, tSun + 0.3), rot: -0.06, align: "center" });
  },
});
sfx(0.9, "whoosh", { gain: 0.6 }); sfx(tSun, "pop", { pitch: 1.2 });

// ---- Scene 2: mechanism (line 1) ----
const S2 = { start: S1.end - 0.65, end: lineEnd(1) + 0.8 };
const tAir = at(1, "air"), tScatter = at(1, "scatters"), tShort = at(1, "short"), tWaves = at(1, "waves");
scene({
  name: "scatter", ...S2, bg: "#e7f1f4", transition: "wipe", tlen: 0.65,
  draw(t) {
    // The picture does what the voice says: long waves pass through the air, short waves leave it in every direction.
    text("Short blue waves bounce around the most", 140, 170, { font: BODY, size: 60, color: INK, reveal: seg(t, S2.start + 0.4, S2.start + 1.2) });
    const colors = ["#e04b3a", "#f0a33b", "#f1d54a", "#58b368", "#3b7dd8", "#6a4bc4"];
    const ax = 900, ay = 600, out = seg(t, tScatter, tScatter + 0.7), sides = [-2.5, -2, -1.2, 1.1, 2, 2.6];
    colors.forEach((c, i) => {
      const y = 400 + i * 60;
      ink([[140, y], [ax, ay]], { t, reveal: seg(t, S2.start + 0.4 + i * 0.05, tScatter), color: c, width: 10, wobble: 1.5, seed: i });
      if (i < 4) ink([[ax, ay], [1780, y]], { t, reveal: out, color: c, width: 10, wobble: 1.5, seed: i + 6 });
      else for (let k = 0; k < 3; k++) {
        const ang = sides[(i - 4) * 3 + k];
        arrow(ax, ay, ax + Math.cos(ang) * 360, ay + Math.sin(ang) * 360, { t, reveal: out, color: c, width: 8, seed: i * 3 + k, bend: 0.05 });
      }
    });
    const k = pop(t, tAir, 0.5);
    [[0, 0, 42], [-44, 28, 26], [40, 32, 30], [34, -38, 22]].forEach(([dx, dy, r]) => circle(ax + dx, ay + dy, r * k, { fill: "rgba(47,143,138,.45)", stroke: TEAL }));
    text("air", ax, 730, { font: HAND, size: 60, color: INK, align: "center", alpha: seg(t, tAir, tAir + 0.3) });
    text("Blue scatters", 200, 900, { font: HAND, size: 72, color: "#2b5fb0", alpha: seg(t, tShort, tShort + 0.3) });
    text("Red passes through", 1780, 340, { font: HAND, size: 72, color: "#b7341f", align: "right", alpha: seg(t, tWaves, tWaves + 0.3) });
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
overlay(t => captions(t, { size: 46, font: BODY }));
