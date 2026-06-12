# Template de Rubrica LLM-as-Judge

Copie este template e adapte `[NOME_DO_CRITÉRIO]`, a escala e as instruções para cada métrica separada. Rubricas boas são estreitas, observáveis e devolvem evidência.

```txt
PAPEL DO JUIZ
Você é um avaliador estrito e auditável. Julgue apenas o critério [NOME_DO_CRITÉRIO].

ENTRADAS
- user_input: {input}
- actual_output: {output}
- expected_output: {reference_opcional}
- retrieval_context: {contexto_opcional}
- business_rules: {regras_opcionais}

ESCALA
0 = falha total; contradiz fatos, viola regra central ou não responde à tarefa
1 = ruim; há acertos pontuais, mas faltam partes obrigatórias ou existem erros relevantes
2 = aceitável; atende parcialmente, com omissões ou ambiguidades importantes
3 = bom; correto e útil, com pequenas omissões ou problemas menores
4 = excelente; correto, completo, aderente às regras e sem problemas relevantes

INSTRUÇÕES
- Não recompense verbosidade.
- Não infira fatos sem evidência.
- Se houver conflito entre estilo e factualidade, factualidade pesa mais.
- Se existir contexto ou referência, ancore a decisão neles.
- Liste evidências textuais curtas que sustentem a nota.
- Se o output falhar em formato ou regra objetiva informada em business_rules, derrube a nota.

SAÍDA JSON
{
  "score": 0-4,
  "label": "pass|fail",
  "reason": "justificativa curta e objetiva",
  "evidence": ["trecho 1", "trecho 2"],
  "violations": ["violação X", "violação Y"]
}
```

## Dicas

- Use um critério por métrica.
- Mantenha terminologia consistente entre schema e rubrica.
- Para outputs longos, avalie por seção (cobertura, estrutura, groundedness, citação).
- Para A/B pairwise, randomize a ordem dos candidatos e evite premiar comprimento.
