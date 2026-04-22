# Scoring and Reporting Model

Use this model to generate consistent area ratings and overall release recommendations.

## Area Weights

| Area | Weight |
|---|---:|
| Brand standards | 15 |
| Company policy and standards | 20 |
| Industry guidelines | 15 |
| Regulatory standards | 35 |
| Product and suitability alignment | 15 |

Total possible score: 100

## Scoring Steps

1. Score each area from 0 to 100.
2. Multiply each area score by its weight percentage.
3. Sum weighted values to produce overall score.
4. Apply color rating:
   - Green: 85-100
   - Yellow: 60-84
   - Red: 0-59
5. Apply release recommendation:
   - Approve: no blocking issues and overall Green
   - Revise: no unresolved Red blockers, but overall Yellow or open P1 items
   - Do Not Release: any unresolved blocking Red issue

## Minimum Finding Fields

Each finding should include:

- ID
- Area
- Component
- Finding summary
- Risk rationale
- Severity (High/Med/Low)
- Blocking (Yes/No)
- Recommended fix
- Preferred compliant alternative
- Evidence needed to close

## Consistency Guardrails

- Do not assign Green if any unresolved blocking issue exists.
- Do not assign Approve if required disclosures are missing.
- Do not treat missing substantiation as a minor issue.
- Recalculate overall score after remediations.

## Sample Calculation

| Area | Raw score | Weight | Weighted contribution |
|---|---:|---:|---:|
| Brand standards | 90 | 15% | 13.5 |
| Company policy | 80 | 20% | 16.0 |
| Industry guidelines | 78 | 15% | 11.7 |
| Regulatory standards | 62 | 35% | 21.7 |
| Product/suitability alignment | 85 | 15% | 12.8 |

Overall score: 75.7 (Yellow) -> Recommendation: Revise
