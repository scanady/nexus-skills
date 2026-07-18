# Mappings

A mapping is the relationship between a control and its effect. **Natural** mappings — where the control layout corresponds to the layout of what's controlled — are obvious and need no explanation. Arbitrary mappings force users to memorize or guess.

## The Mapping Spectrum

| Quality | Characteristic | Learning | Example |
|---------|---------------|----------|---------|
| Natural/direct | control *is* the thing | none | touchscreen: tap the element itself |
| Spatial analog | control layout mirrors output | minimal | seat-shaped seat adjuster |
| Cultural convention | learned but universal | one-time | red=stop, green=go |
| Labeled arbitrary | no inherent link, but labeled | moderate | labeled switch panel |
| Unlabeled arbitrary | no link, no label | high (memorize) | unmarked row of identical switches |

Any unlabeled-arbitrary mapping is a failure — convert it to spatial, cultural, or at least labeled.

## Spatial Mapping (most powerful)

Arrange controls in the same pattern as what they control; moving a control up should move something up; keep each control near its target. Digital: inline editing (click the cell you edit), WYSIWYG, drag-to-reorder, pan-the-map-by-dragging, layout builders.

## Proximity Mapping

Place the control next to what it affects. Inline action buttons per row, contextual toolbar above a selection, section-level "Add" button, inline field validation, popover on the triggering element. Failures: a global action bar far from content, settings on a separate page with no preview, an error summary at the top with no inline markers.

## Cultural Mapping

Learned conventions: red=danger / green=safe, X-top-right=close, floppy=save, cart=purchases, LTR/RTL reading order. When conventions conflict: flip arrows by locale, pair color with icon+text, use unambiguous date formats ("10 Feb 2024"), pick a default scroll direction and let users configure.

## Sequential Mapping

Order controls/steps to match the natural task order — temporal order, reading order, dependency order. Wizards left-to-right, form fields in task logic, chronological feeds, breadcrumbs root→current. Failures: City before Street, payment before cart review, Cancel placed before Submit in the reading flow.

## Scorecard

Rate 1–5: spatial correspondence, proximity, direction, convention, sequence, labeling (when not natural), consistency. Average 4.5–5 = excellent (maintain); 3.5–4.4 = good but learnable (improve labels/proximity); 2.5–3.4 = redesign layout; <2.5 = fundamental redesign.

## Classic Failures
- **Stovetop knobs** — 4 knobs in a row for a 2×2 burner grid → arrange knobs in a matching 2×2 or adjacent to each burner.
- **Light-switch panel** — 6 identical switches with no spatial link → floor-plan layout or per-zone labels.
- **Hotel shower** — one unmarked knob for temp + flow → separate controls, color hot/cold, consistent rotation.

## Exercises
- **Map the controls** — sketch control layout and output layout, connect with lines; crossing/long lines = poor mapping.
- **Label-removal test** — remove labels; if users still can't tell what affects what, the mapping leans on labels.
- **Sequential walkthrough** — list task steps chronologically vs the on-screen control order; divergence = broken sequence.
- **Convention audit** — classify each mapping as spatial / cultural / labeled / unlabeled-arbitrary; fix every unlabeled-arbitrary one.
