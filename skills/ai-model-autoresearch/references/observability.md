# Observability & Monitoring Guide

## Purpose

An autonomous experiment loop runs without human supervision. Without proper observability, you cannot tell whether it's making progress, wasting compute, drifting into pathological behavior, or silently failing. This guide covers everything needed to monitor, diagnose, and intervene in the loop — and everything that should be documented throughout the process to ensure the work is reproducible, auditable, and trustworthy.

---

## Experiment Observability

### Results Visualization

`results.jsonl` captures structured data per experiment. Visualize it to spot patterns the raw log hides.

**Metric progression chart** — Plot the primary metric (y-axis) over experiment number (x-axis). Color by status (keep/discard/crash). This is the single most important visualization during a run.

```python
import pandas as pd
import matplotlib.pyplot as plt

import json

with open("results.jsonl") as f:
    results = pd.DataFrame([json.loads(line) for line in f])
fig, ax = plt.subplots(figsize=(12, 5))

colors = {"keep": "#2ecc71", "discard": "#e74c3c", "crash": "#7f8c8d"}
for status, group in results.groupby("status"):
    ax.scatter(group.index, group["primary_metric"], c=colors.get(status, "#333"),
               label=status, s=40, alpha=0.7)

# Draw the "advancing frontier" — best metric so far
best_so_far = results["primary_metric"].cummax()  # or cummin for "lower is better"
ax.plot(best_so_far, color="#2c3e50", linewidth=1.5, linestyle="--", label="best so far")

ax.set_xlabel("Experiment #")
ax.set_ylabel("Primary Metric")
ax.legend()
ax.set_title("Experiment Progression")
plt.savefig("output/[slug]/monitoring/metric_progression.png", dpi=150, bbox_inches="tight")
```

**Additional visualizations to generate:**

| Chart | What It Reveals |
|---|---|
| Metric vs. parameter count scatter | Are bigger models actually better? |
| Metric vs. peak VRAM | Resource efficiency of improvements |
| Keep rate over time (rolling window) | Is the agent still finding improvements or plateauing? |
| Crash rate over time | Is the agent destabilizing? |
| Description word cloud or category counts | What types of experiments are being tried? |
| Metric improvement magnitude histogram | Are gains diminishing? |

### Experiment Tracking Integration

For long runs, consider integrating with experiment tracking tools. The prepare script or a wrapper can log to these:

| Tool | Strengths | Setup Complexity |
|---|---|---|
| **TensorBoard** | Built into PyTorch, local, free | Low — add `SummaryWriter` to prepare script |
| **Weights & Biases (W&B)** | Rich dashboards, team collaboration, cloud-hosted | Low — `wandb.init()` + `wandb.log()` |
| **MLflow** | Open-source, model registry, self-hosted option | Medium — requires server setup |
| **JSONL + matplotlib** | Zero dependencies, full control | Lowest — already have `results.jsonl` |

**Recommendation:** Start with `results.jsonl` + a visualization script. Add W&B or TensorBoard only if running > 100 experiments or collaborating across team members. The visualization script should be included in the project and runnable at any time:

```bash
python src/[slug]/visualize_results.py  # Reads output/[slug]/results.jsonl, outputs charts to output/[slug]/monitoring/
```

---

## Circuit Breakers & Alerting

Circuit breakers automatically detect when the autonomous loop enters a pathological state and either correct course or halt for human review.

### Circuit Breaker Thresholds

| Condition | Threshold | Action |
|---|---|---|
| **Consecutive crashes** | 5 in a row | Halt — the agent is stuck in a broken region of the search space |
| **Consecutive discards** | 20 in a row | Alert — the agent may have plateaued or is exploring unproductive directions |
| **Metric regression** | Best metric hasn't improved in 30 experiments | Alert — consider widening the search space or reviewing data quality |
| **Resource exhaustion** | Disk usage > 90% of available | Halt — checkpoint/data accumulation is filling storage |
| **VRAM creep** | Peak VRAM exceeds 95% of GPU memory for 3 consecutive runs | Alert — next run likely OOMs |
| **Time budget violation** | Run exceeds 3× time budget | Kill run, log as crash, continue |
| **NaN/Inf in metric** | Any occurrence | Kill run, log as crash, revert |

### Implementation in the Program File

Add circuit breaker checks to the experiment loop protocol:

```markdown
AFTER EACH EXPERIMENT:

1. Record result in results.jsonl
2. **Circuit breaker checks:**
   - Count consecutive crashes: if >= 5, STOP and report
   - Count consecutive discards: if >= 20, log a warning, re-read all in-scope files,
     and try a fundamentally different approach (architecture swap, not hyperparameter tweak)
   - Check disk usage: if data/[slug]/ + output/[slug]/checkpoints/ > 90% disk, STOP and report
3. Continue to next experiment
```

### Notification Mechanisms

For unattended multi-hour runs, add lightweight notification:

```python
# Example: simple webhook notification on circuit breaker trigger
import urllib.request, json

def notify(message, webhook_url=None):
    """Send alert when circuit breaker triggers. Configure webhook_url in constants."""
    if not webhook_url:
        print(f"⚠ ALERT: {message}")
        return
    payload = json.dumps({"text": message}).encode()
    req = urllib.request.Request(webhook_url, data=payload,
                                 headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)
```

---

## Convergence Detection

Detecting when the loop has plateaued prevents wasting compute on diminishing returns and signals when to shift strategy.

### Statistical Plateau Detection

Monitor a rolling window of experiments. If the best metric hasn't improved beyond a significance threshold in N experiments, the loop has likely converged.

```python
def detect_plateau(results_df, metric_col, window=20, min_improvement=0.001, direction="higher"):
    """
    Returns True if the best metric hasn't meaningfully improved in the last `window` experiments.

    - window: number of recent experiments to analyze
    - min_improvement: minimum absolute improvement to count as "real progress"
    - direction: "higher" or "lower" (whether the metric should increase or decrease)
    """
    if len(results_df) < window:
        return False

    recent = results_df.tail(window)
    prior = results_df.iloc[:-window]

    if len(prior) == 0:
        return False

    if direction == "higher":
        best_prior = prior[metric_col].max()
        best_recent = recent[metric_col].max()
        return (best_recent - best_prior) < min_improvement
    else:
        best_prior = prior[metric_col].min()
        best_recent = recent[metric_col].min()
        return (best_prior - best_recent) < min_improvement
```

### Strategy Escalation on Plateau

When plateau is detected, the agent should escalate to more radical changes:

| Stage | Trigger | Strategy |
|---|---|---|
| **Normal exploration** | Default | Incremental changes — hyperparameters, minor architecture tweaks |
| **Widened search** | No improvement in 15 experiments | Try different optimizer, learning rate schedule, or regularization approach |
| **Architecture pivot** | No improvement in 30 experiments | Switch architecture family (e.g., Transformer → Mamba, CNN → ViT) |
| **Simplification pass** | No improvement in 40 experiments | Remove components — does the model hold performance with less? |
| **Back to basics** | No improvement in 50 experiments | Re-read all docs, particularly data readiness report and EDA. Is the data ceiling the bottleneck? |

Include these escalation stages in the program file so the agent knows how to respond to plateau.

---

## Checkpoint Management

Model checkpoints can accumulate rapidly during an autonomous loop. Without a strategy, disk fills up and previous best models are lost.

### Checkpoint Strategy

| What to Save | When | Retention Policy |
|---|---|---|
| **Best model weights** | Whenever primary metric improves (status: keep) | Keep indefinitely — this is the prize |
| **Current model weights** | End of every training run | Overwrite each time — only need the latest for eval |
| **Periodic snapshots** | Every 25 experiments | Keep last 3 snapshots — enables rollback without keeping everything |

### Implementation

```python
import shutil
from pathlib import Path

CHECKPOINT_DIR = Path("output/[slug]/checkpoints/")
BEST_MODEL_PATH = CHECKPOINT_DIR / "best_model.pt"
CURRENT_MODEL_PATH = CHECKPOINT_DIR / "current_model.pt"

def save_checkpoint(model, metric, experiment_num, is_best=False):
    """Save model checkpoint with metadata."""
    CHECKPOINT_DIR.mkdir(exist_ok=True)
    state = {
        "model_state_dict": model.state_dict(),
        "metric": metric,
        "experiment_num": experiment_num,
    }
    torch.save(state, CURRENT_MODEL_PATH)
    if is_best:
        shutil.copy(CURRENT_MODEL_PATH, BEST_MODEL_PATH)
    # Periodic snapshot every 25 experiments
    if experiment_num % 25 == 0:
        snapshot_path = CHECKPOINT_DIR / f"snapshot_exp{experiment_num:04d}.pt"
        shutil.copy(CURRENT_MODEL_PATH, snapshot_path)
        # Prune old snapshots: keep only last 3
        snapshots = sorted(CHECKPOINT_DIR.glob("snapshot_*.pt"))
        for old in snapshots[:-3]:
            old.unlink()
```

### Disk Budget

Estimate checkpoint storage before starting:
- Model size × retention count = minimum disk budget for checkpoints
- Add data directory size + results log growth
- Set the disk circuit breaker threshold accordingly

---

## Resource Monitoring

Track resource utilization beyond peak VRAM to diagnose bottlenecks and plan capacity.

### Metrics to Track Per Experiment

| Metric | How to Capture | Why It Matters |
|---|---|---|
| **Peak VRAM (MB)** | `torch.cuda.max_memory_allocated()` | Already tracked — OOM prevention |
| **GPU utilization %** | `nvidia-smi --query-gpu=utilization.gpu` | Low utilization → data loading bottleneck |
| **Training throughput** | Samples/sec or tokens/sec | Quantifies training efficiency across architectures |
| **Disk usage (cumulative)** | `shutil.disk_usage()` | Detect storage creep from checkpoints/logs |
| **Wall-clock time** | Already tracked as `training_seconds` | Verify time budget compliance |

### Extended Results Schema

Add resource fields to each `results.jsonl` entry:

```json
{"commit": "...", "primary_metric": 0.0, "memory_gb": 0.0, "gpu_util_pct": 0.0, "throughput": 0.0, "disk_gb": 0.0, "status": "...", "description": "..."}
```

---

## Reproducibility Manifest

Capture the full environment specification so any experiment can be reproduced exactly.

### Environment Capture

Generate a manifest file at project initialization, before the first experiment:

```python
import platform, subprocess, sys, json, torch
from datetime import datetime

def generate_manifest():
    manifest = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "python_version": sys.version,
        "os": f"{platform.system()} {platform.release()}",
        "architecture": platform.machine(),
        "cuda_version": torch.version.cuda if torch.cuda.is_available() else None,
        "cudnn_version": str(torch.backends.cudnn.version()) if torch.backends.cudnn.is_available() else None,
        "gpu_model": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "gpu_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "gpu_memory_gb": round(torch.cuda.get_device_properties(0).total_mem / 1e9, 1) if torch.cuda.is_available() else 0,
        "torch_version": torch.__version__,
        "packages": subprocess.check_output([sys.executable, "-m", "pip", "freeze"]).decode().strip().split("\n"),
        "random_seed": 42,
    }
    with open("output/[slug]/environment-manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    return manifest
```

### What the Manifest Enables

- **Exact reproduction**: Another researcher can recreate the environment from the manifest
- **Debugging**: When results differ across machines, the manifest reveals hardware/software differences
- **Auditing**: Required for regulatory compliance in some domains
- **Cost estimation**: GPU model + experiment count → approximate compute cost

---

## Data Lineage & Provenance

Track where data came from and what happened to it at every step.

### Data Manifest

Create a `output/[slug]/data-manifest.md` at the end of Stage 1 (Data Acquisition):

```markdown
## Data Manifest — [Project Name]

### Sources

| Source | Location | Pulled On | Row Count | Checksum (SHA256) | Notes |
|--------|----------|-----------|-----------|-------------------|-------|
| Customer table | postgres://prod/customers | 2026-03-15 | 245,891 | a3f2b1... | Snapshot as of 2026-03-01 |
| Claims history | s3://data-lake/claims/ | 2026-03-15 | 1,204,556 | 7e9c4d... | 2020-01 through 2026-02 |
| External enrichment | vendor_api/credit_scores | 2026-03-16 | 230,102 | b8d1e2... | 15,789 customers had no match |

### Assumptions About Data

- Customer table reflects state as of 2026-03-01 (snapshot, not live)
- Claims older than 2020 were excluded due to schema changes
- Credit scores are refreshed quarterly; may be up to 3 months stale

### Transform Lineage

Source → [wrangling] → raw_combined.parquet → [cleaning] → clean.parquet → [features] → features.parquet → train/val split
```

### Data Versioning

For static datasets (most autoresearch use cases), a checksum in the manifest is sufficient. For evolving data:

| Approach | Complexity | When to Use |
|---|---|---|
| **SHA256 hash of data files** | Low | Static datasets; detect accidental changes |
| **DVC (Data Version Control)** | Medium | Large datasets that evolve over time; git-like versioning |
| **Delta Lake / lakeFS** | High | Production data pipelines with schema evolution |

**Minimum requirement:** Record the SHA256 hash of each input data file in the data manifest. If the hash changes between runs, the data changed and all prior experiments may not be comparable.

---

## Decision Log

Capture *why* decisions were made, not just *what* was decided. Every phase produces decisions that shape downstream work.

### Structure

Maintain a running decision log in `output/[slug]/decision-log.md`:

```markdown
## Decision Log — [Project Name]

### DEC-001: Primary metric choice
- **Phase:** Evaluation Design
- **Decision:** Use log loss as primary metric
- **Alternatives considered:** AUC-ROC, F1 (macro), accuracy
- **Rationale:** Log loss penalizes confident wrong predictions, which matters for risk-scoring use case. AUC doesn't account for calibration. Accuracy is misleading with 14:1 class imbalance.
- **Reversibility:** Low — changing the metric invalidates all prior experiment comparisons

### DEC-002: Outlier treatment for income
- **Phase:** Data Readiness
- **Decision:** Clip income at 1st and 99th percentiles
- **Alternatives considered:** Winsorize, log-transform, leave as-is
- **Rationale:** Income has extreme outliers (max $12M) that distort median-based imputation in other features. Clipping preserves information within the relevant range.
- **Reversibility:** Medium — requires re-running src/[slug]/prepare.py and re-establishing baseline

### DEC-003: Model type selection
- **Phase:** Model Selection
- **Decision:** Start with LightGBM, not deep learning
- **Alternatives considered:** MLP, FT-Transformer, Transformer encoder
- **Rationale:** Tabular data with 50K rows and strong hand-engineered features. Literature and EDA suggest tree-based models are the ceiling here.
- **Reversibility:** High — can switch model type in src/[slug]/train.py without changing src/[slug]/prepare.py
```

---

## Assumptions Register

Assumptions are invisible risks. Documenting them makes them visible and testable.

### Structure

Maintain in `output/[slug]/assumptions-register.md`:

```markdown
## Assumptions Register — [Project Name]

| ID | Assumption | Phase | Risk if Wrong | Validation Method | Status |
|----|-----------|-------|---------------|-------------------|--------|
| A-001 | Data is representative of production population | Data Acquisition | Model fails in production | Compare data profile to production logs | ⚠ Unvalidated |
| A-002 | Target labels are accurate | Data Readiness | Model learns wrong patterns | Spot-check 100 random labels with domain expert | ✅ Validated |
| A-003 | Feature-target relationships are stationary | Data Readiness | Model degrades over time | Monitor metric on rolling time windows | ⚠ Unvalidated |
| A-004 | 5-minute time budget is sufficient for meaningful training | Problem Framing | Agent cannot explore complex models | Run baseline and verify non-trivial learning | ✅ Validated |
| A-005 | Class weighting compensates for 14:1 imbalance | Evaluation Design | Metric is dominated by majority class | Compare weighted vs. unweighted baseline | 🔄 In Progress |
```

### When to Update

- Add assumptions during every phase (0–5)
- Validate assumptions when evidence becomes available
- Review the register before starting the autonomous loop — unvalidated high-risk assumptions should be addressed first

---

## Experiment Journal

Beyond the structured `results.jsonl`, a narrative journal captures qualitative observations, pattern recognition, and strategic reasoning that structured data cannot.

### Structure

The experiment journal is an append-only markdown file `output/[slug]/experiment-journal.md`, updated at natural breakpoints (not every experiment — that's what `results.jsonl` is for).

```markdown
## Experiment Journal — [Project Name]

### Entry 1 — Baseline established (experiments 1–1)
- Baseline log loss: 0.342, peak VRAM: 2.1 GB
- LightGBM with default params, 50 features
- Observation: feature importance shows premium_to_income_ratio dominates — good sign from domain engineering

### Entry 2 — Early exploration (experiments 2–15)
- 8/14 experiments improved metric (57% keep rate)
- Learning rate and num_leaves are the most impactful knobs so far
- Depth > 8 consistently worse — overfitting signal
- Best so far: 0.298 (exp 11, lr=0.05, num_leaves=63)

### Entry 3 — Plateau detected (experiments 16–35)
- Keep rate dropped to 15% in last 20 experiments
- Incremental hyperparameter changes yielding < 0.001 improvement
- Hypothesis: the feature set is the ceiling, not the model
- **Strategy shift:** moving to feature interaction experiments in src/[slug]/train.py

### Entry 4 — Feature engineering breakthrough (experiments 36–42)
- Adding learned feature crosses between premium and tenure broke through the plateau
- New best: 0.271 (exp 39)
- Observation: the gap between train and val loss widened — adding regularization next
```

### When to Write Journal Entries

| Trigger | What to Record |
|---|---|
| Baseline established | Initial performance, feature importance, first observations |
| After every 15–20 experiments | Keep rate, best metric, most impactful changes, patterns |
| Plateau detected | What stalled, hypotheses for why, strategy shift plan |
| Breakthrough | What caused it, how to build on it |
| Circuit breaker triggered | What went wrong, how it was resolved |
| End of run | Summary of gains, key learnings, recommendations for next run |

---

## Cost Tracking

Compute costs matter, especially for long runs on cloud GPUs. Track cost to know when diminishing returns make continuing uneconomical.

### Cost Estimation

```python
# Cost estimation per experiment
GPU_COST_PER_HOUR = 2.50  # $/hr — adjust for your GPU (e.g., H100 ~$3.50, A100 ~$2.00, RTX 4090 ~$0.50)

def estimate_cost(results_df, time_col="total_seconds"):
    total_seconds = results_df[time_col].sum()
    total_hours = total_seconds / 3600
    total_cost = total_hours * GPU_COST_PER_HOUR
    cost_per_experiment = total_cost / len(results_df) if len(results_df) > 0 else 0
    return {
        "total_hours": round(total_hours, 2),
        "total_cost_usd": round(total_cost, 2),
        "cost_per_experiment_usd": round(cost_per_experiment, 4),
        "experiments": len(results_df),
    }
```

### Cost-Adjusted Metrics

| Metric | Formula | What It Tells You |
|---|---|---|
| **Cost per improvement** | Total cost / number of metric improvements | Is the money being well spent? |
| **Marginal cost** | Cost of last N experiments / metric gain in last N experiments | Are you in diminishing returns territory? |
| **Cost to target** | (target - current) / recent improvement rate × cost per experiment | Estimated remaining spend to hit target |

### Budget Guardrails

Add to constants in `src/[slug]/prepare.py` or the program file:

```python
MAX_BUDGET_USD = 50.00  # Maximum total spend before halting
GPU_COST_PER_HOUR = 2.50
```

The agent checks cumulative cost after each experiment and halts if the budget is exceeded.

---

## Fairness & Ethical Considerations

For models that make decisions affecting people, fairness is not optional.

### When Fairness Applies

If the model's predictions influence outcomes for individuals (credit decisions, hiring, insurance pricing, medical diagnosis, content moderation, law enforcement), fairness analysis is mandatory. If the model is purely technical (compression, forecasting, anomaly detection on machines), it can be deprioritized.

### Fairness Checklist (Phase 0 Addition)

- [ ] **Identify protected attributes** in the data (race, gender, age, disability, religion, national origin)
- [ ] **Check proxy features** — features highly correlated with protected attributes (zip code → race, name → gender)
- [ ] **Measure baseline fairness** — compute fairness metrics before the autonomous loop begins
- [ ] **Add fairness as a secondary metric** — track but don't necessarily optimize (it should not degrade)

### Fairness Metrics

| Metric | Definition | When to Use |
|---|---|---|
| **Demographic parity** | P(ŷ=1 \| group=A) ≈ P(ŷ=1 \| group=B) | When equal treatment is the goal |
| **Equalized odds** | TPR and FPR equal across groups | When prediction accuracy should be equal across groups |
| **Calibration** | P(y=1 \| ŷ=p, group=A) ≈ p for all groups | When predicted probabilities must be trustworthy per group |
| **Disparate impact ratio** | Selection rate of disadvantaged group / selection rate of advantaged group ≥ 0.8 | Regulatory compliance (ECOA, EU AI Act) |

### Implementation

Add fairness metrics to the evaluation function as secondary metrics:

```python
def evaluate_fairness(y_true, y_pred, protected_attr):
    """Compute fairness metrics across protected groups. Track as secondary metrics."""
    groups = protected_attr.unique()
    metrics = {}
    for group in groups:
        mask = protected_attr == group
        metrics[f"positive_rate_{group}"] = y_pred[mask].mean()
        metrics[f"tpr_{group}"] = y_true[mask & (y_pred == 1)].sum() / y_true[mask].sum()
    # Disparate impact ratio
    rates = [metrics[f"positive_rate_{g}"] for g in groups]
    metrics["disparate_impact_ratio"] = min(rates) / max(rates) if max(rates) > 0 else 0
    return metrics
```

---

## Output Artifacts Summary

See `references/file-system-layout.md` for the full directory structure. All monitoring and documentation artifacts land in `output/[slug]/`.
