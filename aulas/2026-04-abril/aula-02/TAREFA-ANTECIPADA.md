# Tarefa Antecipada — Prepare o Banco de Dados Antes da Aula 02

**Para:** Ademilson
**De:** Prof. Thiago
**Data de envio:** 05/04/2026
**Prazo:** Antes da Aula 02 (09/04/2026)
**Tempo estimado:** 1 a 2 horas (pode dividir em dias!)

---

## Por Que Estou Enviando Isso Agora?

Ademilson, como voce ja tem base de banco de dados e SQL, vamos aproveitar essa semana para fazer algo muito legal: **criar o banco de dados COMPLETO do nosso projeto de portaria!**

Assim, quando chegarmos na Aula 02, voce ja vai ter o banco pronto e vamos direto para a parte mais divertida: **programar o sistema CRUD em Python** (criar, buscar, atualizar e desativar moradores pelo terminal).

Pense assim: essa tarefa e como **preparar os ingredientes antes de cozinhar**. Na aula, a gente cozinha junto!

---

## O Que Voce Vai Fazer

Existe um arquivo chamado **`projeto_portaria_completo.sql`** na pasta `exercicio/`. Esse arquivo e o "esqueleto" completo do banco de dados do nosso sistema de portaria.

Ele contem:

- **5 tabelas completas:** `moradores`, `visitantes`, `funcionarios`, `veiculos` e `acessos` (as 2 últimas vieram do seu rascunho!)
- **Campos novos na tabela moradores:** tipo_morador (proprietario/inquilino), foto_url, dt_foto_validade, biometria_hash, dt_biometria_validade
- **Conceitos importantes:** FOREIGN KEY, CHECK, INDEX
- **Dados de exemplo:** 5 moradores, 4 visitantes e 4 registros de acesso
- **Consultas de estudo:** 15+ exemplos de SELECT para praticar
- **10 exercicios praticos** para resolver (com gabarito!)

**O arquivo esta TODO comentado**, explicando cada linha em portugues. Leia com calma — e como um livro de receitas do banco de dados.

---

## Instalando as Ferramentas (Faça Antes de Tudo!)

Antes de qualquer coisa, precisamos garantir que o SQLite3 está instalado e que você tem uma ferramenta visual para explorar o banco. Siga os passos abaixo de acordo com o seu sistema.

---

### Instalar o SQLite3 no Windows

O SQLite3 é o "motor" do banco de dados — sem ele, não conseguimos criar nada. Veja se já está instalado:

```bash
sqlite3 --version
```

Se aparecer algo como `3.45.0 ...`, já está instalado! Pode pular esta parte.
Se aparecer **"command not found"** ou **"não reconhecido"**, siga os passos abaixo:

**Passo a passo para instalar o SQLite3 no Windows:**

1. Acesse o site oficial: **https://www.sqlite.org/download.html**
2. Na seção **"Precompiled Binaries for Windows"**, clique em **`sqlite-tools-win-x64-*.zip`**
   (o arquivo com `tools` no nome — tem o sqlite3.exe dentro)
3. Extraia o arquivo ZIP em uma pasta fácil de achar, por exemplo:
   `C:\sqlite\`
   Dentro dessa pasta deve ter: `sqlite3.exe`, `sqldiff.exe` e `sqlite3_analyzer.exe`
4. **Adicione ao PATH** (para funcionar em qualquer terminal):
   - Pressione `Win + S` e busque **"variáveis de ambiente"**
   - Clique em **"Editar as variáveis de ambiente do sistema"**
   - Clique em **"Variáveis de Ambiente..."**
   - Em **"Variáveis do sistema"**, clique em **Path** → **Editar**
   - Clique em **Novo** e digite: `C:\sqlite`
   - Clique em **OK** em todas as janelas
5. **Feche e reabra o terminal**, depois teste:

```bash
sqlite3 --version
```

Se aparecer a versão, está pronto! 🎉

---

### Ferramenta Visual: DBeaver ou VS Code (escolha uma!)

O SQLite3 pelo terminal funciona, mas é difícil de visualizar os dados. Uma ferramenta visual vai te ajudar muito — você vê as tabelas como planilhas do Excel!

Escolha a que preferir:

---

#### Opção A — DBeaver (programa separado, mais completo)

O DBeaver é um programa profissional gratuito que funciona com SQLite, MySQL, PostgreSQL e muitos outros bancos. Ótimo para quem quer explorar os dados com mais facilidade.

**Como instalar:**

1. Acesse: **https://dbeaver.io/download/**
2. Baixe o **"Community Edition"** para Windows (o gratuito)
3. Execute o instalador e siga os passos (Next → Next → Install → Finish)
4. Abra o DBeaver

**Como conectar ao banco do projeto:**

1. Clique em **"Nova Conexão"** (ícone de tomada no canto superior esquerdo)
2. Escolha **SQLite** → clique em **Próximo**
3. Em **"Path"**, clique em **"Abrir"** e navegue até a pasta do projeto:
   `n7-portaria-ai/aulas/2026-04-abril/aula-02/exercicio/portaria.db`
4. Clique em **"Testar Conexão"** — se aparecer "Conectado", está funcionando!
5. Clique em **"Concluir"**

**Como usar:**

- No painel esquerdo, clique na conexão → **Schemas** → **main** → **Tables**
- Clique com o botão direito em uma tabela → **"Visualizar Dados"** → vê os registros como planilha!
- Para escrever SQL: clique com botão direito na conexão → **"Editor SQL"** → digite e pressione `Ctrl + Enter`

---

#### Opção B — VS Code com extensão SQLite Viewer (mais simples, sem instalar nada novo)

Se você já usa o VS Code, esta é a opção mais rápida — só instalar uma extensão e está pronto!

**Como instalar a extensão:**

1. Abra o VS Code
2. Pressione `Ctrl + Shift + X` (abre o painel de extensões)
3. Na busca, digite: **`SQLite Viewer`**
4. Instale a extensão de **Florian Klampfer** (tem o ícone de banco de dados verde)
   *(outra opção boa: **"SQLite"** de **alexcvzz** — também funciona muito bem)*
5. Reinicie o VS Code

**Como usar o SQLite Viewer:**

1. No painel esquerdo do VS Code, navegue até:
   `aulas/2026-04-abril/aula-02/exercicio/`
2. Clique no arquivo **`portaria.db`**
3. Pronto! Abre automaticamente uma visualização com todas as tabelas e dados

**Como executar SQL no VS Code (extensão "SQLite" de alexcvzz):**

1. Pressione `Ctrl + Shift + P` (abre o painel de comandos)
2. Digite: **`SQLite: Open Database`** e pressione Enter
3. Escolha o arquivo `portaria.db`
4. No painel esquerdo, aparece **"SQLITE EXPLORER"** — você pode ver as tabelas
5. Para rodar uma consulta: clique com o botão direito em uma tabela → **"New Query"**
6. Digite o SQL e pressione `Ctrl + Shift + Q` para executar

---

> 💡 **Qual escolher?** Se você quer algo mais completo e profissional → **DBeaver**.
> Se quer praticidade sem sair do VS Code → **SQLite Viewer + SQLite (alexcvzz)**.
> Não tem resposta errada — ambas funcionam perfeitamente para o projeto!

---

## Passo a Passo

### Passo 1: Atualize o Projeto e Abra o Terminal

Voce ja tem o projeto clonado — lembra da Aula 01? Agora so precisa **atualizar** para pegar os novos arquivos que eu enviei:

```bash
cd n7-portaria-ai
git pull
```

Depois entre na pasta do exercicio:

```bash
cd aulas/2026-04-abril/aula-02/exercicio/
```

### Passo 2: Leia o Arquivo SQL (Mais Importante!)

Antes de executar, **leia o arquivo `projeto_portaria_completo.sql` com calma**. Ele tem 6 partes:

| Parte | O Que Faz | Conceitos |
|-------|-----------|-----------|
| 1 | Limpeza (DROP TABLE) | Recriar do zero se precisar |
| 2 | Criacao das tabelas | CREATE TABLE, PRIMARY KEY, NOT NULL, UNIQUE, DEFAULT, CHECK |
| 3 | Indices | INDEX para acelerar buscas |
| 4 | Dados de exemplo | INSERT INTO com moradores, visitantes, funcionarios, veiculos e acessos |
| 5 | Consultas de estudo | SELECT, WHERE, LIKE, JOIN, GROUP BY |
| 6 | Exercicios para praticar | 10 desafios com gabarito |

**Dica:** Abra o arquivo no VS Code para ver com cores bonitas (syntax highlighting). Se preferir, pode imprimir as partes 1 a 4 para ler no papel.

### Passo 3: Execute o SQL para Criar o Banco

No terminal, execute:

```bash
sqlite3 portaria.db < projeto_portaria_completo.sql
```

**O que acontece:** O SQLite le o arquivo, cria as 5 tabelas (v3.0), insere os dados de exemplo e executa as consultas. Se tudo der certo, voce vera os resultados das consultas na tela!

### Passo 4: Explore o Banco Criado

Agora você pode explorar o banco de duas formas — escolha a que preferir!

#### Opção A: Pelo Terminal (clássico)

```bash
sqlite3 portaria.db
```

Primeiro, configure a exibição bonita:

```sql
.mode column
.headers on
```

Agora, explore:

```sql
-- Veja quais tabelas existem:
.tables

-- Veja a estrutura da tabela moradores:
.schema moradores

-- Liste todos os moradores:
SELECT * FROM moradores;

-- Liste os visitantes:
SELECT * FROM visitantes;

-- Liste os acessos:
SELECT * FROM acessos;

-- Quem está DENTRO do condominio agora?
SELECT v.nome AS visitante, m.nome AS morador, m.numero_residencia
FROM acessos a
    JOIN visitantes v ON a.visitante_id = v.id
    JOIN moradores  m ON a.morador_id   = m.id
WHERE a.dt_saida_em IS NULL;
```

Para sair do SQLite:
```sql
.quit
```

#### Opção B: Pelo DBeaver ou VS Code (visual — recomendado!)

Se você instalou o **DBeaver**:
1. Abra o DBeaver e conecte ao arquivo `portaria.db` (conforme instruções acima)
2. Clique em **Tables** no painel esquerdo
3. Clique com o botão direito em **moradores** → **Visualizar Dados**
4. Você vê todos os dados como uma planilha — pode editar direto na célula!
5. Para testar as consultas SQL do arquivo: clique com botão direito na conexão → **Editor SQL**
6. Cole qualquer SELECT da Parte 5 do arquivo .sql e pressione `Ctrl + Enter`

Se você instalou o **SQLite Viewer no VS Code**:
1. Clique no arquivo `portaria.db` no explorer do VS Code
2. Veja as tabelas e dados automaticamente
3. Para rodar SQL: `Ctrl + Shift + P` → `SQLite: Open Database` → escolha o `portaria.db`
4. Depois `Ctrl + Shift + P` → `SQLite: New Query` → cole o SQL → `Ctrl + Shift + Q`

> 💡 **Dica:** Veja os mesmos dados pelos dois jeitos! O terminal te dá mais controle, a ferramenta visual te dá mais conforto. No trabalho real, programadores usam os dois.

### Passo 5: Resolva os 10 Exercicios (Parte 6 do arquivo)

No final do arquivo SQL, tem 10 exercicios. Para cada um:

1. **Leia o enunciado** (esta como comentario `--`)
2. **Tente escrever o SQL sozinho** no terminal do SQLite
3. **Confira a resposta** descomentando o gabarito

**Nao precisa acertar todos!** O importante e tentar. Cada tentativa e aprendizado.

Aqui vai um resumo dos exercicios:

| # | Dificuldade | O Que Faz |
|---|------------|-----------|
| 1 | Facil | Inserir novo morador (INSERT) |
| 2 | Facil | Atualizar email (UPDATE) |
| 3 | Facil | Desativar morador - soft delete (UPDATE) |
| 4 | Facil | Listar visitantes nao bloqueados (SELECT WHERE) |
| 5 | Medio | Registrar saida de visitante (UPDATE WHERE NULL) |
| 6 | Medio | Contar visitas por visitante (JOIN + GROUP BY) |
| 7 | Medio | Cadastrar foto de morador (UPDATE) |
| 8 | Medio | Encontrar cadastros incompletos (IS NULL + CASE WHEN) |
| 9 | Facil | Mudar tipo de morador (UPDATE com CHECK) |
| 10 | Desafio | Relatorio de seguranca completo (CASE WHEN + ORDER BY) |

### Passo 6: Salve Seu Progresso no Git

Quando terminar (ou quando quiser salvar o progresso):

```bash
cd ../../../../
git add aulas/2026-04-abril/aula-02/exercicio/
git commit -m "tarefa-antecipada: Criar banco completo e resolver exercicios SQL"
```

---

## Conceitos Que Voce Vai Praticar

Ao completar esta tarefa, voce tera praticado:

| Conceito | Para Que Serve | Exemplo no Arquivo |
|----------|---------------|--------------------|
| CREATE TABLE | Criar tabelas | Parte 1 — 5 tabelas completas |
| PRIMARY KEY | ID unico por registro | `id INTEGER PRIMARY KEY AUTOINCREMENT` |
| NOT NULL | Campo obrigatorio | `nome TEXT NOT NULL` |
| UNIQUE | Valor sem repeticao | `cpf TEXT UNIQUE NOT NULL` |
| DEFAULT | Valor padrao automatico | `bloco TEXT DEFAULT 'A'` |
| CHECK | Validacao no banco | `CHECK(tipo_morador IN ('proprietario', 'inquilino'))` |
| FOREIGN KEY | Ligacao entre tabelas | `FOREIGN KEY (visitante_id) REFERENCES visitantes(id)` |
| INDEX | Acelerar buscas | `CREATE INDEX idx_moradores_cpf ON moradores(cpf)` |
| INSERT INTO | Inserir dados | Parte 4 — moradores, visitantes, funcionarios, veiculos, acessos |
| SELECT | Consultar dados | Parte 5 — 15+ exemplos |
| WHERE | Filtrar resultados | `WHERE ativo = 1 AND bloco = 'A'` |
| LIKE | Busca parcial | `WHERE nome LIKE '%Silva%'` |
| JOIN | Cruzar tabelas | Parte 5.4 — visitante + morador + acesso |
| GROUP BY | Agrupar e contar | `GROUP BY tipo_morador` |
| ORDER BY | Ordenar resultados | `ORDER BY nome` |
| IS NULL | Campos vazios | `WHERE foto_url IS NULL` |
| CASE WHEN | Logica condicional | Exercicios 8 e 10 |
| UPDATE | Atualizar dados | Exercicios 2, 3, 5, 7, 9 |
| Soft Delete | Desativar sem apagar | Exercicio 3 — `ativo = 0` |

---

## O Que Vai Acontecer na Aula 02

Com o banco de dados ja pronto, na Aula 02 vamos:

1. **Revisar rapidamente** o que voce criou (tirar duvidas)
2. **Conectar o banco ao Python** usando sqlite3
3. **Programar o sistema CRUD completo:**
   - Cadastrar novos moradores pelo terminal
   - Listar moradores do banco
   - Buscar por nome
   - Atualizar dados
   - Desativar morador (soft delete)
4. **Criar um menu interativo** em Python

Ou seja: **na aula a gente programa, nao fica so na teoria!**

---

## Duvidas?

Se travar em algum exercicio ou nao conseguir executar o SQL:

1. **Releia os comentarios** no arquivo — cada linha esta explicada
2. **Tente novamente** — errar faz parte do aprendizado
3. **Anote a duvida** para perguntar na Aula 02
4. **Se for algo urgente**, mande mensagem que eu ajudo

**Lembre-se:** Nao precisa ficar perfeito. O importante e ler o arquivo, executar o banco e tentar os exercicios. Qualquer duvida a gente resolve junto na aula!

---

**Bom estudo, Ademilson! Voce esta evoluindo rapido!**
