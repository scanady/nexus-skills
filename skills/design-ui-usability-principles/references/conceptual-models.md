# Conceptual Models

A conceptual model is a mental representation of how something works. Users form one for every product whether the designer intended it or not. When the user's model matches reality the product feels intuitive; when it doesn't it feels broken. The designer's key job is shaping the **system image** so users build a correct model.

## The Three Models

- **Design model** — the designer's (complete, accurate) understanding.
- **User's model** — the user's (often partial, simplified, sometimes wrong) understanding, built entirely from the system image, not from docs.
- **System image** — everything the product communicates (appearance, behavior, feedback, responses). The only bridge between the other two.

```
Designer → Design Model → shapes → System Image → perceived by → User's Mental Model
```

If the system image is unclear or misleading, the user's model diverges and the product feels confusing.

| Alignment | Experience |
|-----------|-----------|
| match | predicts outcomes, confident, recovers easily |
| partial | basic tasks succeed, advanced ones fail |
| mismatch | confused, blames self, calls support (cranks thermostat to 90) |

## Building Correct Models

- **Make the system visible** — show state ("Syncing"/"Offline"), structure (folder tree), process (step indicator), relationships, history.
- **Provide a good framework** — familiar metaphors, a simplified model first, explain behavior not mechanism ("stored safely in the cloud", not "S3 bucket us-east-1"), be consistent.
- **Feedback that reinforces the model** — show cause→effect, confirm expectations, correct misunderstandings, reveal hidden states.

## Metaphors and Their Limits

Metaphors transfer existing knowledge (desktop, folders, trash, cart, inbox, clipboard, bookmark, dashboard) — they give predictability, vocabulary, and implied constraints. But every metaphor eventually breaks: folders vs files-in-multiple-places (aliases/tags), trash vs permanent empty, cart items selling out, "Save" vs auto-save, "cloud" vs physical servers. Handle limits by acknowledging them explicitly, extending with new concepts (tags alongside folders), providing escape hatches (show the real path), and dropping the metaphor when it causes confusion.

## Mismatch Diagnosis

1. **Symptom** — user tries a nonexistent action (model has extra capabilities) / can't find an existing feature (model lacks its location) / expects A gets B / repeats an action (model missing auto-behavior) / is afraid to act (model missing recovery).
2. **Identify the user's model** — "what did you expect? where did you look? how do you think X works?"
3. **Find the gap** — unclear system image / misleading metaphor / over-simplified model / prior-product interference.
4. **Fix the system image** — add signifiers/feedback/state; revise the metaphor; progressive disclosure; onboarding that highlights "how we're different."

## Progressive Model Building

Users shouldn't need the full model to start. Begin simple, reveal complexity on demand: beginner/advanced modes, layered settings, contextual education, graduated onboarding, inline help. Progression: simple model → hit an edge case → richer model → mastery (e.g. "Delete moves to Trash" → "I emptied Trash?" → "Trash is a 30-day holding period…").

## Evaluation Techniques
- **Draw-and-explain** — users sketch how it works; divergence from reality = system-image failure.
- **Prediction test** — "what will happen when you click this?"; wrong prediction = wrong model.
- **Teaching test** — a week-one user explains it to a newcomer; listen for inaccuracy, gaps, hedging.
- **Error analysis** — group errors by the incorrect assumption behind them; each names a model mismatch.

Teach the model through **design, not documentation** (users don't read manuals): onboarding tours, illustrative empty states, one-time inline hints, animated transitions (a file animating to trash teaches deletion), consistent patterns, and error messages that teach ("You can't delete a folder that contains files. Move or delete them first."). **Show, don't tell.**
