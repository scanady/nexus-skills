# data-ai-autoresearch

Design autonomous AI research systems that iteratively improve ML models through automated experimentation.

The skill should generate not only `prepare.py`, `train.py`, and `program.md`, but also a consistent execution layer: a blessed experiment runner plus repo-level instructions that keep autonomous work on the logged path.

## Example Prompts

### Full system design (end-to-end)

```
develop an autoresearch for my problem to create a model that predicts the probability of life insurance customer lapsation based on a set of customer attributes. Success metrics: AUC-ROC ≥ 0.85, precision at top-decile ≥ 0.60.
```

```
set up autoresearch to build a fraud detection model for credit card transactions. I have 2M labeled transactions in Parquet format. Success metrics: precision-recall AUC ≥ 0.80, false positive rate ≤ 1%, recall ≥ 0.90.
```

```
design an autonomous training loop for a time series forecasting model that predicts daily retail demand across 500 SKUs. Success metrics: WMAPE ≤ 15%, RMSE improvement ≥ 20% over naive seasonal baseline.
```

### Data readiness (Phase 0 pre-flight)

```
run a data readiness assessment on my customer churn dataset before we start autoresearch. Success metrics: missing value rate < 5%, feature coverage ≥ 95%, zero duplicate rows.
```

```
I have a messy CSV of insurance claims — help me clean it and engineer features before setting up the autonomous experiment loop. Success metrics: data completeness ≥ 98%, feature-target correlation lift ≥ 10% post-engineering.
```

### Evaluation design

```
design evaluation criteria for a model that predicts patient readmission risk. The metric needs to work for autonomous training with imbalanced classes. Success metrics: F1-score ≥ 0.75, balanced accuracy ≥ 0.80, calibration error (ECE) ≤ 0.05.
```

```
what's the right primary metric for an autonomous training loop on a
recommendation system? I care about ranking quality, not click-through rate. Success metrics: NDCG@10 ≥ 0.45, MAP@50 ≥ 0.30.
```

### Scoped modifications

```
build an autoresearch system for tabular classification, but skip data readiness — I'm using the UCI Adult Income dataset and it's already clean. Success metrics: accuracy ≥ 0.87, AUC-ROC ≥ 0.92.
```

```
autoresearch for my problem — I need to optimize a sentiment classifier.
I have a fine-tuned BERT baseline that gets 0.87 F1, and I want the agent
to explore architecture changes and training strategies to push it higher. Success metrics: F1 ≥ 0.90, inference latency ≤ 50ms, no regression on minority-class recall.
```

### Training harness & experiment tracking

```
create a training harness for my existing PyTorch model so an agent can
autonomously iterate on the architecture and hyperparameters. Success metrics: validation loss improvement ≥ 5% per iteration cycle, training time per run ≤ 30 minutes, experiment reproducibility rate = 100%.
```

```
set up experiment tracking for an autoresearch system — I already have
src/[slug]/prepare.py and src/[slug]/train.py, I need the agent program and results schema. Success metrics: 100% of runs logged with full config, metric delta tracked across runs, top-3 runs reproducible from logged artifacts.
```
