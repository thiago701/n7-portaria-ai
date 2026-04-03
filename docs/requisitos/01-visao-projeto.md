# n7-portaria-ai — Documento de Visão do Projeto

> **Versão:** 1.0 | **Data:** 03/04/2026 | **Status:** Aprovado
> **Autores:** Thiago (Tech Lead / Mentor) & Ademilson (Desenvolvedor / Aprendiz)
> **Organização:** Neural Tech (n7)

---

## 1. Propósito

O **n7-portaria-ai** é um sistema de portaria inteligente para condomínios residenciais, combinando controle de acesso com assistência por Inteligência Artificial. O projeto serve dois objetivos simultâneos:

1. **Produto Comercial** — Entregar uma solução funcional e escalável de gerenciamento de portaria para condomínios, com potencial de comercialização pela Neural Tech.
2. **Projeto Pedagógico** — Servir como veículo de aprendizado de programação para o aluno Ademilson (71 anos), unindo terapia cognitiva, motivação por propósito e desenvolvimento de habilidades técnicas reais.

---

## 2. Problema de Negócio

Condomínios residenciais de pequeno e médio porte enfrentam desafios recorrentes no controle de acesso:

- Registro manual e desorganizado de visitantes
- Falta de histórico de entradas e saídas
- Comunicação falha entre portaria e moradores
- Ausência de relatórios de movimentação
- Custo alto de sistemas tradicionais de portaria

**Oportunidade:** Um sistema acessível, simples e inteligente que digitaliza a portaria, com um assistente IA que agiliza o atendimento e reduz erros humanos.

---

## 3. Visão do Produto

> *"Transformar a portaria de condomínios em um ambiente digital, seguro e inteligente — onde moradores, visitantes e porteiros se conectam com eficiência e simplicidade."*

---

## 4. Público-Alvo

| Perfil | Descrição |
|--------|-----------|
| **Porteiro** | Operador principal do sistema. Registra entradas/saídas, consulta moradores, usa IA como assistente. Porém, há unidades que não tem esse operador, e o nosso aplicativo também tem essa visão. |
| **Morador** | Recebe notificações de visitas, autoriza acessos remotamente, visualiza histórico. |
| **Síndico/Administrador** | Acessa relatórios, gerencia moradores, configura regras do condomínio. |
| **Visitante** | Pessoa registrada na entrada. Não acessa o sistema diretamente. |

---

## 5. Escopo Funcional (Módulos)

### Módulo 1 — Cadastro de Moradores
- Cadastro completo (nome, apartamento, telefone, e-mail)
- Listagem, busca e filtros
- Edição e desativação de moradores
- Foto do morador (será renovada de 2 em 2 anos)
- Biometria Digital (será renovada de 2 em 2 anos)
- Tipo de Morador (inquelino e/ou proprietário)

### Módulo 2 — Registro de Visitantes
- Cadastro do visitante na entrada (nome, documento, motivo, morador visitado)
- Registro de data/hora de entrada e saída
- Histórico de visitas por morador e por período

### Módulo 3 — Controle de Acesso
- Registro de entrada e saída (log)
- Autorização de acesso pelo morador
- Regras de acesso (horários permitidos, lista de bloqueio)

### Módulo 4 — Notificações
- Notificação ao morador quando visitante chega
- Alertas de segurança (tentativa de acesso não autorizado)
- Resumo diário de movimentação

### Módulo 5 — Assistente IA (Portaria Inteligente)
- Chatbot para o porteiro consultar informações rapidamente
- Sugestões automáticas (ex: "Esse visitante já esteve aqui antes")
- Análise de padrões de visitação
- Geração de relatórios por comando de voz/texto

### Módulo 6 — Dashboard e Relatórios
- Painel com métricas do dia (entradas, saídas, visitantes)
- Gráficos de movimentação por período
- Exportação de relatórios (PDF/CSV)

---

## 6. Requisitos Não-Funcionais

| Categoria | Requisito |
|-----------|-----------|
| **Usabilidade** | Interface simples e intuitiva, operável por pessoa sem experiência técnica |
| **Performance** | Resposta em menos de 2 segundos para operações comuns |
| **Segurança** | Dados pessoais protegidos, autenticação obrigatória, logs de auditoria |
| **Disponibilidade** | Sistema funcional offline para operações básicas (cache local) |
| **Escalabilidade** | Suportar de 1 a 500 moradores na versão inicial |
| **Acessibilidade** | Fonte legível, contraste adequado, navegação por teclado |

---

## 7. Stack Tecnológica

Seguindo o princípio do **Mínimo Viável Arquitetural** (Arquitetura Minimalista):

| Camada | Tecnologia | Justificativa |
|--------|------------|---------------|
| **Linguagem** | Python 3.12+ | Familiaridade do aluno, ecossistema rico, simplicidade |
| **Backend** | Flask | Microframework leve, ideal para aprendizado progressivo |
| **Banco de Dados** | SQLite → PostgreSQL | SQLite para desenvolvimento/aprendizado; migração futura |
| **Interface (Fase 1)** | CustomTkinter (GUI desktop) | Feedback visual imediato, ideal para aprendizado |
| **Interface (Fase 5)** | HTML/CSS + Jinja2 → HTMX | Progressão natural para web, sem complexidade de SPA |
| **IA** | OpenAI API / Ollama | Integração simples via API; Ollama para testes offline |
| **Versionamento** | Git + GitHub | Aluno já estuda Git; prática real de fluxo de trabalho |
| **Deploy** | Local → Railway/Render | Desenvolvimento local primeiro; deploy cloud futuro |

---

## 8. Decisões Arquiteturais

### Monólito Modular (não microsserviços)
**Justificativa:** Equipe de 2 pessoas, projeto em fase de aprendizado. A complexidade de microsserviços seria complexidade acidental — o problema de negócio não exige deploy independente nem escala granular. Um monólito bem estruturado com módulos isolados é a escolha correta.

### Estrutura de Pastas do Projeto
```
n7-portaria-ai/
├── app/
│   ├── __init__.py          # Fábrica da aplicação Flask
│   ├── models/              # Modelos de dados (SQLAlchemy ou SQL puro)
│   │   ├── morador.py
│   │   ├── visitante.py
│   │   └── acesso.py
│   ├── routes/              # Rotas/Controllers
│   │   ├── moradores.py
│   │   ├── visitantes.py
│   │   └── dashboard.py
│   ├── services/            # Lógica de negócio
│   │   ├── acesso_service.py
│   │   └── ia_service.py
│   ├── gui/                 # Interface desktop (CustomTkinter)
│   ├── templates/           # HTML/Jinja2 (Fase 5 — módulo web)
│   │   ├── base.html
│   │   ├── moradores/
│   │   └── visitantes/
│   └── static/              # CSS, JS, imagens
├── database/
│   ├── schema.sql           # DDL do banco
│   └── seed.sql             # Dados de teste
├── tests/                   # Testes automatizados
├── docs/                    # Documentação
├── aulas/                   # Materiais de aula
├── config.py                # Configurações
├── run.py                   # Ponto de entrada
└── requirements.txt         # Dependências
```

### Separação de Camadas (Hexagonal Simplificado)
```
Routes (entrada) → Services (regra de negócio) → Models (dados)
```
Sem excesso de interfaces ou abstrações. O isolamento acontece pela organização de pastas e responsabilidades claras.

---

## 9. Fases do Projeto

| Fase | Período | Entregas |
|------|---------|----------|
| **Fase 1 — Fundação** | Abril 2026 | Setup, banco de dados, CRUD moradores, primeira API, GUI desktop (CustomTkinter) |
| **Fase 2 — Visitantes** | Maio 2026 | Cadastro de visitantes, registro de acesso, histórico |
| **Fase 3 — Inteligência** | Junho 2026 | Integração com IA, chatbot do porteiro, sugestões |
| **Fase 4 — Notificações** | Julho 2026 | Sistema de alertas, notificações, regras de acesso |
| **Fase 5 — Dashboard** | Agosto 2026 | Painel de controle, gráficos, relatórios |
| **Fase 6 — Polimento** | Set-Out 2026 | Testes, deploy, documentação final, preparação comercial |

---

## 10. Métricas de Sucesso

### Produto
- Sistema funcional com todos os 6 módulos implementados
- Pelo menos 1 condomínio usando como piloto
- Feedback positivo de usabilidade (porteiro e síndico)

### Pedagógico
- Ademilson capaz de explicar e modificar qualquer parte do código
- Confiança para contribuir em novos projetos da Neural Tech
- Melhora mensurável em memória e disposição (relato do aluno)

---

## 11. Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Complexidade técnica frustra o aluno | Média | Alto | Fracionar em tarefas pequenas; celebrar cada conquista |
| Ritmo lento de desenvolvimento | Alta | Médio | IA acelera partes mecânicas; foco no que ensina |
| Desistência por dificuldade | Baixa | Alto | Terapia pelo prazer; projetos tangíveis que motivam |
| Mudança de requisitos | Média | Baixo | Documentação viva; arquitetura flexível |

---

*Documento aprovado em 03/04/2026. Revisões serão registradas no Git.*
