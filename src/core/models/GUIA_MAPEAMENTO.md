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

## Mapeamento Completo — 9/9 Tabelas

Todas as 9 tabelas do `projeto_portaria_completo.sql` estão mapeadas!

| Tabela SQL | Arquivo Python | Status |
|------------|---------------|--------|
| ✅ moradores | `morador.py` | Feito! (16 campos, CPF + LGPD + biometria) |
| ✅ residencias | `residencia.py` | Feito! (campos do Ademilson: tipo_moradia, interfone, observacao) |
| ✅ morador_residencia | `morador_residencia.py` | Feito! (junction table N:N com 2 FKs) |
| ✅ visitantes | `visitante.py` | Feito! (bloqueio + janela de validade) |
| ✅ funcionarios | `funcionario.py` | Feito! (senha SHA-256, cargos, login) |
| ✅ veiculos | `veiculo.py` | Feito! (3 FKs mutuamente exclusivas) |
| ✅ acessos | `acesso.py` | Feito! (2FA: senha + digital + facial) |
| ✅ config_acesso_morador | `config_acesso_morador.py` | Feito! (política 1:1 por morador) |
| ✅ assinatura_condominio | `assinatura_condominio.py` | Feito! (contrato + vigência) |

**Todos usam funções compartilhadas do `base.py`** (parse_date, parse_datetime).

**Para estudar:** abra cada arquivo `.py` e leia os comentários — eles
explicam o mapeamento SQL → Python passo a passo!
