#!/usr/bin/env python3
"""
Validador de PRD (Product Requirements Document)
Verifica se um arquivo Markdown de PRD atende às seções obrigatórias
e critérios mínimos de qualidade definidos pela skill prd-creator.

Uso:
    python validate_prd.py <caminho_do_prd.md>
    python validate_prd.py <caminho_do_prd.md> --strict

Saída:
    Relatório de pass/fail por seção + score percentual + lista de lacunas.
"""

import argparse
import re
import sys
from pathlib import Path

# Seções obrigatórias que devem existir no PRD
REQUIRED_SECTIONS = [
    ("1. Contexto e Visão", ["1.1 Problema", "1.3 Personas"]),
    ("2. Escopo", ["2.1 In-Scope", "2.2 Out-of-Scope"]),
    ("3. Funcionalidades e Requisitos Funcionais", ["User Story", "Critérios de Aceitação"]),
    ("4. Requisitos Não-Funcionais", []),
    ("7. Restrições Técnicas", []),
    ("11. Glossário de Domínio", []),
]

# Padrões que indicam que RNFs têm métricas (números, unidades, %, comparadores)
RNF_METRIC_PATTERNS = [
    re.compile(r"\b\d+\s*(ms|s|segundos|minutos|h|horas|dias)\b", re.IGNORECASE),
    re.compile(r"\b\d+\.?\d*\s*%\b"),
    re.compile(r"\b[<>]=?\s*\d+\b"),
    re.compile(r"\b\d+\s*(req/s|rps|usuários|usuários simultâneos|GB|MB|KB|linhas|registros)\b", re.IGNORECASE),
    re.compile(r"\b(?:AES|TLS|WCAG|OWASP|ISO|GDPR|LGPD|PCI)\b", re.IGNORECASE),
]

# Padrões proibidos (termos subjetivos sem quantificação)
FORBIDDEN_SUBJECTIVE_TERMS = [
    "rápido", "rápida", "lento", "lenta",
    "fácil", "fácil de usar", "intuitivo", "intuitiva",
    "escalável", "escaláveis", "segurol", "segura" "eficiente", "eficientes",
    "robusto", "robustos", "amigável", "amigáveis",
    "sempre no ar", "alta disponibilidade"  # sem % associado
]


def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[ERRO] Não foi possível ler o arquivo: {e}")
        sys.exit(1)


def check_sections(content: str) -> list[dict]:
    results = []
    for section, subsections in REQUIRED_SECTIONS:
        found = section.lower() in content.lower()
        missing_subs = []
        if found and subsections:
            for sub in subsections:
                if sub.lower() not in content.lower():
                    missing_subs.append(sub)
        results.append({
            "section": section,
            "found": found,
            "missing_subsections": missing_subs,
        })
    return results


def check_rnf_metrics(content: str) -> dict:
    # Extrai a seção 4 de RNF
    rnf_section_match = re.search(
        r"#{2,4}\s*4\.\s*Requisitos Não-Funcionais.*?(?=\n#{2,4}\s*\d+\.|\Z)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if not rnf_section_match:
        return {"has_section": False, "items": 0, "with_metrics": 0, "lines_without_metrics": []}

    rnf_text = rnf_section_match.group(0)
    # Considera cada linha da tabela como um item de RNF
    lines = [ln.strip() for ln in rnf_text.splitlines() if "|" in ln and not ln.strip().startswith("|---")]
    # Remove header
    if len(lines) > 0:
        lines = lines[1:]

    with_metrics = 0
    without_metrics = []

    for line in lines:
        has_metric = any(pat.search(line) for pat in RNF_METRIC_PATTERNS)
        if has_metric:
            with_metrics += 1
        else:
            # Ignora linhas muito curtas ou vazias
            if len(line.replace("|", "").strip()) > 5:
                without_metrics.append(line)

    return {
        "has_section": True,
        "items": len(lines),
        "with_metrics": with_metrics,
        "lines_without_metrics": without_metrics,
    }


def check_bdd_coverage(content: str) -> dict:
    given_count = len(re.findall(r"\b[Gg]iven\b", content))
    when_count = len(re.findall(r"\b[Ww]hen\b", content))
    then_count = len(re.findall(r"\b[Tt]hen\b", content))

    # Verifica se há cenários de erro (palavras-chave comuns)
    error_keywords = ["erro", "error", "falha", "inválido", "inválida", "exceção", "exception", "timeout", "indisponível"]
    error_mentions = sum(content.lower().count(kw) for kw in error_keywords)

    return {
        "given": given_count,
        "when": when_count,
        "then": then_count,
        "has_bdd": given_count > 0 and when_count > 0 and then_count > 0,
        "error_mentions": error_mentions,
        "has_error_scenarios": error_mentions >= 2,
    }


def check_subjective_terms(content: str) -> list[str]:
    findings = []
    lowered = content.lower()
    for term in FORBIDDEN_SUBJECTIVE_TERMS:
        if term in lowered:
            # Tenta não flagrar se o termo estiver dentro de aspas citando o usuário
            # ou em seção de problemas conhecidos
            findings.append(term)
    return findings


def check_glossary(content: str) -> bool:
    return "11. Glossário de Domínio".lower() in content.lower() or "## 11. glossário".lower() in content.lower()


def check_out_of_scope(content: str) -> bool:
    return "Out-of-Scope".lower() in content.lower() or "fora do escopo".lower() in content.lower()


def main():
    parser = argparse.ArgumentParser(description="Valida um PRD segundo os padrões da skill prd-creator")
    parser.add_argument("prd_path", help="Caminho para o arquivo .md do PRD")
    parser.add_argument("--strict", action="store_true", help="Modo estrito: falha se houver termos subjetivos ou RNFs sem métricas")
    args = parser.parse_args()

    prd_path = Path(args.prd_path)
    if not prd_path.exists():
        print(f"[ERRO] Arquivo não encontrado: {prd_path}")
        sys.exit(1)

    content = read_file(prd_path)
    issues = []
    warnings = []

    print(f"\n{'='*60}")
    print(f"VALIDAÇÃO DE PRD: {prd_path.name}")
    print(f"{'='*60}\n")

    # 1. Seções obrigatórias
    print("[1] SEÇÕES OBRIGATÓRIAS")
    section_results = check_sections(content)
    section_score = 0
    for res in section_results:
        status = "✅" if res["found"] else "❌"
        print(f"  {status} {res['section']}")
        if not res["found"]:
            issues.append(f"Seção obrigatória ausente: {res['section']}")
        for sub in res["missing_subsections"]:
            print(f"      ⚠️  Subseção recomendada ausente: {sub}")
            warnings.append(f"Subseção ausente: {sub}")
        if res["found"]:
            section_score += 1

    # 2. RNFs com métricas
    print("\n[2] REQUISITOS NÃO-FUNCIONAIS (RNF)")
    rnf = check_rnf_metrics(content)
    if not rnf["has_section"]:
        issues.append("Seção 4 (RNF) não encontrada")
        print("  ❌ Seção 4 (RNF) não encontrada")
    else:
        print(f"  Itens de RNF encontrados: {rnf['items']}")
        print(f"  Com métricas quantificáveis: {rnf['with_metrics']}")
        if rnf["items"] > 0:
            pct = (rnf["with_metrics"] / rnf["items"]) * 100
            print(f"  Cobertura de métricas: {pct:.0f}%")
            if pct < 80:
                issues.append(f"Apenas {pct:.0f}% dos RNFs possuem métricas quantificáveis (meta: 80%+)")
            for line in rnf["lines_without_metrics"]:
                print(f"      ⚠️  Sem métrica: {line[:80]}...")
        else:
            warnings.append("Nenhum item de RNF detectado na tabela")

    # 3. BDD Coverage
    print("\n[3] CRITÉRIOS DE ACEITAÇÃO (BDD)")
    bdd = check_bdd_coverage(content)
    print(f"  Given: {bdd['given']} | When: {bdd['when']} | Then: {bdd['then']}")
    if bdd["has_bdd"]:
        print("  ✅ BDD detectado")
    else:
        issues.append("Critérios de aceitação BDD (Given/When/Then) não detectados")
        print("  ❌ BDD não detectado")

    if bdd["has_error_scenarios"]:
        print(f"  ✅ Menções a cenários de erro: {bdd['error_mentions']}")
    else:
        warnings.append("Poucos ou nenhum cenário de erro/edge case detectado nos critérios de aceitação")
        print(f"  ⚠️  Poucas menções a cenários de erro ({bdd['error_mentions']})")

    # 4. Termos subjetivos
    print("\n[4] TERMOS SUBJETIVOS")
    subjective = check_subjective_terms(content)
    if subjective:
        print(f"  ⚠️  Termos subjetivos detectados: {', '.join(set(subjective))}")
        if args.strict:
            issues.append(f"Termos subjetivos encontrados: {', '.join(set(subjective))}")
    else:
        print("  ✅ Nenhum termo subjetivo proibido detectado")

    # 5. Glossário
    print("\n[5] GLOSSÁRIO DE DOMÍNIO")
    if check_glossary(content):
        print("  ✅ Glossário presente")
    else:
        issues.append("Glossário de domínio (Seção 11) ausente")
        print("  ❌ Glossário não encontrado")

    # 6. Out-of-Scope
    print("\n[6] DELIMITAÇÃO DE ESCOPO")
    if check_out_of_scope(content):
        print("  ✅ Seção Out-of-Scope presente")
    else:
        warnings.append("Delimitação explícita de out-of-scope não encontrada")
        print("  ⚠️  Out-of-Scope não encontrado")

    # Score final
    total_checks = 4  # seções, RNF, BDD, glossário
    passed = sum([
        section_score >= len(section_results) - 1,  # tolera 1 seção faltando
        rnf["has_section"] and (rnf["with_metrics"] / max(rnf["items"], 1)) >= 0.5,
        bdd["has_bdd"],
        check_glossary(content),
    ])
    score_pct = (passed / total_checks) * 100

    print(f"\n{'='*60}")
    print(f"SCORE FINAL: {score_pct:.0f}% ({passed}/{total_checks} checks principais)")
    print(f"{'='*60}")

    if issues:
        print(f"\n❌ ISSUES ({len(issues)}):")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")

    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")

    if not issues and not warnings:
        print("\n🎉 PRD validado com sucesso! Nenhuma issue ou warning encontrado.")

    # Exit code
    if issues:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
