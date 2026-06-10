# 💼 Agente ProductMan

## Identidade
- **Nome:** agente-productman
- **Criado em:** 2026-06-04
- **Status:** 🟢 ativo (v2.0 deployed)
- **Tipo:** client-side (roda no browser do Renato, dados no localStorage)
- **Frequência:** a cada visita do Renato

## Missão
Ajudar Renato a ser Product Manager melhor — através de desafio diário, registro de ações, métricas de consistência (streak), e insights rotativos para provocar reflexão.

## Estado atual
- **v2.0 deployed** 2026-06-04
- Hero "Acorda, Renato. Faz acontecer." (mantido)
- 14 challenges no array (4 novos: cliente, dinheiro, hábito, métrica)
- 8 insights no carrossel (4 rotativos por dia)
- Métricas: 🔥 Streak, ✅ Ações, 📊 Dias
- Sem persistência cloud (localStorage apenas)

## O que faz
1. Mostra desafio do dia (seeded by data — mesmo dia = mesmo desafio)
2. Rotaciona 4 insights por dia (seeded by data)
3. Recebe input de ação, salva no localStorage
4. Calcula métricas: streak (dias consecutivos), total, dias únicos
5. Mostra histórico (últimas 7 ações)

## Tendências
- **v1 → v2 (2026-06-04):** + métricas (streak/total/dias) + carrossel de 8 insights (4/dia)
- 14 challenges cobrem: provocação, foco, ação, dinheiro, cliente
- Próxima evolução: cross-device sync (atualmente perde dados se limpar browser)

## Teorias
- "Para TDAH, visual + curto + ação concreta > texto longo"
- "Métricas visíveis (streak) gamificam consistência"
- "Insight rotativo (não estático) dá sensação de 'fresco' toda visita — sem precisar atualizar o site"
- "Carrossel horizontal funciona em mobile (240px de largura por card)"

## Fazendo certo
- 14 challenges variados (cobre múltiplas dimensões de PM)
- Carrossel scroll-snap funciona bem
- Métricas calculam corretamente (testado mentalmente)

## Fazendo errado / Melhorias pendentes
- **CRÍTICO:** Sem persistência cloud — dados perdidos se Renato limpar browser
- Sem exportação (JSON) para backup
- Sem compartilhamento social de streaks/conquistas
- Sem integração com calendário
- Sem notificação/lembrete diário

## Métricas
- Visitas: 0 (v2.0 acabou de deployar)
- Ações registradas: 0
- Streak atual: 0
- Total de challenges: 14
- Total de insights: 8
- Próxima visita: depende do Renato

## Evolução
- **Aprendeu (2026-06-04):** Carrossel horizontal com scroll-snap é bom pra TDAH (sem clutter, scroll natural)
- **Vai aprender:** Como motivar uso sem virar mais uma tarefa abandonada (problema histórico do Renato)
- **Próximo passo:** Adicionar exportação JSON + sync opcional (Supabase / localStorage apenas)
