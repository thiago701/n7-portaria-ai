# Exercício Prático — Aula 02

## Seu Objetivo

Criar um banco de dados SQLite com uma tabela de moradores e inserir dados nela usando Python.

**Tempo estimado**: 1 hora e 30 minutos

---

## Passo 1: Criar a Pasta do Banco de Dados

No terminal, na raiz do seu projeto (`n7-portaria-ai`), execute:

```bash
mkdir -p database
```

Pronto! Você criou uma pasta chamada `database` onde vamos guardar nosso arquivo de banco de dados.

**O que significa cada parte**:
- `mkdir`: comando para criar pasta
- `-p`: garante que cria também as pastas "pais" se não existirem
- `database`: nome da pasta

---

## Passo 2: Criar o Arquivo schema.sql

Vamos criar um arquivo SQL que descreve a estrutura da nossa tabela.

Na pasta `database/`, crie um arquivo chamado `schema.sql`.

**Siga as instruções** no arquivo `schema.sql` — ele tem TODOs que você precisará completar!

Para completar, pense:
- Que informações de um morador precisamos guardar?
- Qual tipo de dado é cada uma? (TEXT para texto, INTEGER para números)
- Qual coluna é a "chave" (identificador único)? — essa será a `id` com `PRIMARY KEY`

**Dica**: Revise a teoria no `README.md` para lembrar da sintaxe!

---

## Passo 3: Criar o Script Python

Na pasta `exercicio/`, já existe um arquivo chamado `criar_banco.py`.

**Abra esse arquivo** e complete os TODOs. Você vai:

1. Importar a biblioteca `sqlite3` (já está feito)
2. Criar uma função que conecta ao banco (já está feita)
3. **TODO**: Completar a função `criar_tabela_moradores()` — escreva o comando SQL CREATE TABLE
4. **TODO**: Completar a função `inserir_morador()` — escreva o comando SQL INSERT
5. **TODO**: Completar a função `listar_moradores()` — escreva o comando SQL SELECT

Cada TODO tem um comentário dizendo exatamente o que fazer!

**Dica**: O SQL que você escrever aqui será muito parecido com o que está no `schema.sql`.

---

## Passo 4: Inserir 3 Moradores de Exemplo

Quando você completar a função `inserir_morador()`, o script irá:

1. Criar o banco de dados (se não existir)
2. Criar a tabela `moradores`
3. Inserir 3 moradores de exemplo:
   - Ademilson Silva, CPF 123.456.789-00, Apto 102, Bloco A, Telefone (11) 98765-4321, Email ademilson@email.com
   - Maria Santos, CPF 987.654.321-00, Apto 205, Bloco A, Telefone (11) 99876-5432, Email maria@email.com
   - João Oliveira, CPF 111.222.333-44, Apto 308, Bloco B, Telefone (11) 91234-5678, Email joao@email.com

Esses dados estarão no script, na função `main()`.

---

## Passo 5: Executar o Script

No terminal, dentro da pasta `exercicio/`, execute:

```bash
python criar_banco.py
```

**O que acontecerá**:
1. O banco será criado em `../database/portaria.db`
2. A tabela será criada
3. Os 3 moradores serão inseridos
4. A lista de moradores será exibida na tela

Se tudo correr bem, você verá algo como:

```
Criando banco de dados...
Criando tabela moradores...
Inserindo moradores de exemplo...
Listando todos os moradores:
---
ID: 1, Nome: Ademilson Silva, Apartamento: 102
ID: 2, Nome: Maria Santos, Apartamento: 205
ID: 3, Nome: João Oliveira, Apartamento: 308
---
Banco de dados criado com sucesso!
```

---

## Passo 6: Commit Git

Agora vamos registrar seu trabalho no Git!

Execute:

```bash
git add database/ exercicio/
git commit -m "aula-02: Criar banco de dados com tabela de moradores"
```

**O que cada linha faz**:
- `git add`: Prepara os arquivos para registrar
- `git commit -m`: Cria um "snapshot" do seu trabalho com uma mensagem descritiva

Perfeito! Seu trabalho está registrado no histórico do projeto.

---

## Checklist Final

Antes de considerar o exercício completo, verifique:

- [ ] A pasta `database/` foi criada
- [ ] O arquivo `schema.sql` foi criado e completado
- [ ] O arquivo `criar_banco.py` foi completado (todos os TODOs resolvidos)
- [ ] O script executa sem erros
- [ ] Os moradores aparecem na tela quando você executa o script
- [ ] O commit foi feito com sucesso

---

## Se algo não funcionar...

### Erro: "ModuleNotFoundError: No module named 'sqlite3'"
SQLite3 vem com Python, então isso é raro. Se acontecer:
```bash
pip install pysqlite3
```

### Erro: "SQL syntax error"
Revise a sintaxe SQL no `README.md`. Comandos SQL são muito sensíveis a pequenos erros!

### O banco foi criado, mas não mostra dados
Verifique se a função `inserir_morador()` está sendo chamada corretamente na função `main()`.

### Dúvidas gerais
Consulte o arquivo `material-complementar.md` para recursos adicionais!

---

## Parabéns!

Você completou um exercício real de programação! Você:
- Entendeu a estrutura de um banco de dados
- Escreveu SQL
- Integrou SQL com Python
- Executou um script completo

Isso é muito legal! Você está evoluindo rapidamente.

---

**Próxima aula**: Vamos aprender a consultar dados mais avançadamente e criar interfaces para nosso sistema!
