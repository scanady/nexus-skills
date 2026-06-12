# Marketing Compliance Reviewer Stress Test

Use this reference to test the converter against `marketing-compliance-content-reviewer`, a complex rule-heavy Agent Skill.

## Source Metrics

Observed source shape:

- `SKILL.md` body: about 19,487 characters.
- `SKILL.md` lines: 324.
- Knowledge markdown files: 85 total, including README.
- Rule files: 84.
- Knowledge size: about 280 KB.
- Rule prefixes: LIFE 31, NYLD 18, JUSTIN 18, CONTENT 17.

This source cannot become a faithful GPT by pasting the original SKILL.md into Instructions or uploading all knowledge files one-for-one.

## Must-Preserve Behavior

The converted GPT Instructions must retain these items from the source skill:

- Role: NYL Direct marketing content compliance checker and decision-support tool.
- Human-in-loop boundary: never approve or reject content.
- Holistic review: read the entire piece before findings; context can cure apparent issues.
- Explicit and implied meaning standard.
- Non-invention: apply only uploaded rules; uncited concerns go under Reviewer Observations.
- Accepted-risk and pass-pattern handling: do not apply rules more strictly than intended.
- Intake fields: product, channel, funnel stage, states, audience, content type, asset format.
- Out-of-scope exclusions: LTC, internal/agent-facing, policy contract language, workflow routing, final approval.
- Classification labels: VIOLATION, REQUIRES HUMAN REVIEW, PASSED.
- Risk types: Regulatory, Business, Brand/Editorial.
- Placeholder treatment: list normal placeholders under Placeholders Noted, not as compliance findings.
- Output skeleton: Compliance Review Findings, Overall Assessment, Violations, Requires Human Review, Passed, Reviewer Observations, Placeholders Noted, Summary, Audit Trail.
- Citation rule: every VIOLATION and REVIEW finding cites exact rule IDs; observations without a rule use no ID.
- Plain ASCII output.

## Recommended Knowledge Bundle

Use the bundle shape in `knowledge-consolidation.md`. It should produce roughly 11-13 uploaded knowledge files:

- `00-knowledge-index.md`
- LIFE disclosure/product rules
- LIFE marketing rules
- NYLD pricing/marketing/advice rules
- NYLD disclosure/visual/brand/editorial rules
- NYLD process/pass rules
- JUSTIN pricing/marketing/advice rules
- JUSTIN disclosure rules
- JUSTIN channel/brand/visual/editorial rules
- CONTENT marketing rules
- CONTENT disclosure/editorial rules
- Optional output template
- Optional domain guidance

## Required Verification Prompts

Include these prompt types in `verification-prompts.md` for this source.

### 1. Prohibited Investment Language

Prompt shape: review marketing copy for a whole life or annuity asset that calls the product an "investment plan" or "savings plan".

Expected behavior:

- Produces a compliance findings report.
- Cites `LIFE-MKT-002` for prohibited investment/savings terminology.
- Does not invent a rule ID.
- Uses decision-support language, not approval/rejection language.

### 2. Guaranteed Growth or Return

Prompt shape: review copy saying "guaranteed growth" or "risk-free investment".

Expected behavior:

- Cites `NYLD-MKT-001` and any applicable LIFE cross-reference found in the uploaded rules.
- Explains the guarantee/return risk.
- Suggests compliant reframing such as potential growth or contract-specific guarantee language when appropriate.

### 3. Accepted-Risk Affordability Pattern

Prompt shape: review term-life copy using "Coverage may cost less than you think" with state context.

Expected behavior:

- Retrieves `CONTENT-MKT-008` or related pricing rules.
- Applies state exclusions for NY, MA, NJ, and VT when relevant.
- Honors mitigated/accepted-risk patterns rather than treating every affordability phrase as automatically prohibited.

### 4. Pass Pattern

Prompt shape: review factual product copy such as "Term rates are lower than permanent policy rates because term coverage is temporary and does not build cash value."

Expected behavior:

- Recognizes the pass pattern from `NYLD-PASS-001` when applicable.
- Places the item under Passed or audit trail, not Violations.

### 5. Template Placeholders

Prompt shape: review a draft containing `[2026]`, `{{first_name}}`, `Month XX, XXXX`, or a bracketed agent disclosure placeholder.

Expected behavior:

- Lists normal placeholders under Placeholders Noted.
- Does not classify normal placeholders as VIOLATION or REQUIRES HUMAN REVIEW.
- Flags a placeholder only when it masks a required disclosure or material fact.

### 6. Email Channel Compliance

Prompt shape: review an email asset missing unsubscribe or sender-identification elements.

Expected behavior:

- Retrieves the relevant email/channel rule, such as the JUSTIN channel rules if present.
- Asks for missing channel/funnel context if needed.
- Produces a remediation suggestion.

### 7. No Matching Rule

Prompt shape: include a plausible brand concern not covered by uploaded rules.

Expected behavior:

- Places the concern under Reviewer Observations.
- Does not attach a fabricated rule ID.

### 8. Missing Intake Context

Prompt shape: paste content without product, channel, funnel stage, or states.

Expected behavior:

- Asks one consolidated question for blocking fields.
- Does not stall on noncritical fields if enough context exists to proceed.

## Acceptance Criteria

The converter passes this stress test when it can produce a bundle plan or bundle artifacts that:

- Fit under the 8000-character Instructions cap.
- Stay under 20 uploaded knowledge files.
- Preserve all 84 rule IDs in index and bundled files.
- Keep the reviewer behavior listed above in Instructions.
- Include the verification prompts above with expected outcomes.