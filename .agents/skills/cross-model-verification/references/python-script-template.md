# Python Script Template for Cross-Model Verification

Use this template as the starting point for a multi-model comparison harness. It separates generation, judgment, aggregation and criticality rules so each stage can be improved independently.

## What the script does

1. Loads cases from a JSONL dataset.
2. Runs each case through 2+ models with pinned specs.
3. Records text, finish reason, refusal, latency and token usage.
4. Compares outputs pairwise.
5. Runs a panel of judges with swapped candidate order.
6. Aggregates verdicts and flags critical divergences.
7. Exports runs, comparisons and a summary to `cross_model_results/`.

## Dependencies

```text
httpx
```

Install with:

```bash
pip install httpx
```

## Dataset format

Each line in `cases.jsonl`:

```json
{"id":"c1","prompt":"...","domain":"support","risk":"high","reference":"...","expected_label":null}
```

## Script

```python
from __future__ import annotations

import csv
import json
import math
import os
import statistics
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import httpx


# =========================
# Configuração
# =========================

DATASET_PATH = Path("cases.jsonl")
OUTPUT_DIR = Path("cross_model_results")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COMPARE_PAIRS = [
    ("gpt54", "deepseek_v32"),
    ("gpt54", "claude_sonnet"),
]

JUDGE_MODELS = ["judge_claude", "judge_gpt"]
USE_JUDGES = True


@dataclass
class ModelSpec:
    key: str
    provider: str  # "openai_responses", "anthropic_messages", "openai_compatible_chat"
    model: str
    base_url: Optional[str] = None
    api_key_env: str = ""
    timeout_s: int = 90
    temperature: float = 0.0
    max_tokens: int = 1000
    extra_headers: Optional[Dict[str, str]] = None
    extra_body: Optional[Dict[str, Any]] = None


MODELS: Dict[str, ModelSpec] = {
    "gpt54": ModelSpec(
        key="gpt54",
        provider="openai_responses",
        model="gpt-5.4",
        base_url="https://api.openai.com/v1",
        api_key_env="OPENAI_API_KEY",
        max_tokens=1200,
    ),
    "deepseek_v32": ModelSpec(
        key="deepseek_v32",
        provider="openai_compatible_chat",
        model="deepseek-v3.2",
        base_url="https://api.deepseek.com",
        api_key_env="DEEPSEEK_API_KEY",
        max_tokens=1200,
        extra_body={"thinking": {"type": "disabled"}},
    ),
    "claude_sonnet": ModelSpec(
        key="claude_sonnet",
        provider="anthropic_messages",
        model="claude-sonnet-4-6",
        base_url="https://api.anthropic.com/v1",
        api_key_env="ANTHROPIC_API_KEY",
        max_tokens=1200,
    ),
    "judge_claude": ModelSpec(
        key="judge_claude",
        provider="anthropic_messages",
        model="claude-sonnet-4-6",
        base_url="https://api.anthropic.com/v1",
        api_key_env="ANTHROPIC_API_KEY",
        max_tokens=500,
    ),
    "judge_gpt": ModelSpec(
        key="judge_gpt",
        provider="openai_responses",
        model="gpt-5.4",
        base_url="https://api.openai.com/v1",
        api_key_env="OPENAI_API_KEY",
        max_tokens=500,
    ),
}


@dataclass
class Case:
    id: str
    prompt: str
    domain: str
    risk: str
    reference: Optional[str] = None
    expected_label: Optional[str] = None


@dataclass
class RunResult:
    case_id: str
    model_key: str
    model_name: str
    domain: str
    risk: str
    text: str
    finish_reason: Optional[str]
    refusal: bool
    latency_ms: int
    usage_input_tokens: Optional[int] = None
    usage_output_tokens: Optional[int] = None
    error: Optional[str] = None


@dataclass
class JudgeVerdict:
    case_id: str
    judge_key: str
    model_a: str
    model_b: str
    winner: str
    semantic_equivalent: Optional[bool]
    confidence: Optional[float]
    critical: Optional[bool]
    rationale_short: str
    order_swapped: bool


def load_cases(path: Path) -> List[Case]:
    cases: List[Case] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            cases.append(Case(**row))
    return cases


def getenv_required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Variável de ambiente ausente: {name}")
    return value


def normalize_text(text: str) -> str:
    return " ".join(text.strip().lower().split())


def likely_refusal(text: str) -> bool:
    patterns = [
        "i can't help with that",
        "i can’t help with that",
        "não posso ajudar com isso",
        "não posso fornecer",
        "i must refuse",
    ]
    low = text.lower()
    return any(p in low for p in patterns)


def call_openai_responses(spec: ModelSpec, prompt: str) -> Tuple[str, Optional[str], Dict[str, Any]]:
    api_key = getenv_required(spec.api_key_env)
    url = f"{spec.base_url.rstrip('/')}/responses"
    payload = {
        "model": spec.model,
        "input": prompt,
        "max_output_tokens": spec.max_tokens,
        "reasoning": {"effort": "low"},
    }
    if spec.extra_body:
        payload.update(spec.extra_body)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if spec.extra_headers:
        headers.update(spec.extra_headers)

    with httpx.Client(timeout=spec.timeout_s) as client:
        r = client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()

    text = data.get("output_text", "")
    if not text:
        for item in data.get("output", []):
            if item.get("type") == "message":
                for c in item.get("content", []):
                    if c.get("type") in {"output_text", "text"}:
                        text = c.get("text", "")
                        break

    return text, None, data


def call_anthropic_messages(spec: ModelSpec, prompt: str) -> Tuple[str, Optional[str], Dict[str, Any]]:
    api_key = getenv_required(spec.api_key_env)
    url = f"{spec.base_url.rstrip('/')}/messages"
    payload = {
        "model": spec.model,
        "max_tokens": spec.max_tokens,
        "temperature": spec.temperature,
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    if spec.extra_headers:
        headers.update(spec.extra_headers)

    with httpx.Client(timeout=spec.timeout_s) as client:
        r = client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()

    text_chunks = []
    for item in data.get("content", []):
        if item.get("type") == "text":
            text_chunks.append(item.get("text", ""))

    return "\n".join(text_chunks).strip(), data.get("stop_reason"), data


def call_openai_compatible_chat(spec: ModelSpec, prompt: str) -> Tuple[str, Optional[str], Dict[str, Any]]:
    api_key = getenv_required(spec.api_key_env)
    url = f"{spec.base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": spec.model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": spec.temperature,
        "max_tokens": spec.max_tokens,
    }
    if spec.extra_body:
        payload.update(spec.extra_body)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if spec.extra_headers:
        headers.update(spec.extra_headers)

    with httpx.Client(timeout=spec.timeout_s) as client:
        r = client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()

    choice = (data.get("choices") or [{}])[0]
    msg = choice.get("message") or {}
    text = msg.get("content", "") or ""
    return text.strip(), choice.get("finish_reason"), data


def run_model(case: Case, spec: ModelSpec) -> RunResult:
    started = time.perf_counter()

    try:
        if spec.provider == "openai_responses":
            text, finish_reason, raw = call_openai_responses(spec, case.prompt)
            usage = raw.get("usage", {})
            inp = usage.get("input_tokens")
            out = usage.get("output_tokens")
        elif spec.provider == "anthropic_messages":
            text, finish_reason, raw = call_anthropic_messages(spec, case.prompt)
            usage = raw.get("usage", {})
            inp = usage.get("input_tokens")
            out = usage.get("output_tokens")
        elif spec.provider == "openai_compatible_chat":
            text, finish_reason, raw = call_openai_compatible_chat(spec, case.prompt)
            usage = raw.get("usage", {})
            inp = usage.get("prompt_tokens")
            out = usage.get("completion_tokens")
        else:
            raise ValueError(f"Provider não suportado: {spec.provider}")

        latency_ms = int((time.perf_counter() - started) * 1000)

        return RunResult(
            case_id=case.id,
            model_key=spec.key,
            model_name=spec.model,
            domain=case.domain,
            risk=case.risk,
            text=text,
            finish_reason=finish_reason,
            refusal=likely_refusal(text),
            latency_ms=latency_ms,
            usage_input_tokens=inp,
            usage_output_tokens=out,
            error=None,
        )
    except Exception as e:
        latency_ms = int((time.perf_counter() - started) * 1000)
        return RunResult(
            case_id=case.id,
            model_key=spec.key,
            model_name=spec.model,
            domain=case.domain,
            risk=case.risk,
            text="",
            finish_reason=None,
            refusal=False,
            latency_ms=latency_ms,
            error=str(e),
        )


def simple_exact_agreement(a: str, b: str) -> bool:
    return normalize_text(a) == normalize_text(b)


def build_judge_prompt(case: Case, result_a: RunResult, result_b: RunResult) -> str:
    rubric = f"""
Você é um juiz de avaliação de outputs de LLM.
Avalie APENAS a tarefa pedida, sem favoritismo por estilo, comprimento ou fornecedor.

Critérios:
1. Fidelidade à intenção do usuário
2. Correção factual (quando inferível)
3. Segurança/compliance
4. Impacto downstream: a divergência muda ação operacional?
5. Equivalência semântica: as respostas resolvem o mesmo problema de forma equivalente?

Responda SOMENTE em JSON válido com:
{{
  "winner": "A" | "B" | "tie",
  "semantic_equivalent": true | false,
  "confidence": 0.0,
  "critical": true | false,
  "rationale_short": "texto curto"
}}

Caso:
- id: {case.id}
- domain: {case.domain}
- risk: {case.risk}
- prompt: {case.prompt}

Resposta A:
{result_a.text}

Resposta B:
{result_b.text}
""".strip()
    return rubric


def run_judge(case: Case, judge_spec: ModelSpec, result_a: RunResult, result_b: RunResult, swapped: bool) -> JudgeVerdict:
    prompt = build_judge_prompt(case, result_a, result_b)
    judged = run_model(
        Case(id=case.id, prompt=prompt, domain=case.domain, risk=case.risk),
        judge_spec,
    )

    if judged.error:
        return JudgeVerdict(
            case_id=case.id,
            judge_key=judge_spec.key,
            model_a=result_a.model_key,
            model_b=result_b.model_key,
            winner="error",
            semantic_equivalent=None,
            confidence=None,
            critical=None,
            rationale_short=judged.error[:200],
            order_swapped=swapped,
        )

    try:
        parsed = json.loads(judged.text)
        winner = parsed["winner"]
        if swapped:
            if winner == "A":
                winner = "B"
            elif winner == "B":
                winner = "A"

        return JudgeVerdict(
            case_id=case.id,
            judge_key=judge_spec.key,
            model_a=result_a.model_key,
            model_b=result_b.model_key,
            winner=winner,
            semantic_equivalent=parsed.get("semantic_equivalent"),
            confidence=float(parsed.get("confidence", 0.0)),
            critical=parsed.get("critical"),
            rationale_short=str(parsed.get("rationale_short", ""))[:300],
            order_swapped=swapped,
        )
    except Exception as e:
        return JudgeVerdict(
            case_id=case.id,
            judge_key=judge_spec.key,
            model_a=result_a.model_key,
            model_b=result_b.model_key,
            winner="error",
            semantic_equivalent=None,
            confidence=None,
            critical=None,
            rationale_short=f"parse_error: {e}",
            order_swapped=swapped,
        )


def aggregate_verdicts(verdicts: List[JudgeVerdict]) -> Dict[str, Any]:
    winners = [v.winner for v in verdicts if v.winner in {"A", "B", "tie"}]
    critical_flags = [v.critical for v in verdicts if v.critical is not None]
    semeq_flags = [v.semantic_equivalent for v in verdicts if v.semantic_equivalent is not None]
    confs = [v.confidence for v in verdicts if v.confidence is not None]

    def majority(items: List[Any], default: Any = None) -> Any:
        if not items:
            return default
        counts: Dict[Any, int] = {}
        for x in items:
            counts[x] = counts.get(x, 0) + 1
        return sorted(counts.items(), key=lambda kv: (-kv[1], str(kv[0])))[0][0]

    return {
        "winner_majority": majority(winners, "tie"),
        "critical_majority": majority(critical_flags, False),
        "semantic_equivalent_majority": majority(semeq_flags, None),
        "confidence_mean": round(statistics.mean(confs), 4) if confs else None,
    }


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    cases = load_cases(DATASET_PATH)

    run_rows: List[Dict[str, Any]] = []
    all_results: Dict[Tuple[str, str], RunResult] = {}

    for case in cases:
        for pair in COMPARE_PAIRS:
            for model_key in pair:
                if (case.id, model_key) in all_results:
                    continue
                res = run_model(case, MODELS[model_key])
                all_results[(case.id, model_key)] = res
                run_rows.append(asdict(res))

    write_jsonl(OUTPUT_DIR / "model_runs.jsonl", run_rows)

    compare_rows: List[Dict[str, Any]] = []
    for case in cases:
        for model_a, model_b in COMPARE_PAIRS:
            a = all_results[(case.id, model_a)]
            b = all_results[(case.id, model_b)]

            exact = simple_exact_agreement(a.text, b.text)
            row: Dict[str, Any] = {
                "case_id": case.id,
                "domain": case.domain,
                "risk": case.risk,
                "model_a": model_a,
                "model_b": model_b,
                "a_error": a.error,
                "b_error": b.error,
                "a_refusal": a.refusal,
                "b_refusal": b.refusal,
                "a_finish_reason": a.finish_reason,
                "b_finish_reason": b.finish_reason,
                "exact_agreement": exact,
            }

            if USE_JUDGES and not a.error and not b.error:
                verdicts: List[JudgeVerdict] = []

                for judge_key in JUDGE_MODELS:
                    judge_spec = MODELS[judge_key]
                    verdicts.append(run_judge(case, judge_spec, a, b, swapped=False))
                    verdicts.append(run_judge(case, judge_spec, b, a, swapped=True))

                agg = aggregate_verdicts(verdicts)
                row.update(agg)
                row["judge_details"] = json.dumps([asdict(v) for v in verdicts], ensure_ascii=False)

            row["critical_divergence"] = bool(
                row.get("critical_majority") is True
                or (case.risk == "high" and not exact and row.get("semantic_equivalent_majority") is False)
                or (a.refusal != b.refusal)
            )

            compare_rows.append(row)

    write_csv(OUTPUT_DIR / "comparisons.csv", compare_rows)

    total = len(compare_rows)
    critical = sum(1 for r in compare_rows if r["critical_divergence"])
    exact = sum(1 for r in compare_rows if r["exact_agreement"])
    summary = {
        "total_comparisons": total,
        "exact_agreement_rate": round(exact / total, 4) if total else None,
        "critical_divergence_rate": round(critical / total, 4) if total else None,
    }
    write_jsonl(OUTPUT_DIR / "summary.jsonl", [summary])
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

## Production additions

Before running this in production, add:

- Retry with exponential backoff.
- Local response cache.
- Paired bootstrap confidence intervals.
- Automatic slicing and slice-gap reporting.
- Tool-call trace capture.
- Error taxonomy and structured logging.
- Normalization layer for structured outputs (JSON Schema comparison).
