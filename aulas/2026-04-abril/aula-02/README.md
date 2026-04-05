# Aula 02 — Banco de Dados + CRUD: Do Caderno de Registros ao Sistema em Python

**Data:** 09 de abril de 2026
**Duração:** 2 horas
**Pré-requisito:** Tarefa antecipada concluída (banco `portaria.db` criado com as 3 tabelas)

---

## Antes da Aula: Tarefa Antecipada (feita na semana)

Você recebeu o arquivo `projeto_portaria_completo.sql` e durante a semana:
- Criou 3 tabelas: `moradores` (com foto, biometria e tipo), `visitantes` e `acessos`
- Inseriu dados de exemplo (5 moradores, 4 visitantes, 4 acessos)
- Praticou consultas SELECT, JOIN, GROUP BY
- Resolveu os 10 exercícios SQL

Se ainda não fez, leia o arquivo `TAREFA-ANTECIPADA.md` e siga os passos!

---

## O que Vamos Fazer Hoje

Como você já criou o banco de dados na tarefa da semana, hoje vamos **dar vida a ele usando Python!**

### Parte 1: Revisão + Teoria (30 minutos)

#### 1.1 Verificação do Banco Criado

Vamos começar confirmando que seu banco está funcionando:

```bash
sqlite3 portaria.db
.tables
SELECT COUNT(*) FROM moradores;    -- Deve retornar 5
SELECT COUNT(*) FROM visitantes;   -- Deve retornar 4
SELECT COUNT(*) FROM acessos;      -- Deve retornar 4
.quit
```

Se tiver alguma dúvida dos exercícios SQL da semana, é hora de tirar!

#### 1.2 Recapitulação Rápida: O que é um Banco de Dados?

Imagine que você trabalha na portaria do condomínio e precisa guardar informações sobre todos os moradores:
- **Cada morador tem um papel** com seus dados (nome, CPF, numero_residencia, telefone)
- **Você organiza esses papéis em uma pasta** (isso é uma **tabela**)
- **A pasta fica em um armário** que você acessa rapidamente quando precisa (isso é o **banco de dados**)

Você já fez isso na prática com SQL! Agora vamos fazer pelo Python.

#### 1.3 O que é CRUD?

Você já parou para pensar em como seu celular guarda nomes na agenda de contatos? Pois é... tudo funciona com 4 operações simples que todo programador do mundo usa!

- **C** de **Create** (Criar): Quando você adiciona um novo contato na agenda
- **R** de **Read** (Ler): Quando você abre a agenda e procura por um contato
- **U** de **Update** (Atualizar): Quando você muda o número de telefone de um amigo
- **D** de **Delete** (Deletar): Quando você apaga um contato que não precisa mais

Essas 4 operações — **CRUD** — são exatamente o que todo programa faz com dados.

#### 1.4 SQL que Você Já Conhece → Python

| O que quer fazer | SQL puro (você já sabe!) | Em Python |
|------------------|--------------------------|-----------|
| Inserir morador | `INSERT INTO moradores ...` | `cursor.execute("INSERT INTO moradores ...", (dados))` |
| Listar moradores | `SELECT * FROM moradores` | `cursor.execute("SELECT * FROM moradores")` |
| Buscar por nome | `SELECT ... WHERE nome LIKE '%João%'` | `cursor.execute("SELECT ... WHERE nome LIKE ?", ("%João%",))` |
| Atualizar dados | `UPDATE moradores SET ... WHERE id = 1` | `cursor.execute("UPDATE moradores SET ... WHERE id = ?", (1,))` |
| Soft delete | `UPDATE moradores SET ativo = 0 WHERE id = 1` | `cursor.execute("UPDATE ... SET ativo = 0 WHERE id = ?", (1,))` |

**A grande sacada:** O SQL é o MESMO que você praticou na semana! A diferença é que agora o Python executa ele para você.

#### 1.5 Trabalhando com SQLite3 no Python

```python
import sqlite3

# Conectar ao banco que você já criou
conexao = sqlite3.connect('portaria.db')
cursor = conexao.cursor()

# Executar um comando SQL
cursor.execute("SELECT * FROM moradores WHERE ativo = 1")

# Pegar os resultados
moradores = cursor.fetchall()

# Salvar mudanças (para INSERT, UPDATE, DELETE)
conexao.commit()

# Fechar a conexão quando terminar
conexao.close()
```

#### 1.6 Tratamento de Erros: try/except

Quando trabalhamos com banco de dados, coisas podem dar errado (CPF duplicado, banco travado, etc.). O `try/except` protege seu programa:

```python
try:
    cursor.execute("INSERT INTO moradores (nome, cpf) VALUES (?, ?)", (nome, cpf))
    conexao.commit()
    print("Sucesso!")
except sqlite3.IntegrityError:
    print("Erro: CPF já existe!")
except Exception as erro:
    print(f"Erro inesperado: {erro}")
```

É como dizer: "Tente fazer isso. Se der erro, faça aquilo em vez de travar."

### Parte 2: Prática — Sistema CRUD Completo (1h30)

Vamos construir um **sistema completo de gerenciamento de moradores** com menu interativo!

O arquivo `moradores_crud.py` na pasta `exercicio/` já tem:
- Conexão ao banco pronta
- Menu funcionando
- Função `atualizar_morador()` como exemplo
- TODOs nos lugares que você precisa completar

Você vai implementar:
1. **cadastrar_morador()** — Pede dados e insere no banco (CREATE)
2. **listar_moradores()** — Mostra todos os moradores ativos (READ)
3. **buscar_morador()** — Procura por nome com LIKE (READ específico)
4. **desativar_morador()** — Marca como inativo, sem deletar (DELETE macio)

Siga as instruções detalhadas no `INSTRUCOES.md`!

---

## Checklist de Aprendizado

Ao final desta aula, você conseguirá:

- [ ] Confirmar que o banco `portaria.db` da tarefa da semana está funcionando
- [ ] Explicar o que é CRUD com suas próprias palavras
- [ ] Conectar ao banco de dados SQLite a partir do Python
- [ ] Usar try/except para tratar erros
- [ ] Escrever uma função para cadastrar dados (CREATE)
- [ ] Escrever uma função para listar dados (READ)
- [ ] Escrever uma função para buscar dados (READ específico com LIKE)
- [ ] Escrever uma função para desativar dados (DELETE macio)
- [ ] Criar um menu de texto que coordena todas as operações
- [ ] Validar dados antes de salvar (evitar CPF duplicado)
- [ ] Fazer commit do seu trabalho no Git

---

## Estrutura dos Arquivos

```
aula-02/
├── README.md                       ← Este arquivo (teoria e conceitos)
├── TAREFA-ANTECIPADA.md            ← Instruções da tarefa enviada antes da aula
├── material-complementar.md        ← Vídeos e artigos para aprender mais
├── exercicio/
│   ├── INSTRUCOES.md               ← Passo a passo do exercício da aula
│   ├── schema.sql                  ← Schema da tabela moradores (referência)
│   ├── criar_banco.py              ← Script para criar o banco (referência)
│   ├── projeto_portaria_completo.sql ← SQL completo (tarefa da semana)
│   └── moradores_crud.py           ← SEU ARQUIVO DE TRABALHO DA AULA!
└── slides/
    └── apresentacao-aula02.pptx
```

---

## Próximos Passos

1. Se ainda não fez a tarefa antecipada, faça AGORA! (arquivo `TAREFA-ANTECIPADA.md`)
2. Na aula, abra o `INSTRUCOES.md` e siga os passos
3. Complete o `moradores_crud.py` com as funções CRUD
4. Se ficou com dúvida, revise a teoria acima ou consulte o `material-complementar.md`

**Na Aula 03**, vamos continuar evoluindo o CRUD: adicionar busca de visitantes, consultas com JOIN entre tabelas, e começar a organizar o código em camadas (separação de responsabilidades).

---

**Dica importante**: CRUD aparece em TUDO na programação. Cada aplicativo, site ou sistema que você usa no dia a dia faz CRUD. Depois dessa aula, você vai olhar para o WhatsApp, Instagram e Netflix de um jeito diferente!
