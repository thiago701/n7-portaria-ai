# Exercício Prático — Aula 02: CRUD Completo de Moradores em Python

**Objetivo:** Conectar o banco de dados que você criou na tarefa da semana ao Python e implementar as 4 operações CRUD com menu interativo.

**Pré-requisito:** Banco `portaria.db` já criado com as 3 tabelas (tarefa antecipada)
**Tempo estimado:** 1 hora e 30 minutos

---

## Passo 1: Verificar o Banco da Tarefa Antecipada

Antes de programar, vamos confirmar que o banco está pronto!

```bash
sqlite3 portaria.db
.tables
```

Deve mostrar: `acessos  moradores  visitantes`

```sql
SELECT COUNT(*) FROM moradores;    -- Deve retornar 5
SELECT COUNT(*) FROM visitantes;   -- Deve retornar 4
SELECT COUNT(*) FROM acessos;      -- Deve retornar 4
.quit
```

Se estiver tudo certo, ótimo! Se não, rode o SQL novamente:
```bash
sqlite3 portaria.db < projeto_portaria_completo.sql
```

---

## Passo 2: Relembrando a Tabela Moradores

A tabela que vamos manipular no CRUD tem essa estrutura (você já conhece do SQL!):

```sql
CREATE TABLE moradores (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                TEXT    NOT NULL,
    cpf                 TEXT    UNIQUE NOT NULL,
    numero_residencia         TEXT    NOT NULL,
    bloco               TEXT    DEFAULT 'A',
    telefone            TEXT,
    email               TEXT,
    tipo_morador        TEXT    DEFAULT 'proprietario'
                                CHECK(tipo_morador IN ('proprietario', 'inquilino')),
    foto_url            TEXT,
    dt_foto_validade       TEXT,
    biometria_hash      TEXT,
    dt_biometria_validade  TEXT,
    ativo               INTEGER DEFAULT 1,
    dt_criado_em           TEXT    DEFAULT CURRENT_TIMESTAMP,
    dt_atualizado_em       TEXT    DEFAULT CURRENT_TIMESTAMP
)
```

**Lembra?** Você já inseriu e consultou dados nessa tabela usando SQL puro. Agora vamos fazer o mesmo, mas pelo Python!

---

## Passo 3: Abra o Arquivo de Trabalho

Abra o arquivo **`moradores_crud.py`**. Ele já tem:

- Imports prontos (`sqlite3`, `datetime`)
- Conexão ao banco de dados
- Criação da tabela (IF NOT EXISTS — seguro rodar sempre)
- Funções auxiliares prontas: `limpar_tela()`, `formatar_cpf()`, `buscar_morador_por_cpf()`
- A função `atualizar_morador()` **completa como exemplo**
- A função `menu()` **completa**
- O loop principal `main()` **completo**
- **TODOs** nos lugares que você precisa preencher

---

## Passo 4: Complete as Funções CRUD

### 4.1 Função: cadastrar_morador() — CREATE

**O que fazer:** Adicionar um novo morador ao banco de dados.

**Passo a passo:**
1. Peça o nome com `input("Nome do morador: ")`
2. Peça o CPF com `input("CPF (somente números): ")`
3. Peça o numero_residencia com `input("Apartamento: ")`
4. Peça o email com `input("Email: ")`
5. Valide se o CPF já existe usando `buscar_morador_por_cpf(cpf)`
6. Se existir, mostre mensagem de erro e retorne
7. Se não existir, execute o INSERT:

```python
cursor.execute(
    "INSERT INTO moradores (nome, cpf, numero_residencia, email) VALUES (?, ?, ?, ?)",
    (nome, cpf, numero_residencia, email)
)
conexao.commit()
```

8. Mostre mensagem de sucesso

**Importante:** SEMPRE use `?` para parâmetros, nunca concatene strings! Isso previne SQL injection.

---

### 4.2 Função: listar_moradores() — READ

**O que fazer:** Mostrar todos os moradores ativos na tela.

**Passo a passo:**
1. Execute: `SELECT id, nome, cpf, numero_residencia, email FROM moradores WHERE ativo = 1 ORDER BY nome`
2. Use `cursor.fetchall()` para pegar todos os resultados
3. Se não houver resultados, mostre "Nenhum morador cadastrado"
4. Se houver, mostre em formato de tabela:

```
ID   Nome                      CPF             Apto   Email
---- ------------------------- --------------- ------ -------------------------
1    Ana Paula Ferreira        444.333.222-11  104    ana.ferreira@email.com
```

**Dica:** Use um loop `for` para percorrer os resultados e `formatar_cpf()` para exibir bonito.

---

### 4.3 Função: buscar_morador() — READ específico

**O que fazer:** Procurar um morador pelo nome.

**Passo a passo:**
1. Peça o nome com `input("Digite parte do nome: ")`
2. Execute com LIKE para busca parcial:

```python
cursor.execute(
    "SELECT id, nome, cpf, numero_residencia, email, ativo FROM moradores WHERE nome LIKE ? AND ativo = 1",
    (f"%{nome_busca}%",)
)
```

3. Se encontrar, mostre os dados detalhados
4. Se não encontrar, mostre "Morador não encontrado"

**Lembra do LIKE?** Você praticou isso nos exercícios SQL! O `%` funciona como coringa:
- `%Silva%` → encontra qualquer nome que contenha "Silva"

---

### 4.4 Função: desativar_morador() — DELETE macio

**O que fazer:** Marcar um morador como inativo (NÃO deletar de verdade!).

**Passo a passo:**
1. Peça o ID do morador com `input("ID do morador: ")`
2. Converta para número com `int()`
3. Verifique se o morador existe com SELECT
4. Peça confirmação ao usuário
5. Execute o UPDATE:

```python
cursor.execute(
    "UPDATE moradores SET ativo = 0, dt_atualizado_em = CURRENT_TIMESTAMP WHERE id = ?",
    (id_morador,)
)
conexao.commit()
```

**Por que soft delete?** Porque um DELETE é perigoso demais! Se deletar e se arrepender, perdeu os dados. Com soft delete, os dados ficam "escondidos" mas podem ser recuperados.

---

## Passo 5: Estude a Função Exemplo (atualizar_morador)

A função `atualizar_morador()` já está **completa** no arquivo. Estude ela para entender o padrão:

1. Pede o ID do morador
2. Busca no banco para verificar se existe
3. Mostra os dados atuais
4. Pede os novos dados (ENTER para manter o atual)
5. Executa UPDATE
6. Trata erros com try/except

Use ela como modelo para completar as outras!

---

## Passo 6: Teste Tudo

Depois de completar cada função, teste:

1. **Execute o programa:** `python moradores_crud.py`
2. **Opção 2 (Listar):** Deve mostrar os 5 moradores que você inseriu na tarefa da semana
3. **Opção 1 (Cadastrar):** Cadastre um novo morador
4. **Opção 2 (Listar):** Confirme que o novo morador apareceu
5. **Opção 3 (Buscar):** Busque por "Maria" — deve encontrar
6. **Opção 1 (Cadastrar com CPF repetido):** Tente cadastrar com o mesmo CPF — deve dar erro
7. **Opção 5 (Desativar):** Desative um morador
8. **Opção 2 (Listar):** O desativado NÃO deve aparecer

---

## Passo 7: Commit no Git

Quando tudo estiver funcionando:

```bash
git add aulas/2026-04-abril/aula-02/exercicio/moradores_crud.py
git commit -m "aula-02: Implementar CRUD completo de moradores em Python"
```

---

## Dicas Importantes

### Sobre a Conexão ao Banco

O arquivo já conecta ao banco no início. Se quiser usar o banco que você criou na tarefa da semana, ajuste o caminho:

```python
# Se o portaria.db está na mesma pasta:
conexao = sqlite3.connect('portaria.db')

# Se está em outra pasta:
conexao = sqlite3.connect('../../src/infra/database/portaria.db')
```

### Sobre Parametrização SQL (Segurança!)

```python
# CERTO (seguro):
cursor.execute("SELECT * FROM moradores WHERE cpf = ?", (cpf,))

# ERRADO (perigoso — SQL injection!):
cursor.execute(f"SELECT * FROM moradores WHERE cpf = '{cpf}'")
```

Você aprendeu isso no SQL! O `?` é o equivalente do placeholder.

### Sobre try/except

Envolva TODA operação de banco em try/except:

```python
try:
    cursor.execute(...)
    conexao.commit()
    print("Sucesso!")
except sqlite3.IntegrityError:
    print("Erro: dado duplicado!")
except Exception as erro:
    print(f"Erro: {erro}")
```

---

## Checklist Final

- [ ] Banco `portaria.db` verificado e funcionando
- [ ] Função `cadastrar_morador()` implementada e testada
- [ ] Função `listar_moradores()` implementada e testada
- [ ] Função `buscar_morador()` implementada e testada
- [ ] Função `desativar_morador()` implementada e testada
- [ ] Validação de CPF duplicado funcionando
- [ ] try/except em todas as funções
- [ ] Menu navegando entre as opções
- [ ] Commit feito no Git

---

## O que Vem na Aula 03?

Na próxima aula vamos **continuar evoluindo o sistema**:
- Adicionar gerenciamento de **visitantes** (CRUD da tabela visitantes)
- Fazer **consultas com JOIN** entre tabelas (quem visitou quem?)
- Começar a organizar o código em **camadas** (separação de responsabilidades)
- Trabalhar com **relatórios** (resumo do condomínio)

Ou seja: o banco que você criou na semana e o CRUD de hoje são a **base sólida** para tudo que vem pela frente!

---

**Parabéns! Você está programando de verdade!**
