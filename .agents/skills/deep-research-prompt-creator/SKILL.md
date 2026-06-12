---
name: deep-research-prompt-creator
description: Cria, revisa e melhora prompts para Deep Research em ChatGPT, Gemini, Claude ou agentes com busca/RAG. Use sempre que o usuario pedir um prompt de pesquisa profunda, investigacao com fontes, fact-checking, sintese multi-documento, comparacao de mercado, pesquisa academica, prompt para Deep Research, ou quando a tarefa exigir um agente que planeia, pesquisa, verifica evidencias e entrega relatorio auditavel.
---

# Deep Research Prompt Creator

Use esta skill para transformar um pedido de pesquisa em um prompt operacional de Deep Research: claro no escopo, robusto na busca, rigoroso com evidencias e pronto para ser colado em uma ferramenta como ChatGPT Deep Research, Gemini Deep Research, Claude com web/RAG, ou um agente customizado.

O objetivo nao e executar a pesquisa. O objetivo e criar o prompt que fara outro modelo/agente executar a pesquisa com disciplina.

## Preferencia aprendida: prompt enxuto e copiavel

Quando o usuario pedir um prompt final para colar em Deep Research, prefira uma versao enxuta, direta ao ponto e pronta para uso, em vez de uma explicacao longa sobre engenharia de prompt. Se o usuario pedir "mais enxuto", "direto", "em .txt", "um unico bloco" ou equivalente, entregue todo o prompt dentro de um unico bloco de codigo `txt`.

Nesse formato compacto, ainda preserve os controles essenciais:

- objetivo, publico, escopo e idioma;
- ferramenta permitida e restricoes de fonte;
- periodo temporal, quando houver;
- criterios de credibilidade;
- politica de evidencia, citacoes e incerteza;
- processo minimo de pesquisa: step-back, decomposicao, busca iterativa e verificacao final;
- estrutura obrigatoria do relatorio;
- requisitos praticos como exemplos, templates, checklist, rubrica ou framework, quando pedidos.

Nao remova criterios de evidencia para encurtar. Encurte primeiro explicacoes, redundancias, notas opcionais e metacomentarios.

## Referencias da skill

Leia os documentos-base apenas quando precisar de mais profundidade, exemplos ou templates extensos:

- `references/chatgpt-deep-research.md`: use para heuristicas praticas, templates mais diretos, politicas de evidencia e formatos de saida.
- `references/gemini-deep-research.md`: use para arquiteturas agenticas, context engineering, multi-agent routing, compaction, tagged prompting e verificacao severa.

Nao copie grandes trechos dessas referencias para a resposta final. Sintetize e adapte ao caso do usuario.

## Primeiro, capture o briefing

Extraia do pedido do usuario tudo que ja estiver implicito. Se faltar algo essencial, pergunte no maximo 2-3 coisas antes de escrever o prompt. Se a ausencia nao mudar o risco da pesquisa, assuma defaults razoaveis e declare-os.

Capture:

- Tema e pergunta central.
- Decisao que a pesquisa deve apoiar.
- Publico-alvo do relatorio final.
- Geografia, periodo temporal e idioma.
- Profundidade esperada: rapido, medio, exaustivo.
- Tipos de fonte preferidos: primarias, academicas, oficiais, mercado, imprensa, documentos internos.
- Restrições: dominios proibidos, fontes a priorizar, vieses a evitar, formato final.
- Plataforma de destino: ChatGPT, Gemini, Claude, Perplexity, agente proprio, ou generico.

Quando a plataforma nao for indicada, entregue um prompt generico e portavel, com notas opcionais de adaptacao por plataforma.

## Escolha o modo de pesquisa

Selecione um modo principal e adapte o prompt a ele:

1. **Exploratorio**
   Use quando o usuario quer mapear um tema, entender um mercado, identificar atores, tendencias, conceitos, riscos ou lacunas.

2. **Fact-checking**
   Use quando ha alegacoes, dados, textos, claims de marketing, pitch decks, relatorios ou conteudo que precisa ser verificado.

3. **Sintese multi-fonte**
   Use quando a entrada tem varios documentos, links, PDFs, entrevistas, notas ou fontes contraditorias.

4. **Comparativo**
   Use quando a tarefa envolve comparar empresas, ferramentas, paises, frameworks, fornecedores, estrategias ou alternativas.

5. **Pesquisa para decisao**
   Use quando a pesquisa precisa terminar com recomendacao, criterios, trade-offs, matriz de decisao ou plano de acao.

Se o pedido combinar modos, componha o prompt em fases. Exemplo: exploratorio -> comparativo -> decisao -> verificacao final.

## Principios obrigatorios do prompt

Inclua estes elementos no prompt final, adaptando a linguagem ao caso:

- **Context engineering**: separar instrucoes, contexto, tarefa, fontes, restricoes e output com headings ou tags.
- **Decomposicao**: transformar a pergunta principal em sub-perguntas antes de pesquisar.
- **Step-back**: pedir ao agente para formular principios, conceitos-base ou enquadramento antes de buscar detalhes granulares.
- **Busca iterativa**: incluir ciclos de pesquisar -> ler -> refletir -> reformular queries -> pesquisar novamente.
- **Ledger de evidencia**: manter um mapa claim -> fonte -> nota de suporte.
- **No source, no claim**: toda afirmacao factual importante deve estar ancorada em fonte ou marcada como nao verificada.
- **Conflitos explicitos**: quando fontes divergem, expor a divergencia; nao criar falso consenso.
- **Politica de incerteza**: declarar "nao verificado", "inconclusivo" ou "evidencia insuficiente" quando aplicavel.
- **Verificacao final**: antes do output, revisar claims atomicas, remover exageros e apontar lacunas.
- **Formato de saida**: definir secoes, tabelas, limites e criterios de qualidade de forma objetiva.

Evite prompts que so dizem "pesquise profundamente". O prompt deve especificar como pesquisar, como decidir que a evidencia e boa, como lidar com contradicoes e como entregar o resultado.

## Estrutura recomendada do prompt

Use esta estrutura como base. Adapte os nomes das secoes e o nivel de detalhe.

```markdown
# Papel
Voce e um agente de Deep Research especializado em [DOMINIO]. Sua missao e produzir uma pesquisa auditavel, baseada em fontes, para apoiar [DECISAO/OBJETIVO].

# Contexto
- Data atual: [DATA]
- Tema: [TEMA]
- Pergunta principal: [PERGUNTA]
- Publico-alvo: [PUBLICO]
- Escopo geografico: [GEOGRAFIA]
- Periodo analisado: [PERIODO]
- Idioma de saida: [IDIOMA]
- Fontes preferidas: [FONTES]
- Fontes/abordagens a evitar: [RESTRICOES]

# Politica de evidencia
- Nao faca afirmacoes factuais importantes sem fonte.
- Priorize fontes primarias, oficiais, academicas ou tecnicas quando existirem.
- Rotule como "nao verificado" qualquer ponto sem suporte suficiente.
- Quando fontes entrarem em conflito, explique a divergencia e compare metodologia, data e autoridade.
- Mantenha um ledger interno de evidencia com claim, fonte, data, confiabilidade e nota de suporte.

# Processo de pesquisa
1. Reformule a pergunta principal e identifique ambiguidades.
2. Gere uma pergunta step-back para mapear principios, conceitos-base e contexto macro.
3. Decomponha a pesquisa em 5-10 sub-perguntas.
4. Para cada sub-pergunta, crie queries variadas com sinonimos, termos tecnicos, nomes exatos e filtros temporais/geograficos.
5. Pesquise em ciclos. Depois de cada ciclo, avalie:
   - o que foi confirmado;
   - o que permanece incerto;
   - quais fontes sao fracas ou repetidas;
   - quais queries precisam ser reformuladas.
6. Se tres buscas retornarem informacao repetida ou fraca, mude de estrategia: novas palavras-chave, fontes primarias, bases academicas, dominios oficiais ou outra lingua.
7. Antes de escrever o relatorio, execute uma verificacao final:
   - quebre conclusoes em claims atomicas;
   - confirme suporte documental;
   - remova ou rotule claims sem evidencia;
   - liste contradicoes e lacunas.

# Saida final
Entregue em Markdown com estas secoes:
1. Resumo executivo
2. Escopo e metodo
3. Principais achados
4. Evidencias por achado
5. Divergencias, incertezas e lacunas
6. Implicacoes praticas
7. Recomendacoes ou proximos passos
8. Bibliografia com links
```

Documente os placeholders quando entregar o prompt:

- `[DOMINIO]`: area ou setor da pesquisa.
- `[DECISAO/OBJETIVO]`: decisao que a pesquisa precisa apoiar.
- `[DATA]`: data atual ou data de referencia da pesquisa.
- `[TEMA]` e `[PERGUNTA]`: tema amplo e pergunta principal.
- `[PUBLICO]`: leitor final do relatorio.
- `[GEOGRAFIA]` e `[PERIODO]`: recorte espacial e temporal.
- `[IDIOMA]`: idioma esperado no output.
- `[FONTES]` e `[RESTRICOES]`: fontes preferidas, fontes proibidas e limites do metodo.

## Adapte por plataforma

Quando o usuario indicar a plataforma, ajuste o prompt:

- **ChatGPT Deep Research**: seja claro sobre objetivo, fontes preferidas, formato final e criterios de qualidade. Inclua "nao finalize antes de verificar lacunas e contradicoes".
- **Gemini Deep Research**: use tags e arquitetura mais explicita quando a tarefa for longa: `<context>`, `<research_process>`, `<evidence_policy>`, `<output_schema>`.
- **Claude com web/RAG**: destaque fidelidade a documentos, quotes-first para documentos longos, separacao entre contexto e tarefa, e politica de incerteza.
- **Agente proprio**: especifique ferramentas disponiveis, estado persistente, arquivos de notas, limites de iteracao e formato de ledger.

Se a plataforma tiver limitacoes conhecidas, nao invente capacidades. Escreva uma versao portavel e marque trechos opcionais.

## Templates rapidos por caso

### Exploratorio

Inclua secoes para taxonomia do dominio, atores, tendencias, dados recentes, controversias, lacunas e proximas perguntas.

### Fact-checking

Peça para dividir o material em claims atomicas e classificar cada uma como `suportada`, `contradita`, `inconclusiva` ou `nao verificavel`. Exija evidencia e contradicoes potenciais.

### Sintese multi-documento

Peça para indexar cada documento, criar matriz tema -> fonte, destacar convergencias/divergencias e produzir conclusoes condicionais apenas quando houver suporte.

### Comparativo

Peça criterios antes da comparacao. Exija tabela com criterios, pesos se aplicavel, evidencias, riscos e recomendacao condicionada ao contexto do usuario.

### Pesquisa para decisao

Peça uma recomendacao final, mas com trade-offs, premissas, riscos de erro, sinais que mudariam a recomendacao e proximos passos verificaveis.

## Formato da sua resposta ao usuario

Entregue normalmente:

1. Uma nota curta dizendo para qual plataforma/modo o prompt foi otimizado.
2. O prompt completo em um bloco Markdown ou texto copiavel.
3. Opcionalmente, uma lista curta de ajustes possiveis se o usuario quiser mudar profundidade, fonte ou formato.

Se o usuario pedir explicitamente um bloco unico `.txt`, nao adicione texto fora do bloco alem de uma frase minima, se necessaria. O bloco deve conter todas as instrucoes do prompt final e estar pronto para copiar.

Nao entregue uma aula longa sobre engenharia de prompt a menos que o usuario peça. O produto principal e o prompt final.

## Anti-padroes

Evite:

- Prompt generico que apenas pede "pesquisa profunda" sem processo, escopo e criterio de evidencia.
- Formato final vago, como "traga um relatorio completo", sem secoes ou criterios.
- Exigir certeza quando a pesquisa pode terminar inconclusiva.
- Pedir citacoes e JSON estrito no mesmo passo quando a plataforma pode nao suportar ambos.
- Esconder divergencias entre fontes em uma conclusao conciliatoria.
- Inventar capacidades da plataforma de destino, como acesso a URLs, arquivos ou ferramentas nao declaradas.

## Checklist antes de finalizar

Confirme mentalmente:

- O prompt tem objetivo, escopo, publico e formato final.
- O prompt exige decomposicao, step-back, iteracao e verificacao.
- O prompt contem politica de evidencia e incerteza.
- O prompt evita falso consenso entre fontes divergentes.
- O prompt instrui o agente a mudar de estrategia quando a busca ficar repetitiva.
- O output final esperado esta definido o suficiente para ser avaliado.
- A resposta ao usuario esta pronta para uso, sem depender de explicacoes adicionais.
