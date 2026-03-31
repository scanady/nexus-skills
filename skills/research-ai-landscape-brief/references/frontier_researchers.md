# Frontier Researchers & Labs

Auto-qualify list for the single-source exception rule. When any of these individuals or labs publishes a new GitHub repository, arXiv preprint, or X/Bluesky thread — it qualifies as frontier signal **without requiring cross-platform corroboration**.

Apply the `[FRONTIER]` tag and include in the **Early-Stage / High-Velocity** section.

---

## Independent Researchers

| Name | Handle | Signal Type | Why They Matter |
|------|--------|-------------|-----------------|
| Andrej Karpathy | @karpathy (GitHub/X) | GitHub repo, X thread | Ex-OpenAI/Tesla; built micrograd, nanoGPT, llama2.c, autoresearch. New repos routinely hit trending immediately. |
| George Hotz | @geohot (GitHub/X) | GitHub repo, X thread | Creator of tinygrad; builds against the mainstream stack. New repos signal emerging directions for efficient inference. |
| François Chollet | @fchollet (GitHub/X) | GitHub repo, X post | Created Keras; runs ARC-AGI benchmark. Work on reasoning and abstraction is leading indicator for next-wave benchmarks. |
| Chris Olah | @ch402 (X/Bluesky) | Blog post, paper | Anthropic interpretability lead. New work often reframes how the field understands what's happening inside models. |
| Neel Nanda | @NeelNanda5 (X/GitHub) | Paper, GitHub repo | Mechanistic interpretability; Anthropic. High signal on alignment-adjacent technical progress. |
| Jeremy Howard | @jeremyphoward (GitHub/X) | GitHub repo, blog | Fast.ai; known for making frontier techniques accessible. New repos often signal a technique reaching usability threshold. |
| Tim Dettmers | @Tim_Dettmers (X) | Paper, GitHub repo | bitsandbytes; quantization research. New papers signal what will be standard in 6 months. |
| Harrison Chase | @hwchase17 (GitHub/X) | GitHub repo | LangChain creator; new repos signal direction of OSS agent tooling. |
| Simon Willison | @simonw (GitHub/X/blog) | Blog post, GitHub repo | LLM engineering practitioner; signal for what works in production. |

---

## Lab Accounts (GitHub + arXiv)

Any release, repo, or preprint from these accounts auto-qualifies:

| Lab | GitHub Org | arXiv Affiliation | Primary Signal |
|-----|-----------|-------------------|----------------|
| OpenAI | `openai` | "OpenAI" in authors | Model releases, alignment research, API capabilities |
| Anthropic | `anthropic` | "Anthropic" in authors | Claude updates, interpretability papers, safety research |
| Google DeepMind | `google-deepmind` | "Google DeepMind" in authors | Gemini, Gemma, AlphaFold-era biosci AI, robotics |
| Meta AI (FAIR) | `facebookresearch`, `meta-llama` | "Meta" or "FAIR" in authors | Llama releases, PyTorch updates, open model weights |
| Mistral AI | `mistralai` | "Mistral" in authors | New model weights; high signal for open frontier models |
| xAI | `xai-org` | "xAI" in authors | Grok releases, API launches |
| Apple ML | `apple` | "Apple" in authors | On-device inference, CoreML, MLX framework |
| Microsoft Research | `microsoft` | "Microsoft" in authors | Phi models, Copilot research, enterprise AI |
| EleutherAI | `EleutherAI` | "EleutherAI" in authors | Open evals, Pythia, GPT-NeoX; benchmark and infra signal |
| Allen Institute for AI | `allenai` | "Allen Institute" in authors | OLMo, AI2 Tulu; open research stack |
| Hugging Face | `huggingface` | "Hugging Face" in authors | Model hub, Transformers library, Spaces platform |

---

## High-Signal OSS Builders

New repos from these accounts often reach trending before any press coverage:

| Handle | Known For | Watch Signal |
|--------|-----------|--------------|
| ggerganov (GitHub) | llama.cpp, whisper.cpp | Any new repo signals local inference direction |
| lllyasviel (GitHub) | ControlNet, ComfyUI, Fooocus | Image/video generation tooling |
| oobabooga (GitHub) | text-generation-webui | OSS UI/UX for local models |
| vllm-project (GitHub) | vLLM inference engine | Production inference performance |
| BerriAI (GitHub) | LiteLLM | API routing and multi-provider tooling |
| run-llama (GitHub) | LlamaIndex | Agent orchestration, RAG |
| langchain-ai (GitHub) | LangChain, LangGraph | Agent frameworks, LLM tooling |
| unslothai (GitHub) | Unsloth | Training efficiency; signals fine-tuning accessibility |

---

## Notable Voices on X / Bluesky

X threads from these accounts auto-qualify for frontier signal, even without a linked repo or paper:

| Handle | Platform | Why They Matter |
|--------|----------|-----------------|
| @sama (Sam Altman) | X | OpenAI CEO; threads often precede announcements |
| @AnthropicAI | X | Official Anthropic announcements |
| @ylecun (Yann LeCun) | X/Bluesky | Meta Chief AI Scientist; contrarian takes with high evidence |
| @ilyasut (Ilya Sutskever) | X | SSI co-founder; threads rare but extremely high signal |
| @demishassabis | X | Google DeepMind CEO |
| @DrJimFan | X | NVIDIA Embodied AI; robotics/agent frontier |
| @cwolferesearch | X | AI safety researcher; early signal on frontier risks |
| @emollick (Ethan Mollick) | X | Wharton prof; early practical AI adopter patterns |

---

## arXiv Watch — Key Author Patterns

When searching arXiv, flag any paper where:
- First or last author is from a major lab listed above
- Author list includes ≥2 known names from the researcher table above
- Paper has ≥3 different institutional affiliations (broad collaboration = high attention)
- Title contains: "GPT-", "Claude", "Gemini", "Llama", "reasoning", "agent", "alignment", "interpretability", "emergent"

---

## Usage in the Skill

In **Step 3 (Filter & Corroborate)**:
> Check all single-source GitHub repos and arXiv papers against `references/frontier_researchers.md`. If the author, org, or handle matches any entry, apply `[FRONTIER]` tag and route to the **Early-Stage / High-Velocity** section — no corroboration required.

In **Step 4 (Categorize)**:
> Route `[FRONTIER]`-tagged items to the **🚀 Early-Stage / High-Velocity** category.

---

*Maintainer note: Update this file quarterly or when significant new voices emerge. Add handles for researchers who repeatedly surface breakthrough work before wider coverage.*
