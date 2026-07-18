# Human Error

There is no such thing as human error — there is only bad design. When someone errs, the cause is almost always a design flaw: poor feedback, misleading signifiers, bad mappings, missing constraints, or a broken conceptual model. Blaming users is the designer's greatest failure. Instead, prevent errors, tolerate them, and make recovery easy.

## Slips vs Mistakes

| | Slips | Mistakes |
|--|-------|----------|
| Definition | correct intention, wrong action | wrong intention, correctly executed |
| Cause | attention/motor/habit failure | wrong mental model, wrong rule, faulty reasoning |
| Noticed | often immediately | maybe not until consequences appear |
| Fix approach | make actions distinct + recoverable | build correct models + better information |

## Slip Types

- **Action-based** — adjacent target (Delete next to Edit), similar habitual action (old password), description similarity (wrong file from similar names). Fix: distance + distinct style; distinguishing info prominent.
- **Memory-lapse** — omitted step (no attachment after "see attached"), lost place, forgotten intention. Fix: detect omissions, persist state, show progress, provide search/history.
- **Mode errors** — right action, wrong mode (typing with Caps Lock; silent mode change). Fix: always show the current mode; announce mode changes; follow platform shortcut conventions.
- **Capture errors** — a frequent action overrides the intended rare one (autopilot to old office). Fix: interruptions at decision points.

## Mistake Types

- **Rule-based** — wrong rule / misclassified situation / outdated rule ("Reply All" habit). Fix: show recipient count, diagnose the situation, version/timestamp rules.
- **Knowledge-based** — incomplete/incorrect model, analogy failure (undo works as a stack, not a timeline). Fix: make the model explicit; redesign the system image.
- **Memory-lapse** — forgotten goal/plan/evaluation criteria. Fix: reminders, task lists/checklists, before/after comparison.

## Prevention

- **Slips** — separate destructive from routine actions by distance and color; confirm irreversible actions; visible mode indicators; interrupts at decision points; auto-detect likely omissions; constraints.
- **Mistakes** — clear conceptual models; contextual info at the point of decision; safe exploration with undo; wizards/guides; sensible defaults; visible checklists; comparisons.

## Recovery

- **Undo** — single, multi-level, time-limited toast, version history, soft delete.
- **Confirmation** — only for high-consequence irreversible actions ("Delete 47 files permanently?"), never routine ("Are you sure you want to save?") — routine confirmations breed dialog blindness.
- **Autosave** — continuous, with a visible "All changes saved" indicator, named save points, and conflict resolution.
- **Clear error messages** — `what happened → why → how to fix → alternative`. "We couldn't save your changes. Your connection dropped. Check it and retry, or download a copy. [Retry][Download]" beats "Error 500."

## Error Tolerance

Assume users will err and minimize consequences: reversibility (soft delete, versioned edits), low-cost experimentation (previews, sandboxes, undo), graduated consequences (minor action = minor consequence), data preservation (never discard user data without confirmed intent; form data survives errors/navigation/timeout), graceful degradation.

## Swiss-Cheese Defenses

Errors become disasters only when holes in every defense layer align. Give critical actions **≥3 layers**: (1) UI constraints prevent the action, (2) warnings alert before proceeding, (3) immediate feedback lets the user catch it, (4) undo/reversal, (5) recovery (backup, support). If one layer fails, another catches it.

## Audit

Prevention: destructive actions separated + confirmed (irreversible only); input constraints; omission detection; visible mode indicators; safe defaults. Detection: feedback <100ms; inline errors that say what/why/how without blame; state always visible. Recovery: undo for non-destructive actions; recoverable trash; form data preserved on error; autosave; version history; session recovery. Systemic: errors logged for design improvement (not user blame); common errors tracked and addressed; error rate treated as a product metric.
