# Skill Completeness Checklist

Use this checklist before considerar uma skill "pronta" ou antes de iniciar evals. Uma skill incompleta gera resultados inconsistentes e dificulta iteração.

## Estrutura e Arquitetura

- [ ] Diretório da skill nomeado em kebab-case (ex: `prd-creator`, `data-exporter`)
- [ ] Arquivo `SKILL.md` presente na raiz
- [ ] Frontmatter YAML válido com `name` e `description` obrigatórios
- [ ] `name` em kebab-case, max 64 caracteres
- [ ] `description` max 1024 caracteres, sem angle brackets (`<` ou `>`)
- [ ] `description` é "pushy" — menciona não apenas O QUE faz, mas QUANDO usar
- [ ] SKILL.md tem menos de 500 linhas (ideal < 300). Se maior, usar progressive disclosure com `references/`
- [ ] Recursos bundled organizados em `scripts/`, `references/`, `assets/` conforme necessário
- [ ] Progressive disclosure aplicado: SKILL.md aponta para references em vez de conter tudo inline

## Qualidade de Conteúdo

- [ ] Instruções em forma imperativa (comandos diretos ao agente)
- [ ] Explicação do **porquê** por trás das instruções (não apenas MUSTs em capslock)
- [ ] Exemplos de input/output inclusos quando aplicável
- [ ] Templates de output definidos explicitamente quando o formato é fixo
- [ ] Anti-padrões documentados (o que NÃO fazer e por quê)
- [ ] Sem ambiguidade — termos como "rápido", "fácil", "intuitivo" foram evitados ou quantificados
- [ ] Principle of Lack of Surprise atendido — intenção da skill é clara e não enganosa

## Testabilidade

- [ ] 2-3 test prompts realistas identificados
- [ ] Testes salvos em `evals/evals.json` (prompts, expected_output)
- [ ] Assertions quantitativas draftadas (verificáveis objetivamente)
- [ ] Test cases cobrem happy path e edge cases principais
- [ ] Se a skill gera arquivos: teste verifica o arquivo gerado, não apenas o texto da resposta

## Scripts e Automação

- [ ] Scripts em `scripts/` são reutilizáveis e bem documentados
- [ ] Scripts têm shebang e docstring explicando uso
- [ ] Scripts verificam erros e retornam exit codes apropriados
- [ ] Não há hardcoded paths que quebram em outros ambientes

## Validação Final

- [ ] `python scripts/quick_validate.py <skill-dir>` passa sem erros
- [ ] Se SKILL.md > 300 linhas: verificar se references/ poderia absorver parte do conteúdo
- [ ] Se skill gera código: testar se o código executa sem erro óbvio
- [ ] Se skill usa templates: verificar se placeholders estão todos documentados

## Documentação de Referência

- [ ] `references/` contém documentação suplementar claramente nomeada
- [ ] Arquivos de referência > 300 linhas possuem table of contents
- [ ] SKILL.md indica QUANDO ler cada arquivo de referência
- [ ] Não há duplicação de conteúdo entre SKILL.md e references/
