---
name: ai-evals
description: Use this skill whenever you need to design, implement or review AI evaluations — LLM-as-Judge, evaluation rubrics, deterministic validation, agent output quality, hallucination detection, faithfulness/groundedness checks, RAG metrics, regression tests, or CI gates for prompts and agents. It gives you a hybrid workflow (deterministic checks first, rubric-based LLM judges second, human calibration third) with concrete examples for DeepEval, Phoenix, Ragas and LangSmith. Trigger for building eval suites, choosing metrics, writing rubrics, validating JSON/Markdown outputs, detecting hallucinations, comparing model/prompt versions, setting pass/fail gates, or improving agent quality.
---

# AI Evals

## Overview

AI outputs need both cheap, exact checks and expensive, semantic judgment. Relying on only one side gives you either false confidence or unnecessary cost.

Use a **three-layer hybrid stack**:

```txt
Traces reais + dataset gold
        ↓
Validadores determinísticos
(schema, regex, enums, ranges, business rules)
        ↓
LLM-as-Judge com rubricas
(correctness, faithfulness, relevance, tone, policy)
        ↓
Amostra humana para calibração
(disagreement review, few-shot, judge alignment)
        ↓
CI/CD gates + dashboard + monitoramento online
```

Why this order: structure is cheap to verify and unambiguous. Semantic quality is expensive and noisy. Human calibration keeps the judge honest over time.

## When to Use

Use this skill when you are:

- Building an eval suite for a prompt, agent, RAG or skill.
- Choosing metrics for output quality.
- Writing or reviewing an LLM-as-Judge rubric.
- Validating JSON, Markdown or text output contracts.
- Detecting hallucination, faithlessness or policy violations.
- Comparing two prompt/model/policy variants.
- Setting CI gates for releases.
- Investigating a regression in agent behavior.

## The Eval Workflow

### 1. Define the output contract

Every skill, agent or prompt must declare what valid output looks like:

- JSON schema with required fields, enums and ranges.
- Markdown headings or structure expected.
- Text constraints (length, tone, required clauses).

Version this contract with the code. It is the foundation of deterministic validation.

### 2. Build a slice-balanced dataset

Aim for at least five slices per capability:

- Happy path
- Boundary condition
- Ambiguous input
- Adversarial or known-failure case
- Real production trace

Mix real data, historical data, human-curated data and synthetic data. Start small and grow based on failure modes you actually see.

### 3. Run deterministic validators first

Check everything a parser or rule can check:

- JSON parses and matches schema.
- Required fields are present.
- Enums, ranges and regex constraints hold.
- Business rules are satisfied.
- Tool-call sequence matches expectation.

These are hard gates. If they fail, there is no point in running the expensive judge.

### 4. Apply LLM-as-Judge with rubrics

For semantic dimensions, use a dedicated judge per metric. A good rubric has:

- One narrow criterion per metric.
- Explicit 0-4 scale with clear boundaries.
- Consistent terms between schema and prompt.
- Structured output: `score`, `label`, `reason`, `evidence`, `violations`.

See `references/rubric-template.md` for a copy-paste template.

### 5. Calibrate against humans

The judge is a model, not a source of truth. Before turning semantic scores into hard gates:

- Label a representative sample with humans.
- Measure judge-human agreement.
- Review disagreements and update the rubric or few-shots.
- Version the rubric and calibration date.

Target high agreement for objective categories; keep subjective metrics as soft alerts until stable.

### 6. Wire to CI and dashboards

- PR smoke suite: deterministic checks + small semantic sample.
- Full suite before release: all metrics, groundedness, baseline comparison.
- Hard fail on format, required fields and business rules.
- Soft fail / review on semantic metrics until calibrated.
- Track regressions against an official baseline.

See `references/ci-gates.md` for the full CI design.

## Metrics

Pick one metric per question. Do not bundle factual accuracy, tone, completeness and safety into a single score.

See `references/metrics-dimensions.md` for the complete map of dimensions, ground truth and preferred validators.

Quick reference:

| Use when you want to check... | Start with |
| --- | --- |
| JSON/schema/enum/range | `jsonschema`, custom Python validator |
| Exact or near-exact answer | Exact match, string similarity |
| Factual correctness vs reference | DeepEval `GEval` or Ragas correctness |
| RAG groundedness | DeepEval `FaithfulnessMetric` / Ragas faithfulness |
| Hallucination vs canonical context | DeepEval `HallucinationMetric` |
| Relevance to user intent | GEval relevance rubric |
| Agent tool/trajectory quality | Trajectory match + goal-completion rubric |
| Policy/safety | Dedicated critic rubric |

## Tools

You do not have to pick just one. Most teams end up with a harness plus an observability layer.

### Recommended default for Atomica

- **DeepEval** as the code-first harness inside the repo.
- **Phoenix** for traces, datasets, experiments and dashboards.
- **Ragas** when the problem is RAG, groundedness, citation accuracy, tool-calling or pt-BR adaptation.

### Alternative

- **LangSmith** if the project is already centered on LangChain/LangGraph and human correction → few-shot → judge alignment is the main workflow.

See `references/tools-comparison.md` for strengths, fit and cautions of each tool.

## Deterministic Validation Example

```python
import json
from jsonschema import Draft202012Validator

OFFER_SCHEMA = {
    "type": "object",
    "required": ["customer_id", "channel", "discount_pct", "message"],
    "properties": {
        "customer_id": {"type": "string", "minLength": 1},
        "channel": {"type": "string", "enum": ["email", "whatsapp", "sms"]},
        "discount_pct": {"type": "number", "minimum": 0, "maximum": 100},
        "manager_approved": {"type": "boolean"},
        "message": {"type": "string", "minLength": 1},
    },
    "additionalProperties": False,
}

def validate_offer_output(raw_output: str) -> tuple[bool, list[str], dict | None]:
    try:
        payload = json.loads(raw_output)
    except json.JSONDecodeError as exc:
        return False, [f"JSON inválido: {exc.msg}"], None

    validator = Draft202012Validator(OFFER_SCHEMA)
    errors = []

    for err in sorted(validator.iter_errors(payload), key=lambda e: list(e.path)):
        path = "/".join(str(p) for p in err.path) or "$"
        errors.append(f"{path}: {err.message}")

    discount = payload.get("discount_pct", 0)
    if discount > 20 and payload.get("manager_approved") is not True:
        errors.append("Regra de negócio: desconto > 20% exige manager_approved=true.")

    if payload.get("channel") == "whatsapp" and len(payload.get("message", "")) > 1000:
        errors.append("Regra de negócio: WhatsApp não pode passar de 1000 caracteres.")

    return len(errors) == 0, errors, payload
```

If validation fails, fail hard. Only invoke the LLM judge after the deterministic layer passes.

## LLM-as-Judge Example

```python
import os
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, SingleTurnParams

EVAL_MODEL = os.getenv("EVAL_MODEL", "gpt-5.4-mini")

test_case = LLMTestCase(
    input="Qual é a política de cancelamento?",
    actual_output="O cliente pode cancelar em até 30 dias com reembolso integral.",
    expected_output="O cliente pode cancelar em até 7 dias com reembolso integral."
)

correctness_metric = GEval(
    name="correctness",
    criteria="Determine se actual_output está factual e semanticamente correto com base em expected_output.",
    evaluation_steps=[
        "Compare os fatos centrais de actual_output com expected_output.",
        "Penalize contradições factuais de forma pesada.",
        "Penalize omissão de fatos obrigatórios.",
        "Ignore diferenças meramente estilísticas."
    ],
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.EXPECTED_OUTPUT,
    ],
    threshold=0.8,
    model=EVAL_MODEL,
)

correctness_metric.measure(test_case)
print("score:", correctness_metric.score)
print("reason:", correctness_metric.reason)
```

For RAG faithfulness vs hallucination examples, see `references/deepeval-example.md`.

## Common Pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| Using LLM to check JSON validity | Wastes money and adds noise | Use `jsonschema`, regex, parsers |
| One metric for many criteria | Scores become unactionable | Split into one metric per dimension |
| Rubric with vague boundaries | Judges drift and disagree | Use explicit 0-4 scale with concrete anchors |
| Same model as generator and judge | Self-preference bias | Use a different, capable judge model |
| Skipping human calibration | Semantic gates are untrustworthy | Label samples, measure agreement, iterate |
| No baseline | Cannot detect regression | Pin an official prompt/model/dataset version |
| Pairwise without randomization | Position bias | Randomize candidate order |

## Edge Cases

- **Creativity**: prefer pairwise comparison or instance-specific rubrics, with human audit by sample.
- **Long outputs**: split evaluation by section (coverage, groundedness, structure, citation).
- **Multi-turn agents**: evaluate thread, goal completion, trajectory and tool use, not just the final response.
- **pt-BR outputs**: adapt metric prompts/few-shots or validate that English judge prompts still align.

## Verification Checklist

Before declaring an eval ready:

- [ ] Output contract is versioned and deterministic validators exist.
- [ ] Dataset has at least five slices.
- [ ] Each metric covers one criterion only.
- [ ] Every semantic metric has an explicit rubric with structured output.
- [ ] Judge model differs from generator model when possible.
- [ ] Human calibration sample exists for semantic gates.
- [ ] CI separates hard gates from soft/review gates.
- [ ] Official baseline is pinned and regression logic exists.
- [ ] Rubrics, thresholds, slices and calibration date are documented.

For the full QA checklist, see `references/qa-checklist.md`.

## References

- `references/metrics-dimensions.md` — Mapa completo de dimensões, ground truth e validadores.
- `references/rubric-template.md` — Template de rubrica LLM-as-Judge.
- `references/deepeval-example.md` — Exemplos DeepEval: GEval, faithfulness, hallucination, schema validation.
- `references/ci-gates.md` — Design de gates para PR e release.
- `references/tools-comparison.md` — Comparativo de DeepEval, Phoenix, Ragas, LangSmith e OpenAI Evals.
- `references/qa-checklist.md` — Checklist mínimo de QA para evals na Atomica.
