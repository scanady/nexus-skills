# Model Selection Guide

## Choosing the Baseline Architecture

The baseline model should be:
- **Functional**: Produces valid output and a non-trivial metric on the first run
- **Not optimized**: Leaves headroom for the agent to improve
- **Simple**: Easy for the agent to understand and modify
- **Well-structured**: Clear separation between architecture definition, optimizer setup, and training loop

## Architecture Families

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
| Hyena | Implicit convolution-based; subquadratic | Long-context language, DNA sequence modeling |

Key knobs: state dimension, expansion factor, convolution kernel size, selective scan parameters, number of layers.

**Trade-off:** Excellent long-sequence scaling and fast inference. Less mature tooling than Transformers; some tasks (retrieval, in-context learning) may still favor attention.

### Hybrid Architectures

Combine attention layers with SSM or other layers to get benefits of both.

| Model | Structure | Best For |
|---|---|---|
| Jamba | Alternating Mamba + Transformer layers with MoE | Large-scale language modeling with long context |
| Zamba | Shared attention layer + Mamba backbone | Efficient language modeling |
| StripedHyena | Alternating Hyena + attention layers | Long-context language tasks |
| Griffin | Gated linear recurrence + local attention | Efficient language modeling |

**Trade-off:** Can capture both local detail (attention) and long-range dependencies (SSM). More complex to implement and tune.

### Linear Attention & Recurrent Alternatives

Replace quadratic attention with linear-complexity mechanisms while retaining sequence modeling capability.

| Model | Key Trait | Best For |
|---|---|---|
| RWKV | Linear-complexity RNN-Transformer hybrid; runs as RNN at inference | Language modeling, generation with constant-memory inference |
| xLSTM (Extended LSTM) | Modernized LSTM with exponential gating and matrix memory | Sequence tasks where recurrent inductive bias helps |
| RetNet (Retentive Network) | Retention mechanism: parallel training, recurrent inference | Language modeling with efficient inference |
| Linear Transformer | Kernel-based linear attention approximation | When attention cost is the bottleneck |

**Trade-off:** Dramatically cheaper inference and linear training scaling, but may underperform full attention on tasks requiring precise token-to-token lookups.

### Mixture of Experts (MoE)

Sparse architectures that route each input to a subset of "expert" sub-networks. More parameters per FLOP.

| Model | Key Trait | Best For |
|---|---|---|
| MoE Transformer (Mixtral-style) | Top-k expert routing per token | Language modeling at scale; more capacity without proportional compute increase |
| MoE-Mamba | Alternating Mamba + MoE layers | Combining SSM efficiency with expert specialization |
| Soft MoE | Differentiable routing, no discrete selection | Vision tasks, when hard routing causes training instability |

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
| GIN (Graph Isomorphism Network) | Maximally expressive among message-passing GNNs | Graph classification, when distinguishing graph structures matters |
| Equivariant GNN (e.g., EGNN, SchNet) | Respects physical symmetries (rotation, translation) | Molecular dynamics, protein structure, physics simulations |

Key knobs: number of layers, hidden dimension, aggregation function, dropout, attention heads (for GAT).

**Trade-off:** Essential when data has explicit relational structure. Not applicable to grid data (use CNNs) or flat sequences (use Transformers/SSMs).

### MLPs & Tabular Specialists

For structured/tabular data, simpler architectures often match or beat complex ones.

| Model | Key Trait | Best For |
|---|---|---|
| MLP with residual connections | Simple, fast, strong baseline | Tabular regression and classification |
| TabNet | Attention-based feature selection | Tabular data when feature importance matters |
| FT-Transformer | Transformer applied to tabular features | When feature interactions are complex |
| KAN (Kolmogorov-Arnold Network) | Learnable activation functions on edges | Scientific computing, symbolic regression, low-dimensional data |
| XGBoost / LightGBM (non-neural) | Gradient boosted trees | Tabular data baseline; hard to beat with neural methods on many tasks |

**Trade-off:** Tabular data often doesn't benefit from deep architectures. Start with MLP or tree-based baselines; only go deeper if they underperform.

### Diffusion & Generative Models

For generating new data (images, audio, molecules, etc.).

| Model | Key Trait | Best For |
|---|---|---|
| Diffusion Transformer (DiT) | Transformer-backbone diffusion | Image generation at scale |
| Latent Diffusion (Stable Diffusion) | Diffusion in latent space via autoencoder | High-resolution image generation |
| VAE (Variational Autoencoder) | Learned latent space with reconstruction | Simple generation, representation learning |
| Flow Matching | Continuous normalizing flows, simpler training than diffusion | Generation tasks, emerging alternative to diffusion |
| GAN | Adversarial training (generator vs. discriminator) | Image generation where sample quality > diversity |

**Trade-off:** Diffusion models produce high-quality outputs but are slow to iterate on in a 5-minute budget. VAEs are faster to train. GANs are unstable to tune autonomously.

## Architecture by Problem Type

Use these tables to select a starting baseline. The agent can explore beyond these during autonomous experiments.

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
| Tabular | KAN | 2 layers, 64 nodes | For low-dimensional scientific/structured data |
| Graph | GCN or GAT | 3 layers, 128 dim | When data has explicit relational structure |
| Molecular | Equivariant GNN (SchNet/EGNN) | 4 layers, 128 dim | Respects physical symmetries |

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
| Molecular generation | Equivariant GNN + diffusion | 4 layers, 128 dim | Domain-specific but powerful |

### Regression / Forecasting

| Task | Architecture | Starting Config | Notes |
|---|---|---|---|
| Tabular regression | MLP with residual connections | 3 layers, 256 dim | Start here; often hard to beat |
| Tabular regression | KAN | 2 layers, 64 nodes | Try for smooth, low-dimensional functions |
| Time series | PatchTST (Transformer) | 4 layers, 128 dim, patch size 16 | Patches time series like ViT patches images |
| Time series | Mamba / S4 | 4 layers, 128 dim | Strong for very long horizons |
| Time series | Temporal CNN (TCN) | 6 layers, 64 channels | Simple baseline, fast |
| Time series | xLSTM | 4 layers, 128 dim | When recurrent inductive bias helps |
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
