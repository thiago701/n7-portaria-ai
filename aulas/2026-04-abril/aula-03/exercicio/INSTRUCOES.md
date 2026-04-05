# Exercício Aula 03: CRUD Avançado — Visitantes, Acessos e Relatórios

**Objetivo:** Expandir o sistema da Aula 02 com CRUD de visitantes, registro de acessos e consultas com JOIN.

**Pré-requisito:** CRUD de moradores da Aula 02 funcionando
**Tempo estimado:** 1 hora e 30 minutos

---

## Passo 1: Preparação

### 1.1 Verificar que o banco tem as 3 tabelas

```bash
sqlite3 portaria.db
.tables
```

Deve mostrar: `acessos  moradores  visitantes`

```sql
SELECT COUNT(*) FROM moradores;    -- 5 ou mais (você pode ter adicionado na Aula 02)
SELECT COUNT(*) FROM visitantes;   -- 4
SELECT COUNT(*) FROM acessos;      -- 4
.quit
```

### 1.2 Relembrando a tabela visitantes

```sql
CREATE TABLE visitantes (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                TEXT    NOT NULL,
    documento           TEXT    NOT NULL,
    tipo_documento      TEXT    DEFAULT 'RG'
                                CHECK(tipo_documento IN ('RG', 'CNH', 'PASSAPORTE', 'OUTRO')),
    telefone            TEXT,
    foto_url            TEXT,
    bloqueado           INTEGER DEFAULT 0,
    motivo_bloqueio     TEXT,
    dt_criado_em           TEXT    DEFAULT CURRENT_TIMESTAMP
)
```

### 1.3 Relembrando a tabela acessos

```sql
CREATE TABLE acessos (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    visitante_id        INTEGER NOT NULL,
    morador_id          INTEGER,
    motivo              TEXT    NOT NULL,
    dt_entrada_em          TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dt_saida_em            TEXT,
    porteiro            TEXT,
    observacoes         TEXT,
    FOREIGN KEY (visitante_id) REFERENCES visitantes(id),
    FOREIGN KEY (morador_id)   REFERENCES moradores(id)
)
```

---

## Passo 2: Abra o Arquivo de Trabalho

Abra o arquivo **`sistema_portaria.py`**. Ele já tem:

- Conexão ao banco e criação das tabelas (IF NOT EXISTS)
- Todo o CRUD de moradores da Aula 02 (já pronto!)
- Funções auxiliares prontas
- Menu expandido com novas opções
- **TODOs** nos lugares que você precisa completar

---

## Passo 3: Implemente o CRUD de Visitantes

### 3.1 cadastrar_visitante() — CREATE

Mesmo padrão do `cadastrar_morador()`. Peça:
- Nome do visitante
- Documento (RG, CNH, etc.)
- Tipo de documento
- Telefone

```python
cursor.execute(
    "INSERT INTO visitantes (nome, documento, tipo_documento, telefone) VALUES (?, ?, ?, ?)",
    (nome, documento, tipo_doc, telefone)
)
```

### 3.2 listar_visitantes() — READ

```python
cursor.execute(
    "SELECT id, nome, documento, tipo_documento, telefone, bloqueado FROM visitantes ORDER BY nome"
)
```

**Dica:** Mostre se o visitante está bloqueado ou liberado!

### 3.3 bloquear_visitante() — "DELETE" macio

Diferente de moradores (que usam `ativo = 0`), visitantes usam `bloqueado = 1`:

```python
cursor.execute(
    "UPDATE visitantes SET bloqueado = 1, motivo_bloqueio = ? WHERE id = ?",
    (motivo, id_visitante)
)
```

Peça o motivo do bloqueio — é importante para segurança!

---

## Passo 4: Implemente o Registro de Acessos

### 4.1 registrar_entrada() — Visitante chegou!

O fluxo:
1. Peça o ID do visitante (ou busque por nome)
2. Verifique se NÃO está bloqueado
3. Peça o ID do morador que autorizou
4. Peça o motivo da visita
5. Registre a entrada:

```python
cursor.execute(
    "INSERT INTO acessos (visitante_id, morador_id, motivo, porteiro) VALUES (?, ?, ?, ?)",
    (visitante_id, morador_id, motivo, porteiro)
)
```

### 4.2 registrar_saida() — Visitante saiu!

1. Mostre quem está dentro (acessos onde `dt_saida_em IS NULL`)
2. Peça o ID do acesso
3. Atualize com a hora de saída:

```python
cursor.execute(
    "UPDATE acessos SET dt_saida_em = CURRENT_TIMESTAMP WHERE id = ?",
    (acesso_id,)
)
```

---

## Passo 5: Implemente as Consultas com JOIN

### 5.1 quem_esta_dentro() — Visitantes atualmente no condomínio

```python
cursor.execute("""
    SELECT v.nome AS visitante, m.nome AS morador, m.numero_residencia, a.motivo, a.dt_entrada_em
    FROM acessos a
        JOIN visitantes v ON a.visitante_id = v.id
        JOIN moradores  m ON a.morador_id   = m.id
    WHERE a.dt_saida_em IS NULL
""")
```

### 5.2 historico_acessos() — Últimos acessos registrados

```python
cursor.execute("""
    SELECT v.nome AS visitante, m.nome AS morador, m.numero_residencia,
           a.motivo, a.dt_entrada_em, a.dt_saida_em, a.porteiro
    FROM acessos a
        JOIN visitantes v ON a.visitante_id = v.id
        JOIN moradores  m ON a.morador_id   = m.id
    ORDER BY a.dt_entrada_em DESC
    LIMIT 10
""")
```

---

## Passo 6: Implemente o Relatório do Condomínio

Uma função que mostra um resumo geral:

```python
cursor.execute("""
    SELECT
        (SELECT COUNT(*) FROM moradores WHERE ativo = 1)           AS moradores_ativos,
        (SELECT COUNT(*) FROM moradores WHERE tipo_morador = 'proprietario' AND ativo = 1) AS proprietarios,
        (SELECT COUNT(*) FROM moradores WHERE tipo_morador = 'inquilino' AND ativo = 1)    AS inquilinos,
        (SELECT COUNT(*) FROM visitantes)                          AS total_visitantes,
        (SELECT COUNT(*) FROM visitantes WHERE bloqueado = 1)      AS bloqueados,
        (SELECT COUNT(*) FROM acessos)                             AS total_acessos,
        (SELECT COUNT(*) FROM acessos WHERE dt_saida_em IS NULL)      AS dentro_agora
""")
```

Exiba de forma bonita:

```
╔══════════════════════════════════════╗
║   RESUMO DO CONDOMÍNIO               ║
╠══════════════════════════════════════╣
║ Moradores ativos:    5               ║
║   - Proprietários:   3               ║
║   - Inquilinos:      2               ║
║ Visitantes total:    4               ║
║   - Bloqueados:      1               ║
║ Total de acessos:    4               ║
║ Dentro agora:        1               ║
╚══════════════════════════════════════╝
```

---

## Passo 7: Teste o Sistema Completo

1. **Listar visitantes** — Deve mostrar os 4 da tarefa antecipada
2. **Cadastrar visitante** — Adicione um novo
3. **Registrar entrada** — Registre a entrada de um visitante
4. **Quem está dentro?** — Deve mostrar o visitante que acabou de entrar
5. **Registrar saída** — Registre a saída
6. **Quem está dentro?** — Não deve mais aparecer
7. **Bloquear visitante** — Bloqueie o "José Suspeito"
8. **Tentar registrar entrada de bloqueado** — Deve negar!
9. **Relatório** — Veja o resumo completo

---

## Passo 8: Commit no Git

```bash
git add aulas/2026-04-abril/aula-03/exercicio/
git commit -m "aula-03: CRUD visitantes, registro de acessos e relatorios"
```

---

## Checklist Final

- [ ] CRUD de visitantes: cadastrar, listar, buscar, bloquear
- [ ] Registro de entrada de visitantes
- [ ] Registro de saída de visitantes
- [ ] Verificação de visitante bloqueado
- [ ] Consulta "quem está dentro" (JOIN)
- [ ] Histórico de acessos (JOIN)
- [ ] Relatório do condomínio
- [ ] Menu expandido funcionando
- [ ] Commit feito no Git

---

**Na Aula 04**, vamos transformar tudo isso em uma API REST com Flask!
