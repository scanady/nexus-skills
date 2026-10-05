# File System Layout

All deliverables are organized into three top-level directories by purpose. `[slug]` is the project/experiment name (e.g., `insurance-lapse-predictor`). Documentation artifacts from the preparation phases are persisted in `output/[slug]/` so they remain available as a reference throughout the autonomous loop and for future audits.

```
src/[slug]/
├── prepare.py                          # Phase 3 output — fixed data pipeline (read-only to agent)
├── train.py                            # Phase 4 output — baseline training script (agent-modifiable)
├── program.md                          # Phase 5 output — agent instructions
├── visualize_results.py                # Script to generate monitoring charts from results.jsonl
└── pyproject.toml                      # Dependencies (fixed)

data/[slug]/                            # Cached data, tokenizer, shards (gitignored)
├── train_*.bin                         # Training data shards
├── val_*.bin                           # Validation data
└── tokenizer.model                     # Trained tokenizer

output/[slug]/
├── results.jsonl                       # Experiment log (created at baseline, append-only)
├── run.log                             # Most recent training output (overwritten each run)
├── problem-brief.md                    # Phase 1 output — problem framing, objectives, constraints
├── data-readiness-report.md            # Phase 0 output — EDA findings, cleansing decisions, quality gates
├── evaluation-spec.md                  # Phase 2 output — metric definition, harness design, validation strategy
├── model-selection-rationale.md        # Phase 4 output — model type decision, architecture choice, baseline justification
├── assumptions-register.md             # Created in Phases 0–1, updated throughout — documented assumptions with risk and validation status
├── decision-log.md                     # Append-only — rationale for every major design decision across all phases
├── data-manifest.md                    # Phase 0 output — data sources, checksums, provenance, transform lineage
├── environment-manifest.json           # Generated at project init — full environment specification for reproducibility
├── experiment-journal.md               # Append-only during autonomous loop — qualitative observations and strategy shifts
├── eda/                                # EDA visualization artifacts
│   ├── eda_overview.png
│   ├── feature_interactions.png
│   ├── temporal_analysis.png
│   └── ...
├── monitoring/                         # Runtime monitoring visualizations
│   ├── metric_progression.png
│   └── resource_utilization.png
└── checkpoints/
    ├── best_model.pt                   # Best-performing model weights (kept indefinitely)
    ├── current_model.pt                # Most recent model weights (overwritten each run)
    └── snapshot_exp*.pt                # Periodic snapshots (last 3 kept)
```

## Directory Rationale

- **`src/[slug]/`** — Code you write. Fixed for the duration of the run (except `train.py`, which the agent edits). Version-controlled.
- **`data/[slug]/`** — Input data produced by preparation. Gitignored (too large). Reproducible by re-running `src/[slug]/prepare.py`.
- **`output/[slug]/`** — Everything the process produces: experiment log, training output, documentation artifacts, visualizations, checkpoints. Gitignored for binary/large files (`results.jsonl` and `.md` files may be committed).

## Why Persist Preparation Artifacts

- **Traceability**: Every cleaning decision, feature engineering choice, and metric design can be traced back to documented reasoning
- **Reproducibility**: A new team member (or a future you) can understand why `src/[slug]/prepare.py` does what it does
- **Auditability**: For regulated domains (finance, healthcare), documentation of data handling decisions is often required
- **Iteration**: If the autonomous loop plateaus, reviewing the data readiness report and EDA may reveal new feature engineering opportunities or data quality issues to address
