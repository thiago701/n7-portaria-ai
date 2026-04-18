#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  MODELO DE DOMÍNIO: Morador
  n7-portaria-ai | Aula 02
============================================================

Este arquivo mapeia a tabela 'moradores' do banco de dados
para uma classe Python usando @dataclass.

┌─────────────────────────────────────────────────────────┐
│  TABELA SQL              →   CLASSE PYTHON              │
│  moradores               →   Morador                    │
│  coluna 'nome'           →   atributo self.nome         │
│  cada linha              →   um objeto Morador(...)      │
└─────────────────────────────────────────────────────────┘

POR QUE USAR @dataclass?
  - Gera __init__() automaticamente (não precisa escrever)
  - Gera __repr__() (print bonito do objeto)
  - Gera __eq__() (comparação por valores)
  - É padrão do Python — sem instalar nada!

COMO LER ESTE ARQUIVO:
  Cada atributo tem um comentário explicando:
    1. O que é
    2. Qual coluna SQL corresponde
    3. Tipo de dado e valor padrão
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional

from src.core.models.base import parse_date, parse_datetime


@dataclass
class Morador:
    """
    Representa um morador do condomínio.

    Mapeamento direto da tabela SQL 'moradores':
    ┌──────────────────────┬──────────────────┬───────────────┐
    │ Coluna SQL           │ Atributo Python  │ Tipo Python   │
    ├──────────────────────┼──────────────────┼───────────────┤
    │ id                   │ id               │ Optional[int] │
    │ nome                 │ nome             │ str           │
    │ cpf                  │ cpf              │ str           │
    │ telefone             │ telefone         │ Optional[str] │
    │ email                │ email            │ Optional[str] │
    │ dt_nascimento        │ dt_nascimento    │ Optional[date]│
    │ foto                 │ foto             │ Optional[bytes]│
    │ dt_foto_validade     │ dt_foto_validade │ Optional[date]│
    │ biometria            │ biometria        │ Optional[bytes]│
    │ dt_biometria_validade│ dt_biometria_val │ Optional[date]│
    │ termos_lgpd          │ termos_lgpd      │ Optional[bytes]│
    │ dt_aceite_lgpd       │ dt_aceite_lgpd   │ Optional[datetime]│
    │ ativo                │ ativo            │ bool          │
    │ correlation_id       │ correlation_id   │ str           │
    │ dt_criado_em         │ dt_criado_em     │ Optional[datetime]│
    │ dt_atualizado_em     │ dt_atualizado_em │ Optional[datetime]│
    └──────────────────────┴──────────────────┴───────────────┘

    Uso básico:
        >>> morador = Morador(
        ...     nome="João Silva",
        ...     cpf="11122233344",
        ...     correlation_id="abc123..."
        ... )
        >>> print(morador.nome)
        João Silva
        >>> print(morador.ativo)
        True
    """

    # ──────────────────────────────────────────────────────
    # CAMPOS OBRIGATÓRIOS (NOT NULL no SQL)
    # Estes devem ser passados ao criar o objeto.
    # ──────────────────────────────────────────────────────

    nome: str
    # SQL: nome TEXT NOT NULL
    # Nome completo do morador. Obrigatório.

    cpf: str
    # SQL: cpf TEXT UNIQUE NOT NULL CHECK(length(cpf) = 11)
    # CPF com 11 dígitos, sem pontos ou traços.
    # UNIQUE = não pode ter dois moradores com o mesmo CPF.

    correlation_id: str
    # SQL: correlation_id TEXT UNIQUE NOT NULL
    # Identificador único para sincronização.
    # Gerado por: hashlib.sha256(f'moradores:{cpf}'.encode()).hexdigest()

    # ──────────────────────────────────────────────────────
    # CAMPOS OPCIONAIS (podem ser NULL no SQL)
    # Estes têm valor padrão None — não precisa passar.
    # ──────────────────────────────────────────────────────

    id: Optional[int] = None
    # SQL: id INTEGER PRIMARY KEY AUTOINCREMENT
    # Gerado automaticamente pelo banco ao inserir.
    # Quando criamos um Morador novo, id ainda não existe (None).

    telefone: Optional[str] = None
    # SQL: telefone TEXT
    # Telefone de contato. Ex: '83999001122'

    email: Optional[str] = None
    # SQL: email TEXT CHECK(email LIKE '%@%.%')
    # E-mail com validação básica (precisa ter @ e .)

    dt_nascimento: Optional[date] = None
    # SQL: dt_nascimento DATE
    # Data de nascimento. Formato: date(2000, 1, 15)

    # ── Dados biométricos e foto ─────────────────────────

    foto: Optional[bytes] = None
    # SQL: foto BLOB
    # Bytes da foto (JPG/PNG). Em produção:
    #   with open('foto.jpg', 'rb') as f: foto = f.read()

    dt_foto_validade: Optional[date] = None
    # SQL: dt_foto_validade DATE
    # Renovar a cada 2 anos — pessoas mudam!

    biometria: Optional[bytes] = None
    # SQL: biometria BLOB
    # Template biométrico (impressão digital).

    dt_biometria_validade: Optional[date] = None
    # SQL: dt_biometria_validade DATE
    # Renovar a cada 2 anos.

    # ── LGPD (Lei Geral de Proteção de Dados) ────────────

    termos_lgpd: Optional[bytes] = None
    # SQL: termos_lgpd BLOB
    # PDF dos Termos de Uso aceitos — evidência jurídica.

    dt_aceite_lgpd: Optional[datetime] = None
    # SQL: dt_aceite_lgpd DATETIME
    # Quando o morador aceitou os termos. NULL = pendente.

    # ── Controle do registro ─────────────────────────────

    ativo: bool = True
    # SQL: ativo BOOLEAN DEFAULT 1 CHECK(ativo IN (0, 1))
    # True = ativo. False = soft delete (dado preservado).

    dt_criado_em: Optional[datetime] = None
    # SQL: dt_criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
    # Preenchido automaticamente pelo banco.

    dt_atualizado_em: Optional[datetime] = None
    # SQL: dt_atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP
    # Atualizado a cada UPDATE.

    # ──────────────────────────────────────────────────────
    # MÉTODOS DE VALIDAÇÃO
    # ──────────────────────────────────────────────────────

    def __post_init__(self):
        """
        Executado automaticamente DEPOIS do __init__().
        Valida os dados assim que o objeto é criado.
        """
        self._validar_cpf()
        self._validar_email()

    def _validar_cpf(self):
        """CPF deve ter exatamente 11 dígitos numéricos."""
        cpf_limpo = self.cpf.strip()
        if not cpf_limpo.isdigit():
            raise ValueError(f"CPF deve conter apenas números. Recebido: '{self.cpf}'")
        if len(cpf_limpo) != 11:
            raise ValueError(f"CPF deve ter 11 dígitos. Recebido: {len(cpf_limpo)} dígitos")
        self.cpf = cpf_limpo  # garante que está limpo

    def _validar_email(self):
        """E-mail deve conter @ e . (mesma regra do CHECK SQL)."""
        if self.email is not None:
            if "@" not in self.email or "." not in self.email:
                raise ValueError(f"E-mail inválido: '{self.email}'. Deve conter @ e .")

    # ──────────────────────────────────────────────────────
    # MÉTODOS DE CONVERSÃO (banco ↔ objeto)
    # ──────────────────────────────────────────────────────

    @classmethod
    def from_db_row(cls, row) -> "Morador":
        """
        Cria um Morador a partir de uma linha do banco (sqlite3.Row).

        Uso:
            cursor.execute("SELECT * FROM moradores WHERE id = ?", (1,))
            linha = cursor.fetchone()
            morador = Morador.from_db_row(linha)
        """
        return cls(
            id=row["id"],
            nome=row["nome"],
            cpf=row["cpf"],
            telefone=row["telefone"],
            email=row["email"],
            dt_nascimento=parse_date(row["dt_nascimento"]) if row["dt_nascimento"] else None,
            foto=row["foto"],
            dt_foto_validade=parse_date(row["dt_foto_validade"]) if row["dt_foto_validade"] else None,
            biometria=row["biometria"],
            dt_biometria_validade=parse_date(row["dt_biometria_validade"]) if row["dt_biometria_validade"] else None,
            termos_lgpd=row["termos_lgpd"],
            dt_aceite_lgpd=parse_datetime(row["dt_aceite_lgpd"]) if row["dt_aceite_lgpd"] else None,
            ativo=bool(row["ativo"]),
            correlation_id=row["correlation_id"],
            dt_criado_em=parse_datetime(row["dt_criado_em"]) if row["dt_criado_em"] else None,
            dt_atualizado_em=parse_datetime(row["dt_atualizado_em"]) if row["dt_atualizado_em"] else None,
        )

    def to_db_dict(self) -> dict:
        """
        Converte o Morador para um dicionário pronto para INSERT/UPDATE.

        Uso:
            dados = morador.to_db_dict()
            colunas = ', '.join(dados.keys())
            placeholders = ', '.join(['?'] * len(dados))
            cursor.execute(
                f"INSERT INTO moradores ({colunas}) VALUES ({placeholders})",
                tuple(dados.values())
            )
        """
        dados = {
            "nome": self.nome,
            "cpf": self.cpf,
            "telefone": self.telefone,
            "email": self.email,
            "dt_nascimento": str(self.dt_nascimento) if self.dt_nascimento else None,
            "foto": self.foto,
            "dt_foto_validade": str(self.dt_foto_validade) if self.dt_foto_validade else None,
            "biometria": self.biometria,
            "dt_biometria_validade": str(self.dt_biometria_validade) if self.dt_biometria_validade else None,
            "termos_lgpd": self.termos_lgpd,
            "dt_aceite_lgpd": str(self.dt_aceite_lgpd) if self.dt_aceite_lgpd else None,
            "ativo": 1 if self.ativo else 0,
            "correlation_id": self.correlation_id,
        }
        return dados

    # ──────────────────────────────────────────────────────
    # MÉTODOS DE EXIBIÇÃO
    # ──────────────────────────────────────────────────────

    @property
    def cpf_formatado(self) -> str:
        """Retorna CPF formatado: 123.456.789-01"""
        c = self.cpf
        if len(c) == 11 and c.isdigit():
            return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"
        return c

    @property
    def nome_curto(self) -> str:
        """Retorna primeiro e último nome: 'João Silva'"""
        partes = self.nome.split()
        if len(partes) >= 2:
            return f"{partes[0]} {partes[-1]}"
        return self.nome

    @property
    def status_texto(self) -> str:
        """Retorna 'Ativo' ou 'Inativo'."""
        return "Ativo" if self.ativo else "Inativo"

    def resumo(self) -> str:
        """Retorna um resumo de uma linha do morador."""
        return (
            f"[{self.id or 'NOVO'}] {self.nome} | "
            f"CPF: {self.cpf_formatado} | "
            f"Tel: {self.telefone or '—'} | "
            f"{self.status_texto}"
        )


# ──────────────────────────────────────────────────────────
# EXEMPLO DE USO (execute este arquivo para testar!)
# ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import hashlib

    print("=" * 60)
    print("  TESTANDO O MODELO Morador")
    print("=" * 60)

    # 1. Criar um morador novo
    cpf_teste = "11122233344"
    correlation = hashlib.sha256(f"moradores:{cpf_teste}".encode()).hexdigest()

    morador = Morador(
        nome="João Carlos da Silva",
        cpf=cpf_teste,
        correlation_id=correlation,
        telefone="83999001122",
        email="joao.silva@email.com",
    )

    print(f"\n1. Morador criado:")
    print(f"   {morador.resumo()}")
    print(f"   Nome curto: {morador.nome_curto}")
    print(f"   CPF formatado: {morador.cpf_formatado}")

    # 2. Converter para dicionário (pronto para INSERT)
    dados = morador.to_db_dict()
    print(f"\n2. Dicionário para INSERT:")
    for chave, valor in dados.items():
        print(f"   {chave}: {valor}")

    # 3. Testar validação de CPF inválido
    print(f"\n3. Testando validação:")
    try:
        morador_invalido = Morador(
            nome="Teste", cpf="123", correlation_id="x"
        )
    except ValueError as e:
        print(f"   ✓ CPF inválido detectado: {e}")

    # 4. Testar validação de e-mail inválido
    try:
        morador_invalido = Morador(
            nome="Teste", cpf="11111111111",
            correlation_id="x", email="sem-arroba"
        )
    except ValueError as e:
        print(f"   ✓ E-mail inválido detectado: {e}")

    print(f"\n{'=' * 60}")
    print("  TUDO FUNCIONANDO!")
    print("=" * 60)
