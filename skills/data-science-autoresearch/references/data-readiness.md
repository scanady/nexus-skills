# Data Readiness Guide (Phase 0 Pre-Flight)

## Purpose

This phase ensures the data is understood, clean, and feature-complete before the autonomous experiment loop begins. Decisions made here become fixed infrastructure in `prepare.py`. Rushing through this phase — or skipping it — means the autonomous agent optimizes on top of flawed foundations.

**When to run:** Always for real-world or unfamiliar data. Skip only for well-known benchmark datasets (MNIST, CIFAR, FineWeb, etc.) where data quality is already established.

**Who runs this:** The human (or a separate analysis agent), not the autonomous experiment agent. This is a thinking phase, not a training phase.

## Step 1: Exploratory Data Analysis (EDA)

EDA is a human insight activity. The goal is to build intuition about the data so that every downstream decision — metric choice, feature engineering, cleaning strategy — is informed rather than guessed.

### Data Profiling Checklist

Run these automatically and review the output:

```python
# Structural profile
df.shape                           # (rows, columns)
df.dtypes                          # Column types
df.describe(include='all')         # Summary statistics
df.isnull().sum() / len(df)        # Null rates per column
df.nunique()                       # Cardinalities (flag low-cardinality numerics, high-cardinality categoricals)
df.duplicated().sum()              # Exact duplicate rows
```

### Distribution Analysis

- **Target variable**: Plot distribution. For classification, report class balance ratio. For regression, check for skew, bimodality, or heavy tails.
- **Numeric features**: Histograms or KDE plots. Flag features with extreme skew (|skew| > 2), heavy tails, or multi-modal distributions.
- **Categorical features**: Value counts. Flag categories with < 1% representation (consider grouping into "other"). Flag categories that appear only in train or only in validation.
- **Temporal features**: Plot over time if applicable. Check for seasonality, trends, or regime changes.

### Correlation & Relationships

- **Feature-target correlation**: Compute point-biserial (for binary target) or Pearson/Spearman (for continuous target) for each feature. Rank by absolute correlation.
- **Feature-feature correlation**: Compute pairwise correlation matrix. Flag pairs with |r| > 0.85 — these are candidates for dropping one to reduce multicollinearity.
- **Interaction effects**: For top-5 features by target correlation, plot 2D interaction heatmaps with target.

### Data Leakage Detection

This is the most critical check. Data leakage silently inflates metrics and produces models that fail in production.

- **Direct leakage**: Is any feature derived from the target or from future information? (e.g., "policy_cancelled_date" when predicting lapsation)
- **Indirect leakage**: Is any feature a near-perfect proxy for the target? (AUC > 0.95 for a single feature against the target is suspicious)
- **Temporal leakage**: If the data has a time dimension, is the train/validation split temporal? Random splits on time-series data leak future information.
- **Group leakage**: If multiple rows relate to the same entity (e.g., same customer over multiple years), are all rows for an entity in the same split?

### Outlier Assessment

For each numeric feature:
- Compute IQR boundaries: Q1 − 1.5×IQR, Q3 + 1.5×IQR
- Count observations beyond boundaries
- Decide: clip, winsorize, or leave. Document the decision and rationale.

**Decision framework:**
- If outliers are data errors (impossible values) → clip at physical/business limits
- If outliers are rare but real → keep them; the model should handle extremes
- If outliers are extreme but meaningful (top 0.1% income) → winsorize to reduce influence without removing information

## Step 2: Data Cleansing

Every cleansing decision becomes a fixed transform in `prepare.py`. Document each one so it can be reviewed, audited, or revised later.

### Null Handling Decision Matrix

| Null Rate | Feature Importance | Recommended Strategy |
|---|---|---|
| < 1% | Any | Impute with median (numeric) or mode (categorical) |
| 1–5% | High (top quartile correlation with target) | Impute with median/mode + add binary "was_null" indicator column |
| 1–5% | Low | Impute with median/mode |
| 5–20% | High | Impute + "was_null" indicator. Investigate why nulls occur — they may be informative |
| 5–20% | Low | Consider dropping the feature entirely |
| > 20% | Any | Drop the feature unless nulls are informative (e.g., "no claims filed" → null claims fields) |

### Categorical Cleaning

- Standardize casing and whitespace (`" Male "` → `"male"`)
- Merge semantically identical categories (`"M"` and `"male"` → `"male"`)
- Group rare categories (< 1% of data) into `"other"` — unless the rare category is meaningful for the problem
- Decide encoding strategy: label encoding (ordinal), one-hot (low cardinality ≤ 10), or leave for learned embeddings in the model

### Numeric Cleaning

- Apply clip bounds from outlier assessment (e.g., `income.clip(0, 500_000)`)
- Log-transform heavily right-skewed features (income, monetary amounts) — measure if skew improves
- Apply chosen imputation strategy for nulls

### Duplicate Handling

- **Exact duplicates**: Drop. Keep first occurrence.
- **Near-duplicates** (same entity, slightly different timestamps): Investigate. May indicate data collection issues or may be legitimate repeat observations.

## Step 3: Domain Feature Engineering (Round 1)

Create features that require business knowledge. These live in `prepare.py` because the autonomous agent shouldn't change them — they represent known domain relationships.

### Feature Engineering Patterns

| Pattern | Example | When to Use |
|---|---|---|
| **Ratio** | premium_to_income_ratio | Two features have a meaningful business ratio |
| **Threshold/flag** | is_new_policy (age < 24 months) | A known business boundary exists |
| **Bucket** | age_group (18–30, 31–45, 46–60, 61+) | Non-linear relationship with target around known thresholds |
| **Time-since** | months_since_last_payment | Recency matters more than raw count |
| **Rolling aggregate** | avg_missed_payments_last_6m | Recent trend is more predictive than all-time aggregate |
| **Interaction** | missed_payments × premium_amount | Two features combine to create a stronger signal |
| **Indicator** | has_ever_claimed (claims_filed > 0) | Binary presence is more meaningful than count |
| **Relative position** | income_percentile | Where the individual sits in the distribution matters more than raw value |

### What NOT to engineer here

- Mathematical transforms the model can learn (polynomial, log, square root) — these go in `train.py`
- Feature selection — let the model (or the agent experimenting with feature attention) handle this
- Complex interactions without clear domain justification — let the model discover these

## Step 4: Data Quality Gates

These are pass/fail checks. If any fail, go back and fix the issue before proceeding to the autonomous loop.

### Gate 1: Completeness
- No feature used in training has > 5% nulls after cleansing
- If a feature exceeds this, document why it's being kept (e.g., nulls are informative)

### Gate 2: Class Balance Assessment
- Compute imbalance ratio (majority_class / minority_class)
- If ratio > 10:1, document the strategy:
  - Metric choice that handles imbalance (log loss, AUC, macro F1 — not accuracy)
  - Class weighting in the loss function (initial value in `train.py`, experimentable by the agent)
  - Oversampling/undersampling in `prepare.py` (if used, document the method and ratio)

### Gate 3: Train/Validation Distribution
- For each top-10 feature (by target correlation), compare train vs. validation distributions
- KS statistic > 0.1 or visual divergence → investigate. May indicate temporal drift, sampling bias, or data leakage.
- Target distribution should be similar in train and validation (within 1 percentage point for classification)

### Gate 4: Leakage Scan
- No single feature achieves AUC > 0.95 against the target (unless it's a known strong signal with domain justification)
- No feature derived from the target or from future information is present
- If temporal data: train/validation split respects time ordering

### Gate 5: Feature Variance
- No feature has zero variance (constant column)
- No feature has > 99% of values being the same (near-constant — likely uninformative)

## Output: Data Readiness Report

Produce a structured report summarizing:

```markdown
## Data Readiness Report — [Project Name]

### Dataset Profile
- Rows: X | Columns: Y | Target: Z
- Target distribution: [class counts or histogram description]
- Null rate summary: [worst features listed]

### EDA Findings
- [Key correlations with target]
- [Feature pairs with high collinearity]
- [Outlier treatment decisions]
- [Leakage concerns: none found / [specific concerns]]

### Cleansing Decisions
| Feature | Issue | Resolution |
|---------|-------|------------|
| feature_a | 3% nulls | Imputed with median |
| feature_b | Extreme skew | Log-transformed |
| ... | ... | ... |

### Domain Features Created
| Feature | Definition | Rationale |
|---------|-----------|-----------|
| premium_to_income_ratio | annual_premium / income | Premium burden predicts lapsation |
| ... | ... | ... |

### Quality Gate Results
| Gate | Status | Notes |
|------|--------|-------|
| Completeness | ✅ PASS | Max null rate after cleansing: 0.3% |
| Class Balance | ⚠️ WARN | 14:1 imbalance, using log loss + class weighting |
| Train/Val Distribution | ✅ PASS | KS < 0.05 for all features |
| Leakage Scan | ✅ PASS | No single-feature AUC > 0.90 |
| Feature Variance | ✅ PASS | No constant features |
```

This report becomes an input to Phase 3 (Data Pipeline & Infrastructure). Every cleansing decision and domain feature listed here is implemented as fixed code in `prepare.py`.
