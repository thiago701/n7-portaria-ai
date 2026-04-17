#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  MODELO DE DOMINIO: Funcionario
  n7-portaria-ai | Aula 02
============================================================

Este arquivo mapeia a tabela 'funcionarios' do banco de dados
para uma classe Python usando @dataclass.

O QUE E UM FUNCIONARIO?
  Pessoa que TRABALHA no condominio:
  - porteiro  → quem opera o sistema na portaria
  - zelador   → manutencao geral
  - administrador → gestao do condominio
  - outro     → qualquer outro cargo

  >> CONTRIBUICAO DO ADEMILSON (v3.0):
  Ele identificou que o sistema precisava saber QUEM registrou
  cada acesso. Isso deu origem a esta tabela!

SEGURANCA:
  O campo senha_hash armazena o SHA-256 da senha — NUNCA
  a senha em texto puro! Se alguem acessar o banco, nao
  consegue descobrir as senhas.

  Python: import hashlib
          hashlib.sha256('minha_senha'.encode()).hexdigest()
          → '64 caracteres hexadecimais'

MAPEAMENTO:
  +-----------------------+------------------+-----------------+
  | Coluna SQL            | Atributo Python  | Tipo Python     |
  +-----------------------+------------------+-----------------+
  | id                    | id               | Optional[int]   |
  | nome                  | nome             | str             |
  | cpf                   | cpf              | str             |
  | cargo                 | cargo            | str             |
  | setor                 | setor            | Optional[str]   |
  | login                 | login            | str             |
  | senha_hash            | senha_hash       | str             |
  | ativo                 | ativo            | bool            |
  | correlation_id        | correlation_id   | str             |
  | dt_criado_em          | dt_criado_em     | Optional[datetime]|
  +-----------------------+------------------+-----------------+
============================================================
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.core.models.base import parse_datetime


# ============================================================
# CARGOS VALIDOS
# ============================================================
# O banco aceita apenas estes valores (CHECK constraint).
# 'porteiro' e o padrao — e o cargo mais comum.

CARGOS_VALIDOS = ("porteiro", "zelador", "administrador", "outro")


@dataclass
class Funcionario:
    """
    Representa um funcionario do condominio.

    Exemplos de uso:
        >>> import hashlib
        >>> senha = hashlib.sha256("senha123".encode()).hexdigest()
        >>> func = Funcionario(
        ...     nome="Jose Porteiro",
        ...     cpf="11122233344",
        ...     login="jose.porteiro",
        ...     senha_hash=senha,
        ...     correlation_id="abc123..."
        ... )
        >>> print(func.cargo)  # 'porteiro'
    """

    # ──────────────────────────────────────────────────────
    # CAMPOS OBRIGATORIOS (NOT NULL no SQL)
    # ──────────────────────────────────────────────────────

    nome: str
    # SQL: nome TEXT NOT NULL
    # Nome completo do funcionario.

    cpf: str
    # SQL: cpf TEXT UNIQUE NOT NULL CHECK(length(cpf) = 11)
    # CPF sem pontos (11 digitos). UNIQUE = nao repete.

    login: str
    # SQL: login TEXT UNIQUE NOT NULL
    # Login unico para acessar o sistema.
    # Ex: 'jose.porteiro', 'maria.zeladora'

    senha_hash: str
    # SQL: senha_hash TEXT NOT NULL CHECK(length(senha_hash) = 64)
    # SHA-256 da senha (SEMPRE 64 caracteres hex).
    #
    # NUNCA armazenar senha em texto puro!
    # Python: hashlib.sha256('senha'.encode()).hexdigest()
    #
    # Por que 64? SHA-256 gera 256 bits = 32 bytes = 64 hex chars.

    correlation_id: str
    # SQL: correlation_id TEXT UNIQUE NOT NULL
    # Hash SHA-256 para sincronizacao.

    # ──────────────────────────────────────────────────────
    # CAMPOS OPCIONAIS (com valor padrao)
    # ──────────────────────────────────────────────────────

    id: Optional[int] = None
    # SQL: id INTEGER PRIMARY KEY AUTOINCREMENT

    cargo: str = "porteiro"
    # SQL: cargo TEXT DEFAULT 'porteiro'
    #      CHECK(cargo IN ('porteiro','zelador','administrador','outro'))
    # O cargo determina as permissoes no sistema.

    setor: Optional[str] = None
    # SQL: setor TEXT
    # Texto livre: 'portaria', 'administracao', 'limpeza', 'manutencao'.
    # Nao tem CHECK — o condominio define os setores.

    ativo: bool = True
    # SQL: ativo BOOLEAN DEFAULT 1 CHECK(ativo IN (0, 1))
    # True = ativo. False = desligado (soft delete).

    dt_criado_em: Optional[datetime] = None
    # SQL: dt_criado_em DATETIME DEFAULT CURRENT_TIMESTAMP

    # ──────────────────────────────────────────────────────
    # VALIDACOES
    # ──────────────────────────────────────────────────────

    def __post_init__(self):
        """Valida os dados assim que o objeto e criado."""
        self._validar_cpf()
        self._validar_cargo()
        self._validar_senha_hash()

    def _validar_cpf(self):
        """CPF deve ter exatamente 11 digitos numericos."""
        cpf_limpo = self.cpf.strip()
        if not cpf_limpo.isdigit():
            raise ValueError(f"CPF deve conter apenas numeros. Recebido: '{self.cpf}'")
        if len(cpf_limpo) != 11:
            raise ValueError(f"CPF deve ter 11 digitos. Recebido: {len(cpf_limpo)} digitos")
        self.cpf = cpf_limpo

    def _validar_cargo(self):
        """cargo deve ser um dos valores aceitos."""
        if self.cargo not in CARGOS_VALIDOS:
            raise ValueError(
                f"cargo invalido: '{self.cargo}'. "
                f"Valores aceitos: {CARGOS_VALIDOS}"
            )

    def _validar_senha_hash(self):
        """senha_hash deve ter exatamente 64 caracteres hexadecimais."""
        if len(self.senha_hash) != 64:
            raise ValueError(
                f"senha_hash deve ter 64 caracteres (SHA-256). "
                f"Recebido: {len(self.senha_hash)} caracteres"
            )

    # ──────────────────────────────────────────────────────
    # CONVERSAO: BANCO → OBJETO
    # ──────────────────────────────────────────────────────

    @classmethod
    def from_db_row(cls, row) -> "Funcionario":
        """
        Cria um Funcionario a partir de uma linha do banco.

        Uso:
            cursor.execute("SELECT * FROM funcionarios WHERE id = ?", (1,))
            linha = cursor.fetchone()
            func = Funcionario.from_db_row(linha)
        """
        return cls(
            id=row["id"],
            nome=row["nome"],
            cpf=row["cpf"],
            cargo=row["cargo"] or "porteiro",
            setor=row["setor"],
            login=row["login"],
            senha_hash=row["senha_hash"],
            ativo=bool(row["ativo"]),
            correlation_id=row["correlation_id"],
            dt_criado_em=parse_datetime(row["dt_criado_em"]),
        )

    # ──────────────────────────────────────────────────────
    # CONVERSAO: OBJETO → BANCO
    # ──────────────────────────────────────────────────────

    def to_db_dict(self) -> dict:
        """Converte para dicionario pronto para INSERT/UPDATE."""
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "cargo": self.cargo,
            "setor": self.setor,
            "login": self.login,
            "senha_hash": self.senha_hash,
            "ativo": 1 if self.ativo else 0,
            "correlation_id": self.correlation_id,
        }

    # ──────────────────────────────────────────────────────
    # METODOS DE EXIBICAO
    # ──────────────────────────────────────────────────────

    @property
    def cpf_formatado(self) -> str:
        """Retorna CPF formatado: 123.456.789-01"""
        c = self.cpf
        if len(c) == 11 and c.isdigit():
            return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"
        return c

    @property
    def status_texto(self) -> str:
        """Retorna 'Ativo' ou 'Desligado'."""
        return "Ativo" if self.ativo else "Desligado"

    def resumo(self) -> str:
        """Retorna um resumo de uma linha."""
        setor_txt = f" ({self.setor})" if self.setor else ""
        return (
            f"[{self.id or 'NOVO'}] {self.nome} | "
            f"{self.cargo}{setor_txt} | "
            f"Login: {self.login} | {self.status_texto}"
        )


# ──────────────────────────────────────────────────────────
# EXEMPLO DE USO (execute este arquivo para testar!)
#   python src/core/models/funcionario.py
# ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import hashlib

    print("=" * 60)
    print("  TESTANDO O MODELO Funcionario")
    print("=" * 60)

    # 1. Criar porteiro
    senha = hashlib.sha256("porteiro123".encode()).hexdigest()
    cid = hashlib.sha256(b"funcionarios:22233344455").hexdigest()
    f = Funcionario(
        nome="Jose da Silva",
        cpf="22233344455",
        login="jose.silva",
        senha_hash=senha,
        setor="portaria",
        correlation_id=cid,
    )
    print(f"\n1. Funcionario criado:")
    print(f"   {f.resumo()}")
    print(f"   CPF formatado: {f.cpf_formatado}")

    # 2. Dicionario para INSERT
    dados = f.to_db_dict()
    print(f"\n2. Dicionario para INSERT:")
    for chave, valor in dados.items():
        print(f"   {chave}: {valor}")

    # 3. Validacoes
    print(f"\n3. Testando validacoes:")
    try:
        Funcionario(nome="X", cpf="123", login="x",
                    senha_hash=senha, correlation_id="x")
    except ValueError as e:
        print(f"   OK! CPF invalido: {e}")

    try:
        Funcionario(nome="X", cpf="11111111111", login="x",
                    cargo="gerente", senha_hash=senha, correlation_id="x")
    except ValueError as e:
        print(f"   OK! Cargo invalido: {e}")

    try:
        Funcionario(nome="X", cpf="11111111111", login="x",
                    senha_hash="curta", correlation_id="x")
    except ValueError as e:
        print(f"   OK! Senha curta: {e}")

    print(f"\n{'=' * 60}")
    print("  TUDO FUNCIONANDO!")
    print("=" * 60)
