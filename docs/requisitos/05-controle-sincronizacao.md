# n7-portaria-ai — Controle de Sincronização de Requisitos

> **Versao:** 2.0 | **Data:** 09/04/2026
> **Objetivo:** Garantir que codigo, SQL e documentacao estejam sempre alinhados com os requisitos do projeto.

---

## 1. Regra de Ouro

> **Toda mudanca em requisitos DEVE ser propagada para todos os artefatos impactados.**
> Em caso de divergencia entre documentos, o `01-visao-projeto.md` e a **fonte da verdade**.
> Em caso de divergencia entre documentacao e SQL, o `projeto_portaria_completo.sql` e a **fonte tecnica da verdade** (schema real).

---

## 2. Cadeia de Dependencia dos Documentos

Quando um documento muda, os documentos abaixo dele na cadeia precisam ser revisados:

```
01-visao-projeto.md (FONTE DA VERDADE — requisitos de negocio)
    |
    +-- 02-requisitos-funcionais.md
    |       +-- Requisitos RF-xxx devem refletir os modulos do doc 01
    |
    +-- 03-arquitetura.md
    |       +-- Schema do banco de dados deve refletir os campos do doc 01
    |       +-- Diagrama de camadas deve refletir a estrutura real de pastas
    |
    +-- projeto_portaria_completo.sql (FONTE TECNICA DA VERDADE — schema real)
    |       +-- CREATE TABLE deve espelhar o schema do doc 03
    |       +-- E a referencia que o codigo Python deve seguir
    |
    +-- criar_banco_final.py
    |       +-- Deve gerar portaria.db identico ao SQL acima
    |
    +-- Modelos Python (src/core/models/)
    |       +-- Dataclasses devem mapear 1:1 as tabelas do SQL
    |       +-- base.py, morador.py, e futuros: visitante.py, etc.
    |
    +-- Exercicios das aulas (moradores_crud.py, sistema_portaria.py)
    |       +-- Devem usar a mesma estrutura de tabelas do SQL do projeto
    |
    +-- Material didatico (README.md, slides, GUIA_MAPEAMENTO.md)
    |       +-- Devem descrever os campos corretos
    |
    +-- DESIGN_SYSTEM_SLIDES.md
            +-- Identidade visual padrao para todos os slides
```

---

## 3. Checklist de Sincronizacao

Ao alterar qualquer campo, modulo ou regra, verificar:

- [ ] `01-visao-projeto.md` — A visao reflete a mudanca?
- [ ] `02-requisitos-funcionais.md` — Os RF-xxx refletem a mudanca?
- [ ] `03-arquitetura.md` — O schema do banco foi atualizado?
- [ ] `projeto_portaria_completo.sql` — O CREATE TABLE tem os novos campos?
- [ ] `criar_banco_final.py` — O script Python gera o banco atualizado?
- [ ] `portaria.db` — Regerar com `python criar_banco_final.py`?
- [ ] `src/core/models/` — Os dataclasses refletem o schema?
- [ ] `moradores_crud.py` (aula 02) — Os JOINs e campos estao corretos?
- [ ] `sistema_portaria.py` (aula 03) — Os CRUDs de visitantes/acessos estao corretos?
- [ ] `GUIA_MAPEAMENTO.md` — A receita de mapeamento reflete o schema?
- [ ] `README.md` das aulas — As referencias a exercicios e campos estao corretas?
- [ ] Slides das aulas — Os diagramas e listas de tabelas estao atualizados?

---

## 4. Historico de Sincronizacoes

| Data | Mudanca | Documentos atualizados | Responsavel |
|------|---------|----------------------|-------------|
| 03/04/2026 | Versao inicial do projeto | Todos os documentos criados (01 a 05, roadmap) | Thiago |
| 04/04/2026 | Adicao de foto, biometria e tipo_morador no Modulo 1 | 02-requisitos, 03-arquitetura, projeto_portaria_completo.sql, schema.sql, criar_banco.py, moradores_crud.py | Thiago + IA |
| 09/04/2026 | **Revisao arquitetural v8.0:** moradores N:N residencias, 9 tabelas, 2FA, LGPD, correlation_id SHA-256, config_acesso_morador, assinatura_condominio | 03-arquitetura (schema completo), projeto_portaria_completo.sql (1039 linhas), criar_banco_final.py (novo), portaria.db (novo), moradores_crud.py (reescrito com JOINs), src/core/models/morador.py (novo), src/core/models/base.py (novo), GUIA_MAPEAMENTO.md (novo), slides aula 02 (novo), DESIGN_SYSTEM_SLIDES.md (novo), README aula 02 (reescrito) | Thiago + IA |
| 09/04/2026 | **Sincronizacao geral:** Atualizacao de TODOS os docs de requisitos para refletir o estado real do codigo e banco | 01-visao-projeto, 02-requisitos-funcionais, 03-arquitetura, 05-controle-sincronizacao, roadmap | Thiago + IA |

---

## 5. Protocolo para o Assistente IA

**INSTRUCAO PERMANENTE:** Sempre que for solicitado a criar, editar ou revisar qualquer artefato do projeto n7-portaria-ai, o assistente DEVE:

1. **Antes de criar/editar:** Ler o `01-visao-projeto.md` para verificar a versao mais recente dos requisitos.
2. **Apos criar/editar:** Verificar se o artefato esta consistente com o schema do `03-arquitetura.md` e com o `projeto_portaria_completo.sql`.
3. **Se encontrar divergencia:** Perguntar ao Thiago antes de corrigir, informando exatamente o que diverge e em quais arquivos.
4. **Ao propagar mudancas:** Seguir a cadeia de dependencia da secao 2 e marcar cada item do checklist da secao 3.
5. **Registrar:** Adicionar uma linha no historico de sincronizacoes (secao 4) quando uma propagacao for feita.
6. **Slides:** Seguir o `docs/DESIGN_SYSTEM_SLIDES.md` para manter a identidade visual.

---

## 6. Referencia Rapida — 9 Tabelas do Projeto (v8.0)

Ultima atualizacao: 09/04/2026 — Alinhado com `projeto_portaria_completo.sql`

### Tabela 1: moradores (dados PESSOAIS)
| Campo | Tipo | Restricoes |
|-------|------|-----------|
| id | INTEGER | PK AUTOINCREMENT |
| nome | TEXT | NOT NULL |
| cpf | TEXT | UNIQUE NOT NULL CHECK(length=11) |
| telefone | TEXT | |
| email | TEXT | CHECK(LIKE '%@%.%') |
| dt_nascimento | DATE | |
| foto | BLOB | Bytes da foto JPG/PNG |
| dt_foto_validade | DATE | Renovar a cada 2 anos |
| biometria | BLOB | Bytes do template biometrico |
| dt_biometria_validade | DATE | Renovar a cada 2 anos |
| termos_lgpd | BLOB | Bytes do PDF dos termos aceitos |
| dt_aceite_lgpd | DATETIME | NULL = pendente |
| ativo | BOOLEAN | DEFAULT 1 CHECK IN (0,1) |
| correlation_id | TEXT | UNIQUE NOT NULL — SHA-256 |
| dt_criado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| dt_atualizado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |

> **v8.0:** `numero_residencia`, `bloco`, `tipo_morador` REMOVIDOS — agora em `residencias` e `morador_residencia`.

### Tabela 2: residencias (dados da UNIDADE)
| Campo | Tipo | Restricoes |
|-------|------|-----------|
| id | INTEGER | PK AUTOINCREMENT |
| codigo_condominio | TEXT | NOT NULL |
| numero_residencia | TEXT | NOT NULL |
| bloco | TEXT | NULL em condominios horizontais |
| quadra | TEXT | NULL em condominios verticais |
| andar | INTEGER | NULL em casas |
| tipo_moradia | TEXT | DEFAULT 'apartamento' CHECK IN ('apartamento','casa','comercial','outro') |
| interfone | TEXT | Sugestao do Ademilson |
| observacao | TEXT | Sugestao do Ademilson |
| ativo | BOOLEAN | DEFAULT 1 |
| correlation_id | TEXT | UNIQUE NOT NULL |
| dt_criado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| dt_atualizado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### Tabela 3: morador_residencia (junction N:N)
| Campo | Tipo | Restricoes |
|-------|------|-----------|
| id | INTEGER | PK AUTOINCREMENT |
| morador_id | INTEGER | FK moradores.id NOT NULL |
| residencia_id | INTEGER | FK residencias.id NOT NULL |
| tipo_morador | TEXT | DEFAULT 'proprietario' CHECK IN ('proprietario','inquilino') |
| dt_inicio | DATE | NOT NULL DEFAULT CURRENT_DATE |
| dt_fim | DATE | NULL = ainda ativo |
| ativo | BOOLEAN | DEFAULT 1 |
| correlation_id | TEXT | UNIQUE NOT NULL |
| dt_criado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| — | — | UNIQUE(morador_id, residencia_id, dt_inicio) |

### Tabela 4: visitantes
| Campo | Tipo | Restricoes |
|-------|------|-----------|
| id | INTEGER | PK AUTOINCREMENT |
| nome | TEXT | NOT NULL |
| documento | TEXT | NOT NULL |
| tipo_documento | TEXT | DEFAULT 'RG' CHECK IN ('RG','CNH','PASSAPORTE','OUTRO') |
| telefone | TEXT | |
| foto | BLOB | |
| bloqueado | BOOLEAN | DEFAULT 0 |
| motivo_bloqueio | TEXT | |
| dt_validade_inicio | DATE | NULL = sem restricao |
| dt_validade_fim | DATE | CHECK(fim >= inicio) |
| correlation_id | TEXT | UNIQUE NOT NULL |
| dt_criado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### Tabela 5: funcionarios
| Campo | Tipo | Restricoes |
|-------|------|-----------|
| id | INTEGER | PK AUTOINCREMENT |
| nome | TEXT | NOT NULL |
| cpf | TEXT | UNIQUE NOT NULL CHECK(length=11) |
| cargo | TEXT | DEFAULT 'porteiro' CHECK IN ('porteiro','zelador','administrador','outro') |
| setor | TEXT | |
| login | TEXT | UNIQUE NOT NULL |
| senha_hash | TEXT | NOT NULL CHECK(length=64) — SHA-256, NUNCA texto puro |
| ativo | BOOLEAN | DEFAULT 1 |
| correlation_id | TEXT | UNIQUE NOT NULL |
| dt_criado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### Tabela 6: veiculos
| Campo | Tipo | Restricoes |
|-------|------|-----------|
| id | INTEGER | PK AUTOINCREMENT |
| placa | TEXT | UNIQUE NOT NULL CHECK(length >= 7) |
| modelo | TEXT | |
| cor | TEXT | |
| morador_id | INTEGER | FK moradores.id (nullable) |
| funcionario_id | INTEGER | FK funcionarios.id (nullable) |
| visitante_id | INTEGER | FK visitantes.id (nullable) |
| ativo | BOOLEAN | DEFAULT 1 |
| correlation_id | TEXT | UNIQUE NOT NULL |
| dt_criado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### Tabela 7: acessos (LOG — nunca deletar!)
| Campo | Tipo | Restricoes |
|-------|------|-----------|
| id | INTEGER | PK AUTOINCREMENT |
| visitante_id | INTEGER | FK visitantes.id NOT NULL |
| morador_id | INTEGER | FK moradores.id (nullable) |
| funcionario_id | INTEGER | FK funcionarios.id (nullable) |
| veiculo_id | INTEGER | FK veiculos.id (nullable) |
| tipo_acesso | TEXT | DEFAULT 'pedestre' CHECK IN ('pedestre','garagem') |
| auth_senha | BOOLEAN | DEFAULT 0 — fator 1 de autenticacao |
| auth_digital | BOOLEAN | DEFAULT 0 — fator 2 de autenticacao |
| auth_facial | BOOLEAN | DEFAULT 0 — fator 3 de autenticacao |
| motivo | TEXT | NOT NULL |
| dt_entrada_em | DATETIME | NOT NULL DEFAULT CURRENT_TIMESTAMP |
| dt_saida_em | DATETIME | NULL = ainda dentro |
| porteiro | TEXT | texto livre (compatibilidade) |
| observacoes | TEXT | |
| correlation_id | TEXT | UNIQUE NOT NULL |
| — | — | CHECK(auth_senha + auth_digital + auth_facial >= 1) |

### Tabela 8: config_acesso_morador (1:1 com moradores)
| Campo | Tipo | Restricoes |
|-------|------|-----------|
| id | INTEGER | PK AUTOINCREMENT |
| morador_id | INTEGER | FK moradores.id UNIQUE (1:1) |
| fatores_requeridos | INTEGER | DEFAULT 1 CHECK IN (1,2) |
| permite_senha | BOOLEAN | DEFAULT 1 |
| permite_digital | BOOLEAN | DEFAULT 1 |
| permite_facial | BOOLEAN | DEFAULT 0 |
| correlation_id | TEXT | UNIQUE NOT NULL |
| dt_criado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| dt_atualizado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| — | — | CHECK(permite_senha + permite_digital + permite_facial >= 1) |

### Tabela 9: assinatura_condominio (1 por condominio)
| Campo | Tipo | Restricoes |
|-------|------|-----------|
| id | INTEGER | PK AUTOINCREMENT |
| codigo_condominio | TEXT | UNIQUE NOT NULL |
| nome_condominio | TEXT | NOT NULL |
| endereco | TEXT | |
| responsavel_id | INTEGER | FK moradores.id (sindico) |
| numero_contrato | TEXT | UNIQUE NOT NULL |
| contrato | BLOB | PDF do contrato |
| dt_ativacao | DATE | |
| dt_vigencia_inicio | DATE | NOT NULL |
| dt_vigencia_fim | DATE | CHECK(fim >= inicio) |
| status | TEXT | DEFAULT 'ativo' CHECK IN ('ativo','pendente','vencido','cancelado') |
| observacoes | TEXT | |
| correlation_id | TEXT | UNIQUE NOT NULL |
| dt_criado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| dt_atualizado_em | DATETIME | DEFAULT CURRENT_TIMESTAMP |

---

## 7. Diretriz de Sincronizacao Periodica

> **REGRA:** A cada aula concluida, executar a sincronizacao docs <-> codigo.

### Quando sincronizar

| Gatilho | Acao |
|---------|------|
| Aula concluida | Revisar docs/requisitos contra codigo entregue |
| Novo artefato criado | Registrar na cadeia de dependencia (secao 2) |
| Tabela alterada no SQL | Propagar para docs 03, 05, modelos Python, exercicios |
| Novo modulo adicionado | Adicionar RFs no doc 02, atualizar doc 01 |
| Mudanca no design visual | Atualizar DESIGN_SYSTEM_SLIDES.md |

### Como sincronizar (passo a passo)

1. Rodar `python criar_banco_final.py` e verificar que o banco esta ok
2. Comparar tabelas do `portaria.db` com as listadas na secao 6 deste documento
3. Verificar que cada dataclass em `src/core/models/` mapeia 1:1 com o SQL
4. Verificar que os exercicios das aulas usam os mesmos nomes de tabelas/campos
5. Atualizar o historico (secao 4) com data e resumo da mudanca
6. Atualizar o roadmap se houve progresso de fase

---

*Este documento deve ser consultado sempre que houver duvida sobre a versao correta dos campos ou estruturas do projeto.*
