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

## Program File Structure

### 1. Project Context

Brief description of what the system does, what problem it solves, and what the agent's role is.

```markdown
# [Project Name]

This is an autonomous research system for [problem description]. Your role is to
iteratively improve [what] by modifying [train script name]. You optimize for
[primary metric] (lower/higher is better).
```

### 2. Setup Protocol

Step-by-step instructions for initializing a new experiment run:

1. **Agree on a run tag** — Propose a tag based on the current date (e.g., `apr5`)
2. **Create the branch** — `git checkout -b autoresearch/<tag>` from main
3. **Read in-scope files** — List exactly which files the agent should read for context
4. **Verify data exists** — Check that cached data is present; if not, tell the human to run prepare
5. **Initialize results log** — Create `results.tsv` with the header row
6. **Establish baseline** — Run the training script unmodified and record the baseline metric
7. **Confirm and go** — Report setup status and begin the loop

### 3. Scope Definition

Explicit boundaries on what the agent can and cannot do:

```markdown
**What you CAN do:**
- Modify [train script] — everything is fair game: [list specific knobs]

**What you CANNOT do:**
- Modify [prepare script] — it contains the fixed evaluation and data infrastructure
- Install new packages or add dependencies
- Modify the evaluation function
- Change the validation data
```

Be exhaustive about the CANNOT list. Ambiguity leads to the agent breaking infrastructure.

### 4. Experiment Loop Protocol

The core loop the agent follows indefinitely:

```markdown
LOOP FOREVER:

1. Check current git state (branch, commit)
2. Modify [train script] with an experimental idea
3. git commit with descriptive message
4. Run training: `[run command] > run.log 2>&1`
5. Extract results: `grep "^primary_metric:\|^peak_vram_mb:" run.log`
6. If grep output is empty → crash. Read `tail -n 50 run.log` for stack trace
7. Record results in results.tsv
8. If metric improved → keep changes (advance the branch)
9. If metric equal or worse → `git reset --hard` to previous commit
10. Continue to next experiment
```

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

Tab-separated file (`results.tsv`) with columns:

commit    primary_metric    memory_gb    status    description

- commit: short git hash (7 chars)
- primary_metric: the metric value (e.g., 0.997900), use 0.000000 for crashes
- memory_gb: peak VRAM in GB rounded to 0.1 (use 0.0 for crashes)
- status: keep | discard | crash
- description: short text of what the experiment tried
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

### 8. Autonomy Directive

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
