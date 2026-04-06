# Data Pipeline Design Guide

## Prepare Script Structure

The prepare script is the fixed, read-only infrastructure. It handles everything the agent should NOT touch. When Phase 0 (Data Readiness) has been completed, the cleansing decisions and domain features from that phase are implemented here as fixed transforms.

```
prepare.py (or prepare script)
├── Constants (time budget, sequence length, eval tokens, etc.)
├── Data acquisition (download, extract, validate)
├── Preprocessing (clean per Phase 0 decisions, encode, split)
├── Domain features (business-logic features from Phase 0, locked)
├── Dataloader (efficient batching and iteration)
└── Evaluation function (compute primary metric)
```

## Constants

Define all fixed experiment parameters as constants at the top:

```python
# ============================================================
# FIXED CONSTANTS — Do not modify across experiments
# ============================================================
TIME_BUDGET_SECONDS = 300      # 5-minute fixed training budget
MAX_SEQ_LEN = 1024             # Maximum sequence length
EVAL_TOKENS = 10_000_000       # Tokens used for validation evaluation
VOCAB_SIZE = 8192              # Tokenizer vocabulary size
SEED = 42                      # Random seed for reproducibility
DATA_DIR = "~/.cache/autoresearch/"  # Data storage location
```

### Time Budget Selection

| Compute | Suggested Budget | Expected Experiments/Hour |
|---|---|---|
| Consumer GPU (RTX 3060–4090) | 3–5 minutes | 12–20 |
| Workstation GPU (A6000, RTX 6000) | 5 minutes | 12 |
| Cloud GPU (H100, A100) | 5 minutes | 12 |
| CPU only | 2–3 minutes | 20–30 (models will be tiny) |

Shorter budgets = more experiments but less training signal per experiment. 5 minutes is the sweet spot for GPUs.

## Data Acquisition

```python
def download_data():
    """
    Download and cache the training dataset.
    
    Requirements:
    - Idempotent: safe to run multiple times
    - Cached: check if data exists before downloading
    - Validated: verify checksums or file sizes after download
    - Logged: print progress for long downloads
    """
```

### Data Sources by Problem Type

| Problem Type | Common Sources | Format |
|---|---|---|
| Language modeling | FineWeb, OpenWebText, TinyStories | Text shards |
| Text classification | Domain-specific labeled datasets | CSV/JSON with labels |
| Image classification | ImageNet subset, CIFAR, domain-specific | Image files + labels |
| Time series | Domain-specific sensors, financial data | CSV/Parquet |
| Tabular | UCI ML repo, Kaggle, domain-specific | CSV/Parquet |

## Preprocessing

### Data Cleansing (from Phase 0)

Implement the cleansing decisions documented in the Data Readiness Report as deterministic transforms. Each transform should be a clear function with a docstring explaining the decision and rationale:

```python
def clean_data(df):
    """
    Apply fixed cleansing transforms from Phase 0 Data Readiness.
    
    Each transform corresponds to a documented decision:
    - Null imputation strategy per feature
    - Outlier clip bounds
    - Categorical standardization
    - Duplicate removal
    """
    # Example: clip income at business limits (Phase 0 decision: outlier treatment)
    df["income"] = df["income"].clip(0, 500_000)
    
    # Example: impute nulls (Phase 0 decision: null handling)
    df["feature_a"] = df["feature_a"].fillna(df["feature_a"].median())
    
    return df
```

### Domain Feature Engineering (from Phase 0)

Implement domain features documented in the Data Readiness Report. These require business knowledge and are NOT experimentable by the autonomous agent:

```python
def create_domain_features(df):
    """
    Create business-logic features locked during Phase 0.
    These are fixed across all experiments.
    """
    df["premium_to_income_ratio"] = df["annual_premium"] / df["income"].clip(1)
    df["is_new_policy"] = (df["policy_age_months"] < 24).astype(int)
    return df
```

### Tokenization (for text problems)

```python
def train_tokenizer(text_data, vocab_size):
    """
    Train a BPE tokenizer on the training data.
    
    - Save tokenizer model for reuse
    - Fixed vocab_size defined in constants
    - One-time operation, cached
    """
```

### Data Splitting

- **Training set**: 90–95% of data, split into shards for efficient loading
- **Validation set**: 5–10% of data, never seen during training, used by evaluation function
- **Test set** (optional): Final holdout, only used for reporting — never during the experiment loop

### Sharding

For large datasets, split training data into fixed-size shards:
- Each shard is a self-contained file (numpy array, binary, etc.)
- Shards enable efficient random access and shuffling at the shard level
- Shard size: 50–200MB is practical

## Dataloader

```python
class DataLoader:
    """
    Efficient batched data iteration.
    
    Requirements:
    - Deterministic ordering when seeded
    - Handles sequence packing/padding
    - Returns (input, target) pairs ready for the model
    - Minimal overhead — data loading should not be the bottleneck
    """
```

Key decisions:
- **Sequence packing vs. padding**: Packing is more compute-efficient but harder to implement
- **Batch construction**: Contiguous chunks of the dataset, or random sampling?
- **Device transfer**: Pre-load to GPU or transfer per batch?

## Evaluation Function

The evaluation function is the most critical component of the prepare script.

```python
def evaluate(model, device):
    """
    Compute primary metric on the validation set.
    
    This function:
    1. Sets model to eval mode
    2. Disables gradient computation
    3. Iterates over the FULL validation set (no sampling)
    4. Computes and returns the primary metric + secondary metrics
    5. Restores model to train mode before returning
    
    MUST be deterministic — same model → same metric every time.
    """
```

See `references/evaluation-design.md` for metric selection guidance.

## Guard Rails

Include in the prepare script:

- **NaN detection**: If training loss becomes NaN, fail fast with a clear error message
- **OOM protection**: Catch CUDA OOM errors and report peak memory usage before crashing
- **Time enforcement**: Kill training if it exceeds 2× the time budget
- **Checkpoint**: Save model state at the end of training for evaluation

## File System Layout

```
project/
├── prepare.py          # Fixed infrastructure (read-only to agent)
├── train.py            # Agent-modifiable training script
├── program.md          # Agent instructions
├── results.tsv         # Experiment log (append-only, untracked by git)
├── run.log             # Most recent training output (overwritten each run)
├── pyproject.toml      # Dependencies (fixed)
└── data/               # Cached data, tokenizer, shards (gitignored)
    ├── train_*.bin     # Training data shards
    ├── val_*.bin       # Validation data
    └── tokenizer.model # Trained tokenizer
```
