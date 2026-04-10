# n7-portaria-ai — Roadmap Visual

> **Atualizado em:** 09/04/2026

---

## Visao Geral do Roadmap

```
ABR 2026          MAI 2026          JUN 2026          JUL 2026          AGO 2026          SET-OUT 2026
--------          --------          --------          --------          --------          ------------
 FASE 1            FASE 2            FASE 3            FASE 4            FASE 5            FASE 6
 FUNDACAO          VISITANTES        INTELIGENCIA      INTERATIVIDADE    POLIMENTO          COMERCIAL

 ████░░░░░░       ░░░░░░░░░░        ░░░░░░░░░░        ░░░░░░░░░░       ░░░░░░░░░░        ░░░░░░░░░░
 2/5 concl.

 Aula 01-05        Aula 06-09        Aula 10-13        Aula 14-17       Aula 18-21        Aula 22-25
 5 encontros       4 encontros       4 encontros       4 encontros      4 encontros       4 encontros
```

---

## Detalhamento por Fase

### FASE 1 — Fundacao (Abril 2026) ████░░░░░░

**Objetivo:** Construir a base do projeto e o primeiro modulo completo (Moradores).

```
Semana 1 (03/04)  [CONCLUIDA] Setup + Ambiente + Estrutura
                               Python venv, Git init, VS Code, hello_portaria.py

Semana 2 (09/04)  [CONCLUIDA] Banco de Dados Completo + Dominio Python
                               DBeaver + SQLite, 9 tabelas, N:N, 2FA, LGPD
                               criar_banco_final.py, portaria.db, morador.py
                               moradores_crud.py com JOINs, GUIA_MAPEAMENTO.md
                               Slides com identidade visual padronizada

Semana 3 (16/04)  [PENDENTE]  CRUD Moradores Completo
                               sqlite3, funcoes, validacoes, sistema_portaria.py

Semana 4 (23/04)  [PENDENTE]  API REST com Flask
                               Rotas, HTTP Methods, JSON

Semana 5 (30/04)  [PENDENTE]  Interface Grafica Desktop
                               CustomTkinter, Widgets, Eventos
```

**Marco:** Modulo de Moradores 100% funcional (backend + GUI desktop)

---

### FASE 2 — Visitantes e Acesso (Maio 2026)

**Objetivo:** Implementar o core do negócio — registro e controle de visitantes.

```
Semana 6 (08/05)  ──── Visitantes + SQL JOINs
Semana 7 (15/05)  ──── Entrada e Saída
Semana 8 (22/05)  ──── Histórico e Filtros
Semana 9 (29/05)  ──── Login do Porteiro
```

**Marco:** Fluxo completo de portaria funcional (sem IA)

---

### FASE 3 — Inteligência Artificial (Junho 2026)

**Objetivo:** Adicionar inteligência ao sistema com IA.

```
Semana 10 (05/06)  ──── Regras de Acesso
Semana 11 (12/06)  ──── Notificações
Semana 12 (19/06)  ──── Introdução à IA
Semana 13 (26/06)  ──── Chatbot Porteiro v1
```

**Marco:** Porteiro consegue conversar com IA para consultar o sistema

---

### FASE 4 — Interatividade (Julho 2026)

**Objetivo:** Dashboard e relatórios visuais.

```
Semana 14 (03/07)  ──── Chatbot v2 (memória)
Semana 15 (10/07)  ──── Dashboard
Semana 16 (17/07)  ──── Gráficos
Semana 17 (24/07)  ──── Relatórios PDF/CSV
```

**Marco:** Sistema completo com visualização e exportação de dados

---

### FASE 5 — Polimento (Agosto 2026)

**Objetivo:** Qualidade, testes e preparação para deploy.

```
Semana 18 (07/08)  ──── Interface Web (HTML/CSS/Jinja2)
Semana 19 (14/08)  ──── Testes
Semana 20 (21/08)  ──── PostgreSQL
Semana 21 (28/08)  ──── Deploy
```

**Marco:** Sistema publicado na internet, acessível de qualquer lugar

---

### FASE 6 — Comercialização (Set-Out 2026)

**Objetivo:** Preparar o produto para uso real e comercialização.

```
Semana 22 (04/09)  ──── Segurança
Semana 23 (11/09)  ──── Documentação
Semana 24 (18/09)  ──── Pitch / Demo
Semana 25 (25/09)  ──── Retrospectiva Final
```

**Marco:** Produto pronto para piloto em condomínio real

---

## Métricas de Acompanhamento

| Indicador | Meta |
|-----------|------|
| Aulas realizadas | 25 de 25 |
| Módulos implementados | 6 de 6 |
| Commits do aluno | 100+ |
| Confiança do aluno (autoavaliação 1-10) | 7+ |
| Produto funcional | Sim, com piloto ativo |

---

## Tecnologias por Fase

```
Fase 1:  Python ─── SQLite ─── Flask ─── CustomTkinter ─── Git
Fase 2:  +SQL JOINs ─── +Sessões ─── +Formulários avançados
Fase 3:  +OpenAI API ─── +Prompts ─── +Lógica condicional avançada
Fase 4:  +Matplotlib ─── +Chart.js ─── +Geração de PDF
Fase 5:  +HTML/CSS ─── +Jinja2 ─── +pytest ─── +PostgreSQL ─── +Deploy cloud
Fase 6:  +OWASP ─── +Swagger ─── +Pitch comercial
```

---

*Roadmap vivo — revisado a cada retrospectiva mensal.*
