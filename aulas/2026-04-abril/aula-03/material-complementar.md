# Material Complementar — Revisao sobre Mapeamento de Dominio

Este material resume os conceitos do ebook "Do SQL para o Python"
de forma rapida e visual. Use como cola de consulta durante o jogo
e sempre que precisar relembrar!

---

## Os 5 Pontos da Mochila

Esses sao os conceitos que voce PRECISA carregar consigo.
Se lembrar desses 5, voce consegue mapear qualquer tabela!

### 1. Tabela vira Classe

```
SQL:    CREATE TABLE moradores (...)
Python: class Morador:
```

O nome da tabela e plural e minusculo (moradores).
O nome da classe e singular e com letra maiuscula (Morador).

### 2. Coluna vira Atributo

```
SQL:    nome TEXT NOT NULL
Python: nome: str
```

Cada coluna da tabela se torna um campo da classe Python.

### 3. Use @dataclass

```python
from dataclasses import dataclass

@dataclass
class Morador:
    nome: str
    cpf: str
```

O `@dataclass` e a "etiqueta magica" que diz ao Python:
"Gere o __init__, __repr__ e __eq__ automaticamente pra mim!"

### 4. NULL vira Optional

```
SQL:    telefone TEXT           (aceita NULL)
Python: telefone: Optional[str] = None
```

Se a coluna aceita NULL no banco, no Python usamos Optional
com valor padrao None.

### 5. Obrigatorios Primeiro!

```python
@dataclass
class Morador:
    # SEM valor padrao (obrigatorios) — VEM PRIMEIRO
    nome: str
    cpf: str

    # COM valor padrao (opcionais) — VEM DEPOIS
    id: Optional[int] = None
    telefone: Optional[str] = None
    ativo: bool = True
```

Essa ordem e OBRIGATORIA no Python. Trocar da erro!

---

## Tabela de Traducao Rapida

Use esta tabela como "dicionario de bolso":

```
SQL                          Python
─────────────────────────    ──────────────────────────
TEXT NOT NULL                str
TEXT (aceita NULL)           Optional[str] = None
INTEGER PRIMARY KEY          Optional[int] = None
INTEGER NOT NULL             int
BOOLEAN DEFAULT 1            bool = True
BOOLEAN DEFAULT 0            bool = False
DATE / DATETIME              Optional[date/datetime] = None
BLOB                         Optional[bytes] = None
TEXT DEFAULT 'valor'         str = "valor"
```

---

## Exemplo Completo: Visitante

### No banco (SQL):

```sql
CREATE TABLE visitantes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nome            TEXT NOT NULL,
    documento       TEXT NOT NULL,
    tipo_documento  TEXT DEFAULT 'RG',
    telefone        TEXT,
    bloqueado       BOOLEAN DEFAULT 0
);
```

### No Python:

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Visitante:
    # Obrigatorios (sem valor padrao)
    nome: str
    documento: str

    # Opcionais (com valor padrao)
    id: Optional[int] = None
    tipo_documento: str = "RG"
    telefone: Optional[str] = None
    bloqueado: bool = False
```

### Passo a passo da traducao:

1. `id INTEGER PRIMARY KEY` → auto-gerado → `Optional[int] = None`
2. `nome TEXT NOT NULL` → obrigatorio → `str` (sem padrao)
3. `documento TEXT NOT NULL` → obrigatorio → `str` (sem padrao)
4. `tipo_documento TEXT DEFAULT 'RG'` → tem padrao → `str = "RG"`
5. `telefone TEXT` → aceita NULL → `Optional[str] = None`
6. `bloqueado BOOLEAN DEFAULT 0` → tem padrao → `bool = False`
7. Reordena: obrigatorios (nome, documento) primeiro, opcionais depois!

---

## Metodos Uteis nos Nossos Models

Todos os models do projeto seguem o mesmo padrao:

```python
# Converter linha do banco → objeto Python
morador = Morador.from_db_row(row)

# Converter objeto Python → dicionario para INSERT
dados = morador.to_db_dict()

# Ver resumo legivel
print(morador.resumo())
```

---

## As 9 Tabelas do Projeto

Todas mapeadas! Cada uma esta em `src/core/models/`:

```
moradores           → morador.py           (16 campos)
residencias         → residencia.py        (campos do Ademilson!)
morador_residencia  → morador_residencia.py (tabela de ligacao N:N)
visitantes          → visitante.py         (bloqueio + validade)
funcionarios        → funcionario.py       (senha SHA-256)
veiculos            → veiculo.py           (3 donos possiveis)
acessos             → acesso.py            (2FA: senha+digital+facial)
config_acesso       → config_acesso_morador.py (politica 1:1)
assinatura          → assinatura_condominio.py (contrato)
```

---

## Dica de Ouro

Quando olhar um CREATE TABLE novo, faca sempre nesta ordem:

1. Identifique as colunas NOT NULL → serao campos obrigatorios
2. Identifique as colunas com DEFAULT ou que aceitam NULL → opcionais
3. Escreva a classe com obrigatorios PRIMEIRO
4. Adicione @dataclass no topo
5. Pronto! Teste criando um objeto

---

## Perguntas Frequentes

### "Preciso decorar todos os tipos?"

Nao! Use a tabela de traducao acima como referencia.
Com a pratica, vai se tornando natural.

### "Por que id e Optional[int] e nao int?"

Porque quando criamos um objeto NOVO, ele ainda nao tem id.
O banco gera o id depois do INSERT (AUTOINCREMENT).
Entao o id comeca como None e so recebe valor depois de salvar.

### "O que acontece se eu colocar opcional antes de obrigatorio?"

O Python da erro! Campos sem valor padrao NAO podem vir
depois de campos com valor padrao. E uma regra da linguagem.

---

## Proximos Passos

Na **Aula 04**, vamos colocar a mao no codigo de verdade:
criar models novos no projeto usando tudo que praticamos hoje.
Depois do jogo, tudo faz muito mais sentido!
