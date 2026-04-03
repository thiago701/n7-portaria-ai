# Exercício Aula 03: CRUD Completo de Moradores

**Objetivo:** Implementar as 4 operações de dados (CRUD) em um sistema real de gerenciamento de moradores.

**Tempo estimado:** 1 hora e 30 minutos

---

## Passo 1: Preparação

Antes de começar a programar, vamos entender o que já temos:

### 1.1 Revisar o banco de dados da Aula 02

Na aula anterior, criamos um banco de dados com a tabela de moradores. Nosso banco tem essa estrutura:

```sql
CREATE TABLE moradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT UNIQUE NOT NULL,
    apartamento TEXT NOT NULL,
    email TEXT,
    ativo INTEGER DEFAULT 1
)
```

**O que significa:**
- `id`: Número único de cada morador (criado automaticamente)
- `nome`: Nome completo
- `cpf`: CPF (deve ser único, sem duplicar)
- `apartamento`: Apto do morador
- `email`: Email para contato
- `ativo`: Número 1 = ativo, 0 = inativo (usamos números porque SQLite não tem booleano)

### 1.2 Abra o arquivo incompleto

Abra o arquivo `moradores_crud.py` que você vai trabalhar. Ele já tem:
- Imports prontos
- Conexão ao banco de dados
- A função menu() completa (mostra as opções)
- A função atualizar_morador() como exemplo pronto
- TODOs nos lugares onde você precisa preencher código

---

## Passo 2: Complete as Funções CRUD

Sua tarefa é completar as funções que estão com TODO. Vamos uma por uma:

### 2.1 Função: cadastrar_morador()

**O que fazer:** Essa função deve adicionar um novo morador ao banco de dados.

**Passo a passo:**
1. Peça o nome ao usuário com `input("Nome do morador: ")`
2. Peça o CPF com `input("CPF (sem pontos): ")`
3. Peça o apartamento com `input("Apartamento: ")`
4. Peça o email com `input("Email: ")`
5. Valide se o CPF já existe no banco
   - Se existe, mostre mensagem de erro e retorne
   - Se não existe, continue
6. Tente inserir no banco com um INSERT SQL
7. Se der erro (por exemplo, CPF duplicado), mostre uma mensagem de erro
8. Se conseguir, mostre "Morador cadastrado com sucesso!"

**Dica:** Use a função `buscar_morador_por_cpf()` que está no arquivo para validar se o CPF já existe.

---

### 2.2 Função: listar_moradores()

**O que fazer:** Mostre na tela todos os moradores cadastrados.

**Passo a passo:**
1. Execute um `SELECT * FROM moradores WHERE ativo = 1` para trazer apenas os ativos
2. Busque todos os registros com `cursor.fetchall()`
3. Se não houver registros, mostre "Nenhum morador cadastrado"
4. Se houver, mostre assim:

```
ID | Nome                | CPF          | Apto | Email
---+---------------------+--------------+------+------------------
1  | João Silva          | 123.456.789  | 101  | joao@email.com
2  | Maria Santos        | 987.654.321  | 202  | maria@email.com
```

**Dica:** Use um loop `for` para percorrer os resultados.

---

### 2.3 Função: buscar_morador()

**O que fazer:** Procure um morador pelo nome e mostre seus dados.

**Passo a passo:**
1. Peça o nome com `input("Digite o nome do morador: ")`
2. Execute um `SELECT * FROM moradores WHERE nome LIKE ?` e use o nome como parâmetro
3. Se encontrar, mostre os dados (ID, Nome, CPF, Apto, Email)
4. Se não encontrar, mostre "Morador não encontrado"

**Dica:** Use `%` no LIKE para buscar parcial: se o usuário digitar "João", encontra "João Silva"

---

### 2.4 Função: desativar_morador()

**O que fazer:** Marque um morador como inativo (não delete de verdade!).

**Passo a passo:**
1. Peça o ID do morador com `input("ID do morador a desativar: ")`
2. Tente converter para número com `int()`
3. Execute um `UPDATE moradores SET ativo = 0 WHERE id = ?`
4. Se a atualização funcionou, mostre "Morador desativado com sucesso"
5. Se der erro, mostre a mensagem de erro

**Importante:** A gente NÃO deleta (DELETE). Apenas marcamos como inativo. Por quê? Porque pode precisar recuperar os dados depois, e um DELETE é perigoso demais!

---

## Passo 3: Valide Duplicatas de CPF

Na função `cadastrar_morador()`, você precisa checar se o CPF já existe.

**Use a função que já existe no arquivo:**

```python
def buscar_morador_por_cpf(cpf):
    # já está implementada - use ela!
```

Ela retorna os dados do morador se existir, ou None se não existir.

---

## Passo 4: Trate Erros com Try/Except

Em cada função que mexe com banco de dados, envolva o código em try/except:

```python
try:
    # seu código SQL aqui
    cursor.execute(...)
    conexao.commit()
    print("Sucesso!")
except Exception as erro:
    print(f"Erro: {erro}")
```

Isso protege seu programa de travar se algo der errado.

---

## Passo 5: Teste Tudo

Depois de completar cada função, teste ela:

1. **Cadastre 3 moradores** com dados diferentes
2. **Liste** para ver se aparece na tela
3. **Busque** pelo nome de um morador
4. **Tente cadastrar o mesmo CPF novamente** - deve dar erro de duplicata
5. **Desative** um morador
6. **Liste novamente** - o desativado NÃO deve aparecer

---

## Passo 6: Commit no Git

Quando tudo estiver funcionando, salve seu trabalho no Git:

```bash
git add .
git commit -m "Aula 03: Implementar CRUD completo de moradores"
```

---

## Dicas Importantes

### Sobre Formatação de CPF

O banco armazena CPF SEM pontos (ex: "12345678901"), mas você pode exibir formatado se quiser:

```python
def formatar_cpf(cpf):
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
```

### Sobre Conexões ao Banco

A conexão ao banco já está pronta no início do arquivo com:

```python
conexao = sqlite3.connect('moradores.db')
cursor = conexao.cursor()
```

Use `cursor` para executar comandos e `conexao.commit()` para salvar!

### Sobre Parametrização SQL

SEMPRE use `?` para parâmetros, nunca concatene strings:

```python
# CERTO:
cursor.execute("SELECT * FROM moradores WHERE cpf = ?", (cpf,))

# ERRADO (não faça!):
cursor.execute(f"SELECT * FROM moradores WHERE cpf = '{cpf}'")
```

O segundo é perigoso porque pode levar a ataques de SQL injection.

---

## Checklist Final

Antes de considerar terminado:

- [ ] Função `cadastrar_morador()` implementada e testada
- [ ] Função `listar_moradores()` implementada e testada
- [ ] Função `buscar_morador()` implementada e testada
- [ ] Função `desativar_morador()` implementada e testada
- [ ] Validação de CPF duplicado funcionando
- [ ] Tratamento de erros (try/except) em todas as funções
- [ ] Menu funcionando - consegue navegar entre as opções
- [ ] Cadastrou 3 moradores de teste e testou tudo
- [ ] Arquivo commitado no Git

---

## Próximos Passos

Após completar esse exercício, você saberá:
- Como guardar dados em um banco de dados a partir do Python
- Como recuperar e exibir dados
- Como validar dados antes de salvar
- Como atualizar dados existentes
- Como fazer um menu de texto profissional

Parabéns! Você está no caminho para ser um programador de verdade! 🎯

