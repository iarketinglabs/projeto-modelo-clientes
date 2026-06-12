# Comparativo de Ferramentas de Eval

A pergunta certa não é "qual é a melhor?", mas "qual camada cada uma resolve melhor".

| Ferramenta | Onde brilha | Melhor encaixe | Cautela em 2026 |
| --- | --- | --- | --- |
| **OpenAI Evals** | Referência conceitual: datasets, graders, trace grading. | Legados OpenAI ou estudo de design de evals. | **Evite greenfield.** Plataforma depreciada: read-only em 31/10/2026 e desligamento em 30/11/2026. A OpenAI recomenda Promptfoo como continuidade. |
| **LangSmith** | Offline + online evals, few-shot a partir de correções humanas, annotation queues, experiments, summary charts e Insights. | Times em LangChain/LangGraph ou com forte workflow human-in-the-loop de alinhamento do juiz. | Melhor retorno quando tudo já está bem traçado. Alguns recursos avançados dependem de planos superiores. |
| **Arize Phoenix** | OSS/OTel, traces → datasets → experiments, comparação de runs, review de failure modes, LLM + code evaluators e human review. | Times que querem observabilidade forte, stack agnóstica e controle operacional. | Brilha mais quando combinado com harness explícito no repositório. |
| **DeepEval** | Experiência code-first: `pytest`, `assert_test()`, `deepeval test run`, métricas prontas, synthetic goldens e multi-turn. | Repositórios Python com eval gates em CI/CD e versionamento de métricas junto do código. | Sozinho é mais harness do que control plane; dashboard colaborativo fica no Confident AI. |
| **Ragas** | Especialista em RAG, groundedness, citation accuracy, tool call accuracy, agent goal accuracy, judge alignment, customização de prompts e adaptação para outros idiomas. | Aplicações com RAG, tool-calling e times que querem mexer fino nas métricas. | Funciona melhor como camada de métricas dentro de uma stack maior. |

## Recomendação padrão para a Atomica

**DeepEval + Phoenix** é a combinação mais equilibrada: disciplina de teste em código + tracing/dashboards sem lock-in de ecossistema de agentes. Use **LangSmith** se o coração da stack for LangChain/LangGraph. Use **Ragas** como especialista para RAG, groundedness, tool-use, citation accuracy e adaptação para pt-BR.
