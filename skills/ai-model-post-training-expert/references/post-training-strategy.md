# Post-Training Strategy Guide

## Overview

Post-training is a family of methods, not a single recipe. The right method depends on the kind of supervision you have, the deployment constraints you must hit, and how much behavior change you need.

## Method Selection Matrix

| Method | Use When | Avoid When | Key Tradeoff |
|--------|----------|------------|--------------|
| Supervised fine-tuning (SFT) | You have high-quality target responses for the behavior you want | You only have pairwise preferences or vague reward signals | Simplest and most stable way to move task behavior |
| LoRA / QLoRA / PEFT | Base model is large and you need efficient adaptation or many task variants | You need a single merged artifact with no adapter dependency and full fine-tuning quality is required | Large memory savings with modest quality tradeoff |
| Full fine-tuning | You control substantial compute and need maximum adaptation capacity | Hardware is limited or you need many cheap variants | Highest flexibility, highest cost |
| Continued pretraining | Domain language shift is large and labeled supervision is limited | The main gap is instruction following rather than domain vocabulary or style | Improves domain fit before instruction or preference tuning |
| DPO / ORPO | You have offline preference pairs and want a simpler alternative to PPO-style RLHF | You need online exploration or reward depends on interactive rollouts | Strong offline alignment with less system complexity |
| PPO / GRPO / online RLHF | Reward requires rollouts, tool use, or long-horizon interaction beyond static preference pairs | Static pairwise preferences are enough | More expressive objective, much higher operational cost |
| Reward model training | You need a learned scoring function to rank generations or drive online RL | A fixed judge or direct preference objective is already sufficient | Adds flexibility but creates another model to validate |
| Distillation | Latency, memory, or serving cost matters more than peak model quality | You still need the teacher's full capability in production | Transfers capability into a cheaper model |
| Model merging / adapter composition | You need to combine compatible deltas after separate training runs | Base checkpoints, tokenizers, or objectives are incompatible | Fast synthesis step, but can create regressions if done carelessly |

## Escalation Ladder

Start with the least complex method that can plausibly solve the problem:

1. Improve prompts and templates first.
2. Use SFT when the target behavior is easy to demonstrate.
3. Use PEFT before full fine-tuning when model size is the limiting factor.
4. Use offline preference optimization before online RL when you already have pairwise preferences.
5. Add reward models or online RL only when static datasets no longer capture the objective.
6. Distill or quantize after behavior quality is acceptable.

## Method Choice Heuristics

- If the user can point to good answers, start with SFT.
- If the user can rank outputs but cannot author ideal responses, use DPO or ORPO.
- If rollout quality depends on tools, environment interaction, or long reasoning traces, consider PPO or GRPO.
- If deployment cost dominates, distill or quantize instead of endlessly pushing the teacher.
- If the domain language is specialized and the base model consistently misunderstands it, add continued pretraining before SFT.

## Compatibility Checks Before Training

- Base checkpoint and tokenizer are fixed and documented.
- Chat template or prompt format is fixed across train and eval.
- Supervised and preference datasets are split cleanly.
- Success metric is tied to the user's actual deployment goal.
- Serving target is clear: adapter, merged weights, quantized artifact, or distilled model.