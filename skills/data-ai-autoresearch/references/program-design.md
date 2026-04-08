# Agent Program Design Guide

## Purpose of the Program File

The program file (`program.md`) is the agent's operating manual. It tells the autonomous agent:
- What it is doing and why
- What it can and cannot modify
- How to run experiments
- How to evaluate results
- How to log outcomes
- When to keep or discard changes
- That it should never stop

The program file is written by the human (with this skill's help) and remains fixed during the autonomous run. The agent reads it at the start and follows it as its loop protocol.

For reliable behavior, the program file should not stand alone. Pair it with a blessed experiment runner and workspace-level customization so the process is enforced by the repo, not just described in markdown.

## Program File Structure

### 1. Project Context

Brief description of what the system does, what problem it solves, and what the agent's role is.

```markdown
# [Project Name]

This is an autonomous research system for [problem description]. Your role is to
iteratively improve [what] by modifying src/[slug]/train.py. You optimize for
[primary metric] (lower/higher is better).
```

### 2. Setup Protocol

Step-by-step instructions for initializing a new experiment run:

1. **Agree on a run tag** — Propose a tag based on the current date (e.g., `apr5`)
2. **Create the branch** — `git checkout -b autoresearch/<tag>` from main
3. **Read in-scope files** — List exactly which files the agent should read for context (including `output/[slug]/` preparation artifacts)
4. **Verify enforcement artifacts exist** — Confirm the blessed runner, workspace instructions, and any file-specific instructions are present
5. **Verify data exists** — Check that cached data is present in `data/[slug]/`; if not, tell the human to run prepare
6. **Initialize results log** — Create `output/[slug]/results.jsonl` (empty file)
7. **Establish baseline** — Run the blessed experiment command unmodified and record the baseline metric
8. **Confirm and go** — Report setup status and begin the loop

### 3. Scope Definition

Explicit boundaries on what the agent can and cannot do:

```markdown
**What you CAN do:**
- Modify src/[slug]/train.py — everything is fair game: [list specific knobs]
- Append entries to output/[slug]/experiment-journal.md
- Save model checkpoints to output/[slug]/checkpoints/

**What you CANNOT do:**
- Modify src/[slug]/prepare.py — it contains the fixed evaluation and data infrastructure
- Modify any files in output/[slug]/ other than experiment-journal.md
- Install new packages or add dependencies
- Modify the evaluation function
- Change the validation data in data/[slug]/
```

Be exhaustive about the CANNOT list. Ambiguity leads to the agent breaking infrastructure.

### 4. Experiment Loop Protocol

The core loop the agent follows indefinitely:

```markdown
LOOP FOREVER:

1. Check current git state (branch, commit)
2. Modify src/[slug]/train.py with an experimental idea
3. git commit with descriptive message
4. Run the blessed experiment command: `python -m [slug].run_experiment --description "<idea>"`
5. Extract results from `output/[slug]/results.jsonl` and, when needed, inspect `output/[slug]/run.log`
6. If grep output is empty → crash. Read `tail -n 50 output/[slug]/run.log` for stack trace
7. Record results in output/[slug]/results.jsonl
8. If metric improved → keep changes (advance the branch)
9. If metric equal or worse → `git reset --hard` to previous commit
10. Continue to next experiment
```

### 4.5. Execution Wrapper And Enforcement

Prefer a dedicated runner over calling `train.py` directly.

**Runner responsibilities:**
- Execute exactly one experiment
- Write `run.log`
- Append one result row on success or crash
- Record provenance fields such as runner name, git commit, branch, timestamp, and train-script hash when practical
- Refresh visualizations or other monitoring outputs after the run

**Repo-level enforcement artifacts:**
- Workspace instructions (`copilot-instructions.md` or `AGENTS.md`) that say only the blessed runner may execute experiments
- File-specific instructions for `train.py` that forbid side probes and require one coherent change per run
- Optional hooks that block known bad patterns such as direct `train.py` execution or inline Python probing during autoresearch

**Direct-run policy:**
- If `train.py` remains executable, require an explicit `--allow-direct-run` style override for manual debugging
- The autonomous loop should never use that override

### 5. Decision Criteria

How the agent decides what to keep vs. discard:

**Keep when:**
- Primary metric improved (even by a small amount) without dramatic resource usage increase
- Primary metric unchanged but code is simpler (simplification win)

**Discard when:**
- Primary metric is worse or unchanged with added complexity
- Resource usage exploded without meaningful metric gain

**Simplicity criterion:** All else being equal, simpler is better. A 0.001 improvement that adds 20 lines of complexity is probably not worth it. A 0.001 improvement from *removing* code is definitely worth it.

### 6. Results Logging Schema

Define the exact format for experiment tracking:

```markdown
## Results Format

JSON Lines file (`results.jsonl`) — one JSON object per experiment, one per line.
Uses Python's built-in `json` module (no additional dependencies).

Required fields:
{
  "experiment": 1,
  "commit": "a3f2b1c",
  "primary_metric": 0.997900,
  "memory_gb": 4.2,
  "gpu_util_pct": 87,
  "throughput": 12500,
  "training_seconds": 300.1,
  "status": "keep",
  "description": "Increased depth from 4 to 6 layers"
}

Field definitions:
- experiment: sequential experiment number (1-indexed)
- commit: short git hash (7 chars)
- primary_metric: the metric value (e.g., 0.997900), use 0.0 for crashes
- memory_gb: peak VRAM in GB rounded to 0.1 (use 0.0 for crashes)
- gpu_util_pct: average GPU utilization % during training (0 for crashes)
- throughput: samples/sec or tokens/sec (0 for crashes)
- training_seconds: wall-clock training time
- status: "keep" | "discard" | "crash"
- description: short text of what the experiment tried

Logging:
import json

def log_result(result: dict, path="output/[slug]/results.jsonl"):
    with open(path, "a") as f:
        f.write(json.dumps(result) + "\n")

Reading:
import json

def load_results(path="output/[slug]/results.jsonl"):
    results = []
    with open(path) as f:
        for line in f:
            results.append(json.loads(line))
    return results
```

### 7. Crash Handling

```markdown
**Crashes:**
- If it's a trivial fix (typo, missing import, off-by-one): fix and re-run
- If the idea is fundamentally broken (OOM, numerical instability): log as crash, revert, move on
- If multiple consecutive crashes: step back, re-read the codebase, try a different approach

**Timeout:**
- If a run exceeds [2× time budget], kill it and treat as a crash
```

### 8. Circuit Breakers

Automated safeguards that detect pathological states and force course correction or halting.

```markdown
**AFTER EACH EXPERIMENT, run circuit breaker checks:**

1. **Consecutive crashes** (threshold: 5): STOP the loop. Report the last 5 crash
   messages and wait for human intervention.
2. **Consecutive discards** (threshold: 20): WARNING. Re-read all in-scope files
   including output/[slug]/data-readiness-report.md and output/[slug]/eda/. Shift to a fundamentally
   different approach (architecture swap, not hyperparameter tweak).
3. **Metric plateau** (threshold: 30 experiments with no improvement): WARNING.
   Escalate to next strategy stage:
   - Normal → Widened search (different optimizer, LR schedule, regularization)
   - Widened → Architecture pivot (switch model family entirely)
   - Pivot → Simplification pass (remove components, test if metric holds)
   - Simplification → Back to basics (re-read all docs, is data quality the ceiling?)
4. **Disk usage > 90%**: STOP. Report disk usage breakdown and wait for human.
5. **VRAM > 95% of GPU memory for 3 consecutive runs**: WARNING. Scale down model
   before next experiment to avoid OOM.
6. **Cost budget exceeded**: STOP. Report total spend and best metric achieved.
```

### 9. Checkpoint Management

```markdown
**Checkpoints:**
- Save best model weights to output/[slug]/checkpoints/best_model.pt whenever metric improves
- Save current model to output/[slug]/checkpoints/current_model.pt after every training run (overwrite)
- Save periodic snapshot every 25 experiments to output/[slug]/checkpoints/snapshot_expNNNN.pt
- Keep only the last 3 periodic snapshots — delete older ones to conserve disk
```

### 10. Experiment Journal

```markdown
**Journal updates** — append to output/[slug]/experiment-journal.md at these breakpoints:
- After baseline is established
- After every 15–20 experiments (note keep rate, best metric, patterns observed)
- When a circuit breaker triggers
- When a breakthrough occurs (significant metric improvement)
- At the end of the run (summary, key learnings, next-run recommendations)

Journal entries should capture qualitative observations, not just numbers.
What patterns are you seeing? What's working and what isn't? What hypotheses
do you have about why?
```

### 11. Autonomy Directive

This is critical — the agent must not pause for human confirmation:

```markdown
**NEVER STOP**: Once the experiment loop has begun, do NOT pause to ask the
human if you should continue. Do NOT ask "should I keep going?" or "is this a
good stopping point?". The human may be away and expects you to continue
indefinitely until manually stopped. You are autonomous.

If you run out of ideas:
- Re-read the in-scope files for new angles
- Try combining previous near-misses
- Try more radical architectural changes
- Try simplifying — remove components and see if the metric holds
- Explore the opposite of what has worked (contrarian experiments)
```

## Tailoring the Program to the Domain

### Language Modeling
- Emphasize architecture exploration (attention patterns, positional encoding, normalization)
- Highlight vocabulary and sequence length interactions
- Note that BPB is the metric, not perplexity (perplexity depends on vocab size)

### Classification
- Emphasize regularization (dropout, augmentation, weight decay)
- Note class balance and metric sensitivity to imbalanced classes
- Suggest data augmentation strategies as experiment ideas

### Regression / Forecasting
- Emphasize feature engineering in the model (learned embeddings, positional features)
- Note sensitivity to outliers in the metric
- Suggest loss function exploration (MSE, MAE, Huber, quantile)

### Generation
- Emphasize sampling quality checks beyond the metric (if applicable as a manual review step)
- Note trade-offs between diversity and quality
- Suggest temperature/top-k/top-p as hyperparameter knobs

## Common Pitfalls

- **Too many constraints**: If the CANNOT list is too long, the agent has no room to explore. Prefer guardrails (metric, time budget) over micromanagement.
- **Vague scope**: "Improve the model" is not enough. Specify the single file, the metric, and the decision protocol.
- **No baseline**: Without a baseline, the agent cannot assess relative improvement.
- **Optimistic time budget**: If training takes 4:58 with the baseline, the agent has no room for larger models. Leave headroom.
- **Forgetting the log format**: Without a structured results log, the agent's experiment history is lost.
- **Side probes**: Inline Python or shell metric checks outside the blessed runner create unlogged decision paths and eventually break trust in the experiment history.
