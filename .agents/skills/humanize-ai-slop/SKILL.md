---
name: humanize-ai-slop
description: Transforma texto gerado por IA em conteudo com voz humana autentica. Use SEMPRE que o usuario pedir para humanizar, desrobotizar, dar voz propria, tirar cara de IA, ou melhorar texto que soa generico, chato ou artificial. Ative tambem quando o usuario mencionar AI slop, texto robotico, cliches de IA, ou quando voce mesmo gerou algo que precisa soar menos perfeito e mais humano. Funciona em PT-BR e EN. Pode aplicar vozes de marca especificas (Atomica ou Arthur Meirelles) quando o contexto indicar.
---

# Humanize AI Slop

Transforma texto com cara de IA em comunicacao humana autentica, mantendo a informacao original e o registro apropriado ao contexto.

## O que e AI slop

AI slop e texto gerado por IA que soa genericamente correto, mas sem alma. Caracteristicas comuns:

- **Aberturas vazias**: "No cenario atual...", "No mundo em constante evolucao...", "Em um panorama cada vez mais..."
- **Verbos pesados demais**: "delve", "navigate", "landscape", "tapestry", "leverage", "foster"
- **Estrutura mecanica**: paragrafos exatamente do mesmo tamanho, listas de 3 itens sempre simetricas, conectores forçados ("Ademais", "Dessa forma", "Nesse contexto")
- **Tom excessivamente neutro**: zero opiniao, zero risco, zero emocao
- **Conclusao com lamina de aco**: frase final que resume tudo de forma perfeitamente redonda

## Processo de humanizacao

Siga estes passos na ordem:

1. **Diagnostique** — identifique quais padroes de AI slop estao presentes. Liste mentalmente ou em rascunho.
2. **Defina o registro** — qual e o tom apropriado para este contexto? (profissional mas direto, casual, tecnico mas acessivel, polemico, etc.)
3. **Reescreva do zero** — nao edite paragrafo a paragrafo. Leia, entenda a ideia central, e reescreva como voce explicaria para uma pessoa real.
4. **Adicione voz** — inclua opiniao, preferencia, experiencia pessoal implícita, ou um ponto de vista. Texto humano tem dono.
5. **Varie o ritmo** — misture frases curtas com longas. Quebre regras gramaticais pequenas se isso soar mais natural. Use um parentese, um travessao, uma interrupcao.
6. **Remova a conclusao forçada** — se o texto termina com um resumo perfeito, provavelmente nao precisa dele. Termine com uma pergunta, um convite, ou simplesmente pare.

## Regras de ouro

- **NUNCA invente fatos** para tornar o texto mais interessante.
- **NUNCA mude o nivel de formalidade** para algo inadequado ao contexto. Um email corporativo continua profissional; so deixa de soar como um robo.
- **NUNCA remova conteudo substantivo** so para encurtar. Humanizar nao e simplificar ate a perda de valor.
- **SEMPRE mantenha o idioma original** do texto de entrada.
- **SEMPRE pergunte ao usuario** se ele quer apenas uma passada leve ou uma reescrita profunda.

## Vozes de marca (quando aplicavel)

Se o contexto indicar que o texto e para **Atomica** ou **Arthur Meirelles**, leia a referencia de voz correspondente antes de reescrever. Isso aplica principios ja validados de humanizacao em vez de inventar um tom generico.

- **Para Atomica:** leia `references/atomica-voice-synthesis.md`
- **Para Arthur Meirelles:** leia `references/arthur-voice-synthesis.md`

## Bases de pesquisa (humanizacao aprofundada)

Quando o usuario pedir uma humanizacao aprofundada, quando o contexto for tecnico/editorial, ou quando voce precisar de frameworks estruturados de revisao, leia as sinteses de pesquisa:

- **Framework de revisao em 9 passos, 14 vicios de IA, checklists operacionais e adaptacao ao PT-BR:** leia `references/chatgpt-humanization-research.md`
- **8 dimensoes do texto humano, tecnicas de especificidade, variacao ritmica, construcao de voz e substituicao de termos genericos:** leia `references/kimi-humanization-research.md`

## Exemplos

### Exemplo 1 (PT-BR, generico)

**Input (AI slop):**
No cenario atual da transformacao digital, as empresas precisam navegar por um panorama cada vez mais complexo de ferramentas e solucoes tecnologicas. Ademais, a implementacao de estrategias baseadas em inteligencia artificial representa um diferencial competitivo fundamental para organizacoes que buscam otimizar processos e impulsionar resultados. Dessa forma, e imperativo que liderancas de negocio adotem uma postura proativa em relacao a inovacao tecnologica.

**Output (humanizado):**
A transformacao digital virou um festival de buzzwords. Todo dia surge uma nova ferramenta prometendo revolucionar tudo. Mas aqui esta a verdade que pouca gente conta: a maioria das empresas nao precisa de mais tecnologia — precisa de clareza sobre qual tecnologia de fato resolve o problema delas.

IA nao e mais diferencial; e sobrevivencia. A questao nao e "se" voce vai usar, e "onde" ela realmente paga o almoco. E isso exige lideranca que pare de assistir do camarote e entre em campo.

### Exemplo 2 (EN, generico)

**Input (AI slop):**
In today's fast-paced digital landscape, content creators must leverage cutting-edge tools to stay ahead of the curve. By harnessing the power of AI-driven solutions, creators can unlock new levels of productivity and foster deeper audience engagement. It is essential to adopt a strategic approach that maximizes the potential of emerging technologies.

**Output (humanizado):**
Everyone's rushing to add AI to their workflow. I get it — I tried it too. But after six months of forcing ChatGPT into every step, I realized something: the best content I made last year came from moments where I was annoyed, confused, or genuinely excited about something.

AI helps you move faster. It does not help you matter more. Use it for the tedious stuff. Save your actual brain for the parts where someone might actually remember what you said.

## Anti-padroes

| O que NAO fazer | Por que |
|---|---|
| Substituir cliches de IA por cliches humanos | Trocar "landscape" por "jornada" nao resolve nada |
| Tornar tudo informal ou engracado | Um contrato continua sendo um contrato |
| Adicionar girias desnecessarias | "Galera, bora falar de compliance" e pior que o original |
| Forcar imperfeicoes artificiais | Erros de proposito parecem tao falso quanto a IA perfeita |
| Remover toda estrutura | Humanidade nao e caos organizacional |
