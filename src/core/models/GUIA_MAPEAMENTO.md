# Como Mapear uma Tabela SQL para Python

## A Receita é Sempre a Mesma!

Pense assim: cada tabela do banco é como uma **ficha cadastral**.
A classe Python é o **modelo dessa ficha**.

```
BANCO DE DADOS (SQL)          PYTHON (classe)
────────────────────          ─────────────────
Tabela moradores        →     class Morador
Coluna 'nome'           →     self.nome
Uma linha (registro)    →     Um objeto Morador(...)
```

## Passo a Passo

### 1. Olhe o CREATE TABLE no SQL

```sql
CREATE TABLE visitantes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nome            TEXT NOT NULL,
    documento       TEXT NOT NULL,
    tipo_documento  TEXT DEFAULT 'RG',
    telefone        TEXT,
    bloqueado       BOOLEAN DEFAULT 0,
    correlation_id  TEXT UNIQUE NOT NULL,
    dt_criado_em    DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Traduza cada coluna

| Coluna SQL | Tipo SQL | Obrigatório? | → Tipo Python | → Valor padrão |
|------------|----------|-------------|---------------|----------------|
| id | INTEGER PRIMARY KEY | Auto | `Optional[int]` | `None` |
| nome | TEXT NOT NULL | Sim | `str` | (sem padrão) |
| documento | TEXT NOT NULL | Sim | `str` | (sem padrão) |
| tipo_documento | TEXT DEFAULT 'RG' | Não | `str` | `"RG"` |
| telefone | TEXT | Não | `Optional[str]` | `None` |
| bloqueado | BOOLEAN DEFAULT 0 | Não | `bool` | `False` |
| correlation_id | TEXT NOT NULL | Sim | `str` | (sem padrão) |
| dt_criado_em | DATETIME DEFAULT | Auto | `Optional[datetime]` | `None` |

### 3. Escreva a classe

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Visitante:
    # Obrigatórios primeiro (sem valor padrão)
    nome: str
    documento: str
    correlation_id: str

    # Opcionais depois (com valor padrão)
    id: Optional[int] = None
    tipo_documento: str = "RG"
    telefone: Optional[str] = None
    bloqueado: bool = False
    dt_criado_em: Optional[datetime] = None
```

### 4. Pronto! Teste:

```python
visitante = Visitante(
    nome="Carlos Entregador",
    documento="12345678",
    correlation_id="abc123"
)
print(visitante.nome)       # Carlos Entregador
print(visitante.bloqueado)  # False
```

## Tabelas para Você Mapear Esta Semana

Siga a mesma receita para criar estes arquivos:

| Tabela SQL | Arquivo Python | Dificuldade |
|------------|---------------|-------------|
| ✅ moradores | `morador.py` | Feito! (exemplo completo) |
| ✅ visitantes | `visitante.py` | Fácil (copie o exemplo acima) |
| ⬜ funcionarios | `funcionario.py` | Fácil |
| ✅ residencias | `residencia.py` | Feito! (com campos do Ademilson: tipo_moradia, interfone, observacao) |
| ⬜ veiculos | `veiculo.py` | Médio |
| ✅ morador_residencia | `morador_residencia.py` | Feito! (junction table N:N com 2 FKs) |

**Dica:** Abra o `projeto_portaria_completo.sql`, encontre o CREATE TABLE
da tabela que vai mapear, e siga os passos 1-2-3 acima!
