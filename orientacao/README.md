# orientacao/

> Documentação interna do **projeto-modelo** — o template/starter kit da Atômica.
> Leia antes de iniciar qualquer projeto de cliente.

---

## O que tem aqui

| Arquivo | Propósito |
|---------|-----------|
| `sobre-o-template.md` | Framework DOE, stack default, regras de ouro, filosofia do template |
| `guia-onboarding.md` | Passo a passo prático: "clonei o repo para um cliente, e agora?" |

---

## Para quem é

- **Membros da equipe Atômica** que vão iniciar novos projetos de cliente
- **Agentes de IA** que precisam entender o contexto do template antes de operar

---

## Estrutura do template

```
projeto-modelo-clientes/
├── orientacao/           # ★ Você está aqui — documentação do template
├── directives/           # Placeholders para o projeto do cliente (substituir ao iniciar)
├── .agents/              # Agentes, skills, comandos (herdados pelo projeto do cliente)
├── executions/           # Onde o código do cliente vai morar
├── tmp/                  # Arquivos temporários
├── .env                  # Secrets e config (preencher por projeto)
└── README.md             # Este arquivo — porta de entrada
```
