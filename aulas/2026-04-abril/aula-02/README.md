# Aula 02 — Banco de Dados na Prática: DBeaver + SQLite + Python

**Data:** 09 de abril de 2026
**Duração:** 2 horas
**Pré-requisito:** Ter o DBeaver instalado (baixe em dbeaver.io)

---

## O que Vamos Fazer Hoje

Hoje é dia de colocar a mão na massa! Vamos:

1. **Configurar o DBeaver** — ferramenta visual para explorar o banco
2. **Abrir e explorar** as tabelas do nosso projeto
3. **Revisar juntos** a estrutura dos dados (moradores, residências, acessos)
4. **Entender como SQL vira Python** — o mapeamento de domínio
5. **Rodar o sistema CRUD** de moradores pelo terminal

Sem pressa — vamos no ritmo certo!

---

## Parte 1: Configurando o DBeaver (30 minutos)

O DBeaver é como um "explorador de arquivos" para bancos de dados.
Em vez de pastas e arquivos, você vê **tabelas e registros**!

### Passo a Passo

1. Abra o DBeaver
2. Menu: **Database → New Connection** (ou botão "+")
3. Procure **SQLite** na lista e clique **Next**
4. Clique **Browse** e navegue até: `src/infra/database/portaria.db`
5. Clique **Test Connection** — deve aparecer "Connected!"
6. Clique **Finish**
7. No painel esquerdo, expanda: **portaria.db → Tables**
8. Clique em **moradores** → aba **Data** para ver os registros!

**Pronto!** Agora você pode ver todos os dados do banco visualmente.

---

## Parte 2: Revisando as Tabelas Juntos (30 minutos)

Nosso banco tem **9 tabelas** — como 9 gavetas de um armário:

| Tabela | O que guarda |
|--------|-------------|
| `moradores` | Dados pessoais (nome, CPF, foto) |
| `residencias` | Apartamentos e casas |
| `morador_residencia` | Quem mora onde (a "ponte") |
| `visitantes` | Quem visita o condomínio |
| `funcionarios` | Porteiros, zeladores |
| `veiculos` | Carros e motos |
| `acessos` | Entradas e saídas |
| `config_acesso_morador` | Regras de segurança |
| `assinatura_condominio` | Contrato do condomínio |

### A Grande Sacada: Tabelas Conectadas

A tabela `moradores` guarda dados **pessoais** (nome, CPF).
O **endereço** fica em `residencias`.
A **ponte** entre eles é `morador_residencia`.

```
moradores  ←→  morador_residencia  ←→  residencias
(pessoa)        (quem mora onde)       (apartamento)
```

Isso permite que um morador tenha vários apartamentos!

---

## Parte 3: SQL → Python — O Domínio (20 minutos)

Cada tabela do banco vira uma **classe Python**:

```python
# No SQL:
#   CREATE TABLE moradores (
#       nome TEXT NOT NULL,
#       cpf  TEXT UNIQUE NOT NULL,
#       ...
#   );

# No Python (arquivo src/core/models/morador.py):
@dataclass
class Morador:
    nome: str              # TEXT NOT NULL → str (obrigatório)
    cpf: str               # TEXT UNIQUE   → str (obrigatório)
    id: Optional[int] = None  # PRIMARY KEY → None (banco gera)
    ativo: bool = True     # DEFAULT 1    → True
```

O arquivo `morador.py` já está pronto com todos os campos mapeados.
Abra e leia os comentários — cada atributo explica a coluna SQL correspondente.

---

## Parte 4: Prática — Rodando o CRUD (40 minutos)

Agora vamos rodar o sistema CRUD pelo terminal!

```bash
cd aulas/2026-04-abril/aula-02/exercicio
python moradores_crud.py
```

O menu permite:
- **1** — Cadastrar um morador novo
- **2** — Listar todos os moradores (com JOIN das residências!)
- **3** — Buscar por nome
- **4** — Atualizar telefone/email
- **5** — Desativar (soft delete)
- **6** — Ver resumo do condomínio

Experimente cadastrar um morador, listar, buscar... Explore!

---

## Tarefa da Semana

Você já tem o modelo de `moradores` pronto (`src/core/models/morador.py`).
Agora é sua vez de criar os modelos das outras tabelas!

### Como fazer:

1. Abra o `GUIA_MAPEAMENTO.md` em `src/core/models/`
2. Abra o `projeto_portaria_completo.sql` no DBeaver
3. Siga a receita: olhe o CREATE TABLE → crie a classe Python

### Tabelas para mapear:

| Arquivo a criar | Tabela SQL | Dificuldade |
|----------------|-----------|-------------|
| `visitante.py` | visitantes | Fácil |
| `funcionario.py` | funcionarios | Fácil |
| `residencia.py` | residencias | Fácil |
| `veiculo.py` | veiculos | Médio |

**Dica:** Comece pelo `visitante.py` — é o mais parecido com `morador.py`!

---

## Checklist de Aprendizado

Ao final desta aula, você conseguirá:

- [ ] Conectar o DBeaver ao banco SQLite
- [ ] Explorar tabelas e dados visualmente
- [ ] Explicar como as 9 tabelas se relacionam
- [ ] Entender o mapeamento SQL → classe Python
- [ ] Rodar o CRUD de moradores pelo terminal
- [ ] Cadastrar, buscar e listar moradores

---

## Estrutura dos Arquivos

```
aula-02/
├── README.md                         ← Este arquivo
├── TAREFA-ANTECIPADA.md              ← Instruções da semana anterior
├── material-complementar.md          ← Vídeos e artigos extras
├── exercicio/
│   ├── INSTRUCOES.md                 ← Passo a passo detalhado
│   ├── moradores_crud.py             ← Sistema CRUD (alinhado ao SQL completo)
│   ├── criar_banco.py                ← Script de criação + missões
│   ├── projeto_portaria_completo.sql ← SQL com todas as 9 tabelas
│   ├── projeto_portaria_sqlserver.sql← Versão SQL Server
│   ├── schema.sql                    ← Schema simplificado
│   └── portaria.db                   ← Banco de dados SQLite
└── slides/
    ├── apresentacao-aula02.pptx      ← Slides da aula
    └── gerar-apresentacao.js         ← Script de geração
```

---

**Lembre-se:** Programação se aprende praticando. Se travar em alguma parte,
releia os comentários no código — eles foram escritos pensando em você!
