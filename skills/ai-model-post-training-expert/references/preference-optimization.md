# Preference Optimization for Post-Training

## Overview

Preference optimization uses relative judgments rather than single gold answers. The core question is not "what is the only right response?" but "which response is better for this objective?"

## Preference Data Shapes

| Signal Type | Example Schema | Typical Methods |
|-------------|----------------|-----------------|
| Pairwise preference | prompt, chosen, rejected | DPO, ORPO, reward model training |
| Ranked list | prompt, candidates[], ranking | Convert to pairs, listwise reward models |
| Scalar score | prompt, response, score | Reward models, rerankers, judge models |
| Online rollout reward | prompt, trajectory, reward | PPO, GRPO, online RLHF |

## Data Quality Checks

- Verify prompt duplication rate and deduplicate obvious repeats.
- Check chosen and rejected responses for leakage, formatting drift, or template mismatch.
- Remove pairs where the "winner" only differs by length or boilerplate unless that is the true objective.
- Sample disagreements between labelers or judges and measure consistency.
- Hold out a preference validation set that is never used for fitting or prompt tweaking.

## Starting Guidance by Method

### DPO
- Best when you have static chosen/rejected pairs.
- Start with a strong SFT checkpoint instead of the raw base model when possible.
- Treat beta or temperature-like scaling as a real tuning knob; too high can overfit preferences quickly.

### ORPO
- Useful when you want a simpler objective that blends supervised and preference learning.
- Start from the same prompt template used in SFT.
- Watch for regressions on raw task accuracy if the odds-ratio term dominates.

### PPO or GRPO
- Use only when rollout reward depends on multi-step behavior or live tool interaction.
- Freeze evaluation criteria before starting.
- Clip aggressively and log reward, KL drift, and failure cases every run.

### Reward Models or Judge Models
- Fit the reward model on held-out preference data.
- Evaluate reward ranking quality separately from the policy model.
- Probe for reward hacking by testing verbose, evasive, or refusal-heavy outputs.

## Evaluation Checklist

- Compare preference win rate against the base and last-best adapted model.
- Run standard task benchmarks so alignment gains do not hide quality regressions.
- Measure refusal rate, verbosity drift, hallucination rate, and latency where relevant.
- Sample qualitative failures after every major metric gain; reward hacking often looks good numerically first.

## Failure Modes

| Failure Mode | Symptom | Response |
|--------------|---------|----------|
| Reward hacking | Metric improves but generations become verbose, evasive, or unnatural | Add regression checks and judge adversarial prompts |
| Template drift | Training looks stable but eval quality collapses | Align chat template and prompt formatting across train and eval |
| Preference overfitting | Win rate rises on train-style prompts but generalization drops | Increase holdout pressure, lower update strength, diversify pairs |
| Judge bias | Model learns to satisfy the judge rather than the user goal | Audit judge prompts, use multi-metric evaluation, sample manual checks |

## Output Expectations

For preference optimization tasks, provide:

1. Preference data schema and validation checks
2. Method choice rationale
3. Training configuration and stability knobs
4. Evaluation plan covering win rate, regression, and safety
5. Deployment notes on whether to ship the adapted model, the reward model, or both