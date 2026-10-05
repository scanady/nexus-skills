# Data Pipeline Design Guide

The data pipeline is the foundation that determines the ceiling of the autonomous experiment loop. No model architecture or training trick can compensate for poorly acquired, understood, or prepared data. This guide covers the full lifecycle: acquiring and understanding data, preparing it for modeling, exploring it through statistical detective work, and implementing the pipeline as fixed infrastructure.

## Pipeline Overview

```
┌───────────────────────────────────────────────────────────────┐
│  DATA PIPELINE STAGES                                         │
│                                                               │
│  Stage 1: Data Acquisition & Understanding                    │
│  ├── Source identification & collection                       │
│  ├── Synthetic data generation (when needed)                  │
│  ├── Schema review & data dictionary                          │
│  └── Initial quality assessment                               │
│                                                               │
│  Stage 2: Data Preparation                                    │
│  ├── Data wrangling (reshape, merge, pivot)                   │
│  ├── Data cleaning (nulls, outliers, types, duplicates)       │
│  ├── Feature engineering (domain + derived features)          │
│  └── Data integration (multi-source reconciliation)           │
│                                                               │
│  Stage 3: Exploratory Data Analysis                           │
│  ├── Statistical profiling                                    │
│  ├── Visualization (distributions, relationships, time)       │
│  ├── Pattern & anomaly detection                              │
│  └── Hypothesis testing                                       │
│                                                               │
│  Stage 4: Pipeline Implementation (src/[slug]/prepare.py)    │
│  ├── Constants & configuration                                │
│  ├── Acquisition & caching                                    │
│  ├── Preprocessing transforms (locked from Stages 1–3)        │
│  ├── Dataloader                                               │
│  └── Evaluation harness                                       │
└───────────────────────────────────────────────────────────────┘
```

Stages 1–3 are human-guided analysis and decision-making. Stage 4 translates those decisions into deterministic code that the autonomous agent treats as read-only infrastructure.

---

## Stage 1: Data Acquisition & Understanding

Before any modeling begins, you must know what data you have, where it comes from, and whether it's sufficient for the problem.

### Data Sourcing Strategies

| Source Type | Examples | Considerations |
|---|---|---|
| **Internal databases** | Production DB, data warehouse, event logs | Access permissions, PII handling, query performance |
| **Public datasets** | UCI ML Repo, Kaggle, HuggingFace, government open data | Licensing, citation requirements, known quality issues |
| **APIs** | REST/GraphQL endpoints, streaming feeds | Rate limits, pagination, authentication, schema versioning |
| **Web scraping** | Structured sites, public directories | Legal compliance (robots.txt, ToS), HTML structure stability |
| **File-based** | CSV, Parquet, JSON, Excel, XML | Encoding issues, schema inconsistencies across files |
| **Sensor/IoT** | Time-series streams, device telemetry | Sampling rates, missing readings, clock drift |
| **Third-party vendors** | Data brokers, enrichment services | Cost, SLA, data freshness, integration format |

### Data Acquisition Checklist

- [ ] Identify all data sources needed for the problem
- [ ] Document access method, credentials, and refresh frequency for each source
- [ ] Verify licensing and legal compliance (especially for PII, GDPR, CCPA)
- [ ] Establish data freshness requirements (real-time, daily, static snapshot)
- [ ] Build idempotent acquisition scripts (safe to re-run, cached, checksummed)
- [ ] Validate row counts and schema against expectations after each pull
- [ ] Document known limitations (sampling bias, missing segments, temporal gaps)

### Synthetic Data Generation

When real data is insufficient — too small, too imbalanced, missing edge cases, or restricted by privacy — synthetic data can fill the gap. Synthetic data is also valuable for stress-testing model robustness.

#### When to Generate Synthetic Data

| Scenario | Technique | Notes |
|---|---|---|
| **Class imbalance** (minority class < 5%) | SMOTE, ADASYN, borderline-SMOTE | Oversample minority class in feature space; apply before train/val split |
| **Insufficient training volume** | Augmentation (domain-specific transforms) | Images: rotation, crop, color jitter. Text: back-translation, synonym replacement. Tabular: noise injection |
| **Privacy restrictions** (can't use real data) | Differential privacy synthetic generation, SDV (Synthetic Data Vault), CTGAN | Generates statistically similar data without exposing individual records |
| **Missing edge cases** | Rule-based generation, simulation | Manufacture rare scenarios the model must handle (e.g., extreme weather, fraud patterns) |
| **Domain simulation** | Physics-based simulation, agent-based modeling | Generate labeled data from a known process (e.g., fluid dynamics, traffic simulation) |
| **Data augmentation for robustness** | Adversarial examples, noise injection, mixup/cutmix | Test model stability under perturbation |

#### Synthetic Data Quality Gates

Synthetic data must be validated before mixing with real data:

- **Statistical fidelity**: Compare distributions of synthetic vs. real data (KS test, visual overlay)
- **Privacy preservation**: Verify no real records appear in synthetic output (nearest-neighbor distance check)
- **Downstream utility**: Train on synthetic, evaluate on real holdout — metric should be within 10–20% of real-only training
- **Labeling accuracy**: For rule-based generation, verify labels match the generation logic
- **No leakage**: Synthetic data must not be generated using information from the validation/test set

```python
# Example: SMOTE for tabular class imbalance
from imblearn.over_sampling import SMOTE

smote = SMOTE(sampling_strategy='minority', random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
# Validate: compare feature distributions before and after
```

```python
# Example: CTGAN for privacy-preserving synthetic tabular data
from sdv.single_table import CTGANSynthesizer

synthesizer = CTGANSynthesizer(metadata)
synthesizer.fit(real_data)
synthetic_data = synthesizer.sample(num_rows=10000)

# Validate: run diagnostic report
from sdv.evaluation.single_table import evaluate_quality
quality_report = evaluate_quality(real_data, synthetic_data, metadata)
```

### Data Understanding & Profiling

Before any transformation, build a mental model of the data:

- **Schema review**: Column names, types, cardinalities, relationships between tables
- **Data dictionary**: What each field means in business terms (not just column names)
- **Provenance**: How was the data collected? What biases might the collection process introduce?
- **Temporal scope**: What time period does the data cover? Are there regime changes?
- **Completeness assessment**: What's missing? Are there known gaps in collection?
- **Volume assessment**: Is there enough data for the intended model complexity?

| Data Volume | Model Complexity Ceiling | Notes |
|---|---|---|
| < 1K rows | Linear models, shallow trees | Deep learning will overfit |
| 1K–10K rows | Ensemble ML, shallow neural nets | Regularization is critical |
| 10K–100K rows | Moderate neural nets, fine-tuned pretrained models | Sweet spot for many problems |
| 100K–1M rows | Full deep learning architectures | Standard range for most DL |
| 1M+ rows | Large models, complex architectures | Scaling laws apply |

---

## Stage 2: Data Preparation

Data preparation transforms raw data into a clean, structured, feature-rich dataset ready for modeling. Decisions made here become fixed transforms in `src/[slug]/prepare.py`.

### Data Wrangling

Wrangling reshapes and restructures data into the format needed for analysis and modeling.

| Operation | When to Use | Example |
|---|---|---|
| **Pivoting/unpivoting** | Data is in wide format but needs to be long (or vice versa) | Monthly columns → single date + value column |
| **Melting** | Multiple measurement columns need to become rows | `revenue_q1, revenue_q2, ...` → `quarter, revenue` |
| **Aggregation** | Row-per-transaction needs to become row-per-entity | Transaction history → customer-level features |
| **Window functions** | Need rolling/cumulative features along a dimension | Rolling 30-day average purchase amount |
| **Reshaping** | Nested or hierarchical data needs flattening | JSON arrays → tabular rows |
| **Type coercion** | Columns have wrong types (strings as numbers, etc.) | `"123.45"` → `123.45`, `"2024-01-15"` → datetime |

```python
# Example: aggregate transaction-level data to customer-level
customer_features = transactions.groupby("customer_id").agg(
    total_spend=("amount", "sum"),
    avg_transaction=("amount", "mean"),
    transaction_count=("amount", "count"),
    days_since_last=("date", lambda x: (reference_date - x.max()).days),
    unique_categories=("category", "nunique"),
)
```

### Data Cleaning

Systematic treatment of data quality issues. Every decision must be documented — these become fixed transforms in the prepare script. See `data-readiness.md` for detailed decision matrices.

**Null handling strategies:**

| Strategy | When | Implementation |
|---|---|---|
| Drop rows | Nulls are rare (< 0.5%) and random | `df.dropna(subset=[cols])` |
| Impute with statistic | Feature is important, nulls are missing-at-random | `df[col].fillna(df[col].median())` |
| Impute + indicator | Nullness itself is informative | `df["col_was_null"] = df[col].isnull()` then impute |
| Forward/backward fill | Time series with intermittent gaps | `df[col].ffill()` |
| Model-based imputation | Complex missing patterns across multiple features | KNN imputer, iterative imputer |
| Drop column | > 20% null and low importance | Remove from pipeline |

**Outlier treatment:**

```python
def clip_outliers(df, col, lower_pctl=1, upper_pctl=99):
    """Clip values outside percentile bounds. Document bounds in data readiness report."""
    lower = df[col].quantile(lower_pctl / 100)
    upper = df[col].quantile(upper_pctl / 100)
    return df[col].clip(lower, upper)
```

**Duplicate handling:**

- Exact duplicates: drop, keep first
- Near-duplicates (same entity, different timestamps): investigate — may be valid repeated observations or data collection errors
- Cross-source duplicates: entity resolution (fuzzy matching on name, address, etc.)

**Type and format standardization:**

- Categorical casing: lowercase, strip whitespace, merge synonyms
- Date parsing: consistent format, timezone handling
- Numeric precision: consistent decimal places, unit alignment
- Encoding: UTF-8 normalization, special character handling

### Feature Engineering

Feature engineering is split between `src/[slug]/prepare.py` (domain features, fixed) and `src/[slug]/train.py` (learned features, experimentable). See `data-readiness.md` Step 3 for the full split rationale.

#### Domain Feature Patterns (Fixed in src/[slug]/prepare.py)

| Pattern | Example | When to Use |
|---|---|---|
| **Ratio** | `premium / income` | Two features have a meaningful business ratio |
| **Threshold/flag** | `is_high_risk = score > 0.8` | Known business decision boundary |
| **Bucket/bin** | `age_group: 18-30, 31-45, ...` | Non-linear relationship at known thresholds |
| **Time-since** | `days_since_last_claim` | Recency matters more than raw dates |
| **Rolling aggregate** | `avg_spend_last_90d` | Recent trend > all-time aggregate |
| **Interaction** | `missed_payments × premium` | Known combined effect |
| **Relative position** | `income_percentile` | Rank matters more than absolute value |
| **Calendar features** | `day_of_week, is_holiday, quarter` | Temporal patterns |
| **Lag features** | `target_t_minus_1, target_t_minus_7` | Time series with autocorrelation |

#### Derived Feature Patterns (Experimentable in src/[slug]/train.py)

- Learned embeddings for high-cardinality categoricals
- Polynomial and cross-feature interaction layers
- Feature selection via attention or gating mechanisms
- Input normalization variants (batch norm, layer norm, learned scaling)
- Dimensionality reduction (PCA, autoencoders) as preprocessing layers

### Data Integration

When data comes from multiple sources, integration introduces its own challenges.

| Challenge | Solution |
|---|---|
| **Schema mismatch** | Map columns across sources using a canonical schema; document mappings |
| **Entity resolution** | Fuzzy matching (Levenshtein distance, phonetic encoding) + manual review for ambiguous matches |
| **Temporal alignment** | Align timestamps to a common reference; handle different granularities (daily vs. monthly) |
| **Key conflicts** | Surrogate keys when natural keys differ across sources |
| **Update frequency mismatch** | Document freshness per source; flag stale joins |
| **Referential integrity** | Validate foreign key relationships after joining; flag orphaned records |

```python
# Example: integrate customer data from CRM and transaction systems
merged = (
    crm_data
    .merge(transaction_features, on="customer_id", how="left", validate="1:1")
    .merge(support_features, on="customer_id", how="left", validate="1:1")
)

# Validate: check for unexpected nulls from failed joins
assert merged["total_spend"].isnull().mean() < 0.05, "Too many customers missing transaction data"
```

---

## Stage 3: Exploratory Data Analysis

EDA is detective work. The goal is to discover patterns, relationships, and anomalies that inform every downstream decision — metric choice, feature selection, model architecture, and cleaning strategy. EDA is not a checkbox; it's an iterative investigation that builds intuition about the data.

### Statistical Profiling

Start with automated profiling, then dig into what the numbers reveal.

```python
# Automated profiling
import pandas as pd

profile = {
    "shape": df.shape,
    "dtypes": df.dtypes.value_counts().to_dict(),
    "null_rates": (df.isnull().sum() / len(df)).sort_values(ascending=False),
    "numeric_stats": df.describe(),
    "categorical_stats": df.describe(include=["object", "category"]),
    "cardinalities": df.nunique().sort_values(),
    "duplicates": df.duplicated().sum(),
    "memory_mb": df.memory_usage(deep=True).sum() / 1e6,
}
```

**Key statistics to compute:**

- **Central tendency**: mean, median, mode — divergence between mean and median flags skew
- **Dispersion**: std, IQR, range, coefficient of variation (CV) — high CV flags noisy features
- **Shape**: skewness (|skew| > 2 → consider log transform), kurtosis (high kurtosis → heavy tails)
- **Correlation**: Pearson (linear), Spearman (monotonic), Kendall (ordinal) — use the right one for the data type
- **Mutual information**: Non-linear dependency measure — catches relationships correlation misses

### Visualization

Generate visualizations to build intuition. Every visualization should answer a specific question.

#### Distribution Visualizations

| Visualization | Question It Answers | When to Use |
|---|---|---|
| **Histogram / KDE** | What does this feature's distribution look like? | Every numeric feature; flag multimodal, skewed, or heavy-tailed |
| **Box plot** | Where are the outliers? | Compare distributions across groups (e.g., target classes) |
| **Violin plot** | What's the full distribution shape per group? | When box plots hide multimodality |
| **Bar chart (value counts)** | What's the category frequency? | Every categorical feature; flag rare categories |
| **Target distribution** | Is the target balanced? Skewed? | Always — informs metric choice and sampling strategy |

#### Relationship Visualizations

| Visualization | Question It Answers | When to Use |
|---|---|---|
| **Scatter plot** | Is there a linear/non-linear relationship? | Pairs of numeric features with target coloring |
| **Correlation heatmap** | Which features are related to each other and the target? | Full feature matrix; flag |r| > 0.85 pairs |
| **Pair plot** | What are the joint distributions of top features? | Top 5–8 features by target correlation |
| **Grouped bar / stacked bar** | How do categories relate to the target? | Categorical features vs. target |
| **Partial dependence plot** | What's the marginal effect of a single feature? | After fitting a quick baseline model |

#### Temporal Visualizations (if applicable)

| Visualization | Question It Answers | When to Use |
|---|---|---|
| **Time series line plot** | Are there trends, seasonality, or regime changes? | Any feature with a time dimension |
| **Rolling statistics** | Is the mean/variance stationary? | Time series modeling — stationarity matters |
| **Lag plot / ACF / PACF** | What's the autocorrelation structure? | Time series — informs lag features and model choice |
| **Seasonal decomposition** | What are the trend, seasonal, and residual components? | When seasonality is suspected |

#### Anomaly Visualizations

| Visualization | Question It Answers | When to Use |
|---|---|---|
| **Isolation forest plot** | Which points are anomalous in high-dimensional space? | When univariate outlier detection isn't enough |
| **DBSCAN cluster plot (2D projection)** | Are there natural clusters? Noise points? | Dataset structure discovery |
| **Residual plot** | Where does a simple model fail? | After fitting a baseline — residual patterns reveal missing features |

```python
# Example: generate a comprehensive EDA visualization suite
import matplotlib.pyplot as plt
import seaborn as sns

fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# Target distribution
sns.histplot(df[target_col], ax=axes[0, 0], kde=True)
axes[0, 0].set_title(f"Target Distribution: {target_col}")

# Correlation heatmap (top features)
top_features = df.corr()[target_col].abs().nlargest(10).index
sns.heatmap(df[top_features].corr(), annot=True, fmt=".2f", ax=axes[0, 1], cmap="RdBu_r")
axes[0, 1].set_title("Top Feature Correlations")

# Null rate bar chart
null_rates = df.isnull().mean().sort_values(ascending=False).head(15)
null_rates.plot.barh(ax=axes[0, 2])
axes[0, 2].set_title("Null Rates (Top 15)")

# Feature distributions (top 3 by target correlation)
for i, feat in enumerate(top_features[1:4]):
    sns.histplot(data=df, x=feat, hue=target_col, ax=axes[1, i], kde=True)
    axes[1, i].set_title(f"Distribution: {feat}")

plt.tight_layout()
plt.savefig("eda_overview.png", dpi=150, bbox_inches="tight")
```

### Pattern & Correlation Discovery

Go beyond simple correlations to find actionable patterns:

- **Feature-target relationships**: Rank features by mutual information, not just linear correlation — many real-world relationships are non-linear
- **Feature-feature redundancy**: Identify clusters of highly correlated features → candidates for dropping or combining
- **Interaction effects**: For top feature pairs, check if their interaction (product, ratio, difference) has stronger target correlation than either alone
- **Segment-specific patterns**: Does the feature-target relationship change across segments (e.g., age groups, regions)? This reveals non-stationarity

```python
# Mutual information for feature ranking (classification)
from sklearn.feature_selection import mutual_info_classif

mi_scores = mutual_info_classif(X, y, random_state=42)
mi_ranking = pd.Series(mi_scores, index=X.columns).sort_values(ascending=False)

# Compare with linear correlation
corr_ranking = X.corrwith(y).abs().sort_values(ascending=False)

# Features that rank HIGH in MI but LOW in correlation → non-linear relationships worth investigating
divergent = mi_ranking.head(20).index.difference(corr_ranking.head(20).index)
```

### Anomaly Detection

Identify data points that don't fit the expected pattern. Anomalies may be errors (fix them), rare-but-real events (keep them), or signals of data quality issues (investigate).

- **Univariate**: Z-score > 3, IQR fences, domain-specific bounds (e.g., age > 120)
- **Multivariate**: Isolation forest, local outlier factor (LOF), Mahalanobis distance
- **Temporal**: Sudden spikes/drops, distribution shifts over time windows
- **Contextual**: Normal in one context but anomalous in another (e.g., high spending is normal for enterprise customers, anomalous for individuals)

### Hypothesis Testing

Use statistical tests to validate or reject assumptions about the data before they propagate into modeling decisions.

| Hypothesis | Test | When to Use |
|---|---|---|
| Feature X differs between target classes | Mann-Whitney U (non-parametric), t-test (normal) | Feature selection — is this feature discriminative? |
| Feature distribution is normal | Shapiro-Wilk (n < 5000), Anderson-Darling | Choosing between parametric and non-parametric methods |
| Two features are independent | Chi-squared test (categorical), distance correlation (continuous) | Feature redundancy assessment |
| Train and validation have same distribution | Kolmogorov-Smirnov (KS) test, Population Stability Index (PSI) | Data leakage / drift detection |
| Feature has changed over time | CUSUM, Page-Hinkley, KS test on time windows | Concept drift detection |
| Synthetic data matches real data | KS test per feature, maximum mean discrepancy (MMD) | Validating synthetic data quality |
| Class proportions differ from expected | Chi-squared goodness of fit | Validating sampling strategy |

```python
# Example: test whether a feature is discriminative for binary classification
from scipy.stats import mannwhitneyu

for col in numeric_features:
    group_0 = df[df[target] == 0][col].dropna()
    group_1 = df[df[target] == 1][col].dropna()
    stat, p_value = mannwhitneyu(group_0, group_1, alternative="two-sided")
    if p_value < 0.01:
        effect_size = abs(group_0.median() - group_1.median()) / df[col].std()
        print(f"{col}: p={p_value:.4e}, effect_size={effect_size:.3f}")
```

```python
# Example: test train/validation distribution alignment
from scipy.stats import ks_2samp

drift_report = []
for col in numeric_features:
    stat, p_value = ks_2samp(train_df[col].dropna(), val_df[col].dropna())
    drift_report.append({"feature": col, "ks_statistic": stat, "p_value": p_value})

drift_df = pd.DataFrame(drift_report).sort_values("ks_statistic", ascending=False)
# Flag features with KS > 0.1 or p < 0.01
```

### EDA Output

Produce a structured EDA summary that feeds into data preparation and model selection decisions:

```markdown
## EDA Summary — [Project Name]

### Key Findings
- [Top discriminative features and their relationship type (linear, non-linear, threshold)]
- [Redundant feature clusters identified]
- [Anomalies found and recommended treatment]
- [Temporal patterns or drift detected]

### Visualization Artifacts
- `eda_overview.png` — Distribution, correlation, and null rate overview
- `feature_interactions.png` — Top interaction effects
- `temporal_analysis.png` — Time-based patterns (if applicable)

### Statistical Test Results
| Test | Result | Implication |
|------|--------|-------------|
| Train/val distribution alignment | KS < 0.05 all features | No split leakage detected |
| Feature discriminativeness | 12 of 30 features significant at p < 0.01 | Focus feature engineering on top 12 |
| ... | ... | ... |

### Decisions Informed
- Metric choice: [informed by class balance, target distribution]
- Features to engineer: [informed by interaction effects, non-linear relationships]
- Cleaning priorities: [informed by anomaly detection, null patterns]
- Model architecture hints: [informed by relationship types, data volume]
```

---

## Stage 4: Pipeline Implementation

Stages 1–3 produce decisions. Stage 4 implements those decisions as the fixed, read-only `src/[slug]/prepare.py` script — the infrastructure the autonomous agent relies on but cannot modify.

```
src/[slug]/prepare.py
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

See `references/file-system-layout.md` for the full directory structure.
