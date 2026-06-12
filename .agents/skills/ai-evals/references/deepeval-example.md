# Exemplos DeepEval

Use estes exemplos como ponto de partida para implementar evals code-first com DeepEval. Versione criteria, evaluation_steps e thresholds junto do código.

## Correctness com GEval (reference-based)

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

## RAG: Faithfulness vs Hallucination

```python
from deepeval.metrics import FaithfulnessMetric, HallucinationMetric
from deepeval.test_case import LLMTestCase

# Caso RAG: groundedness / faithfulness
rag_case = LLMTestCase(
    input="Qual é a política de reembolso?",
    actual_output="Oferecemos reembolso integral em até 30 dias.",
    retrieval_context=[
        "Política oficial: cancelamentos em até 7 dias têm reembolso integral.",
        "Após 7 dias, só trocas por defeito."
    ],
)

faithfulness = FaithfulnessMetric(threshold=0.9)
faithfulness.measure(rag_case)
print("faithfulness_score:", faithfulness.score)
print("faithfulness_reason:", faithfulness.reason)

# Caso não-RAG: hallucination contra contexto canônico
non_rag_case = LLMTestCase(
    input="Quando o contrato vence?",
    actual_output="O contrato vence em 31/12/2027.",
    context=["O contrato vence em 31/12/2026."]
)

hallucination = HallucinationMetric(threshold=0.5)
hallucination.measure(non_rag_case)
print("hallucination_score:", hallucination.score)
print("hallucination_reason:", hallucination.reason)
```

## Validação determinística de JSON/schema + regras de negócio

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
        errors.append(
            "Regra de negócio: desconto acima de 20% exige manager_approved=true."
        )

    if payload.get("channel") == "whatsapp" and len(payload.get("message", "")) > 1000:
        errors.append(
            "Regra de negócio: mensagem de WhatsApp não pode passar de 1000 caracteres."
        )

    return len(errors) == 0, errors, payload
```

## Estratégia de execução

1. Rode validadores determinísticos primeiro.
2. Se falharem, hard fail imediato.
3. Só então rode o LLM judge para semântica.
4. Ative `strict_mode=True` só depois de calibrar o juiz contra labels humanos.
