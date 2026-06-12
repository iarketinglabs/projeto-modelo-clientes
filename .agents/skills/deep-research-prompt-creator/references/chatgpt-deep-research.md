# Indice rapido

- `RESUMO EXECUTIVO PARA IA`: fundamentos operacionais para combinar contexto, iteracao e evidencia em prompts de Deep Research.
- `FUNDAMENTACAO TEORICA`: frameworks como ReAct, Tree of Thoughts, Self-Consistency, Step-Back, RAG e verificacao.
- `HEURISTICAS PRATICAS E TATICAS`: regras IF/THEN para contexto, busca iterativa, mitigacao de alucinacoes e auditoria.
- `BIBLIOTECA DE ESTRUTURAS DE PROMPT`: templates para pesquisa exploratoria, fact-checking, sintese multi-documento e decisao.
- `REPOSITORIO DE FONTES`: links e referencias usados como base teorica.

# TÃ©cnicas de Engenharia de Prompt para OtimizaÃ§Ã£o de Deep Research em LLMs

## RESUMO EXECUTIVO PARA IA

SecÃ§Ã£o: 1

A engenharia de prompt para Deep Research Ã©, de forma operacional, a composiÃ§Ã£o de trÃªs â€œmotoresâ€ num Ãºnico contrato de execuÃ§Ã£o: **(i) engenharia de contexto** (o que entra, em que ordem, e com que fronteiras sintÃ¡cticas), **(ii) engenharia de iteraÃ§Ã£o** (como o modelo planifica, pesquisa, avalia, revÃª e repesquisa), e **(iii) engenharia de evidÃªncia** (como cada afirmaÃ§Ã£o fica ancorada a fontes recuperadas, com capacidade de auditoria e de retracÃ§Ã£o). O desempenho degrada-se de forma previsÃ­vel quando o prompt mistura instruÃ§Ãµes, dados e exemplos sem separadores; quando nÃ£o define a forma de saÃ­da; e quando nÃ£o impÃµe uma polÃ­tica explÃ­cita de incerteza (â€œnÃ£o seiâ€ / â€œnÃ£o verificadoâ€) em vez de completismo. [\[1\]](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api)

A parte â€œcognitivaâ€ do Deep Research moderno Ã© bem capturada por frameworks acadÃ©micos de **razÃ£o+acÃ§Ã£o**, **decomposiÃ§Ã£o**, **pesquisa em Ã¡rvore**, **amostragem e selecÃ§Ã£o**, **reflexÃ£o** e **revisÃ£o com verificaÃ§Ã£o**. O objectivo prÃ¡tico destes frameworks, quando convertidos em heurÃ­sticas de prompt, Ã© transformar um LLM num agente que: (1) gera sub-perguntas e queries; (2) interage com ferramentas de busca/recuperaÃ§Ã£o; (3) mantÃ©m um ledger de evidÃªncia; (4) produz sÃ­ntese final apenas apÃ³s verificaÃ§Ã£o (ou com rÃ³tulos de incerteza). [\[2\]](https://arxiv.org/abs/2210.03629)

A optimizaÃ§Ã£o â€œde produÃ§Ã£oâ€ deve assumir que prompting Ã© disciplina empÃ­rica (ciclo de avaliaÃ§Ã£o â†’ ajuste â†’ reavaliaÃ§Ã£o) e que, em tarefas longas, o custo/latÃªncia/qualidade dependem criticamente de **controlo de forma** (por ex., esquemas), **gestÃ£o de contexto** (compaction) e **estratÃ©gias de repetiÃ§Ã£o estÃ¡vel** (caching) â€” com trade-offs explÃ­citos (ex.: citaÃ§Ãµes vs JSON estrito em certos fornecedores). [\[3\]](https://developers.openai.com/cookbook/examples/evaluation/building_resilient_prompts_using_an_evaluation_flywheel/)

## FUNDAMENTAÃ‡ÃƒO TEÃ“RICA

SecÃ§Ã£o: 2

* **ReAct**: Integra raciocÃ­nio textual com acÃ§Ãµes (tool calls) num traÃ§ado intercalado, mitigando alucinaÃ§Ã£o via interacÃ§Ã£o com uma API de conhecimento e tornando trajectÃ³rias mais interpretÃ¡veis. | Deep Research: orquestra loops â€œpesquisar â†’ ler â†’ decidir prÃ³xima pesquisaâ€, com controlo explÃ­cito de quando actuar vs quando inferir. | Fonte/Link: https://arxiv.org/abs/2210.03629. [\[4\]](https://arxiv.org/abs/2210.03629)

* **Tree of Thoughts (ToT)**: Formula a resoluÃ§Ã£o como **busca em Ã¡rvore** sobre â€œpensamentosâ€ (ramificaÃ§Ã£o \+ avaliaÃ§Ã£o \+ backtracking), em vez de uma Ãºnica cadeia. | Deep Research: explorar mÃºltiplas hipÃ³teses/linhas de pesquisa em paralelo e seleccionar a melhor via por critÃ©rio (cobertura, credibilidade, consistÃªncia). | Fonte/Link: https://arxiv.org/abs/2305.10601. [\[5\]](https://arxiv.org/abs/2305.10601)

* **Self-Consistency**: Amostra mÃºltiplas cadeias de raciocÃ­nio e selecciona a resposta mais consistente (agregaÃ§Ã£o por maioria/consistÃªncia). | Deep Research: gerar mÃºltiplos â€œplanos de pesquisaâ€ e mÃºltiplas sÃ­nteses concorrentes, usando consistÃªncia entre respostas como sinal de robustez antes de consolidar. | Fonte/Link: https://arxiv.org/abs/2203.11171. [\[6\]](https://arxiv.org/abs/2203.11171)

* **Chain-of-Thought (CoT)**: Elicita raciocÃ­nio intermÃ©dio com demonstraÃ§Ãµes/estilo passo-a-passo. | Deep Research: Ãºtil para decompor perguntas em sub-perguntas e explicitar dependÃªncias (multi-hop), mas vulnerÃ¡vel a alucinaÃ§Ã£o se nÃ£o estiver acoplado a ferramentas/recuperaÃ§Ã£o. | Fonte/Link: https://arxiv.org/abs/2201.11903. [\[7\]](https://arxiv.org/abs/2210.03350)

* **Zero-shot CoT**: Induz raciocÃ­nio passo-a-passo sem exemplos (â€œletâ€™s think step by stepâ€ e variantes). | Deep Research: acelera prototipagem quando nÃ£o hÃ¡ corpus de exemplos; funciona como â€œgatilhoâ€ barato para decomposiÃ§Ã£o inicial. | Fonte/Link: https://arxiv.org/abs/2205.11916. [\[8\]](https://arxiv.org/abs/2201.11903)

* **Step-Back Prompting**: ForÃ§a uma etapa de abstracÃ§Ã£o/princÃ­pios antes de resolver, melhorando trajectÃ³ria de raciocÃ­nio. | Deep Research: gera conceitos/frames superiores que servem como expansores de query e como checklist conceptual para cobertura (evita ficar preso a detalhes prematuros). | Fonte/Link: https://arxiv.org/abs/2310.06117. [\[9\]](https://arxiv.org/abs/2310.06117)

* **Least-to-Most Prompting**: Resolve tarefas complexas com sequÃªncia de subtarefas crescentes (de mais simples para mais complexas). | Deep Research: estrutura â€œmicro-objectivosâ€ (definir termos â†’ mapear actores â†’ recolher evidÃªncia â†’ comparar â†’ sintetizar), reduzindo falhas de salto lÃ³gico. | Fonte/Link: https://arxiv.org/abs/2205.10625. [\[10\]](https://arxiv.org/abs/2205.11916)

* **Self-Ask (com Search)**: O modelo interroga-se com sub-perguntas antes da resposta final; pode acoplar motor de busca para responder sub-perguntas. | Deep Research: transforma uma pergunta ampla num grafo de sub-queries e evita â€œuma sÃ³ pesquisaâ€ insuficiente; melhora multi-hop via tool grounding. | Fonte/Link: https://arxiv.org/abs/2210.03350. [\[11\]](https://arxiv.org/abs/2210.03350)

* **RAG (Retrieval-Augmented Generation)**: Recupera documentos relevantes para aumentar o contexto antes de gerar. | Deep Research: base para respostas com fundamentaÃ§Ã£o documental e actualizaÃ§Ã£o temporal (quando a memÃ³ria do modelo Ã© insuficiente/desactualizada). | Fonte/Link: https://arxiv.org/abs/2005.11401. [\[12\]](https://arxiv.org/abs/2005.11401)

* **Self-RAG**: Aprende a intercalar recuperaÃ§Ã£o, geraÃ§Ã£o e â€œcrÃ­ticaâ€/reflexÃ£o para decidir quando recuperar e como corrigir. | Deep Research: agente que ajusta dinamicamente a intensidade de pesquisa e executa auto-verificaÃ§Ã£o orientada a evidÃªncia. | Fonte/Link: https://arxiv.org/abs/2310.11511. [\[13\]](https://arxiv.org/abs/2310.11511)

* **RARR (Researching and Revising)**: PÃ³s-processa saÃ­das para adicionar atribuiÃ§Ã£o e corrigir conteÃºdo nÃ£o suportado via â€œresearch â†’ reviseâ€. | Deep Research: pipeline canÃ³nico â€œrascunho â†’ procurar suporte â†’ revisar para alinhar com evidÃªnciaâ€, com foco em atribuiÃ§Ã£o e factualidade. | Fonte/Link: https://arxiv.org/abs/2210.08726. [\[14\]](https://arxiv.org/abs/2210.08726)

* **Chain-of-Verification (CoV-RAG)**: Integra verificaÃ§Ã£o (scoring/julgamento/reescrita) para corrigir erros de recuperaÃ§Ã£o e inconsistÃªncias de geraÃ§Ã£o, incluindo reescrita de query. | Deep Research: formaliza â€œverificar â†’ re-pesquisar com query melhor â†’ reescrever respostaâ€ como rotina sistemÃ¡tica. | Fonte/Link: https://arxiv.org/abs/2410.05801. [\[15\]](https://arxiv.org/abs/2410.05801)

## HEURÃSTICAS PRÃTICAS E TÃTICAS

SecÃ§Ã£o: 3

### EstruturaÃ§Ã£o de Contexto

ID: 3.1

* **Regra (hierarquia de autoridade)**: IF o agente corre num ambiente com papÃ©is (system/developer/user), THEN fixe invariantes (polÃ­tica de fontes, formato, critÃ©rios de paragem) no nÃ­vel mais alto disponÃ­vel e faÃ§a â€œinstruÃ§Ãµes de tarefaâ€ no nÃ­vel do utilizador para minimizar conflitos. [\[16\]](https://developers.openai.com/cookbook/articles/openai-harmony/)

* **Regra (separaÃ§Ã£o sintÃ¡ctica)**: IF o prompt mistura instruÃ§Ãµes \+ dados \+ exemplos, THEN imponha separadores rÃ­gidos (por ex. \#\#\# / """...""" / tags) e declare explicitamente â€œo que Ã© contextoâ€ vs â€œo que Ã© tarefaâ€. [\[17\]](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api)

* **Regra (ordenaÃ§Ã£o para long context)**: IF tokens(contexto) Ã© grande (â‰ˆ20k+ tokens) OU hÃ¡ mÃºltiplos documentos, THEN: (1) coloque documentos no topo; (2) coloque a query e restriÃ§Ãµes crÃ­ticas no fim; (3) inclua metadados por documento (fonte/data). [\[18\]](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips)

* **Regra (ordenaÃ§Ã£o para contextos curtos/mÃ©dios)**: IF o contexto Ã© curto/mÃ©dio (nÃ£o domina a janela), THEN ponha instruÃ§Ãµes primeiro e isole o texto de entrada com delimitadores; isto reduz ambiguidade de parsing e aumenta obedecÌ§a. [\[19\]](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api)

* **Regra (evitar negaÃ§Ãµes vagas)**: IF pretende limitar â€œadivinhaÃ§Ã£oâ€, THEN nÃ£o use negativos genÃ©ricos (â€œnÃ£o inferirâ€, â€œnÃ£o adivinharâ€) isolados; em vez disso, especifique: â€œpode deduzir *apenas* a partir do contexto fornecido; nÃ£o introduzir informaÃ§Ã£o externaâ€. [\[20\]](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide)

* **Regra (forma de saÃ­da como contrato)**: IF a saÃ­da vai ser consumida por outro agente/sistema, THEN use um esquema (JSON Schema / structured outputs / tool schema estrito) em vez de confiar em â€œprompts fortesâ€ para consistÃªncia. [\[21\]](https://developers.openai.com/api/docs/guides/structured-outputs/)

* **Regra (trade-off citaÃ§Ãµes vs JSON estrito)**: IF precisa **simultaneamente** de (a) JSON estrito e (b) citaÃ§Ãµes inline automÃ¡ticas, THEN separe em 2 passos (Passo A: JSON com IDs/trechos; Passo B: narrativa com citaÃ§Ãµes) porque, em certos fornecedores, citaÃ§Ãµes e structured outputs sÃ£o incompatÃ­veis. [\[22\]](https://platform.claude.com/docs/en/build-with-claude/citations)

* **Regra (controlo de verbosidade)**: IF pretende previsibilidade de comprimento/forma, THEN substitua â€œseja concisoâ€ por limites concretos (p.ex. â€œ3â€“6 frasesâ€, â€œâ‰¤5 bulletsâ€, â€œ1 parÃ¡grafo \+ 1 listaâ€) e defina o â€œshapeâ€ exacto. [\[23\]](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide/)

* **Regra (agentic reminders para tarefas longas)**: IF o objectivo envolve mÃºltiplas pesquisas/iteraÃ§Ãµes, THEN injete lembretes explÃ­citos: **persistÃªncia** (nÃ£o parar cedo), **tool-calling** (nÃ£o inventar quando hÃ¡ ferramenta) e **planeamento** (opcional, para visibilidade). [\[24\]](https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide/)

* **Regra (gestÃ£o de contexto em execuÃ§Ãµes longas)**: IF a interacÃ§Ã£o Ã© longa (multi-turn) e pode saturar a janela, THEN imponha checkpoints de estado (objectivos, fontes chave, decisÃµes) e use mecanismos de compaction/context management quando disponÃ­veis. [\[25\]](https://developers.openai.com/api/docs/guides/compaction)

* **Regra (performance: prefixos estÃ¡veis)**: IF o agente faz muitas iteraÃ§Ãµes com uma base de instruÃ§Ãµes repetida, THEN coloque conteÃºdo estÃ¡vel no prefixo e evite variar tokens iniciais (melhora caching e reduz custo/latÃªncia). [\[26\]](https://developers.openai.com/api/docs/guides/prompt-caching/)

* **Regra (anti-overprompting de ferramentas)**: IF o prompt contÃ©m linguagem agressiva (â€œCRÃTICO: usar sempre ferramentaâ€), THEN suavize para condiÃ§Ãµes (â€œusar quando melhora compreensÃ£oâ€) para evitar overtrigger e chamadas com parÃ¢metros inventados. [\[27\]](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts)

### Busca Iterativa e Refinamento

ID: 3.2

* **Regra (seleccionar modo de pesquisa)**: IF a pergunta Ã© sensÃ­vel a actualidade OU exige mÃºltiplas fontes, THEN force um modo â€œagentic search / deep researchâ€ (planeamento \+ mÃºltiplas buscas \+ sÃ­ntese) em vez de uma Ãºnica busca. [\[28\]](https://developers.openai.com/api/docs/guides/tools-web-search/)

* **Regra (decomposiÃ§Ã£o first-class)**: IF o tema Ã© amplo, THEN gere sub-perguntas antes de pesquisar e mapeie dependÃªncias (o que Ã© definicional, o que Ã© empÃ­rico, o que Ã© controverso). â€œSelf-Askâ€ Ã© um padrÃ£o directo para isto. [\[29\]](https://arxiv.org/abs/2210.03350)

* **Regra (Step-Back antes das queries)**: IF a query tende a ficar â€œpresaâ€ em termos especÃ­ficos (ex.: nomes, siglas), THEN faÃ§a um passo de abstracÃ§Ã£o (princÃ­pios/frames) e converta esse output em expansÃµes de query e critÃ©rios de cobertura. [\[9\]](https://arxiv.org/abs/2310.06117)

* **Regra (ReAct como loop canÃ³nico)**: IF hÃ¡ ferramentas de busca/recuperaÃ§Ã£o, THEN use um loop ReAct: **Pensar â†’ Agir (search/fetch) â†’ Observar â†’ Decidir**; proÃ­ba conclusÃµes sem â€œobservarâ€ evidÃªncia. [\[30\]](https://arxiv.org/abs/2210.03629)

* **Regra (ramificar â†’ avaliar â†’ convergir)**: IF o risco de â€œmiopiaâ€ Ã© alto (tema com vÃ¡rias escolas, mÃºltiplos paÃ­ses, mÃºltiplos perÃ­odos), THEN ramifique 3â€“5 planos/Ã¢ngulos (ToT) e sÃ³ depois consolide o melhor (ou combine) com base em critÃ©rios explÃ­citos. [\[31\]](https://arxiv.org/abs/2305.10601)

* **Regra (Self-Consistency para robustez)**: IF a resposta depende de cadeias de inferÃªncia longas (multi-hop) OU hÃ¡ ambiguidade, THEN gere N candidatos (planos ou sÃ­nteses) e seleccione por consistÃªncia \+ suporte documental antes de escrever versÃ£o final. [\[32\]](https://arxiv.org/abs/2203.11171)

* **Regra (reflexÃ£o pÃ³s-resultados)**: IF uma iteraÃ§Ã£o de pesquisa devolve sinais fracos (fontes pouco credÃ­veis, resultados repetidos), THEN produza uma â€œnota de reflexÃ£oâ€ (o que falta \+ nova estratÃ©gia) e reescreva queries. â€œReflexionâ€ formaliza a utilidade de memÃ³ria textual de feedback. [\[33\]](https://arxiv.org/abs/2303.11366)

* **Regra (revisÃ£o orientada a atribuiÃ§Ã£o)**: IF a primeira sÃ­ntese foi produzida, THEN execute um passo independente â€œresearch \+ reviseâ€ (estilo RARR): listar afirmaÃ§Ãµes â†’ procurar suporte â†’ editar para alinhamento com fontes. [\[34\]](https://arxiv.org/abs/2210.08726)

* **Regra (verificaÃ§Ã£o e reescrita de query)**: IF as passagens recuperadas nÃ£o suportam a resposta (ou estÃ£o fora de foco), THEN re-formule a query e repita a recuperaÃ§Ã£o; CoV-RAG explicita este mecanismo como rotina de correcÃ§Ã£o. [\[35\]](https://arxiv.org/abs/2410.05801)

* **Regra (prompt-chaining para controlo de pipeline)**: IF precisa de inspecionar outputs intermÃ©dios (auditoria/debug/branching), THEN parta em chamadas sequenciais explÃ­citas: rascunho â†’ revisÃ£o contra critÃ©rios â†’ refinamento. [\[36\]](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts)

* **Regra (paralelizaÃ§Ã£o segura)**: IF existem sub-tarefas independentes (ex.: 4 sub-perguntas), THEN pesquise em paralelo; ELSE, se os parÃ¢metros dependem de resultados prÃ©vios, force sequencial e proÃ­ba placeholders. [\[37\]](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts)

### MitigaÃ§Ã£o de AlucinaÃ§Ãµes em Pesquisa

ID: 3.3

* **Regra (polÃ­tica de incerteza)**: IF nÃ£o hÃ¡ suporte suficiente, THEN o agente deve declarar â€œnÃ£o verificÃ¡vel/sem evidÃªnciaâ€ e abstÃ©m-se de inventar; isto reduz alucinaÃ§Ã£o e alinha com directivas de honestidade/uncertainty. [\[38\]](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)

* **Regra (â€œno source, no claimâ€)**: IF a resposta contÃ©m afirmaÃ§Ãµes factuais, THEN cada afirmaÃ§Ã£o deve ligar-se a evidÃªncia recuperada (link/trecho/ID) OU ser explicitamente rotulada como hipÃ³tese. [\[39\]](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)

* **Regra (quotes-first em documentos longos)**: IF a tarefa envolve documentos extensos, THEN extraia primeiro citaÃ§Ãµes/trechos relevantes (word-for-word) e sÃ³ depois sintetize; isto ancora a geraÃ§Ã£o no texto e reduz deriva. [\[40\]](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)

* **Regra (split-step verification)**: IF existe risco de o modelo â€œfingirâ€ capacidade (ex.: acesso a URL ao vivo) OU de alucinar factos raros, THEN force 2 passos: (1) verificar capacidade/evidÃªncia; (2) sÃ³ se OK, gerar resposta. [\[41\]](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide)

* **Regra (RAG quando o conhecimento Ã© dinÃ¢mico/externo)**: IF a pergunta depende de informaÃ§Ã£o fora do treino (actualidade, domÃ­nio proprietÃ¡rio), THEN injete contexto via recuperaÃ§Ã£o (RAG) e proÃ­ba â€œmemÃ³ria do modeloâ€ como fonte. [\[42\]](https://arxiv.org/abs/2005.11401)

* **Regra (auto-crÃ­tica controlada por evidÃªncia)**: IF hÃ¡ risco de â€œresposta bonita mas frÃ¡gilâ€, THEN use um passo de crÃ­tica que tente refutar a resposta com base nas fontes; se nÃ£o encontrar suporte, reescreve/retira. [\[43\]](https://arxiv.org/abs/2410.05801)

* **Regra (best-of-N como detector de fragilidade)**: IF outputs divergem significativamente entre execuÃ§Ãµes com o mesmo contexto, THEN trate a divergÃªncia como sinal de fragilidade e exija mais evidÃªncia (ou reduza escopo) antes de concluir. [\[44\]](https://arxiv.org/abs/2203.11171)

* **Regra (evitar instruÃ§Ãµes contraditÃ³rias)**: IF o prompt tem objectivos simultÃ¢neos (p.ex., â€œnÃ£o inferirâ€ e â€œsintetizarâ€/â€œcalcularâ€), THEN explicite o que Ã© permitido inferir *a partir do contexto*; negativos genÃ©ricos degradam sÃ­ntese e cÃ¡lculo. [\[41\]](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide)

* **Regra (validaÃ§Ã£o de inputs estruturados)**: IF o agente chama ferramentas/funÃ§Ãµes, THEN use schemas estritos (quando disponÃ­veis) para prevenir parÃ¢metros invÃ¡lidos e reduzir falhas silenciosas. [\[45\]](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)

* **Regra (auditoria e rastreabilidade)**: IF o output final precisa de auditoria, THEN produza tambÃ©m um â€œmapa de evidÃªnciaâ€ (claim â†’ fontes) ou um modo â€œcitation-richâ€. Em pipelines com deep research e web search, a infra pode devolver citaÃ§Ãµes e metadados de fonte. [\[46\]](https://developers.openai.com/api/docs/guides/tools-web-search/)

## BIBLIOTECA DE ESTRUTURAS DE PROMPT

SecÃ§Ã£o: 4

* **Template 1: Pesquisa ExploratÃ³ria de Topo de Funil**

* \[SYSTEM | role\]  
  Ã‰s um agente de Deep Research. Objectivo: produzir sÃ­ntese estruturada e auditÃ¡vel com base em evidÃªncia recuperada.  
  PolÃ­tica: nÃ£o inventar factos; quando nÃ£o houver evidÃªncia, marcar como "nÃ£o verificado".

  \[CONTEXT\]  
  Data actual: {YYYY-MM-DD}  
  Idioma de output: pt-PT  
  Escopo/limites: {SCOPE\_LIMITS}  
  PreferÃªncia de fontes: primÃ¡rias (papers, docs oficiais, relatÃ³rios tÃ©cnicos).

  \[TASK\]  
  Tema: {TOPIC}  
  Pergunta principal: {MAIN\_QUESTION}

  \[PROCESS | loop\]  
  1\) Clarificar: gerar 5â€“10 sub-perguntas (definiÃ§Ãµes, estado-da-arte, actores, mÃ©tricas, controvÃ©rsias).  
  2\) Para cada sub-pergunta:  
     2.1) Propor 2â€“4 queries de busca (sinÃ³nimos, termos tÃ©cnicos, acrÃ³nimos).  
     2.2) Pesquisar e recolher fontes primÃ¡rias (mÃ­nimo {N\_SOURCES\_MIN}).  
     2.3) Extrair trechos (ou pontos) que suportem conclusÃµes.  
  3\) Consolidar: criar mapa do campo (taxonomia \+ tendÃªncias \+ lacunas).  
  4\) Verificar: remover ou rotular qualquer afirmaÃ§Ã£o sem suporte.

  \[OUTPUT | schema\]  
  \- Mapa do domÃ­nio (taxonomia)  
  \- Lista de conceitos-chave (definiÃ§Ã£o tÃ©cnica)  
  \- Principais abordagens/frameworks \+ quando aplicar  
  \- QuestÃµes em aberto \+ como pesquisar a seguir  
  \- Bibliografia (URLs)

* **Template 2: ValidaÃ§Ã£o de Dados e Fact-Checking Extremo**

* \[SYSTEM | role\]  
  Ã‰s um verificador factual. NÃ£o escreves narrativa livre antes de construir um ledger de evidÃªncia.  
  Regra: "no source, no claim".

  \[INPUT\]  
  AfirmaÃ§Ãµes a verificar (lista):  
  {CLAIMS\_LIST}

  \[PROCESS\]  
  A) Normalizar afirmaÃ§Ãµes:  
     \- dividir em unidades atÃ³micas (uma afirmaÃ§Ã£o \= um facto verificÃ¡vel)  
  B) Para cada afirmaÃ§Ã£o:  
     B1) Formular query(s) de verificaÃ§Ã£o (inclui termos alternativos \+ datas \+ nomes exactos).  
     B2) Recuperar fontes primÃ¡rias.  
     B3) Classificar estado:  
         \- SUPORTADA | CONTRADITA | INCONCLUSIVA | NÃƒO VERIFICÃVEL  
     B4) Guardar evidÃªncia:  
         \- URL  
         \- excerto/nota curta do que prova  
  C) RevisÃ£o adversarial:  
     \- tentar encontrar 1 fonte credÃ­vel que contradiga cada afirmaÃ§Ã£o SUPORTADA.  
  D) Produzir output final.

  \[OUTPUT | schema\]  
  \- Ledger:  
    \- claim\_id  
    \- claim\_text  
    \- status  
    \- evidence: \[{url, snippet\_or\_note}\]  
    \- contradictions: \[{url, snippet\_or\_note}\] (se existir)  
  \- Resumo:  
    \- % suportadas / contraditas / inconclusivas / nÃ£o verificÃ¡veis

* **Template 3: SÃ­ntese e Cruzamento de MÃºltiplos Documentos/Fontes**

* \[SYSTEM | role\]  
  Ã‰s um sintetizador multi-documento. A tua prioridade Ã©: (1) fidelidade ao material; (2) convergÃªncia/divergÃªncia entre fontes; (3) geraÃ§Ã£o de conclusÃµes condicionais.

  \[INPUT | documents\]  
  Documentos: {DOC\_SET}  
  Formato preferido (quando aplicÃ¡vel):  
  \<documents\>  
    \<document id="D1"\>  
      \<source\>{URL\_OR\_ID}\</source\>  
      \<date\>{DATE}\</date\>  
      \<document\_content\>...\</document\_content\>  
    \</document\>  
    ...  
  \</documents\>

  \[PROCESS\]  
  1\) Indexar: extrair tÃ³picos e afirmaÃ§Ãµes chave por documento.  
  2\) Alinhar: criar matriz "tema â†’ o que cada documento diz".  
  3\) Detectar divergÃªncias:  
     \- contradiÃ§Ãµes directas  
     \- diferenÃ§as de definiÃ§Ã£o  
     \- diferenÃ§as de Ã©poca/escopo/metodologia  
  4\) SÃ­ntese:  
     \- conclusÃµes apenas quando houver convergÃªncia ou quando a divergÃªncia estiver explicitada  
  5\) Auditoria:  
     \- anexar "claim â†’ docs" para cada conclusÃ£o.

  \[OUTPUT | schema\]  
  \- SumÃ¡rio por documento (5â€“10 linhas)  
  \- ConvergÃªncias (com fontes)  
  \- DivergÃªncias/contradiÃ§Ãµes (com fontes)  
  \- SÃ­ntese final (condicional, com limites)  
  \- Bibliografia (URLs)

## REPOSITÃ“RIO DE FONTES

SecÃ§Ã£o: 5

* **OpenAI[\[47\]](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide)** (2026). â€œShell \+ Skills \+ Compaction: Tips for long-running agents that do real workâ€. https://developers.openai.com/blog/skills-shell-tips/. [\[48\]](https://developers.openai.com/blog/skills-shell-tips/)

* OpenAI (2025). â€œIntroduction to deep research in the OpenAI APIâ€. https://developers.openai.com/cookbook/examples/deep\_research\_api/introduction\_to\_deep\_research\_api/. [\[49\]](https://developers.openai.com/cookbook/examples/deep_research_api/introduction_to_deep_research_api/)

* OpenAI (2025). â€œGPT-5.2 Prompting Guideâ€. https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2\_prompting\_guide/. [\[23\]](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide/)

* OpenAI (2026). â€œPrompt Caching 201â€. https://developers.openai.com/cookbook/examples/prompt\_caching\_201/. [\[50\]](https://developers.openai.com/cookbook/examples/prompt_caching_201/)

* OpenAI (\[Sem dados \- Fonte nÃ£o verificada\]). â€œPrompt cachingâ€. https://developers.openai.com/api/docs/guides/prompt-caching/. [\[51\]](https://developers.openai.com/api/docs/guides/prompt-caching/)

* OpenAI (\[Sem dados \- Fonte nÃ£o verificada\]). â€œCompactionâ€. https://developers.openai.com/api/docs/guides/compaction. [\[52\]](https://developers.openai.com/api/docs/guides/compaction)

* OpenAI (\[Sem dados \- Fonte nÃ£o verificada\]). â€œStructured model outputsâ€. https://developers.openai.com/api/docs/guides/structured-outputs/. [\[53\]](https://developers.openai.com/api/docs/guides/structured-outputs/)

* OpenAI (\[Sem dados \- Fonte nÃ£o verificada\]). â€œWeb searchâ€. https://developers.openai.com/api/docs/guides/tools-web-search/. [\[54\]](https://developers.openai.com/api/docs/guides/tools-web-search/)

* OpenAI (2025). â€œBuilding resilient prompts using an evaluation flywheelâ€. https://developers.openai.com/cookbook/examples/evaluation/building\_resilient\_prompts\_using\_an\_evaluation\_flywheel/. [\[55\]](https://developers.openai.com/cookbook/examples/evaluation/building_resilient_prompts_using_an_evaluation_flywheel/)

* OpenAI (2025). â€œOptimizing LLM Accuracyâ€. https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy/. [\[56\]](https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy/)

* OpenAI (2025). â€œOpenAI Harmony Response Formatâ€. https://developers.openai.com/cookbook/articles/openai-harmony/. [\[57\]](https://developers.openai.com/cookbook/articles/openai-harmony/)

* OpenAI (2025). â€œGPT-4.1 Prompting Guideâ€. https://developers.openai.com/cookbook/examples/gpt4-1\_prompting\_guide/. [\[58\]](https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide/)

* OpenAI (2025). â€œPrompt Migration Guideâ€. https://developers.openai.com/cookbook/examples/prompt\_migration\_guide/. [\[59\]](https://developers.openai.com/cookbook/examples/prompt_migration_guide/)

* OpenAI (2025). â€œUsing GPT-5.2â€. https://developers.openai.com/api/docs/guides/latest-model/. [\[60\]](https://developers.openai.com/api/docs/guides/latest-model/)

* OpenAI (\[Sem dados \- Fonte nÃ£o verificada\]). â€œResponses API reference: retrieve (roles & instruction hierarchy)â€. https://developers.openai.com/api/reference/resources/responses/methods/retrieve/. [\[61\]](https://developers.openai.com/api/reference/resources/responses/methods/retrieve/)

* OpenAI (2025). â€œModel Spec (2025-09-12)â€. https://model-spec.openai.com/2025-09-12.html. [\[62\]](https://model-spec.openai.com/2025-09-12.html)

* OpenAI Help Center (\[Sem dados \- Fonte nÃ£o verificada\]; â€œUpdated: last monthâ€). â€œBest practices for prompt engineering with the OpenAI APIâ€. https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api. [\[19\]](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api)

* **Anthropic[\[63\]](https://arxiv.org/abs/2410.05801)** (\[Sem dados \- Fonte nÃ£o verificada\]). â€œClaude prompting best practices: long context prompting / XML structuring / tool usageâ€. https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices. [\[64\]](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips)

* Anthropic (\[Sem dados \- Fonte nÃ£o verificada\]). â€œReduce hallucinationsâ€. https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations. [\[65\]](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)

* Anthropic (\[Sem dados \- Fonte nÃ£o verificada\]). â€œTool use (strict tool use)â€. https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview. [\[66\]](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)

* Anthropic (\[Sem dados \- Fonte nÃ£o verificada\]). â€œStructured outputsâ€. https://platform.claude.com/docs/en/build-with-claude/structured-outputs. [\[67\]](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

* Anthropic (\[Sem dados \- Fonte nÃ£o verificada\]). â€œCitations (feature compatibility)â€. https://platform.claude.com/docs/en/build-with-claude/citations. [\[68\]](https://platform.claude.com/docs/en/build-with-claude/citations)

* **Google Cloud[\[69\]](https://arxiv.org/abs/2305.10601)** (2026). â€œPrompt engineering: overview and guide (Last Updated: 01/14/2026)â€. https://cloud.google.com/discover/what-is-prompt-engineering. [\[70\]](https://cloud.google.com/discover/what-is-prompt-engineering)

* Google Cloud (2026). â€œPrompt design strategies (Last updated 2026-02-23 UTC)â€. https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies. [\[71\]](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies)

* Google Cloud (2026). â€œGemini 3 prompting guide (Last updated 2026-02-23 UTC)â€. https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide. [\[72\]](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide)

* **arXiv[\[73\]](https://developers.openai.com/cookbook/articles/openai-harmony/)** (2022). Yao et al. â€œReAct: Synergizing Reasoning and Acting in Language Modelsâ€. https://arxiv.org/abs/2210.03629. [\[4\]](https://arxiv.org/abs/2210.03629)

* arXiv (2023). Yao et al. â€œTree of Thoughts: Deliberate Problem Solving with Large Language Modelsâ€. https://arxiv.org/abs/2305.10601. [\[5\]](https://arxiv.org/abs/2305.10601)

* arXiv (2022). Wang et al. â€œSelf-Consistency Improves Chain of Thought Reasoning in Language Modelsâ€. https://arxiv.org/abs/2203.11171. [\[6\]](https://arxiv.org/abs/2203.11171)

* arXiv (2022). Wei et al. â€œChain-of-Thought Prompting Elicits Reasoning in Large Language Modelsâ€. https://arxiv.org/abs/2201.11903. [\[7\]](https://arxiv.org/abs/2210.03350)

* arXiv (2022). Kojima et al. â€œLarge Language Models are Zero-Shot Reasonersâ€. https://arxiv.org/abs/2205.11916. [\[8\]](https://arxiv.org/abs/2201.11903)

* arXiv (2022). Zhou et al. â€œLeast-to-Most Prompting Enables Complex Reasoning in Large Language Modelsâ€. https://arxiv.org/abs/2205.10625. [\[10\]](https://arxiv.org/abs/2205.11916)

* arXiv (2023). Zheng et al. â€œTake a Step Back: Evoking Reasoning via Abstraction in Large Language Modelsâ€. https://arxiv.org/abs/2310.06117. [\[9\]](https://arxiv.org/abs/2310.06117)

* arXiv (2022). Press et al. â€œMeasuring and Narrowing the Compositionality Gap in Language Modelsâ€ (Self-Ask). https://arxiv.org/abs/2210.03350. [\[11\]](https://arxiv.org/abs/2210.03350)

* arXiv (2020). Lewis et al. â€œRetrieval-Augmented Generation for Knowledge-Intensive NLP Tasksâ€. https://arxiv.org/abs/2005.11401. [\[12\]](https://arxiv.org/abs/2005.11401)

* arXiv (2023). Asai et al. â€œSelf-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflectionâ€. https://arxiv.org/abs/2310.11511. [\[13\]](https://arxiv.org/abs/2310.11511)

* arXiv (2022). Gao et al. â€œRARR: Researching and Revising What Language Models Say, Using Language Modelsâ€. https://arxiv.org/abs/2210.08726. [\[14\]](https://arxiv.org/abs/2210.08726)

* arXiv (2024). He et al. â€œRetrieving, Rethinking and Revising: The Chain-of-Verification Can Improve Retrieval Augmented Generationâ€. https://arxiv.org/abs/2410.05801. [\[15\]](https://arxiv.org/abs/2410.05801)

* arXiv (2023). Schick et al. â€œToolformer: Language Models Can Teach Themselves to Use Toolsâ€. https://arxiv.org/abs/2302.04761. [\[74\]](https://arxiv.org/abs/2302.04761)

* arXiv (2023). Shinn et al. â€œReflexion: Language Agents with Verbal Reinforcement Learningâ€. https://arxiv.org/abs/2303.11366. [\[75\]](https://arxiv.org/abs/2303.11366)

* arXiv (2023). Zhou et al. â€œLanguage Agent Tree Search (LATS) Unifies Reasoning, Acting, and Planning in Language Modelsâ€. https://arxiv.org/abs/2310.04406. [\[76\]](https://arxiv.org/abs/2310.04406)

* arXiv (2023). Khattab et al. â€œDSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelinesâ€. https://arxiv.org/abs/2310.03714. [\[77\]](https://arxiv.org/abs/2310.03714)

* arXiv (2022). Bai et al. â€œConstitutional AI: Harmlessness from AI Feedbackâ€. https://arxiv.org/abs/2212.08073. [\[78\]](https://arxiv.org/abs/2212.08073)

---

[\[1\]](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api) [\[17\]](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api) [\[19\]](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api) Best practices for prompt engineering with the OpenAI API | OpenAI Help Center

[https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api)

[\[2\]](https://arxiv.org/abs/2210.03629) [\[4\]](https://arxiv.org/abs/2210.03629) [\[30\]](https://arxiv.org/abs/2210.03629) https://arxiv.org/abs/2210.03629

[https://arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629)

[\[3\]](https://developers.openai.com/cookbook/examples/evaluation/building_resilient_prompts_using_an_evaluation_flywheel/) [\[55\]](https://developers.openai.com/cookbook/examples/evaluation/building_resilient_prompts_using_an_evaluation_flywheel/) https://developers.openai.com/cookbook/examples/evaluation/building\_resilient\_prompts\_using\_an\_evaluation\_flywheel/

[https://developers.openai.com/cookbook/examples/evaluation/building\_resilient\_prompts\_using\_an\_evaluation\_flywheel/](https://developers.openai.com/cookbook/examples/evaluation/building_resilient_prompts_using_an_evaluation_flywheel/)

[\[5\]](https://arxiv.org/abs/2305.10601) [\[31\]](https://arxiv.org/abs/2305.10601) [\[69\]](https://arxiv.org/abs/2305.10601) https://arxiv.org/abs/2305.10601

[https://arxiv.org/abs/2305.10601](https://arxiv.org/abs/2305.10601)

[\[6\]](https://arxiv.org/abs/2203.11171) [\[32\]](https://arxiv.org/abs/2203.11171) [\[44\]](https://arxiv.org/abs/2203.11171) https://arxiv.org/abs/2203.11171

[https://arxiv.org/abs/2203.11171](https://arxiv.org/abs/2203.11171)

[\[7\]](https://arxiv.org/abs/2210.03350) [\[11\]](https://arxiv.org/abs/2210.03350) [\[29\]](https://arxiv.org/abs/2210.03350) https://arxiv.org/abs/2210.03350

[https://arxiv.org/abs/2210.03350](https://arxiv.org/abs/2210.03350)

[\[8\]](https://arxiv.org/abs/2201.11903) https://arxiv.org/abs/2201.11903

[https://arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903)

[\[9\]](https://arxiv.org/abs/2310.06117) https://arxiv.org/abs/2310.06117

[https://arxiv.org/abs/2310.06117](https://arxiv.org/abs/2310.06117)

[\[10\]](https://arxiv.org/abs/2205.11916) https://arxiv.org/abs/2205.11916

[https://arxiv.org/abs/2205.11916](https://arxiv.org/abs/2205.11916)

[\[12\]](https://arxiv.org/abs/2005.11401) [\[42\]](https://arxiv.org/abs/2005.11401) https://arxiv.org/abs/2005.11401

[https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)

[\[13\]](https://arxiv.org/abs/2310.11511) https://arxiv.org/abs/2310.11511

[https://arxiv.org/abs/2310.11511](https://arxiv.org/abs/2310.11511)

[\[14\]](https://arxiv.org/abs/2210.08726) [\[34\]](https://arxiv.org/abs/2210.08726) https://arxiv.org/abs/2210.08726

[https://arxiv.org/abs/2210.08726](https://arxiv.org/abs/2210.08726)

[\[15\]](https://arxiv.org/abs/2410.05801) [\[35\]](https://arxiv.org/abs/2410.05801) [\[43\]](https://arxiv.org/abs/2410.05801) [\[63\]](https://arxiv.org/abs/2410.05801) https://arxiv.org/abs/2410.05801

[https://arxiv.org/abs/2410.05801](https://arxiv.org/abs/2410.05801)

[\[16\]](https://developers.openai.com/cookbook/articles/openai-harmony/) [\[57\]](https://developers.openai.com/cookbook/articles/openai-harmony/) [\[73\]](https://developers.openai.com/cookbook/articles/openai-harmony/) https://developers.openai.com/cookbook/articles/openai-harmony/

[https://developers.openai.com/cookbook/articles/openai-harmony/](https://developers.openai.com/cookbook/articles/openai-harmony/)

[\[18\]](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips) [\[64\]](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips) https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips

[https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips)

[\[20\]](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide) [\[41\]](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide) [\[47\]](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide) [\[72\]](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide) https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide

[https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide)

[\[21\]](https://developers.openai.com/api/docs/guides/structured-outputs/) [\[53\]](https://developers.openai.com/api/docs/guides/structured-outputs/) https://developers.openai.com/api/docs/guides/structured-outputs/

[https://developers.openai.com/api/docs/guides/structured-outputs/](https://developers.openai.com/api/docs/guides/structured-outputs/)

[\[22\]](https://platform.claude.com/docs/en/build-with-claude/citations) [\[68\]](https://platform.claude.com/docs/en/build-with-claude/citations) https://platform.claude.com/docs/en/build-with-claude/citations

[https://platform.claude.com/docs/en/build-with-claude/citations](https://platform.claude.com/docs/en/build-with-claude/citations)

[\[23\]](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide/) GPT-5.2 Prompting Guide

[https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2\_prompting\_guide/](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide/)

[\[24\]](https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide/) [\[58\]](https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide/) https://developers.openai.com/cookbook/examples/gpt4-1\_prompting\_guide/

[https://developers.openai.com/cookbook/examples/gpt4-1\_prompting\_guide/](https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide/)

[\[25\]](https://developers.openai.com/api/docs/guides/compaction) [\[52\]](https://developers.openai.com/api/docs/guides/compaction) https://developers.openai.com/api/docs/guides/compaction

[https://developers.openai.com/api/docs/guides/compaction](https://developers.openai.com/api/docs/guides/compaction)

[\[26\]](https://developers.openai.com/api/docs/guides/prompt-caching/) [\[51\]](https://developers.openai.com/api/docs/guides/prompt-caching/) https://developers.openai.com/api/docs/guides/prompt-caching/

[https://developers.openai.com/api/docs/guides/prompt-caching/](https://developers.openai.com/api/docs/guides/prompt-caching/)

[\[27\]](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts) [\[37\]](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts) https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts

[https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts)

[\[28\]](https://developers.openai.com/api/docs/guides/tools-web-search/) [\[46\]](https://developers.openai.com/api/docs/guides/tools-web-search/) [\[54\]](https://developers.openai.com/api/docs/guides/tools-web-search/) https://developers.openai.com/api/docs/guides/tools-web-search/

[https://developers.openai.com/api/docs/guides/tools-web-search/](https://developers.openai.com/api/docs/guides/tools-web-search/)

[\[33\]](https://arxiv.org/abs/2303.11366) [\[75\]](https://arxiv.org/abs/2303.11366) https://arxiv.org/abs/2303.11366

[https://arxiv.org/abs/2303.11366](https://arxiv.org/abs/2303.11366)

[\[36\]](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts) https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts

[https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts)

[\[38\]](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) [\[39\]](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) [\[40\]](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) [\[65\]](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations

[https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)

[\[45\]](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) [\[66\]](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) https://docs.anthropic.com/en/docs/build-with-claude/tool-use

[https://docs.anthropic.com/en/docs/build-with-claude/tool-use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)

[\[48\]](https://developers.openai.com/blog/skills-shell-tips/) Shell \+ Skills \+ Compaction: Tips for long-running agents that do real work

[https://developers.openai.com/blog/skills-shell-tips/](https://developers.openai.com/blog/skills-shell-tips/)

[\[49\]](https://developers.openai.com/cookbook/examples/deep_research_api/introduction_to_deep_research_api/) Introduction to deep research in the OpenAI API

[https://developers.openai.com/cookbook/examples/deep\_research\_api/introduction\_to\_deep\_research\_api/](https://developers.openai.com/cookbook/examples/deep_research_api/introduction_to_deep_research_api/)

[\[50\]](https://developers.openai.com/cookbook/examples/prompt_caching_201/) Prompt Caching 201

[https://developers.openai.com/cookbook/examples/prompt\_caching\_201/](https://developers.openai.com/cookbook/examples/prompt_caching_201/)

[\[56\]](https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy/) https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy/

[https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy/](https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy/)

[\[59\]](https://developers.openai.com/cookbook/examples/prompt_migration_guide/) https://developers.openai.com/cookbook/examples/prompt\_migration\_guide/

[https://developers.openai.com/cookbook/examples/prompt\_migration\_guide/](https://developers.openai.com/cookbook/examples/prompt_migration_guide/)

[\[60\]](https://developers.openai.com/api/docs/guides/latest-model/) https://developers.openai.com/api/docs/guides/latest-model/

[https://developers.openai.com/api/docs/guides/latest-model/](https://developers.openai.com/api/docs/guides/latest-model/)

[\[61\]](https://developers.openai.com/api/reference/resources/responses/methods/retrieve/) https://developers.openai.com/api/reference/resources/responses/methods/retrieve/

[https://developers.openai.com/api/reference/resources/responses/methods/retrieve/](https://developers.openai.com/api/reference/resources/responses/methods/retrieve/)

[\[62\]](https://model-spec.openai.com/2025-09-12.html) https://model-spec.openai.com/2025-09-12.html

[https://model-spec.openai.com/2025-09-12.html](https://model-spec.openai.com/2025-09-12.html)

[\[67\]](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) https://platform.claude.com/docs/en/build-with-claude/structured-outputs

[https://platform.claude.com/docs/en/build-with-claude/structured-outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

[\[70\]](https://cloud.google.com/discover/what-is-prompt-engineering) Prompt Engineering for AI Guide | Google Cloud

[https://cloud.google.com/discover/what-is-prompt-engineering](https://cloud.google.com/discover/what-is-prompt-engineering)

[\[71\]](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies) Overview of prompting strategies Â |Â  Generative AI on Vertex AI Â |Â  Google Cloud Documentation

[https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies)

[\[74\]](https://arxiv.org/abs/2302.04761) https://arxiv.org/abs/2302.04761

[https://arxiv.org/abs/2302.04761](https://arxiv.org/abs/2302.04761)

[\[76\]](https://arxiv.org/abs/2310.04406) https://arxiv.org/abs/2310.04406

[https://arxiv.org/abs/2310.04406](https://arxiv.org/abs/2310.04406)

[\[77\]](https://arxiv.org/abs/2310.03714) https://arxiv.org/abs/2310.03714

[https://arxiv.org/abs/2310.03714](https://arxiv.org/abs/2310.03714)

[\[78\]](https://arxiv.org/abs/2212.08073) https://arxiv.org/abs/2212.08073

[https://arxiv.org/abs/2212.08073](https://arxiv.org/abs/2212.08073)