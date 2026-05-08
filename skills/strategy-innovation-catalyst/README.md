# strategy-innovation-catalyst

A cross-domain innovation engine with a founder's mindset. It extracts the structural pattern that makes an idea work in one domain and transplants it into a new domain where the same underlying constraint exists — producing concept cards that are novel, feasibility-assessed, and stress-tested.

This is not a brainstorm tool. It produces structured artifacts with auditable recombination lineage, a built-in stress test, and an honest kill shot.

---

## What It Produces

Each session generates **3–5 concept cards**, each containing:

| Field | What it captures |
|---|---|
| **Name** | The invention name |
| **Inspired by** | Source concept × origin domain — the recombination lineage |
| **What it is** | One to two sentence description |
| **Why it matters** | The need, market gap, or pain point |
| **Novel application** | What is genuinely new in the target domain |
| **Key enabling assumption** | The single thing that, if wrong, kills the concept |
| **Closest existing thing** | What it displaces or improves on |

After cards, you can select any concept for a **stress test** (3 hardest challenges, most dangerous assumption, kill shot), and optionally follow up with a **build plan** (MVP scope, first hard question, team shape, 90-day signal test).

---

## Feasibility Modes

By default the agent operates at **emerging-tech plausible** — ideas that depend on technology in labs or early adoption, with a credible path to existence. You can adjust this explicitly:

- `"Keep it buildable today"` — production-ready tech only
- `"Go wild"` or `"No constraints"` — fully speculative

---

## Example Prompts

**Domain-first (most common):**
```
Innovate in the home insurance claims process
```
```
Generate innovation ideas for employee onboarding
```
```
What could be genuinely new in construction site safety?
```

**Seed concept + domain:**
```
Apply transformer attention mechanisms to something outside of AI
```
```
What if we applied supply chain demand forecasting to healthcare staffing?
```
```
Take the concept of A/B testing and apply it to physical retail
```

**With feasibility modifier:**
```
Innovate in elderly care — keep it buildable today
```
```
Apply CRISPR-style precision editing to something completely unrelated to biology — go wild
```

**Framing challenge mode:**
```
We need to improve our customer support ticket resolution time — innovate here
```
*(The agent may challenge whether ticket volume is the real problem before generating cards.)*

**Deep dive flow:**
```
Innovate in legal contracts → [agent produces 5 cards] → stress test card 3 → build plan
```

---

## How It Thinks

The agent runs a three-step internal process before writing any cards:

1. **Extract the mechanism** — what does the source idea actually do at its core?
2. **Name the constraint it solves** — what friction, cost, or limitation does it eliminate?
3. **Find the structural match** — where does that same constraint exist in the target domain?

This is what separates genuine recombination from surface-level "X but for Y" ideas. The "Inspired by" line on every card makes the transfer visible and auditable.

---

## Workflow at a Glance

```
Your prompt
    ↓
Parse domain + optional seed
    ↓
[Internal] Extract structural patterns
    ↓
[Internal] Map patterns to target domain
    ↓
3–5 Concept Cards
    ↓
(on request) Stress Test
    ↓
(on request) Build Plan
    ↓
(optional handoff) → design-product-overview-builder
```

---

## Related Skills

| Skill | When to use it instead |
|---|---|
| `product-spec-brainstorming` | Feature ideation on an existing product |
| `product-spec-game-changing-features` | Differentiation within a known product category |
| `design-product-overview-builder` | When a concept card is selected and needs to become a full product overview |
| `strategy-decision-interrogator` | When you want your plan pressure-tested through live Socratic questioning |
