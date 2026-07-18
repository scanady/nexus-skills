# Constraints

Constraints limit possible actions to prevent errors. The principle: instead of telling users what *not* to do, make the wrong action impossible. Every constraint added is one fewer error the user can make.

## Four Types

- **Physical** — shape/size/material restricts action (USB-A one way; childproof cap). Digital equivalent: input masks, character limits, file-type restrictions, min/max values.
- **Cultural** — shared social conventions (red=stop, OK/Cancel order, double-click to open). Powerful but invisible; violating them confuses even when the system "works."
- **Semantic** — meaning of the situation limits options (a rearview mirror only makes sense facing back; can't review an order before adding items). Digital: contextual menus, conditional fields.
- **Logical** — reasoning limits by exclusion (last puzzle piece; radio buttons; can't format text before selecting it; form won't submit until required fields are filled).

## Digital Implementations

**Input validation** — type/range/length/format/enum restrictions, ideally real-time. Best practice: prevent over detect (date picker vs typed date); validate as the user types; explain what's expected ("Phone must be 10 digits"); accept flexible formats and normalize internally.

**Progressive disclosure** — constrain what's shown: collapsed advanced sections, wizards/steppers, conditional fields, role-based visibility, contextual menus.

**Disabled states & forced sequences** — disabled button (with a tooltip explaining *why*), locked wizard steps, conditional enable, time-gated actions, auth gates. **Always explain why something is disabled** — an unexplained disabled control is a constraint that frustrates instead of guiding.

**Undo/recovery** (constrains error *impact*) — immediate undo toast, action history, soft delete (trash), autosave with versions, confirmation dialogs.

## Confirmation Dialogs — Use Sparingly

Appropriate only for **irreversible** (delete account), **high-consequence** (charge a card), or **unusual/rare** actions. NOT for routine (save, close), easily-reversible, or frequent actions. The trap: confirmations on routine actions breed "dialog blindness" — users click Yes without reading, so the *one* confirmation that matters gets dismissed reflexively.

## The Constraint Spectrum

```
Too few                    Just right                Too many
Error-prone, confusing  →  Error-free, guided     →  Frustrating, rigid, patronizing
```

Aim for the middle: enough to prevent errors, not so many users feel restricted.

## Over-Constraining Anti-Patterns

| Anti-pattern | Better |
|--------------|--------|
| blocking copy-paste in forms | allow paste; validate the result |
| session timeout with no warning | warn before, offer extension |
| forced 90-day password change | monitor for breaches instead |
| all fields required when most aren't | mark truly required, make the rest optional |
| blocking submit for non-critical warnings | distinguish errors (block) from warnings (allow with note) |

## Audit

Prevention: type/range/format constraints on inputs; pickers over free text; required fields enforced; precondition-dependent actions disabled with explanation; destructive actions confirmed or undoable. Recovery: undo for non-destructive actions; soft delete; autosave; session recovery. Appropriateness: no constraint for the system's convenience at the user's expense; constraints match error severity; no unnecessary data required; paste allowed; flexible formats normalized.
