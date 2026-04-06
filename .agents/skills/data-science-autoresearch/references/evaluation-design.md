# Evaluation Design Guide

## Choosing a Primary Metric

The primary metric is the single scalar the autonomous agent optimizes. It must satisfy:

1. **Automatically computable** — No human judgment in the loop. The agent must compute it after every experiment.
2. **Deterministic** — Same model state on same data always produces the same value.
3. **Architecture-independent** — Changing model size, vocab size, or architecture should not inherently change the metric's scale.
4. **Fast to compute** — Evaluation must complete in seconds, not minutes. It runs after every experiment.
5. **Monotonic relationship to the real objective** — Lower (or higher) is always better, with no ambiguous middle ground.

## Metric Selection by Problem Type

| Problem Type | Recommended Primary Metric | Direction | Notes |
|---|---|---|---|
| Language modeling | Bits per byte (BPB) | Lower is better | Vocab-size-independent, allows fair comparison across tokenizer changes |
| Text classification | Accuracy or macro F1 on held-out set | Higher is better | Use macro F1 for imbalanced classes |
| Sequence labeling (NER, POS) | Entity-level F1 | Higher is better | Token-level metrics inflate scores |
| Machine translation | BLEU or chrF on held-out set | Higher is better | chrF is more robust to tokenization |
| Summarization | ROUGE-L F1 | Higher is better | Use fixed-length reference summaries |
| Regression | Mean absolute error (MAE) | Lower is better | Less sensitive to outliers than MSE |
| Ranking / retrieval | MRR@K or NDCG@K | Higher is better | Fix K across all experiments |
| Image classification | Top-1 accuracy on validation set | Higher is better | Use fixed augmentation in eval |
| Object detection | mAP@0.5 | Higher is better | Fixed IoU threshold |
| Time series forecasting | Symmetric MAPE or MAE | Lower is better | sMAPE handles zero values |
| Anomaly detection | F1 at fixed threshold | Higher is better | Fix the decision threshold in prepare script |
| Recommendation | Hit rate@K or NDCG@K | Higher is better | Fix K and candidate set |

## Why Bits Per Byte (BPB) Works

Autoresearch uses BPB as its metric because:
- **Vocab-independent**: BPB normalizes by bytes, not tokens. Changing the tokenizer vocabulary size doesn't break comparisons.
- **Architecture-independent**: Whether you use 4 layers or 12, BPB measures the same thing.
- **Interpretable**: Compression rate of the model on the validation data.

For non-language problems, find the equivalent — a metric that is **normalized**, **architecture-agnostic**, and **automatically computable**.

## Designing the Evaluation Harness

The evaluation function lives in the prepare script (read-only). Structure:

```python
def evaluate(model, eval_dataloader, device):
    """
    Compute primary metric on the full validation set.
    
    Requirements:
    - Deterministic: set torch.manual_seed, disable dropout
    - Complete: evaluate on ALL validation data, not a sample
    - Fast: use torch.no_grad(), avoid unnecessary computation
    - Returns: dict with primary metric and secondary metrics
    """
    model.eval()
    # ... compute metric over full validation set ...
    return {
        "primary_metric": value,       # The number the agent optimizes
        "secondary_metric_1": value,   # Tracked, not optimized
        "secondary_metric_2": value,   # Tracked, not optimized
    }
```

## Secondary Metrics

Track but do not optimize:

| Metric | Purpose |
|---|---|
| Peak VRAM (MB) | Monitor resource usage — flag experiments that blow up memory |
| Training wall-clock time | Should always be ~time_budget; flag overruns |
| Parameter count | Track model size trends |
| Inference latency (ms/sample) | Important if deploying the model |
| Throughput (samples/sec) | Training efficiency indicator |

## Evaluation Data Strategy

- **Size**: Large enough that metric variance between identical runs is < 0.1% of the metric range
- **Fixed**: The evaluation set never changes across experiments
- **Representative**: Sampled from the same distribution as the real-world deployment data
- **Separate**: Completely disjoint from training data — no leakage
- **Cached**: Preprocessed and stored so evaluation startup is instant

## Anti-Patterns

- **Using training loss as the metric**: Overfitting looks like progress. Always use held-out validation.
- **Metric depends on model internals**: If changing from attention to convolution breaks the metric computation, the metric is coupled to architecture.
- **Sampling the eval set**: Evaluating on a random subset introduces variance. Use the full eval set every time.
- **Slow evaluation**: If eval takes 2 minutes on a 5-minute time budget, you've lost 40% of experiment capacity.
- **Multiple primary metrics**: The agent needs a single number to decide keep vs. discard. If you have two metrics, combine them into a weighted single score in the evaluation function.
