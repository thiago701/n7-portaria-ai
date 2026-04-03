# n7-portaria-ai — Documento de Arquitetura

> **Versão:** 1.0 | **Data:** 03/04/2026
> **Princípio:** Mínimo Viável Arquitetural — simplicidade como padrão

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

```
┌─────────────────────────────────────────────────────────────┐
│                    APRESENTAÇÃO (Interface)                   │
│      CustomTkinter (desktop) → HTML/CSS + Jinja2 (web)      │
├─────────────────────────────────────────────────────────────┤
│                    ROTAS (Controllers)                        │
│         Flask Blueprints — uma por módulo                    │
│    moradores.py │ visitantes.py │ dashboard.py │ ia.py      │
├─────────────────────────────────────────────────────────────┤
│                    SERVIÇOS (Regras de Negócio)              │
│    acesso_service.py │ notificacao_service.py │ ia_service  │
├─────────────────────────────────────────────────────────────┤
│                    MODELOS (Dados)                            │
│    morador.py │ visitante.py │ acesso.py │ usuario.py       │
├─────────────────────────────────────────────────────────────┤
│                    BANCO DE DADOS                            │
│              SQLite (dev) → PostgreSQL (prod)                │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Fluxo de uma Requisição

```
Fase 1 (Desktop):                    Fase 5+ (Web):
Usuário (GUI)                        Usuário (Browser)
    │                                    │
    ▼                                    ▼
[CustomTkinter]  →  Captura evento   [Flask Route]  →  Recebe requisição HTTP
    │                                    │
    ▼                                    ▼
[Service]        →  Regra de negócio [Service]      →  Regra de negócio
    │                                    │
    ▼                                    ▼
[Model/DB]       →  Lê/grava SQLite  [Model/DB]     →  Lê/grava no banco
    │                                    │
    ▼                                    ▼
[GUI Update]     →  Atualiza tela    [Template]     →  Renderiza HTML
    │                                    │
    ▼                                    ▼
Usuário (GUI)                        Usuário (Browser)
```

---

## 4. Banco de Dados — Modelo Conceitual

### Tabela: moradores
| Coluna | Tipo | Restrições |
|--------|------|------------|
| id | INTEGER | PK, autoincrement |
| nome | TEXT | NOT NULL |
| cpf | TEXT | UNIQUE, NOT NULL |
| apartamento | TEXT | NOT NULL |
| bloco | TEXT | |
| telefone | TEXT | |
| email | TEXT | |
| ativo | BOOLEAN | DEFAULT TRUE |
| criado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| atualizado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### Tabela: visitantes
| Coluna | Tipo | Restrições |
|--------|------|------------|
| id | INTEGER | PK, autoincrement |
| nome | TEXT | NOT NULL |
| documento | TEXT | NOT NULL |
| tipo_documento | TEXT | DEFAULT 'RG' |
| telefone | TEXT | |
| bloqueado | BOOLEAN | DEFAULT FALSE |
| motivo_bloqueio | TEXT | |
| criado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### Tabela: acessos
| Coluna | Tipo | Restrições |
|--------|------|------------|
| id | INTEGER | PK, autoincrement |
| visitante_id | INTEGER | FK → visitantes.id |
| morador_id | INTEGER | FK → moradores.id |
| motivo | TEXT | NOT NULL |
| entrada_em | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| saida_em | DATETIME | |
| autorizado_por | TEXT | |
| porteiro | TEXT | |
| observacoes | TEXT | |

### Tabela: usuarios
| Coluna | Tipo | Restrições |
|--------|------|------------|
| id | INTEGER | PK, autoincrement |
| nome | TEXT | NOT NULL |
| email | TEXT | UNIQUE |
| senha_hash | TEXT | NOT NULL |
| perfil | TEXT | 'porteiro', 'morador', 'admin' |
| ativo | BOOLEAN | DEFAULT TRUE |

### Relacionamentos
```
moradores 1 ←→ N acessos
visitantes 1 ←→ N acessos
usuarios → perfis de acesso ao sistema
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

### Nomenclatura
- **Arquivos:** snake_case (`morador_service.py`)
- **Classes:** PascalCase (`Morador`)
- **Funções:** snake_case (`buscar_morador()`)
- **Variáveis:** snake_case (`nome_completo`)
- **Constantes:** UPPER_SNAKE_CASE (`MAX_VISITANTES`)

### Estrutura de Função
```python
def cadastrar_morador(nome: str, cpf: str, apartamento: str) -> dict:
    """
    Cadastra um novo morador no sistema.

    Args:
        nome: Nome completo do morador
        cpf: CPF do morador (somente números)
        apartamento: Número do apartamento

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

```
Fase 1 (Abril)     →  Python puro + SQL puro + Flask básico + CustomTkinter (GUI)
Fase 2 (Maio)      →  Mais Flask + Formulários avançados + Sessões
Fase 3 (Junho)     →  IA + APIs externas + SQLAlchemy
Fase 4 (Julho)     →  Notificações + WebSockets + Dashboard
Fase 5 (Agosto)    →  HTML/CSS + Jinja2 (módulo web) + Testes + PostgreSQL + Deploy
Fase 6 (Set-Out)   →  Segurança + Documentação + Pitch + Comercialização
```

---

*Arquitetura viva — será atualizada a cada fase do projeto.*
