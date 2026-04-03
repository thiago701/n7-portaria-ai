# Aula 02 — Banco de Dados: O Caderno de Registros Digital

Bem-vindo à segunda aula! Hoje vamos aprender sobre **Banco de Dados**, que é como o coração do nosso sistema de portaria.

## A Analogia: Um Armário de Arquivos Bem Organizado

Imagine que você trabalha na portaria do condomínio e precisa guardar informações sobre todos os moradores:
- **Cada morador tem um papel** com seus dados (nome, CPT, apartamento, telefone)
- **Você organiza esses papéis em uma pasta** (isso é uma **tabela**)
- **A pasta fica em um armário** que você acessa rapidamente quando precisa (isso é o **banco de dados**)

Quando alguém chega na portaria e pergunta "qual é o telefone do morador do apto 102?", você folheia a pasta rapidamente, encontra a informação e responde!

Um banco de dados faz exatamente isso — mas muito mais rápido e com milhões de registros!

## O que vamos aprender hoje

### Teoria (30 minutos)

#### 1. O que é um Banco de Dados?
Um banco de dados é um **local organizado para guardar informações** que você precisa acessar rapidamente.

#### 2. Tabelas, Colunas e Linhas
- **Tabela**: Como uma planilha do Excel. Vamos criar uma tabela chamada `moradores`
- **Colunas**: São as "categorias" de informação. Exemplo: `nome`, `cpf`, `apartamento`
- **Linhas**: Cada linha é um registro diferente. A primeira linha é o "cabeçalho", as demais são os dados

Exemplo visual:

```
┌────────────────────────────────────────────────────────────────┐
│ TABELA: moradores                                              │
├─────┬──────────────────┬────────────────┬──────────────────┐
│ id  │ nome             │ cpf            │ apartamento      │
├─────┼──────────────────┼────────────────┼──────────────────┤
│  1  │ Ademilson Silva  │ 123.456.789-00 │ 102              │
│  2  │ Maria Santos     │ 987.654.321-00 │ 205              │
│  3  │ João Oliveira    │ 111.222.333-44 │ 308              │
└─────┴──────────────────┴────────────────┴──────────────────┘
```

#### 3. Introdução ao SQL
**SQL** significa *Structured Query Language* (Linguagem de Consulta Estruturada). É como uma "língua universal" para falar com bancos de dados.

Os comandos principais são:

- **CREATE TABLE**: Criar uma tabela
  ```sql
  CREATE TABLE moradores (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL
  );
  ```

- **INSERT**: Inserir dados
  ```sql
  INSERT INTO moradores (nome) VALUES ('Ademilson');
  ```

- **SELECT**: Buscar/consultar dados
  ```sql
  SELECT * FROM moradores;
  ```

#### 4. O que é SQLite?
SQLite é um banco de dados **pequeno, rápido e gratuito**. É perfeito para:
- Aplicativos em telefones (WhatsApp, Instagram, etc. usam SQLite!)
- Projetos de aprendizado como o nosso
- Projetos pequenos e médios

Diferente do MySQL ou PostgreSQL (que são mais poderosos, mas também mais complexos), SQLite vem pronto em Python, e é tudo que precisamos!

## Prática (1h30)

Vamos colocar a mão na massa! Você vai:

1. **Criar uma pasta** chamada `database` no seu projeto
2. **Escrever SQL** para criar a tabela `moradores`
3. **Escrever Python** para automatizar a criação do banco
4. **Inserir dados** de exemplo
5. **Consultar os dados** e vê-los aparecendo na tela!

Tudo isso passo a passo, sem pressa!

## Checklist de Aprendizado

Ao final desta aula, você conseguirá:

- [ ] Explicar o que é um banco de dados com suas próprias palavras
- [ ] Entender a estrutura de uma tabela (colunas, linhas, dados)
- [ ] Escrever um comando SQL CREATE TABLE
- [ ] Escrever um comando SQL INSERT para adicionar dados
- [ ] Escrever um comando SQL SELECT para consultar dados
- [ ] Usar Python com SQLite para criar um banco de dados
- [ ] Executar um script Python que cria tabelas e insere dados
- [ ] Consultar dados do banco e exibir no terminal

## Próximos Passos

1. Leia o arquivo `INSTRUCOES.md` na pasta `exercicio/`
2. Siga os passos com calma e atenção
3. Não tenha pressa — é normal tomar tempo!
4. Se ficou com dúvida, revise a teoria acima ou consulte o `material-complementar.md`

Você está indo muito bem! Esta é uma habilidade essencial na programação.

---

**Dica importante**: Banco de dados é um tema que os programadores estudam por anos inteiros. Não se preocupe em entender tudo perfeitamente agora — o importante é ter uma boa intuição e saber usar!
