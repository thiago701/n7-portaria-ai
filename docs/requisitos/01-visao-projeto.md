# n7-portaria-ai — Documento de Visão do Projeto

> **Versao:** 2.0 | **Data:** 09/04/2026 | **Status:** Aprovado
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

### Modulo 1 — Cadastro de Moradores e Residencias
- Cadastro de moradores: dados pessoais (nome, CPF, telefone, e-mail)
- Cadastro de residencias: unidades habitacionais (numero, bloco, quadra, andar, tipo_moradia, interfone)
- Vinculo morador-residencia N:N (um morador pode ter varias unidades, uma unidade pode ter varios moradores)
- Tipo de morador (proprietario/inquilino) definido NO VINCULO, nao no morador
- Listagem, busca e filtros (com JOIN entre moradores, morador_residencia e residencias)
- Edicao e desativacao (soft delete) de moradores
- Foto do morador como BLOB (sera renovada de 2 em 2 anos)
- Biometria digital como BLOB (sera renovada de 2 em 2 anos)
- Conformidade LGPD: armazenamento dos termos aceitos (BLOB) com timestamp do aceite
- Correlation_id SHA-256 para sincronizacao entre bancos

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

### Modulo 6 — Dashboard e Relatorios
- Painel com metricas do dia (entradas, saidas, visitantes)
- Graficos de movimentacao por periodo
- Exportacao de relatorios (PDF/CSV)

### Modulo 7 — Gestao de Funcionarios e Veiculos *(v3.0 — contribuicao do aluno)*
- Cadastro de funcionarios: nome, CPF, cargo, setor, login/senha (hash SHA-256)
- Perfis diferenciados: porteiro, zelador, administrador
- Cadastro de veiculos vinculados a moradores, funcionarios ou visitantes
- Registro de qual funcionario efetuou cada acesso

### Modulo 8 — Seguranca e Autenticacao 2FA *(v8.0)*
- Autenticacao multifator: senha, digital, facial
- Politica de seguranca individual por morador (config_acesso_morador)
- Pelo menos 1 fator obrigatorio em todo registro de acesso
- Configuravel: 1 ou 2 fatores requeridos por morador

### Modulo 9 — Assinatura do Condominio *(v8.0)*
- Contrato do condominio com o servico n7-portaria-ai
- 1 assinatura por condominio (UNIQUE codigo_condominio)
- Status: ativo, pendente, vencido, cancelado
- Armazenamento do PDF do contrato assinado

---

## 6. Requisitos Nao-Funcionais

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

### Estrutura de Pastas do Projeto (atualizada — v2.0)
```
n7-portaria-ai/
├── src/                             # Codigo-fonte (Clean Architecture)
│   ├── core/                        # Domain Layer — sem dependencias externas
│   │   ├── models/                  # Entidades: Morador, Visitante, etc.
│   │   │   ├── base.py              # ModeloBase (campos comuns)
│   │   │   ├── morador.py           # Dataclass Morador (16 campos)
│   │   │   ├── GUIA_MAPEAMENTO.md   # Receita para mapear novas tabelas
│   │   │   └── __init__.py
│   │   └── usecase/                 # Casos de uso (futuro)
│   ├── infra/                       # Infrastructure Layer
│   │   └── database/
│   │       └── biometria/           # Futuro: camera, leitor
│   └── interface/                   # Presentation Layer
│       ├── gui/                     # CustomTkinter (Fase 1-4)
│       │   └── main.py
│       ├── api/                     # Flask Routes (Fase 5+)
│       └── cli/                     # CLI (opcional)
├── aulas/                           # Material didatico por aula
│   └── 2026-04-abril/
│       ├── aula-01/                 # Setup + Ambiente
│       ├── aula-02/                 # DBeaver + SQLite + Dominio Python
│       │   ├── exercicio/
│       │   │   ├── projeto_portaria_completo.sql  # Schema completo (9 tabelas)
│       │   │   ├── criar_banco_final.py           # Gera portaria.db
│       │   │   └── moradores_crud.py              # CRUD com JOINs
│       │   ├── slides/
│       │   └── README.md
│       ├── aula-03/                 # CRUD completo
│       ├── aula-04/                 # Flask REST API (TODOs)
│       └── aula-05/                 # GUI CustomTkinter (TODOs)
├── docs/
│   ├── requisitos/                  # 5 documentos de requisitos
│   ├── roadmap/                     # Roadmap visual
│   └── DESIGN_SYSTEM_SLIDES.md      # Identidade visual dos slides
├── portaria.db                      # Banco SQLite pronto (gerado por criar_banco_final.py)
├── tests/                           # Testes automatizados (futuro)
├── config.py                        # Configuracoes
├── run.py                           # Ponto de entrada
└── requirements.txt                 # Dependencias
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
| Complexidade técnica frustra o aluno | Média | Alto | Fracionar em tarefas pequenas; ce