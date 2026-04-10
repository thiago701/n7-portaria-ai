# n7-portaria-ai — Documento de Arquitetura

> **Versao:** 2.0 | **Data:** 09/04/2026
> **Principio:** Minimo Viavel Arquitetural — simplicidade como padrao
> **Changelog v2.0:** Tabela acessos com 2FA, correlation_id em todas as tabelas, tipo_acesso simplificado

---

## 1. Visão Arquitetural

O n7-portaria-ai adota a filosofia do **Monólito Modular**: uma aplicação única com fronteiras internas bem definidas entre módulos. Essa escolha é deliberada e justificada:

- **Equipe:** 2 pessoas (mentor + aprendiz)
- **Estágio:** MVP / Aprendizado
- **Complexidade essencial:** Baixa a média (CRUD + IA)
- **Complexidade acidental a evitar:** Microsserviços, orquestração, filas, cache distribuído

> *"A melhor arquitetura é aquela que resolve o problema com o menor número possível de partes móveis."*

---

## 2. Diagrama de Camadas

A arquitetura segue o padrão **Clean Architecture** simplificado em 3 camadas:

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERFACE (Presentation)                   │
│      CustomTkinter (desktop) + Flask (web) + CLI              │
│    interface/gui/main.py │ interface/api/ │ interface/cli/    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                    CORE (Domain)                             │
│             ┌──────────────────────────────┐                │
│             │ models/ (Entidades)                      │    │
│             │ Morador, Visitante, Funcionario,         │    │
│             │ Veiculo, Acesso                          │    │
│             └──────────────────────────────┘                │
│             ┌──────────────────────────────┐                │
│             │ usecase/ (Casos de Uso)      │                │
│             │ Regras de negócio isoladas   │                │
│             └──────────────────────────────┘                │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                    INFRA (Infrastructure)                     │
│          database/ (Acesso a dados, repositórios)            │
│          biometria/ (Futuro: câmera, leitor, APIs)          │
│             SQLite (dev) → PostgreSQL (prod)                │
└─────────────────────────────────────────────────────────────┘

Regra de Dependência: Interface → Core ← Infra
(Interface e Infra dependem de Core, nunca o contrário)
```

---

## 3. Fluxo de uma Requisição

```
Fase 1 (Desktop):                    Fase 5+ (Web):
Usuário (GUI)                        Usuário (Browser)
    │                                    │
    ▼                                    ▼
[interface/gui]      [interface/api]
    │                                    │
    ▼                                    ▼
[core/usecase]  →  Aplica regra  [core/usecase]  →  Aplica regra
    │               de negócio         │               de negócio
    ▼                                    ▼
[infra/database]    [infra/database]
    │               Lê/grava em          │               Lê/grava em
    ▼               SQLite/PostgreSQL    ▼               SQLite/PostgreSQL
[GUI Update]     →  Atualiza tela    [Template]     →  Renderiza HTML
    │                                    │
    ▼                                    ▼
Usuário (GUI)                        Usuário (Browser)
```

**Princípio:** Interface chama Use Case (core), que trabalha com Modelos (core). Nunca o contrário.
Infra implementa consultas e persiste dados conforme solicitado por core.

---

## 4. Banco de Dados — Modelo Conceitual

> **v8.0 (09/04/2026):** Revisão arquitetural DBA — morador N:N residências, 1 assinatura por condomínio, correlation_id SHA-256 em todas as tabelas, LGPD blob por morador.
> **v3.0 (09/04/2026):** Tabelas `funcionarios` e `veiculos` adicionadas (contribuição do aluno Ademilson, revisada e incorporada).

### Tabela: moradores *(atualizada — v8.0)*
| Coluna | Tipo | Restrições |
|--------|------|------------|
| id | INTEGER | PK, autoincrement |
| nome | TEXT | NOT NULL |
| cpf | TEXT | UNIQUE, NOT NULL, CHECK(length=11) |
| telefone | TEXT | |
| dt_nascimento | DATE | Opcional |
| email | TEXT | CHECK(LIKE '%@%.%') |
| foto | BLOB | Foto binária do morador |
| dt_foto_validade | DATE | Validade da foto (renovar a cada 2 anos) |
| biometria | BLOB | Bytes brutos da biometria digital |
| dt_biometria_validade | DATE | Validade da biometria (renovar a cada 2 anos) |
| termos_lgpd | BLOB | Bytes do PDF dos termos aceitos (LGPD Lei 13.709/2018) |
| dt_aceite_lgpd | DATETIME | Timestamp do aceite formal dos termos (NULL = pendente) |
| ativo | BOOLEAN | DEFAULT 1, CHECK IN (0, 1) |
| correlation_id | TEXT | UNIQUE NOT NULL — SHA-256 de 'moradores:{cpf}' |
| dt_criado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| dt_atualizado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |

> **Campos removidos em v8.0:** `numero_residencia`, `bloco`, `quadra`, `andar`, `tipo_morador`, `tipo_moradia`, `interfone`, `observacao`, `assinatura_id` → movidos para `residencias` e `morador_residencia`.

### Tabela: residencias *(nova — v8.0)*
| Coluna | Tipo | Restrições |
|--------|------|------------|
| id | INTEGER | PK, autoincrement |
| codigo_condominio | TEXT | NOT NULL — referência ao condomínio |
| numero_residencia | TEXT | NOT NULL |
| bloco | TEXT | NULL em condomínios horizontais |
| quadra | TEXT | NULL em condomínios verticais |
| andar | INTEGER | NULL em casas |
| tipo_moradia | TEXT | DEFAULT 'apartamento', CHECK IN ('apartamento','casa','comercial','outro') |
| interfone | TEXT | Código do interfone da unidade |
| observacao | TEXT | |
| ativo | BOOLEAN | DEFAULT 1, CHECK IN (0, 1) |
| correlation_id | TEXT | UNIQUE NOT NULL — SHA-256 de 'residencias:{tipo}:{bloco}:{num}' |
| dt_criado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| dt_atualizado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### Tabela: morador_residencia *(nova — v8.0, junction table N:N)*
| Coluna | Tipo | Restrições |
|--------|------|------------|
| id | INTEGER | PK, autoincrement |
| morador_id | INTEGER | FK → moradores.id, NOT NULL |
| residencia_id | INTEGER | FK → residencias.id, NOT NULL |
| tipo_morador | TEXT | DEFAULT 'proprietario', CHECK IN ('proprietario','inquilino') |
| dt_inicio | DATE | NOT NULL DEFAULT CURRENT_DATE |
| dt_fim | DATE | NULL = ainda ativo; CHECK(fim >= inicio) |
| ativo | BOOLEAN | DEFAULT 1, CHECK IN (0, 1) |
| correlation_id | TEXT | UNIQUE NOT NULL |
| dt_criado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| — | — | UNIQUE(morador_id, residencia_id, dt_inicio) |

### Tabela: visitantes *(atualizada — v8.0)*
| Coluna | Tipo | Restricoes |
|--------|------|------------|
| id | INTEGER | PK, autoincrement |
| nome | TEXT | NOT NULL |
| documento | TEXT | NOT NULL |
| tipo_documento | TEXT | DEFAULT 'RG', CHECK IN ('RG','CNH','PASSAPORTE','OUTRO') |
| telefone | TEXT | |
| foto | BLOB | |
| bloqueado | BOOLEAN | DEFAULT 0, CHECK IN (0, 1) |
| motivo_bloqueio | TEXT | |
| dt_validade_inicio | DATE | NULL = sem restricao de inicio |
| dt_validade_fim | DATE | NULL = sem restricao de fim; CHECK(fim >= inicio) |
| correlation_id | TEXT | UNIQUE NOT NULL |
| dt_criado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### Tabela: funcionarios *(nova — v3.0, atualizada v8.0)*
| Coluna | Tipo | Restricoes |
|--------|------|------------|
| id | INTEGER | PK, autoincrement |
| nome | TEXT | NOT NULL |
| cpf | TEXT | UNIQUE, NOT NULL, CHECK(length=11) |
| cargo | TEXT | DEFAULT 'porteiro', CHECK IN ('porteiro','zelador','administrador','outro') |
| setor | TEXT | |
| login | TEXT | UNIQUE, NOT NULL |
| senha_hash | TEXT | NOT NULL, CHECK(length=64) — hash SHA-256, nunca senha em texto puro |
| ativo | BOOLEAN | DEFAULT 1, CHECK IN (0, 1) |
| correlation_id | TEXT | UNIQUE NOT NULL |
| dt_criado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### Tabela: veiculos *(nova — v3.0, atualizada v8.0)*
| Coluna | Tipo | Restricoes |
|--------|------|------------|
| id | INTEGER | PK, autoincrement |
| placa | TEXT | UNIQUE, NOT NULL, CHECK(length >= 7) |
| modelo | TEXT | |
| cor | TEXT | |
| morador_id | INTEGER | FK moradores.id (nullable) |
| funcionario_id | INTEGER | FK funcionarios.id (nullable) |
| visitante_id | INTEGER | FK visitantes.id (nullable) |
| ativo | BOOLEAN | DEFAULT 1, CHECK IN (0, 1) |
| correlation_id | TEXT | UNIQUE NOT NULL |
| dt_criado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### Tabela: acessos *(atualizada — v8.0 com 2FA)*
| Coluna | Tipo | Restricoes |
|--------|------|------------|
| id | INTEGER | PK, autoincrement |
| visitante_id | INTEGER | FK visitantes.id, NOT NULL |
| morador_id | INTEGER | FK moradores.id (nullable) |
| funcionario_id | INTEGER | FK funcionarios.id (nullable) — porteiro que registrou |
| veiculo_id | INTEGER | FK veiculos.id (nullable) — se veio de carro |
| tipo_acesso | TEXT | DEFAULT 'pedestre', CHECK IN ('pedestre','garagem') |
| auth_senha | BOOLEAN | DEFAULT 0 — fator 1: porteiro liberou com senha |
| auth_digital | BOOLEAN | DEFAULT 0 — fator 2: leitor biometrico confirmou |
| auth_facial | BOOLEAN | DEFAULT 0 — fator 3: camera reconheceu rosto |
| motivo | TEXT | NOT NULL |
| dt_entrada_em | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| dt_saida_em | DATETIME | nullable — NULL = ainda dentro |
| porteiro | TEXT | texto livre (compatibilidade) |
| observacoes | TEXT | |
| correlation_id | TEXT | UNIQUE NOT NULL |
| — | — | CHECK(auth_senha + auth_digital + auth_facial >= 1) |

> **v8.0:** Campos `auth_senha`, `auth_digital`, `auth_facial` adicionados para autenticacao multifator. `tipo_acesso` simplificado para ('pedestre','garagem'). `correlation_id` adicionado.

### Relacionamentos
```
moradores    1 ←→ N acessos
visitantes   1 ←→ N acessos
funcionarios 1 ←→ N acessos  (porteiro que registrou)
veiculos     1 ←→ N acessos  (veiculo usado no acesso)

moradores    1 ←→ N veiculos
funcionarios 1 ←→ N veiculos
visitantes   1 ←→ N veiculos
```

---

## 5. Decisões Técnicas Justificadas

### Por que Flask e não FastAPI?
- Flask tem curva de aprendizado mais suave
- Interface desktop com CustomTkinter na Fase 1; interface web (Jinja2) introduzida na Fase 5
- Ecossistema maduro com documentação abundante em português
- FastAPI seria overengineering para o contexto atual

### Por que SQLite e não PostgreSQL desde o início?
- Zero configuração — `import sqlite3` e pronto
- Arquivo único — fácil de versionar e transportar
- Perfeito para aprendizado de SQL
- Migração para PostgreSQL será uma aula valiosa no futuro

### Por que não usar ORM (SQLAlchemy) desde o início?
- SQL puro ensina o que realmente acontece no banco
- ORMs abstraem demais para quem está aprendendo
- SQLAlchemy será introduzido na Fase 3 como evolução natural

### Por que HTMX no futuro e não React/Vue?
- Zero JavaScript complexo — HTML turbinado
- Perfeito para quem já entende HTML
- Sem build tools, sem npm, sem webpack
- Interatividade real sem SPA

---

## 6. Padrões de Código

### Estrutura de Diretórios (Clean Architecture)

```
src/
├── core/                    ← Domain Layer (regras de negócio, sem dependências externas)
│   ├── models/             ← Entidades do domínio
│   │   └── __init__.py     ← Morador, Visitante, Acesso, Usuario
│   └── usecase/            ← Casos de uso (aplicação de regras)
│       └── __init__.py     ← CadastrarMorador, RegistrarAcesso, etc
│
├── infra/                   ← Infrastructure Layer (detalhes técnicos)
│   └── database/           ← Acesso a dados, repositórios
│       ├── __init__.py
│       └── biometria/      ← Futuro: integrações com hardware/APIs
│           ├── camera/
│           └── leitor/
│
└── interface/              ← Presentation Layer (como usuários interagem)
    ├── gui/                ← CustomTkinter (Fase 1-4)
    │   ├── main.py
    │   └── morador/
    ├── api/                ← Flask Routes (Fase 5+)
    │   ├── __init__.py
    │   └── blueprints/
    └── cli/                ← Command Line Interface (opcional)
```

### Nomenclatura
- **Arquivos:** snake_case (`cadastrar_morador.py`)
- **Classes:** PascalCase (`Morador`, `CadastrarMorador`)
- **Funções:** snake_case (`buscar_morador()`)
- **Variáveis:** snake_case (`nome_completo`)
- **Constantes:** UPPER_SNAKE_CASE (`MAX_VISITANTES`)

### Estrutura de Função
```python
def cadastrar_morador(nome: str, cpf: str, numero_residencia: str) -> dict:
    """
    Cadastra um novo morador no sistema.

    Args:
        nome: Nome completo do morador
        cpf: CPF do morador (somente números)
        numero_residencia: Número do apartamento/residência

    Returns:
        Dicionário com dados do morador cadastrado

    Raises:
        ValueError: Se CPF já existir no sistema
    """
    # Validação
    # Persistência
    # Retorno
```

### Commits Git
```
tipo: descrição curta

Corpo explicativo (quando necessário)

Exemplos de tipo: feat, fix, docs, style, refactor, test
```

---

## 7. Evolução Planejada

Mantendo a estrutura **Clean Architecture** como base em todas as fases:

```
Fase 1 (Abril)     →  core + infra + interface/gui
                      Python puro + SQL puro + CustomTkinter

Fase 2 (Maio)      →  Expansão de core/usecase + Formulários avançados GUI

Fase 3 (Junho)     →  core/usecase com IA + infra/biometria (APIs)

Fase 4 (Julho)     →  core expandido + Dashboard em GUI
                      WebSockets em infra (opcional)

Fase 5 (Agosto)    →  interface/api (Flask) + interface/gui (mantém CustomTkinter)
                      Testes para core + SQLAlchemy em infra
                      PostgreSQL em produção

Fase 6 (Set-Out)   →  Segurança (autenticação em core/usecase)
                      Testes de integração + Deploy completo
```

**Princípio constante:** core sempre sem dependências externas. interface e infra evoluem
mantendo a separação clara de responsabilidades.

---

*Arquitetura viva — será atualizada a cada fase do projeto.*

### Tabela: config_acesso_morador *(atualizada — v8.0)*
| Coluna | Tipo | Restrições |
|--------|------|------------|
| id | INTEGER | PK, autoincrement |
| morador_id | INTEGER | FK → moradores.id, UNIQUE (1:1) |
| fatores_requeridos | INTEGER | DEFAULT 1, CHECK IN (1, 2) |
| permite_senha | BOOLEAN | DEFAULT 1, CHECK IN (0, 1) |
| permite_digital | BOOLEAN | DEFAULT 1, CHECK IN (0, 1) |
| permite_facial | BOOLEAN | DEFAULT 0, CHECK IN (0, 1) |
| correlation_id | TEXT | UNIQUE NOT NULL — SHA-256 de 'config_acesso_morador:{morador_id}' |
| dt_criado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| dt_atualizado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| — | — | CHECK(permite_senha + permite_digital + permite_facial >= 1) |

### Tabela: assinatura_condominio *(revisada — v8.0)*
> **Mudança v8.0:** De contrato por morador → contrato do CONDOMÍNIO com o serviço n7-portaria-ai. `UNIQUE(codigo_condominio)` garante 1 assinatura por condomínio. `morador_id` renomeado para `responsavel_id` (síndico que assinou).

| Coluna | Tipo | Restrições |
|--------|------|------------|
| id | INTEGER | PK, autoincrement |
| codigo_condominio | TEXT | **UNIQUE**, NOT NULL — 1 assinatura por condomínio |
| nome_condominio | TEXT | NOT NULL — nome comercial do condomínio |
| endereco | TEXT | Nullable |
| responsavel_id | INTEGER | FK → moradores.id, Nullable — síndico responsável |
| numero_contrato | TEXT | UNIQUE, NOT NULL |
| contrato | BLOB | Bytes do PDF do contrato digitalizado |
| dt_ativacao | DATE | Nullable — NULL quando status = 'pendente' |
| dt_vigencia_inicio | DATE | NOT NULL |
| dt_vigencia_fim | DATE | Nullable — NULL = prazo indefinido; CHECK(fim >= inicio) |
| status | TEXT | DEFAULT 'ativo', CHECK IN ('ativo','pendente','vencido','cancelado') |
| observacoes | TEXT | |
| correlation_id | TEXT | UNIQUE NOT NULL — SHA-256 de 'assinatura_condominio:{codigo}:{contrato}' |
| dt_criado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| dt_atualizado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### Relacionamentos (atualizado — v8.0)
```
moradores    N ←→ N residencias        (via morador_residencia — junction table)
moradores    1 ←→ N acessos
visitantes   1 ←→ N acessos
funcionarios 1 ←→ N acessos           (porteiro que registrou)
veiculos     1 ←→ N acessos           (veiculo usado no acesso)

moradores    1 ←→ N veiculos
funcionarios 1 ←→ N veiculos
visitantes   1 ←→ N veiculos

moradores    1 ←→ 1 config_acesso_morador        (política de segurança individual)
condominio   1 ←→ 1 assinatura_condominio        (UNIQUE codigo_condominio — 1 contrato por condo)
moradores    1 ←→ 1 assinatura_condominio        (responsavel_id — síndico que assinou)
```
> **v8.0:** A referência bidirecional `moradores.assinatura_id` foi removida. A assinatura agora pertence ao **condomínio** (não ao morador individual). `UNIQUE(codigo_condominio)` garante no banco que um condomínio não pode ter dois contratos simultâneos.
