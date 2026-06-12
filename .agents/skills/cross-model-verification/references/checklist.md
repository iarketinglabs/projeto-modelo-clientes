# Release Gate Checklist for Cross-Model Verification

Use this checklist before promoting a model change, prompt change or workflow change that affects LLM outputs.

## Experiment setup

- [ ] Pin exact model IDs and the prompt / workflow version.
- [ ] Define success in measurable terms, not "looks better".
- [ ] Fix temperature, max tokens, tools and schema for all models.
- [ ] Document base URLs, API versions and adapter versions.

## Dataset

- [ ] Dataset has a golden set with known answers or rules.
- [ ] Dataset has a production slice with real, anonymized traffic.
- [ ] Dataset has an edge set with previously seen failures.
- [ ] Dataset has a bias set designed to expose asymmetries.
- [ ] Slices cover pt-BR, bilingual, copy, support, extraction, automation and code.
- [ ] Cases are stratified by domain, risk, language, format, channel and ambiguity.

## Execution

- [ ] All models receive the same prompt and parameters.
- [ ] Outputs record `finish_reason` / `stop_reason`.
- [ ] Refusals are detected and logged.
- [ ] Truncation is detected and logged.
- [ ] Latency and token usage are recorded.
- [ ] Tool-call traces are captured when applicable.

## Judgment

- [ ] Deterministic checks run before LLM-as-a-judge.
- [ ] Judges compare structured fields and downstream actions, not only text.
- [ ] Candidate order is swapped and results are aggregated.
- [ ] Judge panel includes models from different families.
- [ ] No model judges outputs from its own family against a competitor.

## Metrics and review

- [ ] Metrics are reported overall and by slice.
- [ ] Confidence intervals or paired bootstrap is used for comparisons.
- [ ] Critical divergence rate is below the agreed threshold.
- [ ] No sensitive slice shows a meaningful gap.
- [ ] Consensus errors are reviewed manually.

## Release decision

- [ ] Rollout starts in shadow mode.
- [ ] Critical cases route to human review or block.
- [ ] Yellow-queue cases have a monitoring plan.
- [ ] Confirmed divergences become new test cases.
- [ ] Decision is documented in the knowledge base with hypothesis, metric, result, decision and owner.
