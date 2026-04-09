#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  MODELO BASE — Guia para Mapear Tabelas SQL → Python
  n7-portaria-ai | Aula 02
============================================================

COMO FUNCIONA O MAPEAMENTO:

  ┌──────────────┐          ┌──────────────────┐
  │  TABELA SQL  │    →     │  CLASSE PYTHON   │
  │  (banco)     │          │  (@dataclass)    │
  └──────────────┘          └──────────────────┘

  Cada TABELA vira uma CLASSE.
  Cada COLUNA vira um ATRIBUTO.
  Cada LINHA vira um OBJETO (instância).

RECEITA PARA MAPEAR UMA TABELA:

  1. Olhe o CREATE TABLE no SQL
  2. Crie uma classe com @dataclass
  3. Para cada coluna, crie um atributo:
     ┌───────────────────────┬────────────────────────┐
     │ Tipo SQL              │ Tipo Python            │
     ├───────────────────────┼────────────────────────┤
     │ INTEGER               │ int                    │
     │ TEXT                   │ str                    │
     │ BOOLEAN (0/1)         │ bool                   │
     │ BLOB                  │ bytes                  │
     │ DATE                  │ date                   │
     │ DATETIME              │ datetime               │
     │ REAL                  │ float                  │
     ├───────────────────────┼────────────────────────┤
     │ NOT NULL              │ campo obrigatório      │
     │ pode ser NULL         │ Optional[tipo] = None  │
     │ DEFAULT valor         │ atributo = valor       │
     │ PRIMARY KEY AUTO...   │ Optional[int] = None   │
     └───────────────────────┴────────────────────────┘

  4. Adicione from_db_row() e to_db_dict()
  5. Adicione validações em __post_init__()

EXEMPLO VISUAL:

  SQL:
    CREATE TABLE visitantes (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        nome        TEXT NOT NULL,
        documento   TEXT NOT NULL,
        telefone    TEXT,
        bloqueado   BOOLEAN DEFAULT 0,
        ...
    );

  Python:
    @dataclass
    class Visitante:
        nome: str                          # NOT NULL → obrigatório
        documento: str                     # NOT NULL → obrigatório
        id: Optional[int] = None           # PRIMARY KEY AUTO → None
        telefone: Optional[str] = None     # pode ser NULL → Optional
        bloqueado: bool = False            # DEFAULT 0 → False
"""

from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


@dataclass
class ModeloBase:
    """
    Classe base com campos comuns a TODAS as tabelas do projeto.

    Toda tabela do n7-portaria-ai tem estes campos:
      - id: chave primária autoincrement
      - correlation_id: identificador único para sincronização
      - dt_criado_em: timestamp de criação

    Quando você for criar o modelo de outra tabela, herde desta:

        @dataclass
        class Visitante(ModeloBase):
            nome: str
            documento: str
            ...

    NOTA PARA O ALUNO:
    ─────────────────
    Herdar de ModeloBase é OPCIONAL neste momento.
    Se preferir, copie os campos id, correlation_id e
    dt_criado_em diretamente na sua classe. O importante
    é praticar o mapeamento!
    """

    id: Optional[int] = None
    # SQL: id INTEGER PRIMARY KEY AUTOINCREMENT
    # Gerado pelo banco. None quando o objeto ainda não foi salvo.

    correlation_id: str = ""
    # SQL: correlation_id TEXT UNIQUE NOT NULL
    # Hash SHA-256 para sincronização sem duplicatas.

    dt_criado_em: Optional[datetime] = None
    # SQL: dt_criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
    # Preenchido automaticamente pelo banco na inserção.


# ──────────────────────────────────────────────────────────
# FUNÇÕES UTILITÁRIAS COMPARTILHADAS
# ──────────────────────────────────────────────────────────

def parse_date(valor) -> Optional[date]:
    """
    Converte string do banco para date do Python.

    O SQLite armazena datas como TEXT ('2026-04-09').
    Esta função converte para date(2026, 4, 9).

    Uso:
        dt = parse_date(row['dt_nascimento'])
    """
    if valor is None:
        return None
    try:
        return datetime.strptime(str(valor), "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def parse_datetime(valor) -> Optional[datetime]:
    """
    Converte string do banco para datetime do Python.

    O SQLite armazena timestamps como TEXT ('2026-04-09 10:30:00').
    Esta função converte para datetime(2026, 4, 9, 10, 30, 0).

    Uso:
        dt = parse_datetime(row['dt_criado_em'])
    """
    if valor is None:
        return None
    try:
        return datetime.strptime(str(valor), "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return None
