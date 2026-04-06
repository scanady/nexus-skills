# data-science-autoresearch

Design autonomous AI research systems that iteratively improve ML models through automated experimentation.

## Example Prompts

### Full system design (end-to-end)

```
develop an autoresearch for my problem to create a model that predicts the
probability of life insurance customer lapsation based on a set of customer attributes.
```

```
set up autoresearch to build a fraud detection model for credit card transactions.
I have 2M labeled transactions in Parquet format.
```

```
design an autonomous training loop for a time series forecasting model that
predicts daily retail demand across 500 SKUs.
```

### Data readiness (Phase 0 pre-flight)

```
run a data readiness assessment on my customer churn dataset before we start autoresearch.
```

```
I have a messy CSV of insurance claims — help me clean it and engineer features
before setting up the autonomous experiment loop.
```

### Evaluation design

```
design evaluation criteria for a model that predicts patient readmission risk.
The metric needs to work for autonomous training with imbalanced classes.
```

```
what's the right primary metric for an autonomous training loop on a
recommendation system? I care about ranking quality, not click-through rate.
```

### Training harness & experiment tracking

```
create a training harness for my existing PyTorch model so an agent can
autonomously iterate on the architecture and hyperparameters.
```

```
set up experiment tracking for an autoresearch system — I already have
prepare.py and train.py, I need the agent program and results schema.
```

### Scoped modifications

```
build an autoresearch system for tabular classification, but skip data readiness —
I'm using the UCI Adult Income dataset and it's already clean.
```

```
autoresearch for my problem — I need to optimize a sentiment classifier.
I have a fine-tuned BERT baseline that gets 0.87 F1, and I want the agent
to explore architecture changes and training strategies to push it higher.
```