# Evidence Audit

Falsificationism applied to proposals: extract claims, design falsification criteria, assess evidence quality, surface competing explanations.

Goal: determine whether evidence actually supports the conclusion — not disprove it.

Key principle: A claim is only meaningful if you can specify what would disprove it.

## Process

1. **Extract** — Identify specific claims (often implicit)
2. **Falsify** — For each claim, specify what would disprove it
3. **Grade** — Evaluate evidence quality
4. **Bias check** — Check for systematic reasoning errors
5. **Compete** — Find alternative explanations for the same evidence

## Claim Extraction

| Type | Example | Often Hidden In |
|------|---------|-----------------|
| **Causal** | "X causes Y" | "Our refactor improved performance" |
| **Predictive** | "X will happen" | "Users will adopt this feature" |
| **Comparative** | "X is better than Y" | "React is the better choice for us" |
| **Existential** | "X doesn't exist" | "There's no alternative that meets our needs" |
| **Universal** | "X is always true" | "Microservices always improve team velocity" |
| **Quantitative** | "X is N" | "This will save 200 hours per quarter" |

### Extraction Method

For each statement:
1. Claim or definition?
2. If claim — what type?
3. What evidence is cited (or implied)?
4. What would make this false?

### Example

```
Statement: "Based on our pilot, Kubernetes will reduce deployment time by 60%."

Claims:
1. Pilot results are representative of production (Predictive)
2. Kubernetes is the cause of the reduction (Causal)
3. The 60% reduction will persist at scale (Quantitative)
```

## Falsification Criteria

| Claim | What Would Disprove It | How to Test |
|-------|----------------------|-------------|
| "Users want feature X" | <10% engage within 30 days | Feature flag + adoption metric |
| "Scales to 100K users" | >500ms at 50K users | Load test at target scale |
| "Migration takes 3 months" | 2+ unknown-unknowns in month 1 | Track surprise count |
| "Framework X is faster" | <5% benchmark difference | Controlled benchmark on representative workload |
| "This reduces costs" | TCO exceeds current cost within 12 months | Full TCO analysis |

### Unfalsifiable Claims (Red Flags)

| Pattern | Example | Problem |
|---------|---------|---------|
| Vague outcome | "This will improve things" | No measurable criterion |
| Moving goalposts | "It'll work eventually" | No time boundary |
| Circular reasoning | "Best because experts recommend it" | Evidence restates the claim |
| Unfalsifiable hedge | "This might help in some cases" | True by definition |

When found: ask "What specific, measurable outcome would tell us this worked or didn't?"

## Evidence Quality

### Evidence Quality Matrix

| Dimension | Strong | Weak |
|-----------|--------|------|
| **Sample size** | Large, representative | Single case, anecdote |
| **Recency** | Within 12 months | 2+ years old |
| **Relevance** | Same domain and scale | Different domain or scale |
| **Independence** | Multiple independent sources | Single source or vendor-provided |
| **Methodology** | Controlled, reproducible | Ad hoc, unreproducible |
| **Specificity** | Precise metrics and conditions | Vague or qualitative |

### Evidence Grading Scale

| Grade | Description | Reliability |
|-------|-------------|------------|
| **A** | Controlled experiment, large sample, reproducible | High confidence |
| **B** | Observational data, reasonable sample, consistent with other evidence | Moderate confidence |
| **C** | Case study, small sample, or single source | Low confidence — needs corroboration |
| **D** | Anecdote, opinion, or vendor marketing | Insufficient — don't base decisions on this alone |
| **F** | No evidence cited | Claim is unsupported |

### Common Weak Evidence Patterns

| Pattern | Example | Why It's Weak |
|---------|---------|---------------|
| Survivorship bias | "Companies using X are successful" | Ignores companies using X that failed |
| Cherry-picked metrics | "Response time improved 40%" | Other metrics may have worsened |
| Vendor benchmarks | "Our tool is 3x faster" | Benchmarks optimized for vendor's strengths |
| Appeal to authority | "Google does it this way" | Google's constraints aren't your constraints |
| Anchoring | "Industry average is X, we're at Y" | The average may not be the right benchmark |

## Cognitive Bias Check

| Bias | Description | Detection Signal |
|------|-------------|-----------------|
| **Confirmation bias** | Seeking evidence that confirms existing belief | Only positive evidence cited |
| **Survivorship bias** | Focusing on successes, ignoring failures | "All successful companies do X" |
| **Anchoring** | Over-relying on first piece of information | First estimate unchanged despite new data |
| **Sunk cost fallacy** | Continuing due to past investment | "We've spent 6 months on this" as justification |
| **Availability heuristic** | Overweighting recent or vivid examples | Decision based on one memorable incident |
| **Bandwagon effect** | "Everyone is doing it" | Trend adoption without fitness assessment |
| **Dunning-Kruger** | Overconfidence in unfamiliar domain | Confident claims outside expertise |
| **Status quo bias** | Preferring current state despite evidence for change | "It's always been this way" |

## Competing Explanations

For every conclusion: "What else could explain this evidence?"

1. State the evidence
2. State the proposed explanation
3. Generate 2-3 alternative explanations
4. Compare explanatory power

### Example

```
Evidence: "Deployment failures dropped 50% after adopting tool X."

Proposed: Tool X is better than the old tool.

Alternatives:
1. Team also started doing more code review in the same period
2. A particularly error-prone service was retired last month
3. Team gained experience that would have improved results with any tool
```

## Output Template

```markdown
## Evidence Audit: [Proposal/Decision]

### Claims Extracted

| # | Claim | Type | Evidence Cited |
|---|-------|------|---------------|
| 1 | [Specific claim] | Causal/Predictive/etc. | [What supports it] |
| 2 | [Specific claim] | Causal/Predictive/etc. | [What supports it] |

### Falsification Criteria

| Claim | What Would Disprove It | How to Test |
|-------|----------------------|-------------|
| #1 | [Specific criterion] | [Concrete test] |
| #2 | [Specific criterion] | [Concrete test] |

### Evidence Quality

| Claim | Evidence Grade | Key Weakness |
|-------|--------------|--------------|
| #1 | A/B/C/D/F | [Primary concern] |
| #2 | A/B/C/D/F | [Primary concern] |

### Bias Check

| Bias Detected | Where | Impact |
|--------------|-------|--------|
| [Bias] | [Where it appears] | [How it distorts the conclusion] |

### Competing Explanations

| Evidence Point | Proposed Explanation | Alternative Explanation | Explanatory Power |
|----------------|---------------------|------------------------|-------------------|
| [Evidence] | [Proposed] | [Alternative] | Proposed / Alternative / Unclear |

### Conclusion

[Whether the evidence supports the conclusion, at what confidence, and what would strengthen it]
```
