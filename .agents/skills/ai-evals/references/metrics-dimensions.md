# Métricas e Dimensões de Avaliação

Use este mapa para transformar perguntas vagas do tipo "a resposta ficou boa?" em perguntas pequenas, audITáveis e mensuráveis. Cada dimensão deve virar uma métrica separada.

| Dimensão | Definição operacional | Ground truth mínimo | Validador preferido |
| --- | --- | --- | --- |
| **Acurácia factual** | A resposta está correta e completa em relação a uma resposta de referência ou fatos validados? | `expected_output`, KB curada ou label humano | LLM-as-Judge reference-based; em tarefas fechadas, combine com similarity/exact match |
| **Fidelidade / groundedness** | Cada claim relevante da resposta está suportada pelo contexto recuperado? | `retrieval_context` | LLM-as-Judge com decomposição de claims |
| **Alucinação** | A resposta inventa fatos não suportados pelo contexto de verdade fornecido? | `context` canônico | LLM-as-Judge reference-based |
| **Relevância** | A saída responde o que o usuário realmente pediu, sem fugir do tópico? | intenção do usuário, labels ou few-shot | LLM-as-Judge reference-free ou reference-based |
| **Cobertura / recall de requisitos** | Todos os fatos, campos ou requisitos obrigatórios apareceram? | checklist, assertions ou schema de requisitos | Regra determinística quando possível; LLM judge com checklist quando semântico |
| **Formato** | O output é JSON/Markdown/texto no contrato esperado? | schema, regex, parser, AST | Determinístico sempre que houver contrato estável |
| **Regra de negócio** | A saída respeita políticas, limites, enums, faixas de desconto, SLAs e regras internas? | regras codificadas + exemplos problema | Híbrido, com hard gate determinístico antes do juiz |
| **Segurança / toxicidade** | A resposta viola política, contém conteúdo tóxico ou comportamento nocivo? | policy rubric e/ou labels | LLM-as-Judge com critic dedicado |
| **Agente / tool use** | O agente chamou a ferramenta certa, na hora certa, e atingiu o objetivo do usuário? | trace esperado, labels humanos ou goal spec | Trajectory match + LLM judge + métricas de tool-call/goal accuracy |
| **Citação correta** | As fontes citadas sustentam as afirmações feitas? | referências esperadas ou contexto recuperado | Métrica específica de citation accuracy / groundedness |

## Regras de ouro

- Uma métrica por pergunta. Não misture "factualidade + tom + completude + segurança" numa mesma nota.
- Ground truth não precisa ser perfeito no primeiro dia. Misture production data, dados históricos, dados curados e dados sintéticos.
- Métricas subjetivas só viram hard gate depois de calibradas contra labels humanos.
