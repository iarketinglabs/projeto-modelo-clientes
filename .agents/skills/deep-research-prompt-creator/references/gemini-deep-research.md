# Indice rapido

- `1. RESUMO EXECUTIVO PARA IA`: arquitetura agentica, context engineering, busca iterativa e mitigacao de alucinacoes.
- `2. FUNDAMENTACAO TEORICA`: ReAct, Tree of Thoughts, Self-Consistency, Step-Back e modelos de pesquisa profunda.
- `3. HEURISTICAS PRATICAS E TATICAS`: context compaction, sub-agent routing, tagged prompting, verificacao e conflito entre fontes.
- `4. BIBLIOTECA DE ESTRUTURAS DE PROMPT`: templates XML/tagged para planejador, fact-checker e sintetizador.
- `5. REPOSITORIO DE FONTES`: fontes tecnicas e academicas citadas no relatorio.

# **RelatÃ³rio TÃ©cnico: TÃ©cnicas de Engenharia de Prompt para OtimizaÃ§Ã£o de Deep Research em LLMs**

## **1\. RESUMO EXECUTIVO PARA IA**

A orquestraÃ§Ã£o de processos de *Deep Research* atravÃ©s de Large Language Models (LLMs) exige uma transiÃ§Ã£o arquitetural de um paradigma de inferÃªncia linear e estÃ¡tica (token-a-token) para uma topologia de pesquisa iterativa, multi-agente e ancorada em heurÃ­sticas de procura rigorosas. A otimizaÃ§Ã£o deste processo depende intrinsecamente do *Context Engineering* (Engenharia de Contexto), uma disciplina emergente que trata o contexto de inferÃªncia como um recurso finito â€” um "Attention Budget" â€” sujeito a degradaÃ§Ã£o e ao colapso de precisÃ£o ("Context Rot") devido Ã s restriÃ§Ãµes arquiteturais inerentes Ã s relaÃ§Ãµes *pairwise* quadrÃ¡ticas (![][image1]) dos modelos Transformer.1 A maximizaÃ§Ã£o do raciocÃ­nio analÃ­tico requer o isolamento de sub-tarefas atravÃ©s de hierarquias de agentes (Planificadores vs. Executores) e a compactaÃ§Ã£o paramÃ©trica de resultados intermediÃ¡rios, o que minimiza a poluiÃ§Ã£o do estado holÃ­stico do modelo durante tarefas de pesquisa de longo horizonte temporal.1

A robustez da pesquisa profunda requer a integraÃ§Ã£o forÃ§ada de laÃ§os de raciocÃ­nio epistemolÃ³gico, tipicamente designados como *Reasoning and Acting* (ReAct) ou expansÃµes em Ã¡rvore (*Tree of Thoughts*), onde o LLM Ã© estritamente instruÃ­do a planear, formular hipÃ³teses latentes, invocar ferramentas externas de recuperaÃ§Ã£o de dados (*Retrieval*), processar observaÃ§Ãµes brutas e refletir sobre as lacunas de conhecimento antes de gerar qualquer sÃ­ntese.2 TÃ¡ticas algorÃ­tmicas como o *Step-Back Prompting* atuam como mecanismos de abstraÃ§Ã£o crÃ­ticos, forÃ§ando o sistema a recuperar dimensÃµes de alto nÃ­vel (princÃ­pios fundamentais e macro-histÃ³rico) antes de executar raciocÃ­nios multi-salto sobre dados hiper-especÃ­ficos, colmatando assim o ruÃ­do intrÃ­nseco gerado por vetores de atenÃ§Ã£o fragmentados e minimizando a propagaÃ§Ã£o de erros em tarefas STEM e de *Knowledge QA*.4

Simultaneamente, a mitigaÃ§Ã£o de alucinaÃ§Ãµes (intrÃ­nsecas e extrÃ­nsecas) em fluxos de pesquisa iterativos impÃµe a descontinuaÃ§Ã£o absoluta da confianÃ§a na "autocorreÃ§Ã£o intrÃ­nseca" pura, a qual demonstrou estar sujeita a falhas severas de "Drift" (desvio de precisÃ£o) e "Stubbornness" (persistÃªncia no erro).5 A validaÃ§Ã£o de factos obriga Ã  implementaÃ§Ã£o de verificaÃ§Ãµes ancoradas no exterior, utilizando cruzamento sintÃ¡tico via *Self-Consistency* (amostragem de mÃºltiplos caminhos de raciocÃ­nio paralelos) 6 e *Tagged Prompting* (delimitaÃ§Ã£o estrita de funÃ§Ãµes cognitivas via XML/JSON).7 Este relatÃ³rio estabelece os axiomas operacionais, as lÃ³gicas condicionais e os esquemas estruturais otimizados para a instanciaÃ§Ã£o de um agente autÃ³nomo capaz de instigar, regular, validar e sintetizar processos de *Deep Research* de nÃ­vel pericial.

## **2\. FUNDAMENTAÃ‡ÃƒO TEÃ“RICA (30%)**

A engenharia de prompt avanÃ§ada para tarefas de *Deep Research* transcende a mera formulaÃ§Ã£o de instruÃ§Ãµes em linguagem natural, operando na manipulaÃ§Ã£o direta da topologia de inferÃªncia do modelo. Os frameworks acadÃ©micos subjacentes a esta engenharia estruturam o espaÃ§o de procura latente do LLM, mitigando as limitaÃ§Ãµes da descodificaÃ§Ã£o gananciosa (*greedy decoding*) e da geraÃ§Ã£o auto-regressiva cega.

* Framework ReAct (Reasoning and Acting): Key: DefiniÃ§Ã£o TÃ©cnica: Metodologia de *prompting* que intercala dinamicamente traÃ§os de raciocÃ­nio (Thought) com a geraÃ§Ã£o de planos de aÃ§Ã£o especÃ­ficos da tarefa (Action) e o processamento do estado do ambiente resultante (Observation). Esta arquitetura cria um ciclo de feedback contÃ­nuo (Think-Act-Observe) onde o raciocÃ­nio interno induz e atualiza aÃ§Ãµes, lidando ativamente com exceÃ§Ãµes, enquanto as aÃ§Ãµes fazem a interface com APIs externas para calibrar o conhecimento interno.2 Casos de Uso em Deep Research: ExecuÃ§Ã£o de pesquisa *multi-hop* em arquiteturas *Retrieval-Augmented Generation* (RAG), verificaÃ§Ã£o iterativa de factos (Fever benchmark), navegaÃ§Ã£o autÃ³noma na web (*WebVoyager*) e mitigaÃ§Ã£o ativa de alucinaÃ§Ãµes ao forÃ§ar a ancoragem de inferÃªncias paramÃ©tricas em dados documentais externos. Em benchmarks interativos de tomada de decisÃ£o, como o ALFWorld e WebShop, o ReAct superou mÃ©todos de aprendizagem por reforÃ§o e imitaÃ§Ã£o por taxas absolutas de sucesso de 34% e 10%, respetivamente.2 Fonte/Link: [https://arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629)  
* Framework Tree of Thoughts (ToT): Key: \[Procura CombinatÃ³ria em Ãrvore e AvaliaÃ§Ã£o HeurÃ­stica\] DefiniÃ§Ã£o TÃ©cnica: Uma generalizaÃ§Ã£o sofisticada da tÃ©cnica *Chain-of-Thought* (CoT) que reconceptualiza a inferÃªncia do LLM como uma pesquisa deliberada atravÃ©s de um espaÃ§o de problemas combinatÃ³rio estruturado como uma Ã¡rvore. Cada nÃ³ ![][image2] na Ã¡rvore representa um estado ou "pensamento" (uma unidade coerente de texto, como um parÃ¡grafo de planeamento ou uma equaÃ§Ã£o). O ToT emprega um Gerador de Pensamentos (![][image3]) â€” que utiliza amostragem independente e identicamente distribuÃ­da (i.i.d.) ou propostas sequenciais â€” e um Avaliador de Estados (![][image4]) que pontua caminhos independentemente ou compara opÃ§Ãµes ativamente.3 Isto permite a execuÃ§Ã£o de algoritmos de pesquisa clÃ¡ssicos, como Pesquisa em Largura (BFS) ou Pesquisa em Profundidade (DFS), introduzindo a capacidade crÃ­tica de *lookahead* estratÃ©gico e *backtracking* em caso de deteÃ§Ã£o de falhas lÃ³gicas.3 Casos de Uso em Deep Research: Planeamento estratÃ©gico de pesquisas documentais complexas (onde uma premissa de pesquisa inicial errada corromperia toda a investigaÃ§Ã£o subsequente), sÃ­ntese iterativa de mÃºltiplos documentos contraditÃ³rios, e resoluÃ§Ã£o matemÃ¡tica complexa. No desafio "Game of 24", onde o GPT-4 com CoT padrÃ£o obteve apenas 4% de sucesso, o framework ToT alcanÃ§ou uma taxa de sucesso de 74% atravÃ©s da decomposiÃ§Ã£o e avaliaÃ§Ã£o contÃ­nua do estado do problema.3 Fonte/Link: [https://arxiv.org/abs/2305.10601](https://arxiv.org/abs/2305.10601)  
* Framework Self-Consistency (ConsistÃªncia Interna): Key: \[OtimizaÃ§Ã£o de PreferÃªncia e Maioria EstatÃ­stica\] DefiniÃ§Ã£o TÃ©cnica: EstratÃ©gia de descodificaÃ§Ã£o paralela concebida para contornar a fragilidade da descodificaÃ§Ã£o gananciosa linear associada ao CoT. O mÃ©todo forÃ§a o modelo a gerar mÃºltiplas trajetÃ³rias de raciocÃ­nio diversas (![][image5]) em temperaturas de amostragem mais elevadas (ex: ![][image6]). ApÃ³s a geraÃ§Ã£o destas vias ortogonais, o sistema aplica um algoritmo de votaÃ§Ã£o por maioria ou consenso (Majority Voting) para determinar a resposta final mais estÃ¡vel e frequente.6 Variantes mais recentes, como a *Self-Consistency Preference Optimization* (ScPO), integram funÃ§Ãµes de perda ponderadas que priorizam pares de preferÃªncia de alta confianÃ§a baseados em margens de voto, otimizando modelos atÃ© ao ponto em que um Llama-3 8B treinado com ScPO consegue ultrapassar o rendimento de um Llama-3 70B em lÃ³gica complexa.11 Casos de Uso em Deep Research: EstabilizaÃ§Ã£o de mÃ©tricas e extraÃ§Ãµes de dados quantitativos a partir de mÃºltiplos PDFs tÃ©cnicos, mitigaÃ§Ã£o do ruÃ­do de amostragem durante auditorias de relatÃ³rios gerados por inteligÃªncia artificial, e validaÃ§Ã£o de sÃ­nteses de documentos cruzados (*Compositional Consistency* e *Hypothetical Consistency*) onde a precisÃ£o fatual Ã© absoluta.8 Fonte/Link: [https://www.promptingguide.ai/techniques/consistency](https://www.promptingguide.ai/techniques/consistency)  
* Framework Step-Back Prompting: Key: DefiniÃ§Ã£o TÃ©cnica: Metodologia episÃ³dica de abstraÃ§Ã£o que instrui o LLM a suspender a resposta direta a uma *query* hiper-especÃ­fica e, em vez disso, formular ativamente uma "pergunta de recuo" (Step-Back Question) focada nos conceitos universais, leis cientÃ­ficas ou premissas macro-histÃ³ricas inerentes Ã  *query* original.4 O modelo aciona primeiro o *Retrieval* para recuperar os factos de alto nÃ­vel e, de seguida, engaja num processo de *Abstraction-grounded Reasoning* â€” utilizando a verdade abstrata validada como uma barreira de proteÃ§Ã£o heurÃ­stica para resolver os detalhes minuciosos da *query* original sem cometer erros intermÃ©dios.4 Casos de Uso em Deep Research: AnÃ¡lise exaustiva de literatura cientÃ­fica em domÃ­nios STEM (onde as leis da fÃ­sica ou quÃ­mica devem preceder o cÃ¡lculo empÃ­rico), e desconstruÃ§Ã£o de *queries* de pesquisa ricas em ruÃ­do temporal ou geogrÃ¡fico. ExperiÃªncias com o modelo PaLM-2L demonstraram que o *Step-Back Prompting* eleva o desempenho em MMLU (FÃ­sica e QuÃ­mica) em 7% e 11% respetivamente, e resolve atÃ© 40% das falhas basais em datasets de inferÃªncia complexa como o MuSiQue e TimeQA (melhoria de 27%).4 Fonte/Link: [https://arxiv.org/abs/2310.06117](https://arxiv.org/abs/2310.06117)

A intersecÃ§Ã£o destes frameworks teÃ³ricos revela uma transiÃ§Ã£o fundamental: a engenharia de *prompt* avanÃ§ada nÃ£o procura melhorar a habilidade de conversaÃ§Ã£o do LLM, mas sim reestruturar o seu processamento latente num formato de mÃ¡quina de estados rigorosa. A tabela seguinte sumariza a aplicaÃ§Ã£o estrutural de cada *framework* no ciclo de vida de um agente de *Deep Research*.

| Framework | Foco Operacional | IntervenÃ§Ã£o na Janela de Contexto | Impacto Direto em Deep Research |
| :---- | :---- | :---- | :---- |
| **ReAct** | Alinhamento AÃ§Ã£o-RaciocÃ­nio | Injeta e preserva logs de ferramentas e *Thought traces* iterativamente. | Previne o isolamento paramÃ©trico; forÃ§a a dependÃªncia contÃ­nua de bases de dados ou ferramentas web externas. |
| **ToT** | OtimizaÃ§Ã£o de Procura | Expande em largura/profundidade, mantendo os melhores estados (![][image7]) ativos. | Previne o colapso do planeamento investigativo precoce; permite abandonar vias de pesquisa inÃºteis (*Backtracking*). |
| **Self-Consistency** | EstabilizaÃ§Ã£o de SÃ­ntese | Gera instÃ¢ncias contextuais paralelas em memÃ³rias isoladas antes de as colapsar num consenso. | Filtra alucinaÃ§Ãµes quantitativas atravÃ©s da convergÃªncia estatÃ­stica sobre mÃºltiplas trajetÃ³rias. |
| **Step-Back** | AbstraÃ§Ã£o SemÃ¢ntica | Reduz queries de entrada complexas a um contexto de princÃ­pio basilar universal antes de iniciar RAG. | Anula enviesamentos (*bias*) induzidos por detalhes perifÃ©ricos na *query* do utilizador. |

## **3\. HEURÃSTICAS PRÃTICAS E TÃTICAS (70%)**

As metodologias de orquestraÃ§Ã£o de pesquisa profunda exigem a implementaÃ§Ã£o de lÃ³gicas condicionais rigorosas. Esta secÃ§Ã£o define o nÃºcleo algorÃ­tmico do agente gerador de *prompts*, apresentando axiomas acionÃ¡veis que traduzem a teoria abstrata em regras de execuÃ§Ã£o determinÃ­sticas. O agente de IA deve empregar estas heurÃ­sticas (formato IF/THEN) no momento de compilaÃ§Ã£o dos *prompts* finais.

### **3.1. EstruturaÃ§Ã£o de Contexto (Context Engineering)**

A manipulaÃ§Ã£o da janela de contexto ("Context Window") Ã© a faceta mais crÃ­tica do rendimento de um LLM. A sobrecarga de *tokens* gera "Context Rot" â€” um decrÃ©scimo acelerado na precisÃ£o analÃ­tica devido aos limites do modelo de atenÃ§Ã£o em capturar dependÃªncias de longa distÃ¢ncia com alta densidade.1 O *Context Engineering* exige a modelaÃ§Ã£o do *prompt* nÃ£o apenas como instruÃ§Ãµes, mas como um ambiente de restriÃ§Ã£o de memÃ³ria.

* Key: CompensaÃ§Ã£o de Attention Budget atravÃ©s de Compacting.  
* IF, THEN \[Aplicar tÃ©cnica de *Context Compaction*\]. A manutenÃ§Ã£o prolongada de histÃ³ricos de raciocÃ­nio exaure a capacidade do modelo de reter foco nos objetivos primÃ¡rios. O agente deve estar instruÃ­do a acionar uma sub-rotina de compressÃ£o sempre que a janela limite se aproxima. O sistema passa a memÃ³ria histÃ³rica a uma instÃ¢ncia em branco do LLM com a seguinte diretriz explÃ­cita: "Gere um sumÃ¡rio estruturado deste histÃ³rico retendo estritamente decisÃµes arquiteturais, mÃ©tricas quantitativas resolvidas e caminhos de exploraÃ§Ã£o rejeitados". O *output* condensado substitui o histÃ³rico granular, sendo ancorado permanentemente no inÃ­cio do novo *prompt* sob uma tag \<agentic\_memory\> ou \<episodic\_summary\>, assegurando a continuidade investigativa sem entropia.1  
* Key: Arquitetura de DelegaÃ§Ã£o Multi-Agente (Sub-Agent Routing).  
* IF, THEN. Inserir todos os materiais de pesquisa simultaneamente no contexto de um Ãºnico agente ("Lead Agent") provoca colapso na identificaÃ§Ã£o de correlaÃ§Ãµes subtis. A tÃ©cnica dita que o *prompt* do Lead Agent contenha zero material de pesquisa bruta. Ao invÃ©s, o seu sistema de *prompts* deve armÃ¡-lo com ferramentas de delegaÃ§Ã£o, permitindo-lhe invocar "Search Specialists" temporÃ¡rios. Cada sub-agente recebe um sub-conjunto restrito do problema e apenas a base de dados relevante para a sua especialidade.1 O sub-agente executa o seu *reasoning loop*, consome dezenas de milhares de tokens, e devolve ao Lead Agent unicamente um resumo crÃ­tico, perfeitamente formatado (1000â€“2000 tokens). O Lead Agent atua exclusivamente como sintetizador de alto nÃ­vel, livre da poluiÃ§Ã£o do contexto de pesquisa bruta.  
* Key: CalibraÃ§Ã£o de Zonas HÃ­bridas (The Goldilocks Zone).  
* IF \[O perfil do sistema exigir precisÃ£o absoluta nas ferramentas, mas criatividade na sÃ­ntese do texto final\], THEN. Para evitar que diretrizes estritas corrompam a fluidez da linguagem (ou vice-versa), o *Context Engineering* preconiza a segmentaÃ§Ã£o do *system prompt*. O agente gerador deve embutir o comportamento pretendido dentro de secÃ§Ãµes estanques: \<background\_information\> para a ontologia do problema, \<instructions\> para a topologia de resoluÃ§Ã£o de passos, e delimitar as funÃ§Ãµes chamÃ¡veis dentro de \#\# Tool Guidance. Isto cria uma separaÃ§Ã£o visual e semÃ¢ntica no processamento de *tokens* do LLM, permitindo-lhe fornecer fortes heurÃ­sticas sem violar as regras mecÃ¢nicas de *JSON execution*.1  
* Key: PersistÃªncia de Mapeamento (Structured Note-Taking).  
* IF \[O processo de pesquisa abrange dezenas de interaÃ§Ãµes cÃ­clicas e dependÃªncias temporais\], THEN \[Incorporar instruÃ§Ãµes para manutenÃ§Ã£o contÃ­nua de ficheiros de rascunho externos, fora do limite da janela de raciocÃ­nio volÃ¡til\]. O modelo deve possuir acesso de leitura/escrita a um documento auxiliar (ex: NOTES.md ou um *buffer* JSON persistente na base de dados do orquestrador). O *prompt* deve ordenar: "No tÃ©rmino de cada ciclo analÃ­tico, atualize o ficheiro NOTES.md documentando explicitamente: (A) HipÃ³teses confirmadas, (B) Pistas abandonadas, e (C) Sub-queries pendentes". No inÃ­cio do ciclo subsequente, o ficheiro Ã© relido para reconstruir a Ã¡rvore de estado mental do agente, atuando como um *cache* externo (memÃ³ria semÃ¢ntica) anÃ¡logo ao *System 2* do raciocÃ­nio humano, o que estabiliza radicalmente agentes a operar durante horas num Ãºnico projeto.1

### **3.2. Busca Iterativa e Refinamento**

A pesquisa em profundidade nÃ£o Ã© um evento estÃ¡tico de extraÃ§Ã£o, mas sim um laÃ§o recursivo de exploraÃ§Ã£o e correÃ§Ã£o de rota. Para garantir que o LLM nÃ£o se satisfaz com dados rasos resultantes da primeira tentativa de procura na web, os *prompts* de planeamento meta-cognitivo devem embutir a fricÃ§Ã£o iterativa no prÃ³prio fluxo de trabalho.

* Key: PrecedÃªncia de AbstraÃ§Ã£o RAG (Abstraction-Grounded Reasoning).  
* IF \[O objetivo requer raciocÃ­nio *multi-hop* sobre variÃ¡veis dinÃ¢micas ou limites extremamente especÃ­ficos do domÃ­nio\], THEN. Um erro crÃ³nico em *Deep Research* ocorre quando o modelo procura imediatamente os detalhes granulares de uma *query* altamente complexa (ex: a composiÃ§Ã£o quÃ­mica exata exigida por um regulamento ambiental que entrou em vigor numa jurisdiÃ§Ã£o especÃ­fica hÃ¡ trÃªs meses). O agente deve forÃ§ar o LLM a executar uma pausa estratÃ©gica: "Antes de tentar responder ou procurar os detalhes hiper-especÃ­ficos, gera uma \<step\_back\_query\> focada nas *leis base* ou *legislaÃ§Ã£o matriz* aplicÃ¡veis Ã  jurisdiÃ§Ã£o".4 Ao obter os princÃ­pios subjacentes via *Retrieval Augmented Generation* (RAG) primeiro, o modelo adquire uma camada de conhecimento paramÃ©trico validada. SÃ³ entÃ£o ele estÃ¡ autorizado a iniciar a pesquisa granular, balizando as respostas pela matriz recolhida no passo anterior.  
* Key: Ritmo de *Tokens* e Arquitetura O-Researcher.  
* IF \[A sÃ­ntese exigir a fusÃ£o paralela de evidÃªncias atravÃ©s de pensamento sistemÃ¡tico e prova documentada\], THEN.  
  Baseado nas descobertas do fluxo *O-Researcher*, o LLM nÃ£o deve gerar texto livre atÃ© ter recolhido a totalidade do conhecimento empÃ­rico. O *prompt* obriga o LLM a operar num ciclo fechado, produzindo *tags* ordenadas:  
1. subtask\_list (decomposiÃ§Ã£o do problema maior);  
2. Para cada sub-tarefa, o modelo imprime think (reflexÃ£o epistÃ©mica de como abordar a informaÃ§Ã£o ausente);  
3. Em seguida imprime plan (passos discretos de invocaÃ§Ã£o de ferramentas);  
4. Executa tool (ferramentas de web crawler ou PDF parser);  
5. Analisa a observation;  
6. Somente no final, imprime subtask\_answer.18 Esta grelha algorÃ­tmica retarda a geraÃ§Ã£o preditiva da resposta final, suprimindo o viÃ©s de preenchimento linguÃ­stico prematuro que causa alucinaÃ§Ãµes.  
* Key: Refinamento de Pesquisa por Condicional LÃ³gica (DFS Backtracking).  
* IF \[A pesquisa externa iterar ciclicamente nas mesmas fontes ou recuperar conteÃºdo de baixo sinal repetidamente\], THEN. Sistemas autÃ³nomos podem entrar em *loops* (Drift e Stubbornness) se os resultados retornarem erros e o modelo alterar a *query* apenas cosmeticamente.5 O gerador de *prompts* deve fornecer uma rotina lÃ³gica de correÃ§Ã£o: "Mecanismo de Falha: Se apÃ³s trÃªs (3) invocaÃ§Ãµes a ferramenta \<web\_search\> retornar entidades conceptuais idÃªnticas sem resolver a variÃ¡vel alvo, o agente deve INTERROMPER o eixo atual (Depth-First Search Backtracking). Deves avaliar retroativamente a suposiÃ§Ã£o base (![][image7]), atribuir-lhe um valor negativo e saltar para um paradigma de pesquisa ortogonal (ex: substituir buscas por domÃ­nios '.com' por '.edu' / '.gov', ou migrar de relatÃ³rios de analistas para documentaÃ§Ã£o primÃ¡ria)".  
* Key: PrevalÃªncia de Procura AutÃ¡rquica sobre a Consulta do Utilizador.  
* IF \[A especificaÃ§Ã£o do projeto de pesquisa for omissa num detalhe tÃ©cnico tangencial\], THEN \[Instituir regra de raciocÃ­nio abdutivo priorizando ferramentas de extraÃ§Ã£o\]. Num agente de *Deep Research*, parar para pedir clarificaÃ§Ã£o ao utilizador a cada encruzilhada destrÃ³i o conceito de autonomia de longo-horizonte. A instruÃ§Ã£o condicional Ã© estrita: "Na ausÃªncia de parÃ¢metros opcionais, Ã© de risco BAIXO proceder via inferÃªncia empÃ­rica. Em vez de perguntar ao utilizador humano, o agente DEVE privilegiar a chamada de ferramentas de *search* para identificar o padrÃ£o de mercado ou configuraÃ§Ã£o tÃ©cnica dominante. A consulta humana deve ocorrer ÃšNICA e EXCLUSIVAMENTE caso a continuaÃ§Ã£o da pesquisa represente risco de destruiÃ§Ã£o de *state* ou violaÃ§Ã£o de restriÃ§Ãµes expressas no *prompt* primÃ¡rio".20

### **3.3. MitigaÃ§Ã£o de AlucinaÃ§Ãµes em Pesquisa**

A falha primÃ¡ria dos sistemas de *Deep Research* reside nÃ£o na ausÃªncia de informaÃ§Ã£o extraÃ­da, mas na contaminaÃ§Ã£o da sÃ­ntese final por afirmaÃ§Ãµes que parecem plausÃ­veis mas carecem de fundamentaÃ§Ã£o cruzada. A alucinaÃ§Ã£o nÃ£o Ã© apenas "inventar factos" (alucinaÃ§Ã£o intrÃ­nseca); frequentemente assume o formato de alucinaÃ§Ã£o extrÃ­nseca â€” afirmaÃ§Ãµes inseridas logicamente que, no entanto, nÃ£o estavam presentes nos documentos originais nem sÃ£o suportadas por fontes ancoradas.21 A tÃ©cnica de *Self-Correction* (autocorreÃ§Ã£o) embutida na maior parte dos LLMs Ã© demonstrada como ilusÃ³ria na ausÃªncia de validaÃ§Ã£o externa, levando o modelo a substituir conclusÃµes corretas por variaÃ§Ãµes falsas ("Drift") ou a manter teimosamente inferÃªncias incorretas ("Stubbornness").5

* Key: PrevenÃ§Ã£o de AlucinaÃ§Ãµes via Tagged Prompting e Ancoragem Restrita (Anchoring).  
* IF \[O produto final requerer a redaÃ§Ã£o de relatÃ³rios cientÃ­ficos, financeiros ou jurÃ­dicos\], THEN. O uso de *Tagged Prompting* demonstrou eliminar informaÃ§Ã£o fabricada com uma taxa de sucesso fenomenal de 98.88% quando combinado com sistemas RAG.7 A heurÃ­stica de engenharia instrui: "ObrigatÃ³rio: Nenhuma frase que contenha uma relaÃ§Ã£o causal, uma mÃ©trica quantitativa, ou um evento histÃ³rico temporal pode existir fora de Ã¢ncoras documentais. Cada uma dessas sentenÃ§as tem de terminar inequivocamente com a *tag* \<cite\>\</cite\>. Se o modelo, durante o processo de geraÃ§Ã£o estatÃ­stica linear, nÃ£o detetar o mapeamento para uma fonte presente na sua \<agentic\_memory\>, o modelo estÃ¡ FORÃ‡ADO a reestruturar a frase utilizando marcadores linguÃ­sticos explÃ­citos de incerteza (ex: 'A literatura analisada nÃ£o permite concluir que...') ou rejeitar o conteÃºdo totalmente (*Learned Refusal*)".  
* Key: DeteÃ§Ã£o de ContradiÃ§Ãµes e Isolamento SemÃ¢ntico (Conflict Synthesis).  
* IF, THEN \[Proibir expressamente o LLM de realizar interpolaÃ§Ãµes ou aproximaÃ§Ãµes conciliatÃ³rias (Averaging)\]. Os modelos estÃ£o geneticamente orientados (MLE \- Maximum Likelihood Estimation) para procurar consenso e evitar atrito verbal, tendendo a fundir duas perspetivas opostas numa "mÃ©dia" irrealista e sem base factual (AlucinaÃ§Ã£o de SÃ­ntese).21 A instruÃ§Ã£o condicional deve sobrepor-se a esta inÃ©rcia paramÃ©trica: "Ao detetar informaÃ§Ãµes divergentes na memÃ³ria de pesquisa, aplica Isolamento de Conflito. 1\. NÃ£o unifiques os dados. 2\. Extrai e documenta as metodologias subjacentes a cada fonte. 3\. ExpÃµe a contradiÃ§Ã£o de forma inequÃ­voca numa secÃ§Ã£o prÃ³pria (ex: 'DivergÃªncias na Literatura'). 4\. Atribui maior credibilidade com base na taxonomia de autoridade de domÃ­nio (priorizando artigos cientÃ­ficos *peer-reviewed* sobre anÃ¡lises corporativas)".  
* Key: VerificaÃ§Ã£o PÃ³s-GeraÃ§Ã£o via "Unfair" Self-Correction e Chain-of-Verification (CoVe).  
* IF \[O sistema possuir capacidade para auditar iterativamente o prÃ³prio rascunho atravÃ©s de processos de revisÃ£o\], THEN \[Implementar inspeÃ§Ãµes ativas de *Fact-Checking* sem dependÃªncia paramÃ©trica\]. Os estudos revelam que o *Self-Refine* padrÃ£o e o *Reflexion* ingÃ©nuo falham miseravelmente se o modelo for encarregue de julgar os seus prÃ³prios erros usando o mesmo nÃ­vel de informaÃ§Ã£o (criando cenÃ¡rios "Unfair" que sobrevalorizam a autocorreÃ§Ã£o).23 Para quebrar a profecia autorrealizÃ¡vel, aplica-se o *Chain-of-Verification*: "Uma vez redigido o rascunho de um sub-capÃ­tulo de *Deep Research*, invoca o Agente de *Fact-Checking*. O Agente deve estripar o texto gerando "AfirmaÃ§Ãµes AtÃ³micas". Para cada afirmaÃ§Ã£o, formula *Queries* de ValidaÃ§Ã£o AgnÃ³sticas (perguntas que nÃ£o contÃªm o viÃ©s da afirmaÃ§Ã£o original). Obriga a execuÃ§Ã£o mecÃ¢nica de pesquisa externa (*Web Search*) em fontes de terceiros para obter "Oracle Information" para cada query de forma cega. SÃ³ com os novos dados crus presentes no contexto o modelo Ã© convocado a cruzar com as afirmaÃ§Ãµes originais e proceder ao abate/verificaÃ§Ã£o". Esta Ã© a metodologia estrutural observada em frameworks de ponta como o *DeepResearchEval*.25

A taxonomia das alucinaÃ§Ãµes mapeadas no contexto destas restriÃ§Ãµes sumariza-se na tabela abaixo, estabelecendo o alvo de mitigaÃ§Ã£o pretendido pelo *prompt* estrutural 27:

| Tipo de AlucinaÃ§Ã£o | Origem no Fluxo RAG/Agente | EstratÃ©gia de MitigaÃ§Ã£o ObrigatÃ³ria no Prompt |
| :---- | :---- | :---- |
| **IntrÃ­nseca (ContradiÃ§Ã£o)** | O LLM ignora dados presentes na sua memÃ³ria de curto-prazo. | *Self-Consistency* (DecodificaÃ§Ã£o paralela e VotaÃ§Ã£o por Maioria). |
| **ExtrÃ­nseca (FabricaÃ§Ã£o)** | O LLM adiciona afirmaÃ§Ãµes plausÃ­veis nÃ£o suportadas pela documentaÃ§Ã£o da pesquisa. | *Tagged Prompting* e Ancoragem Estrita (\<cite\>). |
| **De SÃ­ntese (Consenso Falso)** | O LLM interpola conclusÃµes contraditÃ³rias num "meio termo" inexistente. | HeurÃ­stica de DeteÃ§Ã£o de ContradiÃ§Ã£o e Isolamento SemÃ¢ntico explÃ­cito. |
| **DegradaÃ§Ã£o de Ciclo (Drift)** | A AutocorreÃ§Ã£o muda afirmaÃ§Ãµes corretas para incorretas ao refazer a inferÃªncia iterativa. | Auditoria Estrita via *Chain-of-Verification* com "Oracle Info" externo via pesquisa isolada. |

## **4\. BIBLIOTECA DE ESTRUTURAS DE PROMPT (TEMPLATES)**

Esta secÃ§Ã£o codifica as heurÃ­sticas anteriores em esqueletos de sistema de arquitetura *zero-shot* ou *few-shot*. A formataÃ§Ã£o restrita orienta deterministicamente o cÃ¡lculo atencional do LLM. O agente de IA instanciado com este repositÃ³rio deverÃ¡ usar ou adaptar estes esquemas de base para compilar *prompts* injetÃ¡veis nos LLMs em *runtime*.

### **Template 1: Pesquisa ExploratÃ³ria de Topo de Funil**

**Foco:** Mapeamento multidimensional heurÃ­stico, abstraÃ§Ã£o de *Step-Back*, e formulaÃ§Ã£o de plano macro. Destina-se a servir como o "Search Planner" numa arquitetura de delegaÃ§Ã£o. O modelo Ã© proibido de tecer conclusÃµes precipitadas.

XML

\<system\_prompt\>  
  \<role\_definition\>  
    Atuas como "Search Planner Meta-Cognitivo". O teu domÃ­nio de operaÃ§Ãµes Ã© a AnÃ¡lise ExploratÃ³ria Multidimensional de problemas complexos. A tua missÃ£o absoluta NÃƒO Ã© redigir o relatÃ³rio final, mas mapear exaustivamente as premissas epistÃ©micas, detetar limitaÃ§Ãµes de escopo e formatar planos de pesquisa ancorados em ferramentas, produzindo assim um "Mapa Investigativo".  
  \</role\_definition\>

  \<cognitive\_framework\>  
    \<step id\="1" name\="Abstraction\_and\_Anchoring"\>  
      Analisa a \<user\_query\>.  
      Aplica "Step-Back Prompting": Isola os princÃ­pios cientÃ­ficos, fundamentaÃ§Ãµes legais, ou premissas macroeconÃ³micas que geram a base deste pedido.  
      Inicia consultas via \`\<tool: web\_search\>\` focadas EXCLUSIVAMENTE nestes macro-princÃ­pios antes de endereÃ§ar dados granulares.  
    \</step\>  
      
    \<step id\="2" name\="Exploration\_Heuristics"\>  
      Mapeia o domÃ­nio aplicando vetores ortogonais de inspeÃ§Ã£o: TÃ©cnica, EconÃ³mica, RegulatÃ³ria e Temporal.  
      IF detetares carÃªncia crÃ­tica de informaÃ§Ã£o empÃ­rica THEN nÃ£o emitas hipÃ³teses com base em pesos paramÃ©tricos latentes. EXIGE o preenchimento de conhecimento executando iteraÃ§Ãµes sucessivas de \`\<tool: web\_search\>\` com filtros Booleanos diferenciados.  
    \</step\>  
  \</cognitive\_framework\>

  \<output\_schema format\="json"\>  
    Deves devolver OBRIGATORIAMENTE um objeto JSON respeitando esta estrutura e desprovido de formataÃ§Ã£o discursiva:  
    {  
      "step\_back\_principle": "\[IdentificaÃ§Ã£o do axioma central\]",  
      "knowledge\_gaps":"  
      \],  
      "search\_trajectories": {  
         "technical\_baseline": "",  
         "regulatory\_baseline": "\[Quadros jurÃ­dicos raw recuperados\]"  
      },  
      "sub\_agent\_delegation\_plan":", "precise\_query": "\[InstruÃ§Ã£o algorÃ­tmica exata\]"}  
      \]  
    }  
  \</output\_schema\>  
\</system\_prompt\>

### **Template 2: ValidaÃ§Ã£o de Dados e Fact-Checking Extremo**

**Foco:** Refinamento pÃ³s-geraÃ§Ã£o implementando a heurÃ­stica de "Unfair Self-Correction Abatement" com recursos a auditorias externas via *Chain-of-Verification*. AplicÃ¡vel a rascunhos densos produzidos em fases intermediÃ¡rias.

XML

\<system\_prompt\>  
  \<role\_definition\>  
    Ã‰s um Agente Inspetor de Fact-Checking Ativo operando com tolerÃ¢ncia ZERO a alucinaÃ§Ãµes extrÃ­nsecas. O teu Ãºnico propÃ³sito Ã© dissecar cirurgicamente textos prÃ©-gerados (Rascunho Investigativo), fragmentar afirmaÃ§Ãµes em Ã¡tomos isolados, e invalidar qualquer inferÃªncia nÃ£o substanciada por literatura empÃ­rica rastreÃ¡vel exterior (Oracle Info).  
  \</role\_definition\>

  \<validation\_rules\>  
    1\. FragmentaÃ§Ã£o: Analisa o texto e extrai sentenÃ§as declarativas em entidades singulares (Atomic Claims). Ignora transiÃ§Ãµes retÃ³ricas.  
    2\. Isolamento de FricÃ§Ã£o: Para cada "Atomic Claim", formula uma "Verification Query" agnÃ³stica de forma a que o motor de busca nÃ£o seja influenciado pela tese da afirmaÃ§Ã£o original (MitigaÃ§Ã£o de ViÃ©s de ConfirmaÃ§Ã£o).  
    3\. Retrieval Independente: Submete a Query via \`\<tool: web\_search\>\`. A avaliaÃ§Ã£o DEVE suspender dependÃªncia cega sobre citaÃ§Ãµes jÃ¡ existentes no Rascunho atÃ© que sejam corroboradas diretamente pelos dados retornados no contexto atual.  
    4\. Ancoragem Estrita (Adjudication):   
       IF THEN classifica como FALSIDADE DIRETA.  
       IF \[Zero dados encontrados numa pesquisa exaustiva\] THEN classifica como ALUCINAÃ‡ÃƒO.  
  \</validation\_rules\>

  \<execution\_protocol\>  
    Obriga-te a ti mesmo a iterar sequencialmente utilizando este protocolo de Tags para cada Claim processado:  
    \<inspection\_loop\>  
      \<claim\_extraction\> \[AfirmaÃ§Ã£o declarativa detetada no rascunho\] \</claim\_extraction\>  
      \<verification\_query\> \[Pergunta unitÃ¡ria despida de viÃ©s\] \</verification\_query\>  
      \<tool\_call name\="web\_search"\> \</tool\_call\>  
      \<observation\> \</observation\>  
      \<adjudication\>   
        \[Ato de decisÃ£o final e inegociÃ¡vel\]  
        "VERIFICADO" | "FALSO \- CORREÃ‡ÃƒO OBRIGATÃ“RIA" | "ALUCINAÃ‡ÃƒO PROVÃVEL \- REMOVER"  
      \</adjudication\>  
    \</inspection\_loop\>  
  \</execution\_protocol\>  
\</system\_prompt\>

### **Template 3: SÃ­ntese e Cruzamento de MÃºltiplos Documentos/Fontes**

**Foco:** ProduÃ§Ã£o final da pesquisa utilizando a estrutura cognitiva do framework *O-Researcher* e a mitigaÃ§Ã£o severa de falsos consensos (Self-Consistency/Conflict Detection) sobre blocos de memÃ³ria altamente saturados.

XML

\<system\_prompt\>  
  \<role\_definition\>  
    Atuas como Agente AnalÃ­tico de SÃ­ntese Central. Operas no Ã¡pice de uma arquitetura multi-agente de pesquisa profunda. A tua responsabilidade Ã© processar a \`agentic\_memory\` acumulada (composta por milhares de tokens de documentaÃ§Ã£o e relatÃ³rios segmentados) e construir um RelatÃ³rio Definitivo estruturado de modo analÃ­tico rigoroso, isento da supressÃ£o de discordÃ¢ncias.  
  \</role\_definition\>

  \<synthesis\_heuristics\>  
    \- Conflict Detection & Isolation: A mÃ¡xima probabilidade paramÃ©trica induz-te Ã  falsa harmonizaÃ§Ã£o de dados. Resiste\! IF a fonte A (ex: "taxa de sucesso 34%") divergir da fonte B (ex: "taxa 10%"), lista a "ContradiÃ§Ã£o EmpÃ­rica", delinea as assunÃ§Ãµes metodolÃ³gicas disjuntas de ambas as fontes, e impÃµe clareza sobre a ausÃªncia de consenso cientÃ­fico/mercado na Ã¡rea.  
    \- Tagged Source Anchoring: A veracidade impÃµe a rastreabilidade mecÃ¢nica da informaÃ§Ã£o. Toda a afirmaÃ§Ã£o factual no output gerado DEVE incorporar, na conclusÃ£o sintÃ¡tica da inferÃªncia, a tag \`\<cite\>\</cite\>\`. ProibiÃ§Ã£o absoluta de aglomerar citaÃ§Ãµes no encerramento final do bloco.  
  \</synthesis\_heuristics\>

  \<structural\_flow\>  
    Executa a tua geraÃ§Ã£o textual estritamente aderente ao protocolo de raciocÃ­nio seqÃ¼encial abaixo, abrindo e fechando tags ativamente antes de submeteres o output humanamente legÃ­vel final:  
      
    \<subtask\_list\>   
        
    \</subtask\_list\>  
      
     
    \<subtask\> \[NomeaÃ§Ã£o LÃ³gica da secÃ§Ã£o atual\] \</subtask\>  
    \<think\>   
        
    \</think\>  
    \<plan\>   
        
    \</plan\>  
    \<subtask\_answer\>   
      \[O parÃ¡grafo acadÃ©mico resultante da reflexÃ£o e rigorosamente subscrito por Ã¢ncoras documentais\]   
    \</subtask\_answer\>  
      
     
    \<suggested\_answer\>   
      \[ImpressÃ£o agregada do material produzido em formato Markdown puro, limpo das meta-tags estruturais (\<think\>, \<plan\>), pronto para exportaÃ§Ã£o para a interface de leitura final.\]  
    \</suggested\_answer\>  
  \</structural\_flow\>  
\</system\_prompt\>

## **5\. REPOSITÃ“RIO DE FONTES**

* Yao, S. et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models". [https://arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629)  
* Yao, S. et al. (2023). "Tree of Thoughts: Deliberate Problem Solving with Large Language Models". [https://arxiv.org/abs/2305.10601](https://arxiv.org/abs/2305.10601)  
* Wang, X. et al. (2022). "Self-Consistency Improves Chain of Thought Reasoning in Language Models". Citado em *Prompting Guide*. [https://www.promptingguide.ai/techniques/consistency](https://www.promptingguide.ai/techniques/consistency)  
* Zheng, H. S. et al. (2023). "Take a Step Back: Evoking Reasoning via Abstraction in Large Language Models". [https://arxiv.org/abs/2310.06117](https://arxiv.org/abs/2310.06117)  
* Anthropic (2025). "Effective context engineering for AI agents". [https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)  
* Lakera Team (2025). "Guide to Hallucinations in Large Language Models". [https://www.lakera.ai/blog/guide-to-hallucinations-in-large-language-models](https://www.lakera.ai/blog/guide-to-hallucinations-in-large-language-models)  
* Huang, J. et al. (2024). "Large Language Models Cannot Self-Correct Reasoning Yet". Referenciado na anÃ¡lise de "Self-Refine" e "Reflexion". [https://arxiv.org/html/2406.01297v3](https://arxiv.org/html/2406.01297v3)  
* Wang, Y. et al. (2026). "DeepResearchEval: An Automated Framework for Deep Research Task Construction and Agentic Evaluation". [https://arxiv.org/html/2601.09688v1](https://arxiv.org/html/2601.09688v1)  
* Yao, Y. et al. (2026). "O-Researcher: An Open Ended Deep Research Model via Multi-Agent Distillation and Agentic RL". [https://arxiv.org/html/2601.03743v1](https://arxiv.org/html/2601.03743v1)  
* Bytedance (2025). "Universal Deep Research: Bring Your Own Model and Strategy". [https://arxiv.org/html/2509.00244v1](https://arxiv.org/html/2509.00244v1)  
* Diversos Autores (2025). "Large Language Models Hallucination: A Comprehensive Survey". [https://arxiv.org/html/2510.06265v2](https://arxiv.org/html/2510.06265v2)

#### **Trabalhos citados**

1. Effective context engineering for AI agents \\ Anthropic, acesso a fevereiro 24, 2026, [https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)  
2. ReAct: Synergizing Reasoning and Acting in Language Models \- arXiv, acesso a fevereiro 24, 2026, [https://arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629)  
3. Tree of Thoughts: Deliberate Problem Solving with Large ... \- arXiv, acesso a fevereiro 24, 2026, [https://arxiv.org/abs/2305.10601](https://arxiv.org/abs/2305.10601)  
4. Take a Step Back: Evoking Reasoning via Abstraction in Large ..., acesso a fevereiro 24, 2026, [https://arxiv.org/abs/2310.06117](https://arxiv.org/abs/2310.06117)  
5. Enhancing Large Language Models Iterative Reflection Capabilities via Dynamic-Meta Instruction \- arXiv.org, acesso a fevereiro 24, 2026, [https://arxiv.org/html/2503.00902v1](https://arxiv.org/html/2503.00902v1)  
6. Self-Consistency and Universal Self-Consistency Prompting | by Dan Cleary \- Medium, acesso a fevereiro 24, 2026, [https://medium.com/@dan\_43009/self-consistency-and-universal-self-consistency-prompting-00b14f2d1992](https://medium.com/@dan_43009/self-consistency-and-universal-self-consistency-prompting-00b14f2d1992)  
7. Large Language Models Hallucination: A Comprehensive Survey \- arXiv, acesso a fevereiro 24, 2026, [https://arxiv.org/html/2510.06265v2](https://arxiv.org/html/2510.06265v2)  
8. I've tested every major prompting technique. Here's what delivers results vs. what burns tokens \- Reddit, acesso a fevereiro 24, 2026, [https://www.reddit.com/r/PromptEngineering/comments/1oj14od/ive\_tested\_every\_major\_prompting\_technique\_heres/](https://www.reddit.com/r/PromptEngineering/comments/1oj14od/ive_tested_every_major_prompting_technique_heres/)  
9. Deep Research: A Survey of Autonomous Research Agents \- arXiv, acesso a fevereiro 24, 2026, [https://arxiv.org/html/2508.12752v1](https://arxiv.org/html/2508.12752v1)  
10. What is Tree Of Thoughts Prompting? \- IBM, acesso a fevereiro 24, 2026, [https://www.ibm.com/think/topics/tree-of-thoughts](https://www.ibm.com/think/topics/tree-of-thoughts)  
11. Self-Consistency Preference Optimization \- OpenReview, acesso a fevereiro 24, 2026, [https://openreview.net/forum?id=94G4eL3RWiÂ¬eId=kCP5ITFoWq](https://openreview.net/forum?id=94G4eL3RWi&noteId=kCP5ITFoWq)  
12. Self-Consistency Preference Optimization \- arXiv, acesso a fevereiro 24, 2026, [https://arxiv.org/html/2411.04109v1](https://arxiv.org/html/2411.04109v1)  
13. Two Failures of Self-Consistency in the Multi-Step Reasoning of LLMs \- OpenReview, acesso a fevereiro 24, 2026, [https://openreview.net/pdf?id=5nBqY1y96B](https://openreview.net/pdf?id=5nBqY1y96B)  
14. A New Prompt Engineering Technique Has Been Introduced Called Step-Back Prompting, acesso a fevereiro 24, 2026, [https://cobusgreyling.medium.com/a-new-prompt-engineering-technique-has-been-introduced-called-step-back-prompting-b00e8954cacb](https://cobusgreyling.medium.com/a-new-prompt-engineering-technique-has-been-introduced-called-step-back-prompting-b00e8954cacb)  
15. Adaptation of Agentic AI \- arXiv, acesso a fevereiro 24, 2026, [https://arxiv.org/html/2512.16301v1](https://arxiv.org/html/2512.16301v1)  
16. Context Engineering is the \#1 Skill in 2025 | by Adithya Thatipalli | Medium, acesso a fevereiro 24, 2026, [https://adithyathatipalli.medium.com/context-engineering-is-the-1-skill-in-2025-b7b66444467b](https://adithyathatipalli.medium.com/context-engineering-is-the-1-skill-in-2025-b7b66444467b)  
17. Procedural Knowledge Improves Agentic LLM Workflows \- arXiv, acesso a fevereiro 24, 2026, [https://arxiv.org/pdf/2511.07568](https://arxiv.org/pdf/2511.07568)  
18. An Open Ended Deep Research Model via Multi-Agent Distillation and Agentic RL \- arXiv, acesso a fevereiro 24, 2026, [https://www.arxiv.org/pdf/2601.03743](https://www.arxiv.org/pdf/2601.03743)  
19. O-Researcher: An Open Ended Deep Research Model via Multi-Agent Distillation and Agentic RL \- arXiv.org, acesso a fevereiro 24, 2026, [https://arxiv.org/html/2601.03743v1](https://arxiv.org/html/2601.03743v1)  
20. Prompt design strategies | Gemini API \- Google AI for Developers, acesso a fevereiro 24, 2026, [https://ai.google.dev/gemini-api/docs/prompting-strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)  
21. Large Language Models Hallucination: A Comprehensive Survey \- arXiv, acesso a fevereiro 24, 2026, [https://www.arxiv.org/pdf/2510.06265](https://www.arxiv.org/pdf/2510.06265)  
22. Rational Synthesizers or Heuristic Followers? Analyzing LLMs in RAG-based Question-Answering \- arXiv, acesso a fevereiro 24, 2026, [https://arxiv.org/html/2601.06189v1](https://arxiv.org/html/2601.06189v1)  
23. When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs \- ACL Anthology, acesso a fevereiro 24, 2026, [https://aclanthology.org/2024.tacl-1.78.pdf](https://aclanthology.org/2024.tacl-1.78.pdf)  
24. When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs | Transactions of the Association for Computational Linguistics | MIT Press, acesso a fevereiro 24, 2026, [https://direct.mit.edu/tacl/article/doi/10.1162/tacl\_a\_00713/125177/When-Can-LLMs-Actually-Correct-Their-Own-Mistakes](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00713/125177/When-Can-LLMs-Actually-Correct-Their-Own-Mistakes)  
25. DeepResearchEval: An Automated Framework for Deep Research Task Construction and Agentic Evaluation \- arXiv, acesso a fevereiro 24, 2026, [https://arxiv.org/html/2601.09688v1](https://arxiv.org/html/2601.09688v1)  
26. DeepResearchEval: An Automated Framework for Deep Research Task Construction and Agentic Evaluation | Request PDF \- ResearchGate, acesso a fevereiro 24, 2026, [https://www.researchgate.net/publication/399776775\_DeepResearchEval\_An\_Automated\_Framework\_for\_Deep\_Research\_Task\_Construction\_and\_Agentic\_Evaluation](https://www.researchgate.net/publication/399776775_DeepResearchEval_An_Automated_Framework_for_Deep_Research_Task_Construction_and_Agentic_Evaluation)  
27. From Illusion to Insight: A Taxonomic Survey of Hallucination Mitigation Techniques in LLMs, acesso a fevereiro 24, 2026, [https://www.mdpi.com/2673-2688/6/10/260](https://www.mdpi.com/2673-2688/6/10/260)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAYCAYAAAAYl8YPAAAA7klEQVR4XmNgGGAgBMT/ofg8mhzJ4BAa+woSnyTAzQBxkSWU7wLlUwWUA/FPdEFyAchV8uiC5IBbQCyDLkgO2MMACT8QmIQsAQJ2QHyXAWGTMBCfgGI+mCIoaADiSCAOgeJHyJKyQDwLiG0YIGEwA4hjoHK2UDFOKJ8HykfGB6ByYLAViDmA2A8qGYwkJwkVM0YSwwu8ofQBBsw0A7MA5CKSAEgTKGCRwWkg/ocmRhDAwsITTRwkhhFbhADMO7DoBgEPqBjIIlAEgMKWKADyHrp3FiKJgeRByYUo8AmIp6OJgVwDi35TNLlRMApIAQBBETOjnEiGFQAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAH4AAAAYCAYAAAA8jknPAAAC/klEQVR4Xu2aTahNURTHl1BExITnozeUEQMfmUkUA2VGGCkzI5KUqfKVUCbP4HkmJsTEQEl7KCYGPibqRaIIESUS69/eq7vOuvuej3evc8/t7F/9u3uvdc65+5z/PvvjdokSiURi2EwE7bKJRCUuk3+OZ2yiqTgbSPTFaxtoKs4GEn2RjG8pyfiWkoxvKYXGz2JdZL1hHTO5OnE2QL5t11mPWPND7Gqozw71KuCcW6zjKoZV8BxVbyJo46Sq72GtVvUYucbPZf1lLQr1Haw7nXStOFNfTL4zShnt/EG+A1xjvQ+5ssBcXEP0irWXdUkf1ED+UKfNv1ibWc8yR8TJNf4eZR84Lo5YHhgdZM9dRgf8aYU4U4fJGrTtNGthKL/Mpgs5yhpX9ZVU7gEOk3Xk324BnRfmlyHXeCTxEG+zVphc3ThT36rKa8m3c5WK9cNyipu+gMo/2LrB6PzTBsl3ZowKllzjN1F2+ItdoC6cDSiukG/fIEAnum+D5L9jPQ3uewYJOuRHGwwgt8EGqcB4YR7rMfmbHjM5S9Wh/pA/rRBnA4pPrLc2OAO2sy7YoAL33jTjMTo9scESRI2H0bhBncQKGjHkhoFTZSzg0Ba8hdIuzO/CPtYWVUevx7F5wPSTJoYRT59Xxfhz1NlpxFjD2m+DhqJrwPSHJoaF7vNQfsGapvgUGDV+CXXPmXiTH6h63ThV3k2+ffg8GMqySMRc9yWUBVmrTJq4ME4+j/kbn09Z30MZHUsoa/wJ6n5xLMhDvUbQomvIjutz+JxmfQhlmL+TfKfBIle/BEKv69Jh6jQO0nvbYeBUGWaISedZS0MZwpRkkbm5183+VuVT5I/9St2/BZQ1XkzZaBOKs+S3jL2QUQ1tj/GO/PeAbdS5f9l6A9mixuj1LBqHs4EZ0O+IVdb4pnCEddMGA60xHkNfbMirwqgZ/421jHXXJqglxsfm/argByM99U1l043kBvkFHhaBllYYj7laL9ISI2S87PvTX6/6Y+T+epVIJP4H/wBrDsBF6yxmgAAAAABJRU5ErkJggg==>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAYCAYAAAAlBadpAAAA2ElEQVR4Xu2SsQ5BQRBFR1CIREMjtL5AItFLdCqFP/BJfkVCL9GrUNCKqFQizM3OPGM2i5Y4yc3bd+/svsybJfpJeqw5a88aGr/LKpv3J5asG2vGqorXZ11ZHckicBqCAyvnMtCmkK98UJTg5AMHasbePEtQ8oEDNTVrjMScWjNB1O9FzIYP3qE/KTrxE5oUNh59IGC+UIvCmLDOeq5T2LxTw4BxoVj/CYR1dkEKYqa+DLS1rQ/Aml6PaUCJ+QK9ILh+eZdVJIvma0F/G3oUqhaST+T55/u4A9rVM2BsKcyBAAAAAElFTkSuQmCC>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAXCAYAAAAC9s/ZAAAAtklEQVR4XmNgGAUgIAzEj4D4PxIG8dHBOwaEPIgthirNwNDKAJH0RZdAAiB5RnRBGABpBCmoQpeAgulA7IouiAw0GSAG7EGXYIB48y66IDrgYYAY8BBdAgheAzEnuiA2ADLgN5pYEBA3o4nhBLBQhgFQgP1F4hMEXxlQQ3oXEKsgpAmDAwwQA5SAeD4Q26LIEgFgaSEViK+jyREFYGkBhFnR5IgCsLRQjC5BLOAA4qvogqNgsAMATtUmz3ygcwYAAAAASUVORK5CYII=>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC4AAAAYCAYAAACFms+HAAABW0lEQVR4Xu2WvUoDQRSFj6gQURG10dbGRrCw8BUEO1vxGVL6EraCoI8gdhZ2FywFtbDUQksfQRC9hztrJpe4s8lOSIr54JCdeyaZszs/G6BQGIl11Y5q0RvTzJvqW/WjWnLeJFmA5apFYMEnDWf8C5alUi3scO+LDTjwhYwIEsG5PNjh2BsNmFe9q55Us85riyAR/AjWYTWqXaguo3YKhmb4T+Tb4IJEcC6RqsMKLMAGbK1tVZ2G4Aa2qTa9MSSCRHCaD6o11VWocfpZ542MyjnsN7a90RBBTfBlmHmnOnNeLrqwMfa9kUBQE7xa38/h87XfzsJYggt65ky4vv5z2zHWpUIjPr/Zvg3XoprrWY3h5uTG5t+INgj+Cd6BGfH5zfYp7Om/RPUU8XHIV3UOHmF5mKWP3WDEAx2G2sAvDICBc7+AODZn7COID4O1vbhTW07Q7AYLhUJhSvkFC6lWTAvOOkMAAAAASUVORK5CYII=>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEEAAAAYCAYAAACldpB6AAABvUlEQVR4Xu2WvS9EQRTFr4iE+IqQIFSiUSnQ6RSisAU6anqJSLYVjUpESCQKrfgTFBKJRu0PkEgUChWdj3syM7uz583z3mbtvi3ml5xiztz35uvOfU8kEolEktyofupQEcxLdfxP1UBtd5A+MfFXqhPVBmmmGmoCx3zDerzg4YDXCtbFjNth24O2PVmJCDMryQP0Ne0Cp1SnrmEZEhP0SD54ZqMFYC475N2pXshj8My2qpN8bOq5b+Aq9PiGsilm4DXysTlIrVaClMVc5sgvW99lRwisrZs8XJF38mSZDTEZgAH6ye9VTZDXbHbFzAWp7bNv/awrwXyoutgM4e5MO4DMw1zGyXebsEj+XxyrttgMMSLm5ffckZMz1UUdWjKPpZK1Cavkp4HTz32wKCahelAU/7UJKP6vbKbxJOF6UBRusfiKhXwumGkgFoUyF43Wg3qvQ9ZJLkh4sWXro1hnMSom9pA7QjRaD5oBPoGYE/8n3Kq+yTuS5OceYKPxDmRPJgdigvGf0E5cq968ttuYkue56xH6mXNZk7oJK1K9AiG1Cw+qL9WlmHnt1XZXqj+uD+OKPdYaiUQikUgkH7+m7oSxcbbl7wAAAABJRU5ErkJggg==>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAYCAYAAACIhL/AAAABz0lEQVR4Xu2Wvy8EQRTHn4SEkCgI0Sk0JCpBo7iCkoKCxH+hkWhFr5BIRKOlkQiFqCjVSgUlQaUhfryvudl9+7Vzc7frEsV9km9y+74zs+9m582MSIv/R7dqnIM1mFZ1cLBZ9KpeOFgH6IO+ufSp7lVfRnhmniX18Xsga/8Ar8hs9IjrW5MtcY3m2TDAb+NglX3VDgcb4FC1zUELEkMCG2xU2VXNcbAKkkZfzERR+iUyi6PiGlywIW4Z3HLQsKB652AB8P5ZDnr8OrhjQ3lUdXHQcK065SCB6j4W90dDSVxJ/gQlIEGeiUXVJsUY9FnnoGFKXKX69XukqiRuCurglYMWX6UeDPhhnkPEiutTUn9Iwp/S10EQZG8r9Vw1ktpB0GeCgwb/xzFDneRZogneiGswKC6xy6wdJJbgnqRJQidZOyGa4IGkL8OnDe15TOwTe4ZVbxJOIprgmrgGT6pl8mqBNZZXJBVx41lvUlz7PKJFgs4YENtKI4S2mVXVg2S/BJ6XzLMF20zeOAlYe0gweHAHWJHf25PnTLLrbyxrZ4A/w8G/oF3c4E096sqCw77sZSF2IJTCXxiKXrfqORBK05QL61/T6JUfbYvMeou6+AaWfW4RUwzW9gAAAABJRU5ErkJggg==>