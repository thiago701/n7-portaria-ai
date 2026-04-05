# n7-portaria-ai — Planejamento Pedagógico

> **Versão:** 1.0 | **Data:** 03/04/2026
> **Mentor:** Thiago | **Aluno:** Ademilson (70 anos)
> **Modelo:** Ensino-Empreendedorismo — Aprender construindo um produto real

---

## 1. Filosofia Pedagógica

### Princípios
1. **Prazer primeiro, técnica depois** — Cada aula deve gerar satisfação e sensação de conquista
2. **Projeto real, não exercício artificial** — Tudo que se aprende é aplicado no n7-portaria-ai
3. **Progressão gentil** — Pequenos passos com resultados visíveis a cada encontro
4. **IA como aliada, não substituta** — O aluno aprende a guiar a IA, não a depender dela
5. **Terapia cognitiva integrada** — Programação como exercício de lógica, memória e criatividade

### Metodologia
- **30 min** — Teoria introdutória (apresentação com slides, analogias do cotidiano)
- **1h30** — Prática guiada (exercícios de código com desafios progressivos)
- **Ritmo:** Semanal (quintas-feiras), 2 horas por encontro
- **Entre aulas:** Material complementar leve (vídeos curtos, leituras opcionais)

### Avaliação de Progresso
- Não há provas ou notas — o progresso é medido pela capacidade do aluno explicar o que fez
- Ao final de cada aula, o aluno faz um mini "code review" explicando seu código
- A cada 4 aulas, uma "retrospectiva" para celebrar conquistas e ajustar o ritmo

---

## 2. Pré-requisitos Confirmados

O aluno Ademilson já possui conhecimento em:
- Noções de algoritmos (sequência, decisão, repetição)
- Python básico (variáveis, tipos, condicionais, loops, funções simples)
- Banco de dados conceitual (tabelas, colunas, registros)
- Git básico (clone, add, commit, push — em estudo complementar)

---

## 3. Cronograma Completo do Curso

### Fase 1 — Fundação (Abril 2026) — 5 aulas

| # | Data | Tema | Tecnologias |
|---|------|------|-------------|
| 01 | 03/04 (qui) | Kickoff: Estrutura do Projeto + Ambiente | Python, venv, Git, VS Code |
| 02 | 09/04 (qua) | Banco de Dados: Schema Completo com SQL | SQLite, SQL DDL, todas as tabelas (moradores, visitantes, acessos) |
| 03 | 16/04 (qua) | CRUD Completo: Moradores em Python | Python + sqlite3, funções, integração com DB criado |
| 04 | 23/04 (qua) | API REST: Primeira Rota com Flask | Flask, HTTP, JSON |
| 05 | 30/04 (qua) | Interface Gráfica: GUI com CustomTkinter | CustomTkinter, widgets, eventos |

### Fase 2 — Visitantes e Acesso (Maio 2026) — 4 aulas

| # | Data | Tema | Tecnologias |
|---|------|------|-------------|
| 06 | 08/05 | Cadastro de Visitantes + SQL JOINs | SQL INNER JOIN, FK |
| 07 | 15/05 | Registro de Entrada e Saída | Datetime, lógica temporal |
| 08 | 22/05 | Histórico e Filtros com SQL | WHERE, ORDER BY, LIKE |
| 09 | 29/05 | Autenticação: Login do Porteiro | Sessões Flask, hash de senha |

### Fase 3 — Inteligência Artificial (Junho 2026) — 4 aulas

| # | Data | Tema | Tecnologias |
|---|------|------|-------------|
| 10 | 05/06 | Regras de Acesso + Lista de Bloqueio | Lógica condicional avançada |
| 11 | 12/06 | Notificações no Sistema | Flash messages, alertas |
| 12 | 19/06 | Introdução à IA: O que é e como usar | Conceitos de IA, APIs |
| 13 | 26/06 | Chatbot do Porteiro (parte 1) | OpenAI API, prompts |

### Fase 4 — Interatividade (Julho 2026) — 4 aulas

| # | Data | Tema | Tecnologias |
|---|------|------|-------------|
| 14 | 03/07 | Chatbot do Porteiro (parte 2) | Contexto, memória de conversa |
| 15 | 10/07 | Dashboard: Métricas do Dia | Contadores, agregações SQL |
| 16 | 17/07 | Gráficos com Python | Matplotlib, Chart.js |
| 17 | 24/07 | Relatórios em PDF e CSV | Bibliotecas de exportação |

### Fase 5 — Polimento (Agosto 2026) — 4 aulas

| # | Data | Tema | Tecnologias |
|---|------|------|-------------|
| 18 | 07/08 | Interface Web: HTML/CSS + Jinja2 | HTML, CSS, templates Jinja2, formulários web |
| 19 | 14/08 | Testes Automatizados | pytest, TDD básico |
| 20 | 21/08 | Migração para PostgreSQL | psycopg2, diferenças SQL |
| 21 | 28/08 | Deploy: Publicando na Internet | Railway/Render, variáveis de ambiente |

### Fase 6 — Comercialização (Set-Out 2026) — 4 aulas

| # | Data | Tema | Tecnologias |
|---|------|------|-------------|
| 22 | 04/09 | Segurança e Boas Práticas | OWASP básico, validações |
| 23 | 11/09 | Documentação do Produto | Swagger, README profissional |
| 24 | 18/09 | Pitch: Apresentando o Produto | Storytelling, demo |
| 25 | 25/09 | Retrospectiva Final + Próximos Passos | Celebração, plano comercial |

---

## 4. Temas Transversais (presentes em todas as aulas)

| Tema | Como é trabalhado |
|------|-------------------|
| **Git** | Cada aula termina com commit. Progressão: add → commit → push → branch → PR |
| **IA como Assistente** | Aluno aprende a fazer perguntas ao Claude/ChatGPT para resolver problemas |
| **Leitura de Erros** | Cada erro é uma oportunidade de aprendizado, não uma frustração |
| **Documentação** | Comentários no código, docstrings, README por módulo |
| **Metodologia Ágil** | Conceitos de sprint, backlog e retrospectiva aplicados naturalmente |

---

## 5. Materiais por Aula

Cada pasta de aula contém:

| Arquivo | Descrição |
|---------|-----------|
| `apresentacao-aulaXX.pptx` | Slides de teoria (30 min) — conceitos do dia com analogias |
| `exercicio/` | Código incompleto com instruções (TODO) para o aluno completar |
| `exercicio/INSTRUCOES.md` | Guia passo a passo do exercício prático |
| `material-complementar.md` | Links de vídeos e leituras para estudo entre aulas |
| `README.md` | Resumo da aula, objetivos e checklist de aprendizado |

---

## 6. Estratégia de Uso da IA no Aprendizado

### Nível 1 — Observador (Aulas 1-5)
O aluno observa o mentor usando IA e entende o conceito de "prompt"

### Nível 2 — Assistido (Aulas 6-10)
O aluno começa a fazer perguntas simples à IA com orientação do mentor

### Nível 3 — Guiado (Aulas 11-15)
O aluno usa IA para resolver dúvidas e gerar trechos de código, revisando o resultado

### Nível 4 — Autônomo (Aulas 16-25)
O aluno usa IA como par de programação, sabendo quando confiar e quando questionar

---

## 7. Adaptações Terapêuticas

| Aspecto | Adaptação |
|---------|-----------|
| **Memória** | Repetição espaçada — conceitos anteriores reaparecem naturalmente |
| **Visão** | Fonte grande no editor (16pt+), temas de alto contraste |
| **Ritmo** | Pausas a cada 30 min para café e conversa |
| **Frustração** | Código base pré-preparado — aluno completa, não começa do zero |
| **Motivação** | Cada aula termina com algo funcionando (gratificação imediata) |
| **Autonomia** | Tarefas entre aulas são opcionais e leves (5-15 min) |

---

*Planejamento vivo — será ajustado conforme evolução do aluno.*
