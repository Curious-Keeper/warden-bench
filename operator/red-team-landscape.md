# Red-Team & Jailbreak Tooling — Landscape

Where this project's harness sits relative to production red-team tooling, with
sources for further reading. Generated as background notes for the workshop
CFP — not a survey, not exhaustive.

## What this project's harness is

The notebook in [operator/](operator/) is a textbook
implementation of **PAIR** (Prompt Automatic Iterative Refinement, Chao et
al. 2023). One attacker LLM, one judge LLM, linear iteration with feedback.
That's the academic baseline most modern red-team tools build on.

Three companion modules live alongside the notebook and can be driven from
the CLI or imported into the notebook:

- [`operator/tap/`](operator/tap/) — **TAP** (Tree of
  Attacks with Pruning, Mehrotra et al. 2023). Tree-search variant of PAIR.
- [`operator/gap/`](operator/gap/) — **GAP** (Graph of
  Attacks with Pruning, Bagdasaryan et al. 2025, EMNLP-Industry). Successor
  to TAP that shares insights from pruned branches across the whole graph.
- [`operator/crescendo/`](operator/crescendo/) —
  **Crescendo** (Russinovich et al. 2024). Multi-turn benign-to-escalation
  conversation rather than single-shot prompts.

The cross-pass loop layer (`run_loop`, `warden-state.json`) extends PAIR
toward a self-bootstrapping mini-corpus: passes accumulate exhausted
angles and verified solves, so subsequent passes only burn compute on
unsolved levels and avoid repeating angles that already failed.

## 2025–2026 landscape update

The field has matured rapidly toward **multi-turn / agentic** attacks,
**graph-based search**, **RL-driven trajectory optimization**, and
**production-grade open-source frameworks**. Linear PAIR + basic TAP is now
considered entry-level; this harness has caught up by adding GAP, Crescendo,
and a DeepTeam-inspired probe/seed extension.

### Open-source frameworks (where most security teams actually live)

- **[DeepTeam](https://github.com/confident-ai/deepteam)** (Confident AI,
  2025) — the breakout open-source LLM/agent red-teaming framework.
  Single-turn + advanced multi-turn attacks (Linear, Tree,
  CrescendoJailbreaking). Built-in mappings to OWASP Top 10 for LLMs 2025
  and OWASP Agentic Systems & Infrastructure (ASI) Top 10 2026.
- **[Garak](https://github.com/leondz/garak)** (Leon Derczynski / NVIDIA) —
  modular vulnerability scanner. Probe / detector library; like `nmap` for
  LLM vulns. Actively maintained.
- **[PyRIT](https://github.com/Azure/PyRIT)** (Microsoft) — added the **AI
  Red Teaming Agent** (April 2025), native Crescendo, multi-modal support.
- **[Promptfoo](https://www.promptfoo.dev/)** — `redteam` mode, multi-modal
  attacks, OWASP Agentic AI Top 10 plugins, Hydra-style multi-turn
  orchestration (2025–2026 releases).

### Academic algorithms more sophisticated than PAIR

- **TAP** (Tree of Attacks with Pruning, Mehrotra et al. 2023) — branching
  + pruning. ~5–10× more efficient than PAIR.
  Implemented at [`tap/tap.py`](operator/tap/tap.py).
- **GAP** (Graph of Attacks with Pruning, Bagdasaryan et al. 2025,
  EMNLP-Industry) — direct successor to TAP. Replaces independent trees
  with a *shared graph* so insights from pruned branches transfer to
  surviving siblings on the next layer. Higher success rate + better
  stealth than TAP. Implemented at
  [`gap/gap.py`](operator/gap/gap.py).
- **Crescendo** (Russinovich, Salem, Eldan 2024) — multi-turn attack that
  starts benign and escalates one step per turn; the warden's prior
  compliance becomes leverage on the next turn. Implemented at
  [`crescendo/crescendo.py`](operator/crescendo/crescendo.py).
- **APRT** (Wang et al. 2025, COLING) — Automated Progressive Red Teaming.
  Hides the actual extraction inside a multi-step request whose individual
  sub-asks are benign. Seed patterns added to the corpus via
  [`deepteam_extras.py`](operator/deepteam_extras.py).
- **STAR** (Strategy-driven Automatic Jailbreak Red-teaming, ICLR 2026) —
  moves exploration into the model's latent activation space to avoid
  "strategy collapse." Not implemented here (white-box requirement).
- **AutoAdv** (2025) — training-free multi-turn framework, ~95% ASR in 6
  turns on Llama-3.1-8B via pattern manager + temperature manager + two-
  phase rewriting. Conceptually similar to our Crescendo module but with
  more aggressive temperature scheduling.
- **Automatic LLM Red Teaming** (arXiv 2508.04451, Aug 2025) — frames
  red-teaming as dialogue trajectory optimization with hierarchical RL.
  Solves sparse-reward / long-horizon problems that linear PAIR struggles
  with.
- **GCG** (Greedy Coordinate Gradient, Zou et al. 2023) — white-box,
  gradient-based, produces those weird `"describe ; ! !! !!"` adversarial
  suffixes. Needs an open-weight surrogate model. Doesn't transfer well to
  current aligned models, but the technique is foundational and the
  AdvBench corpus comes from this paper.
- **AutoDAN** (Liu et al. 2023) — genetic algorithm: population of prompts
  evolved via mutation and crossover. Fitness from target-model responses.

### Fine-tuned attacker models

- **MasterKey** (Deng et al. 2024) — fine-tuned a model specifically to
  produce jailbreaks. Doesn't refuse, doesn't hedge.
- **AdvPrompter** (Paulus et al. 2024) — single forward pass produces an
  attack wrapper. PAIR-quality results without the iteration cost.
- **Abliterated models** — community fine-tunes (typically Llama-3
  derivatives) with the refusal direction ablated from the residual
  stream. Widely used as attacker LLMs in research because they don't
  refuse to generate edge-case attacks. This project's Sonnet 4.6 attacker
  *does* sometimes hedge.

### Knowledge bases and benchmarks

- **HarmBench** / **AdvBench** / **JailbreakBench** — standardized
  harmful-behavior corpora for benchmarking. ~500–1000 reference behaviors
  each.
- **Vector DBs of historical attacks** — production tools (Lakera,
  HiddenLayer) maintain proprietary corpora of every attack ever observed
  against their guard products. New target → semantic search for the
  closest known-good attack → seed PAIR with it.
- **Lakera's Gandalf playthrough threads** — thousands of community-posted
  solves on Twitter/Reddit are effectively a public corpus for the exact
  game this lab clones.

## What's now wired into this project's harness

| Pattern                          | Where it lives                                           | Inspired by                                                                                          |
| -------------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| PAIR feedback loop               | `prior` list in `run_level`, `AttackerBrief.render`      | Chao et al. 2023                                                                                     |
| LLM-based judge                  | `judge_response()` with adaptive thinking                | PyRIT scoring engines                                                                                |
| Defense fingerprinting           | `fingerprint_level()`, `_FINGERPRINT_PROBES`             | Garak `probes/leakreplay`, `promptinject`, `encoding`, `dan`, `goodside`                             |
| Discover → exploit workflow      | `run_loop(blind=True)`                                   | Garak's probe→detector pipeline; PyRIT scoring engines; DeepTeam discovery phase                     |
| Cross-pass corpus                | `warden-corpus.json` + auto-grow in `run_loop`           | Lakera-style historical-attack vector DB                                                             |
| Curated persona-override seeds   | `_PLINY_L6` (5 patterns)                                 | elder-plinius/L1B3RT4S, G0DM0D3                                                                      |
| Curated semantic-completion seeds| `_PLINY_L8` (3 patterns)                                 | Pliny semantic-completion frames                                                                     |
| Input obfuscation                | `parseltongue.py`                                        | elder-plinius/G0DM0D3 `parseltongue.ts`                                                              |
| **Tree search (TAP)**            | `tap/tap.py`                                             | Mehrotra et al. 2023                                                                                 |
| **Graph search (GAP)**           | `gap/gap.py`                                             | Bagdasaryan et al. 2025 (EMNLP-Industry)                                                             |
| **Multi-turn (Crescendo)**       | `crescendo/crescendo.py`                                 | Russinovich et al. 2024; DeepTeam CrescendoJailbreaking                                              |
| **DeepTeam fingerprint probes**  | `DEEPTEAM_FINGERPRINT_PROBES` in `deepteam_extras.py`    | DeepTeam (Crescendo, agentic tool-misuse, APRT, Goodside confused-deputy)                            |
| **DeepTeam corpus seeds**        | `seed_corpus_with_deepteam_attacks` (L4/L5/L7/L8)        | OWASP ASI 2026, APRT, DeepTeam Crescendo                                                             |

What's still missing relative to production:

- **Fine-tuned attacker model** — using general Sonnet 4.6 means hedging
  on edge-case attacks. An abliterated open-weight attacker would be more
  aggressive.
- **Multi-modal probes** — text only. No image / audio / Unicode-tag
  smuggling.
- **RL trajectory optimization** — the Crescendo module follows a fixed
  arc shape rather than learning the optimal escalation per target.
- **Ensemble** — single attacker model. Production tools fan out across
  multiple attackers and pick the best result.

## Practical takeaway for the workshop

For an 8-level CTF aimed at small-business owners in 90 minutes, simpler
is right — the notebook's PAIR loop teaches the *pattern* (LLM-vs-LLM
iteration), which is the conceptual leap. TAP / GAP / Crescendo are
optional add-ons for the levels where PAIR plateaus (L5–L8) and for
demos where the audience wants to see *why* multi-turn or graph search
genuinely matters.

The cheapest demonstration arc:

1. **PAIR baseline.** Run `run_loop()` from the notebook. L1–L6 pass,
   L7 ~50/50, L8 fails.
2. **TAP on L7.** `python tap/tap.py 7` — show how branching exploration
   converges where PAIR plateaued.
3. **GAP on L8.** `python gap/gap.py 8` — show the StrategyMemory
   passing insights between pruned branches.
4. **Crescendo on L8.** `python crescendo/crescendo.py 8 --turns 7` —
   show how multi-turn commitment defeats the canned-refusal trap when
   single-shot mechanical attacks can't.

Each step takes under 60 seconds at workshop budget and produces
reviewable JSONL logs side-by-side.

## Glossary

- **PAIR** — Prompt Automatic Iterative Refinement. Attacker LLM + judge
  LLM in a feedback loop. The pattern this notebook implements.
- **TAP** — Tree of Attacks with Pruning. Branching variant of PAIR.
- **GAP** — Graph of Attacks with Pruning. 2025 successor to TAP that
  shares insights from pruned branches across the graph.
- **Crescendo** — multi-turn attack that starts benign and gradually
  escalates; each turn references the target's prior compliance.
- **CrescendoJailbreaking** — DeepTeam / PyRIT 2025 productionization of
  the Crescendo pattern.
- **APRT** — Automated Progressive Red Teaming (Wang et al. 2025).
  Hides the extraction inside a multi-step request whose sub-asks are
  individually benign.
- **GCG** — Greedy Coordinate Gradient. White-box gradient-optimized
  adversarial-suffix attack.
- **Abliteration** — technique that ablates the "refusal direction" from
  an open-weight model's residual stream, producing a model that won't
  refuse.
- **Defense fingerprinting** — probing a target with known signatures to
  identify which guardrails are active before launching real attacks.
- **AdvBench / HarmBench / JailbreakBench** — standard public benchmarks
  for evaluating jailbreak attacks.
- **Adversarial suffix** — a string of seemingly-random tokens, optimized
  to flip an aligned model into compliance when appended to a harmful
  request. The hallmark output of GCG-style attacks.
- **Confused deputy** — an attack class (Goodside, etc.) where the
  target is asked to act as a proxy for a different (legitimate-sounding)
  authority, bypassing the persona/role lock.
