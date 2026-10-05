# Model Selection Guide

## Choosing the Baseline Architecture

The baseline model should be:
- **Functional**: Produces valid output and a non-trivial metric on the first run
- **Not optimized**: Leaves headroom for the agent to improve
- **Simple**: Easy for the agent to understand and modify
- **Well-structured**: Clear separation between architecture definition, optimizer setup, and training loop

## Model Type Decision Framework

The first decision is not which specific architecture to use, but which *category* of model is appropriate. This depends on data volume, problem complexity, interpretability requirements, and compute constraints.

### Decision Matrix

| Factor | Favors Machine Learning | Favors Deep Learning | Favors Hybrid |
|---|---|---|---|
| **Data volume** | < 10K samples | > 100K samples | 10K–100K (ML baseline, DL if it beats) |
| **Feature type** | Tabular, structured | Unstructured (text, image, audio) | Mixed structured + unstructured |
| **Interpretability** | Required (regulatory, medical, finance) | Not required or post-hoc explanations suffice | Interpretable ensemble + DL component |
| **Compute budget** | Limited (CPU only, no GPU) | GPU available, training time acceptable | Moderate — ML for fast iteration, DL for final model |
| **Feature engineering** | Domain experts available, features well-understood | Features are raw/high-dimensional, let the model learn representations | Domain features + learned representations |
| **Latency requirements** | Sub-millisecond inference required | Inference latency is flexible | ML for real-time, DL for batch |
| **Baseline expectations** | Need a strong, fast baseline to beat | Working on a problem where DL is proven SOTA | Want the best of both worlds |

### When to Choose Machine Learning

- **Tabular data**: Gradient boosted trees (XGBoost, LightGBM, CatBoost) consistently match or beat deep learning on structured tabular datasets. Start here.
- **Small datasets**: With < 10K samples, ML models with proper cross-validation will outperform deep learning which needs more data to learn effective representations.
- **Interpretability required**: Linear models, decision trees, and rule-based systems provide inherent interpretability. SHAP values add post-hoc explainability to tree ensembles.
- **Fast iteration**: ML models train in seconds to minutes. For rapid prototyping and hypothesis testing, ML is unbeatable.
- **Production constraints**: Many production systems require sub-millisecond inference, small model footprint, or CPU-only deployment.

### When to Choose Deep Learning

- **Unstructured data**: Text, images, audio, video — deep learning is the clear winner. Transformers for text, CNNs/ViTs for images, specialized architectures for audio.
- **Large datasets**: With > 100K samples, deep learning models can learn complex representations that surpass hand-engineered features.
- **Sequence and temporal modeling**: LSTMs, Transformers, Mamba, and SSMs handle variable-length sequences naturally.
- **Representation learning**: When the goal includes learned embeddings (for downstream tasks, similarity search, clustering), deep learning is necessary.
- **State-of-the-art performance**: For problems where DL is proven SOTA (NLP, computer vision, speech), start with DL.

### When to Choose Hybrid / Ensemble

- **Mixed data types**: Tabular features processed by gradient boosted trees, concatenated with neural network embeddings from text/image inputs.
- **Stacking**: ML models (XGBoost, logistic regression) as meta-learners on top of DL model predictions.
- **Feature augmentation**: Use DL to create embeddings from unstructured data, then feed those as features into ML models for the final prediction.
- **Phased approach**: Start with ML for a fast baseline, then add DL components only where they demonstrably improve performance.

---

## Traditional Machine Learning Models

For tabular/structured data and as baselines for any problem, ML models remain essential. These train fast, require less data, and often match or beat DL on structured problems.

### Linear Models

| Model | Best For | Key Hyperparameters | Notes |
|---|---|---|---|
| **Logistic Regression** | Binary/multiclass classification baseline | C (regularization), penalty (L1/L2/ElasticNet) | Fast, interpretable, strong baseline |
| **Linear Regression / Ridge / Lasso** | Regression baseline | alpha (regularization strength) | Ridge for multicollinearity, Lasso for feature selection |
| **ElasticNet** | Regression with many features | alpha, l1_ratio | Combines L1 and L2 benefits |

### Tree-Based Models

| Model | Best For | Key Hyperparameters | Notes |
|---|---|---|---|
| **Decision Tree** | Interpretable baseline, feature importance | max_depth, min_samples_leaf | Overfit-prone alone; valuable in ensembles |
| **Random Forest** | General-purpose classification/regression | n_estimators, max_depth, max_features | Robust, parallelizable, hard to overfit |
| **XGBoost** | Tabular data (competition winner) | learning_rate, max_depth, n_estimators, subsample, colsample_bytree | Often best tabular performance; highly tunable |
| **LightGBM** | Large tabular datasets, speed-critical | learning_rate, num_leaves, n_estimators, min_child_samples | Faster than XGBoost on large data; leaf-wise growth |
| **CatBoost** | Tabular with many categoricals | learning_rate, depth, iterations | Native categorical handling; less tuning needed |

### Support Vector Machines

| Model | Best For | Key Hyperparameters | Notes |
|---|---|---|---|
| **SVC (RBF kernel)** | Small-to-medium classification (< 50K rows) | C, gamma | Strong with proper scaling; doesn't scale to large data |
| **SVR** | Small-to-medium regression | C, gamma, epsilon | Same scaling limitations |
| **LinearSVC** | Large-scale text classification | C | Scales well; equivalent to logistic regression with hinge loss |

### Other Commonly Used Models

| Model | Best For | Key Hyperparameters | Notes |
|---|---|---|---|
| **KNN (K-Nearest Neighbors)** | Small datasets, anomaly detection | n_neighbors, metric, weights | No training phase; slow at inference for large datasets |
| **Naive Bayes (Gaussian/Multinomial)** | Text classification, fast baseline | var_smoothing (Gaussian), alpha (Multinomial) | Extremely fast; surprisingly strong for text |

### Ensemble Methods

| Method | How It Works | When to Use |
|---|---|---|
| **Bagging** | Train multiple models on bootstrap samples, average predictions | Reduce variance of high-variance models (trees) |
| **Boosting** | Sequentially train models to correct previous errors | XGBoost/LightGBM/CatBoost are the practical implementations |
| **Stacking** | Train a meta-model on the predictions of base models | Combine diverse model types (tree + linear + neural) |
| **Voting** | Average or majority-vote across different model types | Quick ensemble without meta-learning |
| **Blending** | Like stacking but uses a holdout set instead of cross-validation | Simpler than stacking, slightly less data-efficient |

### Time Series & Forecasting Models (Classical / Statistical)

These models are purpose-built for temporal data. Use them as strong baselines before trying DL time series architectures.

| Model | Best For | Key Characteristics | Notes |
|---|---|---|---|
| **ARIMA / SARIMA** | Univariate forecasting with trend + seasonality | Autoregressive + moving average + differencing | The classical baseline; handles stationarity via differencing. SARIMA adds seasonal component |
| **Exponential Smoothing (ETS)** | Univariate forecasting, short-to-medium horizon | Weighted averages with exponential decay | Holt-Winters variant handles trend + seasonality. Fast, interpretable |
| **Prophet** | Business time series with strong seasonality + holidays | Additive/multiplicative decomposition, automatic changepoint detection | Meta's library; great for business forecasting with irregular holidays and missing data |
| **VAR (Vector Autoregression)** | Multivariate time series (< 10 variables) | Each variable is a linear function of past values of all variables | Use when variables influence each other (e.g., supply and demand) |
| **TBATS / BATS** | Complex seasonality (multiple seasonal periods) | Trigonometric seasonality, Box-Cox, ARMA errors | Handles daily + weekly + annual seasonality simultaneously |
| **Theta Method** | Simple, robust univariate forecasting | Decomposes into two theta lines and extrapolates | Often surprisingly competitive; M3 competition winner |
| **LightGBM / XGBoost** (with lag features) | Tabular time series, many exogenous features | Tree-based; requires manual lag/window feature engineering | Strong when you have rich exogenous features alongside the time series |

**When to use classical vs. ML vs. DL for time series:**

| Scenario | Best Approach |
|---|---|
| Single series, < 1K points, need fast baseline | ARIMA / ETS / Theta |
| Single series with holidays, changepoints, interpretability needed | Prophet |
| Multiple related series, < 10K points per series | VAR, LightGBM with lag features |
| Many series (100+), cross-learning beneficial | Global DL models (PatchTST, TFT, N-BEATS) |
| Long sequences (1K+ timesteps), complex patterns | DL (Mamba, PatchTST, TimesNet) |
| Rich exogenous features alongside time series | LightGBM with lag features, or TFT |

### ML Model Selection by Problem Type

| Problem Type | Recommended Starting Model | Strong Alternatives |
|---|---|---|
| Binary classification (tabular) | LightGBM or XGBoost | Logistic Regression (baseline), CatBoost, Random Forest |
| Multi-class classification (tabular) | LightGBM or XGBoost | Random Forest, CatBoost |
| Regression (tabular) | LightGBM or XGBoost | Ridge Regression (baseline), Random Forest |
| Text classification | Logistic Regression + TF-IDF (baseline) | LinearSVC + TF-IDF, Naive Bayes |
| Anomaly detection (tabular) | Isolation Forest | Local Outlier Factor, One-Class SVM |
| Ranking | LambdaMART (LightGBM ranker) | XGBoost ranker |
| Univariate forecasting | ARIMA / ETS (baseline), Prophet | Theta, SARIMA |
| Multivariate forecasting | LightGBM with lag features | VAR, XGBoost with lag features |
| Survival analysis | Cox Proportional Hazards, Random Survival Forest | Gradient boosted survival models |

---

## Deep Learning Architecture Families

Before selecting by problem type, understand the major architecture families available. The agent can explore across families during autonomous experimentation.

### Transformer (Attention-Based)

The dominant architecture for most tasks. Uses self-attention to capture relationships across the full input sequence.

| Variant | Key Trait | Best For |
|---|---|---|
| Decoder-only (GPT-style) | Autoregressive, causal masking | Text generation, language modeling, code |
| Encoder-only (BERT-style) | Bidirectional attention | Classification, NER, embeddings |
| Encoder-decoder (T5-style) | Cross-attention between input and output | Translation, summarization, seq2seq |
| Vision Transformer (ViT) | Patches images into token sequences | Image classification, detection |
| Diffusion Transformer (DiT) | Transformer backbone for diffusion process | Image/video generation |

Key knobs: depth, width, number of heads, attention pattern (full, sliding window, sparse), activation function, normalization (pre-norm vs. post-norm), positional encoding (learned, RoPE, ALiBi).

**Trade-off:** Quadratic attention cost in sequence length. Fast and well-tooled, but expensive on very long sequences.

### State Space Models (SSMs)

Process sequences in linear time using continuous-time state space dynamics. Strong alternative to Transformers for long-sequence tasks.

| Model | Key Trait | Best For |
|---|---|---|
| Mamba | Selective SSM with input-dependent parameters; linear-time, hardware-aware | Language modeling, audio, genomics, long sequences |
| Mamba-2 | Structured state space duality (SSM ≈ attention); faster training | Same as Mamba with improved training efficiency |
| S4 | Original structured SSM; handles irregularly sampled data | Long-range time series, audio, scientific sequences |

Key knobs: state dimension, expansion factor, convolution kernel size, selective scan parameters, number of layers.

**Trade-off:** Excellent long-sequence scaling and fast inference. Less mature tooling than Transformers; some tasks (retrieval, in-context learning) may still favor attention.

### Hybrid Architectures

Combine attention layers with SSM or other layers to get benefits of both.

| Model | Structure | Best For |
|---|---|---|
| Jamba | Alternating Mamba + Transformer layers with MoE | Large-scale language modeling with long context |

**Trade-off:** Can capture both local detail (attention) and long-range dependencies (SSM). More complex to implement and tune.

### Linear Attention & Recurrent Alternatives

Replace quadratic attention with linear-complexity mechanisms while retaining sequence modeling capability.

| Model | Key Trait | Best For |
|---|---|---|
| RWKV | Linear-complexity RNN-Transformer hybrid; runs as RNN at inference | Language modeling, generation with constant-memory inference |
| xLSTM (Extended LSTM) | Modernized LSTM with exponential gating and matrix memory | Sequence tasks where recurrent inductive bias helps |

**Trade-off:** Dramatically cheaper inference and linear training scaling, but may underperform full attention on tasks requiring precise token-to-token lookups.

### Mixture of Experts (MoE)

Sparse architectures that route each input to a subset of "expert" sub-networks. More parameters per FLOP.

| Model | Key Trait | Best For |
|---|---|---|
| MoE Transformer (Mixtral-style) | Top-k expert routing per token | Language modeling at scale; more capacity without proportional compute increase |

Key knobs: number of experts, top-k selection, load balancing loss weight, expert capacity factor.

**Trade-off:** Higher total parameter count but similar compute per forward pass. Requires careful load balancing to avoid expert collapse.

### Convolutional Networks (CNNs)

Spatial inductive bias through learned filters. Still strong for vision and structured spatial data.

| Model | Key Trait | Best For |
|---|---|---|
| ConvNeXt / ConvNeXt v2 | Modernized ResNet with Transformer-style training | Image classification, especially with limited data |
| EfficientNet v2 | Compound scaling (depth, width, resolution) | Image classification with compute constraints |
| ResNet / ResNeXt | Residual connections, well-understood | Strong baseline for any vision task |
| U-Net | Encoder-decoder with skip connections | Segmentation, diffusion model backbone |
| Temporal CNN (TCN) | 1D causal convolutions over time | Time series when sequence length is fixed/moderate |
| WaveNet | Dilated causal convolutions | Audio generation, speech synthesis |

**Trade-off:** Strong spatial/local inductive bias. Less flexible than Transformers for global relationships but more data-efficient on spatial tasks.

### Graph Neural Networks (GNNs)

Operate on graph-structured data where relationships between entities matter.

| Model | Key Trait | Best For |
|---|---|---|
| GCN (Graph Convolutional Network) | Spectral convolutions on graphs | Node classification, molecular property prediction |
| GAT (Graph Attention Network) | Attention over graph neighbors | When neighbor importance varies |
| GraphSAGE | Sampling-based inductive learning | Large graphs, inductive (unseen nodes at inference) |

Key knobs: number of layers, hidden dimension, aggregation function, dropout, attention heads (for GAT).

**Trade-off:** Essential when data has explicit relational structure. Not applicable to grid data (use CNNs) or flat sequences (use Transformers/SSMs).

### MLPs & Tabular Specialists

For structured/tabular data, simpler architectures often match or beat complex ones.

| Model | Key Trait | Best For |
|---|---|---|
| MLP with residual connections | Simple, fast, strong baseline | Tabular regression and classification |
| TabNet | Attention-based feature selection | Tabular data when feature importance matters |
| FT-Transformer | Transformer applied to tabular features | When feature interactions are complex |
| XGBoost / LightGBM (non-neural) | Gradient boosted trees | Tabular data baseline; hard to beat with neural methods on many tasks |

**Trade-off:** Tabular data often doesn't benefit from deep architectures. Start with tree-based or MLP baselines; only go deeper if they underperform.

### Diffusion & Generative Models

For generating new data (images, audio, molecules, etc.).

| Model | Key Trait | Best For |
|---|---|---|
| Diffusion Transformer (DiT) | Transformer-backbone diffusion | Image generation at scale |
| Latent Diffusion (Stable Diffusion) | Diffusion in latent space via autoencoder | High-resolution image generation |
| VAE (Variational Autoencoder) | Learned latent space with reconstruction | Simple generation, representation learning |
| GAN (Generative Adversarial Network) | Adversarial training (generator vs. discriminator) | Image generation where sample quality > diversity |

**Trade-off:** Diffusion models produce high-quality outputs but are slow to iterate on in a 5-minute budget. VAEs are faster to train. GANs are unstable to tune autonomously.

### Time Series Deep Learning Models

Purpose-built neural architectures for forecasting and temporal pattern recognition. These often outperform classical methods when you have many related series (cross-learning) or long sequences with complex dependencies.

| Model | Key Trait | Best For |
|---|---|---|
| Temporal Fusion Transformer (TFT) | Attention + gating with static/known/observed inputs | Multi-horizon forecasting with rich covariates; interpretable attention weights |
| PatchTST | Patches time series into subsequences, then applies Transformer | Long-term forecasting; channel-independent design handles multivariate well |
| N-BEATS | Pure MLP with backward/forward residual decomposition | Univariate and multivariate forecasting; no need for feature engineering |
| N-HiTS | Hierarchical version of N-BEATS with multi-rate sampling | Long-horizon forecasting; more compute-efficient than N-BEATS |
| TimesNet | Transforms 1D time series into 2D tensors to capture multi-period patterns | General time series: forecasting, classification, anomaly detection, imputation |
| TSMixer | MLP-based, mixes across time and features | Multivariate forecasting when Transformer overhead isn't justified |
| Informer | ProbSparse attention for long sequences | Long-sequence time series forecasting (1K+ steps) |
| Autoformer | Auto-correlation mechanism replacing attention | Forecasting with strong seasonal patterns |
| iTransformer | Inverted Transformer — attention across variables, not time | Multivariate forecasting where cross-variable relationships matter most |
| DeepAR | Autoregressive RNN with probabilistic output | Probabilistic forecasting; produces prediction intervals, not just point estimates |
| Temporal CNN (TCN) | 1D causal dilated convolutions | Fast baseline for fixed-length sequences; simple to implement |

Key knobs: lookback window, forecast horizon, number of layers, hidden dimension, patch size (PatchTST), number of stacks/blocks (N-BEATS), attention heads.

**Trade-off:** DL time series models shine with many related series and long sequences. For single short series, classical methods (ARIMA, ETS, Prophet) are often better. Many DL time series models are available in libraries like [Darts](https://github.com/unit8co/darts), [NeuralForecast](https://github.com/Nixtla/neuralforecast), and [PyTorch Forecasting](https://github.com/jdb78/pytorch-forecasting).

## Deep Learning Architecture by Problem Type

Use these tables to select a starting deep learning baseline. The agent can explore beyond these during autonomous experiments. For ML baselines on tabular data, see the ML Model Selection by Problem Type table above.

### Sequence Modeling (Text, Time Series, Audio)

| Scale | Architecture | Starting Config | Notes |
|---|---|---|---|
| Small (< 10M params) | Transformer decoder | 4 layers, 256 dim, 4 heads | Well-understood, fast to iterate |
| Small (< 10M params) | Mamba | 4 layers, 256 dim | Good for long sequences on limited compute |
| Medium (10–100M params) | Transformer decoder | 8 layers, 512 dim, 8 heads | Autoresearch default range |
| Medium (10–100M params) | Mamba / Mamba-2 | 8 layers, 512 dim | Linear scaling in sequence length |
| Medium (10–100M params) | RWKV | 8 layers, 512 dim | Constant-memory inference |
| Large (100M+ params) | Transformer decoder | 12+ layers, 768+ dim | Needs high-end GPU |
| Large (100M+ params) | Jamba / hybrid | Mixed attention + Mamba layers | Long context with attention quality |

Agent exploration directions: try SSM vs. attention architecture swaps, hybrid layer patterns (e.g., alternating Mamba and attention), different positional encoding schemes, attention pattern variants (sliding window, sparse).

### Classification (Text, Image, Tabular)

| Data Type | Architecture | Starting Config | Notes |
|---|---|---|---|
| Text | Transformer encoder | 4 layers, 256 dim | Bidirectional attention for classification |
| Text | Mamba encoder variant | 4 layers, 256 dim | Try if sequence length is very long |
| Image | ConvNeXt / ConvNeXt v2 | ConvNeXt-Tiny | Strong with limited data, fast training |
| Image | ViT (Vision Transformer) | ViT-Tiny | Better with large data; needs more augmentation |
| Image | EfficientNet v2 | EfficientNet-B0 | Good compute-accuracy trade-off |
| Tabular | MLP with residual connections | 3 layers, 256 dim | Often competitive; always try first |
| Tabular | FT-Transformer | 3 layers, 192 dim | When feature interactions are complex |
| Graph | GCN or GAT | 3 layers, 128 dim | When data has explicit relational structure |

### Generation (Text, Image, Code, Audio)

| Task | Architecture | Starting Config | Notes |
|---|---|---|---|
| Text generation | Transformer decoder | Same as sequence modeling | Proven default |
| Text generation | Mamba / RWKV | Same as sequence modeling | Try for long-form generation |
| Code generation | Transformer decoder | Same as text, with code tokenizer | May need larger context window |
| Image generation | Diffusion Transformer (DiT) | DiT-S/2 | Best quality but slow per iteration |
| Image generation | VAE | Small encoder-decoder, 128 latent dim | Faster training, simpler to iterate on |
| Image generation | Flow Matching | U-Net or Transformer backbone | Emerging simpler alternative to diffusion |
| Audio generation | WaveNet (dilated causal CNN) | 10 layers, 64 channels, dilation doubling | Natural fit for raw audio |
| Audio generation | Transformer decoder | 4 layers, 256 dim, mel spectrogram tokens | Tokenize audio first, then model as sequence |

### Regression / Forecasting

| Task | Architecture | Starting Config | Notes |
|---|---|---|---|
| Tabular regression | MLP with residual connections | 3 layers, 256 dim | Start here; often hard to beat |
| Time series (short horizon) | Temporal CNN (TCN) | 6 layers, 64 channels | Simple DL baseline, fast |
| Time series (medium horizon) | PatchTST | 4 layers, 128 dim, patch size 16 | Patches time series like ViT patches images |
| Time series (long horizon) | N-BEATS or N-HiTS | 3 stacks, 256 dim | Pure MLP; no feature engineering needed |
| Time series (with covariates) | Temporal Fusion Transformer (TFT) | 4 layers, 128 dim | Best when you have static + known + observed inputs |
| Time series (very long sequences) | Mamba / S4 | 4 layers, 128 dim | Strong for 1K+ timesteps |
| Time series (multivariate) | iTransformer or TSMixer | 4 layers, 128 dim | Cross-variable attention or MLP mixing |
| Time series (probabilistic) | DeepAR | 3 layers, 128 dim | Produces prediction intervals |
| Time series (seasonal patterns) | Autoformer | 4 layers, 128 dim | Auto-correlation captures seasonality |
| Time series (general) | TimesNet | 4 layers, 128 dim | Versatile — forecasting, classification, anomaly detection |
| Spatial | ResNet-18 or ConvNeXt-Tiny | Default config | For grid-structured spatial data |
| Spatial | GNN (GCN or GraphSAGE) | 3 layers, 128 dim | For irregular spatial graphs (e.g., sensor networks) |

### Anomaly Detection

| Task | Architecture | Starting Config | Notes |
|---|---|---|---|
| Sequence anomaly | Transformer encoder + reconstruction | 4 layers, 128 dim | Detect anomalies via reconstruction error |
| Sequence anomaly | Mamba autoencoder | 4 layers, 128 dim | Better for long sequences |
| Tabular anomaly | Autoencoder (MLP) | 3 layers, bottleneck 32 dim | Classic approach; reconstruction threshold |
| Image anomaly | CNN autoencoder or VAE | Small encoder-decoder | Reconstruct normal; flag high-error inputs |

### Recommendation / Ranking

| Task | Architecture | Starting Config | Notes |
|---|---|---|---|
| Collaborative filtering | MLP with learned embeddings | 3 layers, 128 embedding dim | Embed users and items |
| Sequential recommendation | Transformer decoder | 4 layers, 128 dim | Model user history as a sequence |
| Sequential recommendation | Mamba | 4 layers, 128 dim | Try for very long user histories |
| Graph-based recommendation | GCN or GAT | 3 layers, 128 dim | When user-item interactions form a graph |

## Optimizer Recommendations

| Optimizer | When to Use | Starting LR | Notes |
|---|---|---|---|
| AdamW | Default for nearly all problems | 3e-4 to 1e-3 | Safest starting point |
| Muon + AdamW | Large Transformers (autoresearch default) | Muon: 0.02, AdamW: 3e-4 | Muon for attention weights, AdamW for embeddings |
| SGD + momentum | Image classification with augmentation | 0.1 with cosine decay | Still strong for CNNs |
| Lion | Memory-efficient alternative to AdamW | 1e-4 to 3e-4 | Uses sign of momentum; lower memory than Adam |
| Shampoo | When optimizer exploration is a priority | 1e-3 | Second-order; higher per-step cost but faster convergence |
| Sophia | For large language models | 1e-4 | Lightweight second-order; clips per-coordinate |
| 8-bit Adam (bitsandbytes) | When GPU memory is tight | Same as AdamW | Quantized optimizer states; nearly free memory savings |
| Schedule-Free (AdamW) | When LR schedule tuning is tedious | 1e-3 | Eliminates need for warmup/decay schedule |

The optimizer should be in the train script (modifiable), not the prepare script.

### Learning Rate Schedules

| Schedule | When to Use |
|---|---|
| Cosine decay with linear warmup | Default for most training runs |
| Linear warmup then constant | Short training budgets where decay doesn't help |
| Cosine with warm restarts | When exploring multiple "phases" in one run |
| One-cycle | Image classification with SGD |
| No schedule (Schedule-Free optimizer) | When using Schedule-Free AdamW variant |

## Structuring the Train Script

The train script must be self-contained and clearly organized:

```python
# ============================================================
# MODEL ARCHITECTURE — Agent can modify everything here
# ============================================================
DEPTH = 8
WIDTH = 512
NUM_HEADS = 8
# ... model class definition ...

# ============================================================
# OPTIMIZER — Agent can modify choice and hyperparameters
# ============================================================
LEARNING_RATE = 3e-4
WEIGHT_DECAY = 0.1
# ... optimizer setup ...

# ============================================================
# TRAINING LOOP — Agent can modify batch size, schedule, etc.
# ============================================================
DEVICE_BATCH_SIZE = 16
TOTAL_BATCH_SIZE = 2**17
# ... training loop ...
```

**Constants at the top**: All tunable knobs should be named constants at the top of the file, not buried in function calls.

**Clear sections**: The agent needs to quickly identify what to change. Use section headers.

**Logging**: Print the primary metric, secondary metrics, and key config at the end of training in a parseable format.

## Output Format

The training script must print results in a consistent, parseable format:

```
---
primary_metric:     0.997900
training_seconds:   300.1
total_seconds:      325.9
peak_vram_mb:       45060.2
total_tokens_M:     499.6
num_steps:          953
num_params_M:       50.3
---
```

This format allows `grep "^primary_metric:" run.log` to extract the key result.

---

## Training Foundation: Connecting Pipeline to Model

The training baseline is not just a model architecture — it's the culmination of every decision made in problem framing, the data pipeline, and model selection. A well-prepared foundation dramatically narrows the search space and gives the autonomous agent a strong starting point.

### How Preparation Shapes the Baseline

| Preparation Decision | Impact on Training Baseline |
|---|---|
| **Problem framing** (objective, success metrics, constraints) | Determines loss function, evaluation metric, and output layer design |
| **Data volume & quality** | Sets model complexity ceiling — small/noisy data → simpler model, heavy regularization |
| **Feature engineering** (domain features in src/[slug]/prepare.py) | Reduces what the model must learn — strong features → simpler model can succeed |
| **Class balance** | Determines class weighting in loss, sampling strategy, and metric choice |
| **Data types** (tabular vs. unstructured vs. mixed) | Determines model category (ML vs. DL vs. hybrid) |
| **Compute constraints** | Sets parameter budget, batch size limits, and time budget per experiment |
| **EDA findings** (non-linear relationships, interactions) | Suggests architecture features (attention, feature crossing, non-linear activations) |
| **Temporal structure** | Determines whether sequence models, lag features, or cross-sectional models are appropriate |

### Baseline Design Principles

1. **Start with the simplest model that can succeed** — If EDA shows linear feature-target relationships on tabular data, start with logistic regression or a shallow tree ensemble, not a Transformer.
2. **Match model complexity to data volume** — See the data volume table in Stage 1 of the data pipeline guide. Overly complex models on small data waste experiment iterations on regularization tuning.
3. **Encode preparation findings** — If EDA revealed strong interactions, include interaction features. If it found non-linear relationships, ensure the model can capture them (trees, non-linear activations, kernel methods).
4. **Leave headroom** — The baseline should be functional but not optimized. Use default hyperparameters, moderate depth, standard optimizer settings. The autonomous agent's job is to find the optimal configuration.
5. **Make the baseline deterministic** — Fixed seed, fixed data splits, fixed preprocessing. The first run should always produce the same metric, establishing a reliable comparison point.

### Foundation Checklist (before starting the autonomous loop)

- [ ] Problem objective and success metric are defined and validated against real-world goals
- [ ] Data pipeline produces clean, feature-rich data with documented transforms
- [ ] EDA findings have been incorporated into feature engineering and model selection
- [ ] Model type (ML, DL, hybrid) is justified by data characteristics
- [ ] Baseline architecture is chosen with clear rationale from the selection tables above
- [ ] Baseline runs within the time budget and produces a valid primary metric
- [ ] All preparation decisions are locked in `src/[slug]/prepare.py` — the agent only modifies `src/[slug]/train.py`
- [ ] The gap between baseline performance and target metric defines the agent's search space
