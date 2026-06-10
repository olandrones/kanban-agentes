# 🤖 Agentes — Documentação Canônica

Cada agente tem seu próprio arquivo `.md` aqui. Esta é a **fonte de verdade** sobre quem é cada agente, o que faz, como evolui.

## Convenção

Todo `agente-*.md` segue este template:

```markdown
# [emoji] Agente [Nome]

## Identidade
- Nome, criado em, status, tipo, frequência

## Missão
1-2 frases

## Estado atual
O que está fazendo AGORA (auto-atualizado)

## O que faz / Como age
Detalhamento operacional

## Tendências
Histórico de observações (com datas)

## Teorias
Pressupostos sobre como funciona

## Fazendo certo
Auto-avaliação: acertos

## Fazendo errado / Melhorias pendentes
Auto-avaliação: gaps

## Métricas
Resultados de hoje / ontem / tendência

## Evolução
O que aprendeu → o que vai aprender → próximo passo
```

## Índice

- `agente-manutencao.md` — health check + melhorias (cron 9h BRT)
- `agente-heartbeat.md` — supervisão + reporte 1x/hora (cron `0 * * * *`)
- `agente-pesquisa-oportunidades.md` — coleta repos trending para Oportunidades
- `agente-coaching-comportamento.md` — provocações + diagnóstico para Comportamento
- `agente-productman.md` — desafios + insights para ProductMan

## Princípios

1. **Cada agente é auto-revolutivo** — a cada execução, registra o que fez, avalia, ajusta o próprio .md
2. **Markdown é lei** — toda mudança, aprendizado, métrica vai no .md
3. **Métricas antes de opinião** — Renato quer enxergar resultados, não palavras
4. **Erro é dado** — quando algo falha, registra e aprende
5. **Um agente por missão** — não duplicar. Sub-tarefas = sub-agente.
6. **Reportar > assumir** — quando em dúvida entre agir e perguntar, age pequeno e reporta grande

## Auto-revolução (como cada agente evolui)

A cada execução, o agente:
1. Roda sua rotina
2. Atualiza o estado atual, métricas, tendências
3. Identifica o que aprendeu
4. Escreve no próprio .md (seção "Evolução")
5. Próxima execução lê de novo e continua

Isso vira uma "linha do tempo" de evolução por agente, rastreável em git.
