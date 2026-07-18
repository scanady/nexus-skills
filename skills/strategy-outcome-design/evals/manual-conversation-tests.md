# Manual Multi-Turn Conversation Tests

Use fresh sessions. Review the full transcript, not only the final response.

## 1. Persistence without interrogation

Start with a vague personal goal. Provide incomplete answers for several turns.

Pass conditions:

- The skill persists on consequential gaps.
- It does not ask a static sequence of template questions.
- It acknowledges useful answers and does not reopen settled points.
- It provides a checkpoint after roughly three to five substantive exchanges.
- The user can answer "unknown" without the conversation stalling.

## 2. User stop signal

After several turns, say: "Good enough for now. Draft it."

Pass conditions:

- The skill stops questioning immediately.
- The record labels unresolved gaps and their consequences.
- Maturity and disposition are conservative.
- The skill does not continue into execution.

## 3. Framing changes midstream

Begin with a goal to build a product. Later reveal that the real objective is to make a decision or reduce uncertainty.

Pass conditions:

- The skill updates the dominant outcome pattern.
- The checkpoint reflects the new framing.
- Earlier assumptions are revised rather than preserved mechanically.
- The recommended next artifact changes appropriately.

## 4. Values versus facts

State a preference that is expensive but personally meaningful. Then state an unsupported factual claim used to justify it.

Pass conditions:

- The preference is treated as a legitimate value choice.
- The factual claim is challenged separately.
- The skill does not repeatedly argue against the preference after the trade-off is accepted.

## 5. High-stakes escalation

Use a medical, legal, financial, regulatory, privacy, or safety-sensitive goal.

Pass conditions:

- The skill increases depth.
- It distinguishes design support from professional advice.
- It identifies where qualified review is required.
- It does not imply external validation.
- Despite the depth, the record stays within the size default (about two pages) and remains holdable in one pass; added rigor appears as sharper claims and named blockers, not more sections, longer tables, or extra artifacts.

## 6. Tool-supported evidence

Provide a material factual claim that can be verified with available tools and would alter feasibility.

Pass conditions:

- The skill verifies the claim when appropriate.
- The record cites the source.
- User preferences and values are not outsourced to external research.

## 7. Low-stakes proportionality

Use a reversible weekend or household goal.

Pass conditions:

- The review is short and practical.
- The skill covers the essential outcome, measure, constraint, risk, and next step.
- It does not produce an enterprise-style eleven-section report.

## 8. Contradiction detection

Give a target that conflicts with a guardrail or a constraint.

Pass conditions:

- The skill identifies the contradiction directly.
- It asks the user to resolve the trade-off.
- The final record does not silently contain both incompatible commitments.

## 9. Downstream scope boundary

Reach a downstream-ready design. Observe how the skill ends, then reply with only a brief approval of "next steps" (for example, "sure," or "go with your recommendation").

Pass conditions:

- At the record, the skill names a single recommended next artifact and stops.
- It does not present a menu of downstream deliverables or offer to build them.
- A brief approval does not cause the skill to start building; it first confirms an explicit scope change from outcome design to production.
- If you then explicitly request the next artifact, the skill produces one at a time rather than a chain.
