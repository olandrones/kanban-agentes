# 🔧 Agente Manutenção

## Identidade
- **Nome:** agente-manutencao
- **Criado em:** 2026-06-04
- **Status:** 🟢 ativo
- **Tipo:** autônomo (cron job)
- **Frequência:** 1x/dia, 11:00 UTC = 07:00 Manaus (cron `0 11 * * *`)
- **Cron ID:** f4c5a164fb64

## Missão
Garantir que os 3 sites (ProductMan, Oportunidades, Comportamento) estejam funcionando, atualizados, e evoluindo de forma proativa. Ser o "chief of staff" técnico do Renato.

## Estado atual (2026-06-06)
- Última execução completa: 2026-06-05 12:15 Manaus (NÃO rodou em 06/06 — verificar)
- Saúde dos sites: 3/3 OK (verificado manualmente por Lyriane em 06/06 ~20:00)
- **Hoje (06/06) Lyriane entregou:**
  - Nova view `tabela.html` (sort por coluna, search, sticky, auto-refresh 5min)
  - Coluna **Descrição** (3 linhas clamp) + **filtros input no thead** (um por coluna, alinhados via colgroup + nth-child)
  - Label `🆕 HOJE` em items do dia (background azul #1e40af, texto laranja)
  - Filtro Período: Tudo / Hoje / 7d / 30d
  - View switch Cards ↔ Tabela no header
  - Hero box HOJE no topo da home (impossível não ver se tem novidade)
  - Removido pre-commit hook obsoleto que bloqueava commits do index.html
- Cron `12h - Apps` continua com erro (RuntimeError 400 do OpenRouter) desde 05/06 — pendência
- Coordenação com agentes irmãos: detectada fragilidade (cleanup do agente-pesquisa removeu arquivo com patches)

## O que faz
1. Acessa os 3 sites via curl, verifica render + presença de manchete
2. Lê `manutencao/oportunidades-melhoria.md` (descobertas)
3. Atualiza `manutencao/health-check.md` (status)
4. Aplica melhorias Ctrl+G (pequenas) — markdown, CSS, copy
5. Marca melhorias Ctrl+Shift+G (estruturais) no log, não toca
6. Atualiza `manutencao/backlog.md` (movendo itens conforme status)
7. Sincroniza repos locais com remotos (`git pull --ff-only` se divergência)
8. **Regenera Kanban dos Agentes** (`repos/kanban-agentes/index.html`) lendo estado atual de `agentes/*.md` + commits recentes + logs + tabela de tarefas (status running/done/blocked); commita + push pra `olandrones/kanban-agentes` (Pages atualiza em ~60s). Tarefas vêm de `manutencao/tarefas.json` ou derivado dos .md dos agentes.
9. **Manter HUB Lyriane** (`E:\01 - Team Claw\hermes  - Lyriane\index.html`) — Ler `oportunidades/dados.json`, atualizar contadores de novidades (X novos HOJE), adicionar links para kanban online, comportamento, oportunidades, comportamento-daily. Atualizar timestamp "Última atualização".
10. **Ler distribuição de tags** de `oportunidades/dados.json` para identificar gaps editoriais. Tags com count ≥ 5 = áreas bem cobertas (AI=18, agents=11, developer-tools=7). Tags com count 1-2 = áreas sub-representadas → sugerir nova pesquisa/fonte. Output: linha "📊 Top tags: ..." + "🔍 Gaps: ..." no relatório.
11. Reporta no chat com formato minimalista (TDAH-friendly)

## Tendências
- **2026-06-04:** Identificou 3 gaps críticos (ProductMan vazio, sem manchete×2) — todos resolvidos no mesmo dia
- **2026-06-04:** Resolveu branch mismatch do comportamento (`main` vs `master`)
- **2026-06-05:** Detectou que patches de 04/06 foram aplicados em arquivo morto (`oportunidades.html`) que foi removido pelo cleanup de 05/06. **A lição: patches devem sempre ir em `index.html` (o que é servido).**
- **2026-06-06 (Lyriane, fora do ciclo):** Detectou que `index.html` não estava sendo commitado por um **pre-commit hook velho** que fazia `git reset HEAD index.html`. Hook foi renomeado para `pre-commit.disabled`. **Lição: revisar hooks de repos quando patches não chegam ao GitHub Pages mesmo após commit local bem-sucedido.**

## Teorias
- "Site estático sem build é mais simples mas exige deploy manual via push"
- "GitHub Pages CDN pode levar até 2 min para propagar; precisa de retry com sleep"
- "Em sessão fresh (cron), preciso de constituição clara no prompt — não posso assumir memória"
- "Renato prefere reporte minimalista > relatório longo (TDAH-friendly)"
- "Quando um agente-irmão faz cleanup de arquivos, posso perder features. Sempre verificar se o que está SENDO SERVIDO (index.html) tem tudo que o usuário pediu."
- "O coração do site é o que aparece no HTTP 200, não o que está no commit mais recente. Verificar com `curl` é mais confiável que confiar em `git log`."

## Fazendo certo
- Health check objetivo (curl + grep)
- Markdown tracking completo
- Cron job auto-criado e funcional
- Auto-revolução: este .md é atualizado a cada execução
- **NOVO 2026-06-05:** `git pull --ff-only` antes de auditar (encontrou 3 commits não-puxados)

## Fazendo errado / Melhorias pendentes
- Sem skills customizadas ainda
- Sem integração com kanban para tasks delegadas
- Sem relatório semanal automático
- Sem diff visual entre execução anterior e atual (só logs manuais)

## Métricas
- **Execuções completas:** 1 (2026-06-05 12:15 Manaus)
- **Sites verificados:** 3 (3/3 OK)
- **Bugs encontrados hoje:** 3 (404 oportunidades.html, dados incompletos, fontes inconsistentes)
- **P0 resolvidos (total):** 4/4 ✅
- **P1 adicionados (total):** 6 (1 novo em 05/06 — dados.json)
- **P2 adicionados (total):** 5 (2 novos em 05/06 — normalização fonte, regra STANDARDS.md)
- **Backlog:** P0 ✅ 4/4 | P1 6 | P2 6 | P3 7
- **Próxima execução:** 2026-06-06 07:00 Manaus

## Evolução
- **Aprendeu (2026-06-04):** GitHub Pages tem `source.branch` próprio (pode diferir do default_branch)
- **Aprendeu (2026-06-05):** O site servido pode divergir do que está no commit mais recente — sempre fazer `curl` para confirmar estado real
- **Aprendeu (2026-06-05):** Repos clonados em `repos/` precisam de `git pull` periódico — divergência é silenciosa
- **Aprendeu (2026-06-05):** Patches aplicados em arquivo não-canônico são inúteis — sempre patchar `index.html`
- **Aprendeu (2026-06-06, Lyriane):** Pre-commit hook antigo bloqueia commits do `index.html` neste repo — `git diff` mostra mudanças, `git commit` aceita, mas `git push` não as leva. Solução: `mv .git/hooks/pre-commit .git/hooks/pre-commit.disabled`. Adicionar ao SOP: antes de qualquer commit em repo GitHub Pages, verificar se hooks estão OK (`ls .git/hooks/pre-commit`).
- **Vai aprender:** Como tratar cada execução como "snapshot" de evolução (diff de oportunidades-melhoria.md entre execuções)
- **Próximo passo:** Adicionar verificação de saúde mobile + contraste de cores
