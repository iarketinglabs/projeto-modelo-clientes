# Checklist de QA para Evals na Atomica

Use como padrão mínimo para qualquer agente, automação ou skill que gere JSON, Markdown ou texto livre.

- [ ] **Contrato de saída versionado.** Cada skill tem um contrato explícito de output: schema JSON, headings Markdown esperados ou estrutura mínima do texto. Formato validado deterministicamente, não por LLM.
- [ ] **Dataset mínimo por slice.** Pelo menos cinco slices: happy path, boundary condition, caso ambíguo, caso adversarial e caso vindo de trace real de produção. Misture dados reais, históricos, curados e sintéticos.
- [ ] **Uma métrica por pergunta.** Não misture "factualidade + tom + completude + segurança" na mesma nota. Se quiser quatro coisas, crie quatro métricas.
- [ ] **Rubrica auditável.** Toda métrica semanticamente subjetiva tem escala explícita, fronteiras claras e saída estruturada com `score`, `label`, `reason` e `evidence`.
- [ ] **Judge separado do gerador sempre que possível.** Reduz risco de auto-preferência e de otimização cega para um único avaliador.
- [ ] **Randomização em A/B.** Em pairwise evals, randomize a ordem A/B e não recompense comprimento por padrão.
- [ ] **Calibração do juiz.** O juiz tem seu próprio benchmark com labels humanos. Meça alinhamento, revise casos de desacordo e transforme correções humanas em few-shots/versionamento de prompt.
- [ ] **Target de agreement.** Para categorias objetivas, mire alto acordo humano-judge antes de transformar score semântico em hard gate.
- [ ] **RAG não é tudo igual.** Meça retrieval e geração separadamente: contexto relevante/preciso, depois faithfulness/groundedness, e por fim citation accuracy se houver fontes citadas.
- [ ] **Agentes exigem trace evals.** Não aprove um agente só pela resposta final; avalie handoffs, tool calls, trajetória e goal completion.
- [ ] **Long-form pede decomposição.** Para relatórios, pesquisas e respostas longas, quebre a avaliação por seção: cobertura, groundedness, estrutura, citação e aderência a regras do domínio.
- [ ] **PT-BR precisa de métricas adaptadas.** Se a saída final é em português, adapte prompts/few-shots das métricas ou valide que a judge prompt em inglês continua alinhada.
- [ ] **Baseline oficial e regressão.** Sempre marque uma versão oficial do prompt/model/dataset para comparação de regressão.
- [ ] **Documentação obrigatória.** Registre no KB da Atomica: rubricas, thresholds, slices do dataset, baseline oficial, falhas conhecidas, exceções aceitas e data da última calibração do juiz.

## Síntese

Use código para o que é verificável, use LLM Judge para o que é semântico, e use humano para calibrar o próprio juiz.
