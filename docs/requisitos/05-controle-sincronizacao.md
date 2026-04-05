# n7-portaria-ai — Controle de Sincronização de Requisitos

> **Versão:** 1.0 | **Data:** 04/04/2026
> **Objetivo:** Garantir que código, SQL e documentação estejam sempre alinhados com os requisitos do projeto.

---

## 1. Regra de Ouro

> **Toda mudança em requisitos DEVE ser propagada para todos os artefatos impactados.**
> Em caso de divergência entre documentos, o `01-visao-projeto.md` é a **fonte da verdade**.

---

## 2. Cadeia de Dependência dos Documentos

Quando um documento muda, os documentos abaixo dele na cadeia precisam ser revisados:

```
01-visao-projeto.md (FONTE DA VERDADE)
    │
    ├── 02-requisitos-funcionais.md
    │       └── Requisitos RF-xxx devem refletir os módulos do doc 01
    │
    ├── 03-arquitetura.md
    │       └── Schema do banco de dados deve refletir os campos do doc 01
    │
    ├── SQL do projeto (projeto_portaria_completo.sql)
    │       └── CREATE TABLE deve espelhar o schema do doc 03
    │
    ├── Exercícios das aulas (schema.sql, criar_banco.py, moradores_crud.py)
    │       └── Devem usar a mesma estrutura de tabelas do SQL do projeto
    │
    └── Material didático (README.md, INSTRUCOES.md de cada aula)
            └── Devem descrever os campos corretos e quantidades de exercícios
```

---

## 3. Checklist de Sincronização

Ao alterar qualquer campo, módulo ou regra no `01-visao-projeto.md`, verificar:

- [ ] `02-requisitos-funcionais.md` — Os RF-xxx refletem a mudança?
- [ ] `03-arquitetura.md` — O schema do banco foi atualizado?
- [ ] `projeto_portaria_completo.sql` — O CREATE TABLE tem os novos campos?
- [ ] `schema.sql` (template da aula) — Os TODOs refletem os campos corretos?
- [ ] `criar_banco.py` — O CREATE TABLE no Python foi atualizado?
- [ ] `moradores_crud.py` — O CREATE TABLE IF NOT EXISTS foi atualizado?
- [ ] `INSTRUCOES.md` das aulas — As descrições de campos estão corretas?
- [ ] `README.md` das aulas — As referências a exercícios e campos estão corretas?

---

## 4. Histórico de Sincronizações

| Data | Mudança no doc 01 | Documentos atualizados | Responsável |
|------|-------------------|----------------------|-------------|
| 03/04/2026 | Versão inicial do projeto | Todos os documentos criados | Thiago |
| 04/04/2026 | Adição de foto, biometria e tipo_morador no Módulo 1 | 02-requisitos, 03-arquitetura, projeto_portaria_completo.sql, schema.sql, criar_banco.py, moradores_crud.py, INSTRUCOES.md (aulas 02 e 03), README.md (aulas 02 e 03) | Thiago + IA |

---

## 5. Protocolo para o Assistente IA

**INSTRUÇÃO PERMANENTE:** Sempre que for solicitado a criar, editar ou revisar qualquer artefato do projeto n7-portaria-ai, o assistente DEVE:

1. **Antes de criar/editar:** Ler o `01-visao-projeto.md` para verificar a versão mais recente dos requisitos.
2. **Após criar/editar:** Verificar se o artefato está consistente com o schema do `03-arquitetura.md`.
3. **Se encontrar divergência:** Perguntar ao Thiago antes de corrigir, informando exatamente o que diverge e em quais arquivos.
4. **Ao propagar mudanças:** Seguir a cadeia de dependência da seção 2 e marcar cada item do checklist da seção 3.
5. **Registrar:** Adicionar uma linha no histórico de sincronizações (seção 4) quando uma propagação for feita.

---

## 6. Campos Canônicos da Tabela `moradores` (referência rápida)

Última atualização: 04/04/2026

| Campo | Tipo | Obrigatório | Origem (doc 01) |
|-------|------|-------------|-----------------|
| id | INTEGER PK AUTOINCREMENT | Auto | Padrão |
| nome | TEXT NOT NULL | Sim | Cadastro completo |
| cpf | TEXT UNIQUE NOT NULL | Sim | Cadastro completo |
| numero_residencia | TEXT NOT NULL | Sim | Cadastro completo |
| bloco | TEXT DEFAULT 'A' | Não | Cadastro completo |
| telefone | TEXT | Não | Cadastro completo |
| email | TEXT | Não | Cadastro completo |
| tipo_morador | TEXT DEFAULT 'proprietario' | Não | "Tipo de Morador (inquilino e/ou proprietário)" |
| foto_url | TEXT | Não | "Foto do morador (será renovada de 2 em 2 anos)" |
| dt_foto_validade | TEXT | Não | "será renovada de 2 em 2 anos" |
| biometria_hash | TEXT | Não | "Biometria Digital (será renovada de 2 em 2 anos)" |
| dt_biometria_validade | TEXT | Não | "será renovada de 2 em 2 anos" |
| ativo | INTEGER DEFAULT 1 | Não | Soft delete (padrão do projeto) |
| dt_criado_em | TEXT DEFAULT CURRENT_TIMESTAMP | Auto | Padrão |
| dt_atualizado_em | TEXT DEFAULT CURRENT_TIMESTAMP | Auto | Padrão |

---

*Este documento deve ser consultado sempre que houver dúvida sobre a versão correta dos campos ou estruturas do projeto.*
