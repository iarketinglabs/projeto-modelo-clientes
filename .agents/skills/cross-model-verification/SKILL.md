---
name: cross-model-verification
description: Run cross-model verification to detect bias, vendor lock-in and critical divergences by executing the same prompts through multiple LLMs. Use whenever the user asks for model comparison, bias detection, vendor lock-in analysis, LLM divergence checks, shadow mode setup, multi-model evaluation, or wants to compare outputs from GPT, Claude, DeepSeek, Kimi or GLM before production decisions.
---

# Cross-Model Verification

Compare the same prompt across two or more LLMs to surface bias, vendor lock-in risk and dangerous divergences before they reach production. This skill treats cross-model verification as a risk-detection system, not a truth oracle: agreement between models is a stability signal, not a proof of correctness.

## When to use this skill

- You are choosing between models for a high-stakes workflow.
- You need to detect bias across languages, demographics or domains.
- You want to reduce vendor lock-in by validating that another model can handle the same task.
- You are setting up shadow mode, A/B testing or a gated review pipeline.
- A production incident suggests one model behaves differently from another.
- You need metrics and a report to justify a model change or fallback strategy.

## Core principles

1. **Freeze the experiment.** Pin exact model IDs, prompts, parameters, tools and schemas. Comparing "GPT-5.4" against "Claude" is not a fair experiment; compare `gpt-5.4-XXXX` against `claude-sonnet-4-6-XXXX`.
2. **Compare at the business level.** A marketing post can diverge in style safely; a lead classification, price, deadline or compliance decision cannot. Compare structured fields, downstream actions and safety flags, not just raw text.
3. **Standardize outputs.** Use JSON Schema / structured outputs whenever possible so divergence is measurable. Record `finish_reason`, refusals and truncation alongside the output.
4. **The judge cannot be the accused.** Separate generator and judge families to reduce self-preference bias. Use multiple judges and swap candidate order.
5. **Aggregate by slice.** Averages hide problems. Report metrics by domain, risk, language, format and channel.
6. **Escalate selectively.** Send only critical divergences to human review; route benign differences to logging.

## Recommended model IDs

Use pinned snapshots, not family names. Update these references when newer snapshots become available:

- OpenAI: `gpt-5.4`, `gpt-5.5` (or the latest pinned snapshot)
- Anthropic: `claude-sonnet-4-6` (Claude IDs are already snapshots)
- DeepSeek: `deepseek-v3.2`, `deepseek-v4-preview`
- Kimi: `kimi-k2.6`
- Zhipu: `glm-5`, `glm-5.1`

## Workflow

```text
Entrada -> Normalização de prompt/schema -> Modelo A
                                       -> Modelo B
                                       -> Modelo C opcional

Saídas -> Checks determinísticos
      -> Comparação pareada / júri de juízes
      -> Métricas por slice
      -> Regras de criticidade
      -> [seguir] | [shadow log] | [revisão humana] | [bloquear]
```

### Step 1: Freeze inputs

- Pin model IDs and prompt version.
- Fix temperature (usually `0.0`), max tokens, tools and schema.
- Build a dataset with four buckets: **golden set**, **production slice**, **edge set** and **bias set**.
- Stratify slices by domain, risk (low/medium/high), language, format, channel and ambiguity type.

### Step 2: Run models

- Run each case through all target models using the same prompt and parameters.
- Capture raw text, structured output, `finish_reason`, refusal flags, latency and token usage.
- For implementation details, read `references/python-script-template.md`.

### Step 3: Apply deterministic checks first

Run these before any LLM-as-a-judge call:

- Schema valid and complete?
- Refusal detected?
- Output truncated?
- Exact or normalized match on key fields?
- Business rules violated (price, deadline, label, action)?
- Regex or validation matches reference?

### Step 4: Comparative judgment

For open-ended outputs, use pairwise classification instead of free-form scoring:

- Are the outputs semantically equivalent?
- Which output better satisfies criterion X?
- Does the divergence change a downstream action?
- Is there safety, compliance or bias risk?

Reduce judge bias:

- Swap candidate order and aggregate.
- Use a panel of judges from different families.
- Never let a model judge outputs from its own family against a competitor.

### Step 5: Aggregate by slice

Group results by:

- Domain: copy, support, extraction, strategy, code, legal/compliance
- Risk level: low, medium, high
- Language: pt-BR, en-US, bilingual
- Format: free text, JSON, tool use
- Channel: internal, customer-facing, automation
- Ambiguity: clear, ambiguous, adversarial, incomplete

### Step 6: Apply criticality rules

Route each comparison:

- **Green queue**: low risk, no material divergence, log only.
- **Yellow queue**: relevant but reversible divergence, shadow monitor or secondary routing.
- **Red queue**: changes a decision, external action, compliance, safety, money or customer message; send to human review or block.

For detailed criteria, read `references/criticality-criteria.md`.

### Step 7: Feed back the dataset

Add confirmed divergences to the golden set, bias set or edge set. Document architecture decisions in the project knowledge base with hypothesis, metric, result, decision and owner.

## Metrics

Track these metrics overall and per slice:

| Metric | Definition |
|---|---|
| Structural failure rate | Invalid schema, truncation, timeout or refusal |
| Agreement rate | Same label or semantic equivalence / N |
| Semantic divergence rate | Judged not equivalent / N |
| Critical divergence rate | High-risk cases with material divergence / N |
| Consensus error rate | All models agree but answer is wrong / N |
| Judge order stability | Verdict unchanged when candidate order is swapped |
| Slice gap | Metric(slice A) − Metric(slice B) |
| Win/tie/loss | Pairwise outcome after judge aggregation |

For categorical labels, prefer **Cohen's kappa** over raw agreement to correct for chance. For multiple judges or human raters, use **Krippendorff's alpha**.

Use paired bootstrap or equivalent confidence intervals before declaring one variant better than another. Do not change provider or prompt based on a 0.7-point average difference.

## Confidence gap proxy

When logprobs or calibrated scores are unavailable, estimate uncertainty by combining:

```text
CGP_i = z(1 - self_consistency_i)
      + z(inter_model_disagreement_i)
      + z(1 - judge_consensus_i)
```

Treat vendor confidence scores as extra features, not single sources of truth.

## Shadow mode and gated review

- **Shadow mode**: run the secondary model silently on a sample of traffic and log divergence metrics without affecting users.
- **Gated review**: route high-risk, high-uncertainty or critically divergent cases to a human reviewer or external judge before any irreversible action.

Start every production rollout in shadow mode. Only promote a model swap after slice-level metrics stabilize and critical divergences are resolved.

## Bias detection

Use established benchmarks as a skeleton, then localize them:

- **BBQ** for biased question answering
- **StereoSet** for stereotypical associations
- **BOLD** for open-ended generation bias

For pt-BR and marketing contexts, build a localized bias set covering professions, regions, accents, education, gender, race, religion and social context. Translation alone distorts bias; the problem is culturally situated.

For benchmark pointers and localization tips, read `references/bias-benchmarks.md`.

## Tooling recommendations

- **LangSmith**: datasets, experiments, offline/online evals, production traces.
- **Arize Phoenix**: observability, multi-provider comparison, human annotations.
- **Custom scripts**: provider adapters, slicing, bootstrap scoring, criticality tagging.

Avoid building new long-term dependencies on OpenAI's deprecated third-party Evals surface.

## Cost and latency optimization

Cross-model verification is expensive by design. Reduce cost with:

- Prompt caching where available.
- Batch APIs for offline evaluation.
- Shared judge rubrics and reusable system prompts.
- Small smoke tests (300–500 stratified cases) before large baselines (~1,000+ cases).

## Deliverables

At the end of a verification run, produce:

1. A divergence report. Use `references/report-template.md`.
2. A criticality decision log. Use `references/criticality-criteria.md`.
3. Updated test datasets with new confirmed cases.
4. A release gate checklist. Use `references/checklist.md`.

## Checklist before release

Read `references/checklist.md` for the full gate. The minimum checks are:

- Model IDs and prompt version are pinned.
- Success is defined by measurable criteria, not "looks better".
- Tasks are separated by risk level.
- Comparison includes actions and structured fields, not just text.
- Dataset has golden, production, edge and bias buckets.
- Slices cover pt-BR, bilingual, copy, support, extraction, automation and code.
- Outputs record stop reason, refusal, truncation, latency and tokens.
- Judges use swapped order and different families.
- Critical cases go to human review or block.
- Rollout starts in shadow mode.
- Confirmed divergences become new test cases.

## Limitations

- Cross-model verification measures disagreement and risk, not absolute truth.
- Models can confidently agree on a wrong answer.
- LLM judges have position bias, self-preference bias and style bias; calibrate them against humans on critical subsets.
- Vendor capabilities are similar but not identical; use real multi-adapter harnesses, not abstractions that hide important differences.
