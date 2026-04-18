#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  MODELO DE DOMINIO: AssinaturaCondominio
  n7-portaria-ai | Aula 02
============================================================

Este arquivo mapeia a tabela 'assinatura_condominio' do banco
para uma classe Python usando @dataclass.

O QUE E ASSINATURA_CONDOMINIO?
  E o CONTRATO do condominio com o sistema n7-portaria-ai.
  Cada condominio tem UMA assinatura (UNIQUE codigo_condominio).

  Pense como a "licenca de uso" do software:
  - Quem assinou (responsavel_id → sindico/administrador)
  - Numero do contrato e PDF do contrato assinado
  - Periodo de vigencia (inicio e fim)
  - Status: ativo, pendente, vencido ou cancelado

  REGRA: dt_vigencia_fim >= dt_vigencia_inicio
  (a vigencia nao pode terminar antes de comecar!)

MAPEAMENTO:
  +-----------------------+--------------------+------------------+
  | Coluna SQL            | Atributo Python    | Tipo Python      |
  +-----------------------+--------------------+------------------+
  | id                    | id                 | Optional[int]    |
  | codigo_condominio     | codigo_condominio  | str              |
  | nome_condominio       | nome_condominio    | str              |
  | endereco              | endereco           | Optional[str]    |
  | responsavel_id        | responsavel_id     | Optional[int]    |
  | numero_contrato       | numero_contrato    | str              |
  | contrato              | contrato           | Optional[bytes]  |
  | dt_ativacao           | dt_ativacao        | Optional[date]   |
  | dt_vigencia_inicio    | dt_vigencia_inicio | date             |
  | dt_vigencia_fim       | dt_vigencia_fim    | Optional[date]   |
  | status                | status             | str              |
  | observacoes           | observacoes        | Optional[str]    |
  | correlation_id        | correlation_id     | str              |
  | dt_criado_em          | dt_criado_em       | Optional[datetime]|
  | dt_atualizado_em      | dt_atualizado_em   | Optional[datetime]|
  +-----------------------+--------------------+------------------+
============================================================
"""

from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

from src.core.models.base import parse_date, parse_datetime


# ============================================================
# STATUS VALIDOS DA ASSINATURA
# ============================================================
# 'ativo'     = contrato vigente, sistema funcionando
# 'pendente'  = contrato criado mas ainda nao ativado
# 'vencido'   = contrato expirou (precisa renovar)
# 'cancelado' = contrato encerrado

STATUS_VALIDOS = ("ativo", "pendente", "vencido", "cancelado")


@dataclass
class AssinaturaCondominio:
    """
    Contrato de uso do sistema n7-portaria-ai por um condominio.

    Exemplos de uso:
        >>> from datetime import date
        >>> assinatura = AssinaturaCondominio(
        ...     codigo_condominio="COND-001",
        ...     nome_condominio="Residencial Palmeiras",
        ...     numero_contrato="CONTRATO-2026-001",
        ...     dt_vigencia_inicio=date(2026, 1, 1),
        ...     correlation_id="abc123..."
        ... )
        >>> print(assinatura.status)  # 'ativo'
    """

    # ──────────────────────────────────────────────────────
    # CAMPOS OBRIGATORIOS (NOT NULL no SQL)
    # ──────────────────────────────────────────────────────

    codigo_condominio: str
    # SQL: codigo_condominio TEXT UNIQUE NOT NULL
    # Codigo unico do condominio. Ex: 'COND-001'.
    # UNIQUE = so 1 assinatura por condominio.

    nome_condominio: str
    # SQL: nome_condominio TEXT NOT NULL
    # Nome oficial. Ex: 'Residencial Palmeiras'

    numero_contrato: str
    # SQL: numero_contrato TEXT UNIQUE NOT NULL
    # Numero do contrato. Ex: 'CONTRATO-2026-001'

    dt_vigencia_inicio: Optional[date] = None
    # SQL: dt_vigencia_inicio DATE NOT NULL
    # Quando o contrato comeca a valer.

    correlation_id: str = ""
    # SQL: correlation_id TEXT UNIQUE NOT NULL

    # ──────────────────────────────────────────────────────
    # CAMPOS OPCIONAIS (com valor padrao)
    # ──────────────────────────────────────────────────────

    id: Optional[int] = None
    # SQL: id INTEGER PRIMARY KEY AUTOINCREMENT

    endereco: Optional[str] = None
    # SQL: endereco TEXT
    # Endereco do condominio.

    responsavel_id: Optional[int] = None
    # SQL: responsavel_id INTEGER
    #      FOREIGN KEY (responsavel_id) REFERENCES moradores(id)
    # FK → morador que e o sindico/administrador do condominio.

    contrato: Optional[bytes] = None
    # SQL: contrato BLOB
    # Bytes do PDF do contrato assinado.

    dt_ativacao: Optional[date] = None
    # SQL: dt_ativacao DATE
    # Quando o sistema foi ativado para este condominio.

    dt_vigencia_fim: Optional[date] = None
    # SQL: dt_vigencia_fim DATE CHECK(dt_vigencia_fim IS NULL
    #                                OR dt_vigencia_fim >= dt_vigencia_inicio)
    # Quando o contrato expira. None = sem prazo definido.

    status: str = "ativo"
    # SQL: status TEXT DEFAULT 'ativo'
    #      CHECK(status IN ('ativo','pendente','vencido','cancelado'))

    observacoes: Optional[str] = None
    # SQL: observacoes TEXT

    dt_criado_em: Optional[datetime] = None
    # SQL: dt_criado_em DATETIME DEFAULT CURRENT_TIMESTAMP

    dt_atualizado_em: Optional[datetime] = None
    # SQL: dt_atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP

    # ──────────────────────────────────────────────────────
    # VALIDACOES
    # ──────────────────────────────────────────────────────

    def __post_init__(self):
        """Valida os dados assim que o objeto e criado."""
        self._validar_status()
        self._validar_datas()

    def _validar_status(self):
        """status deve ser um dos valores aceitos."""
        if self.status not in STATUS_VALIDOS:
            raise ValueError(
                f"status invalido: '{self.status}'. "
                f"Valores aceitos: {STATUS_VALIDOS}"
            )

    def _validar_datas(self):
        """dt_vigencia_fim nao pode ser anterior a dt_vigencia_inicio."""
        if self.dt_vigencia_inicio and self.dt_vigencia_fim:
            if self.dt_vigencia_fim < self.dt_vigencia_inicio:
                raise ValueError(
                    f"dt_vigencia_fim ({self.dt_vigencia_fim}) nao pode ser "
                    f"antes de dt_vigencia_inicio ({self.dt_vigencia_inicio})"
                )

    # ──────────────────────────────────────────────────────
    # CONVERSAO: BANCO → OBJETO
    # ──────────────────────────────────────────────────────

    @classmethod
    def from_db_row(cls, row) -> "AssinaturaCondominio":
        """
        Cria uma AssinaturaCondominio a partir de uma linha do banco.

        Uso:
            cursor.execute("SELECT * FROM assinatura_condominio LIMIT 1")
            linha = cursor.fetchone()
            assinatura = AssinaturaCondominio.from_db_row(linha)
        """
        return cls(
            id=row["id"],
            codigo_condominio=row["codigo_condominio"],
            nome_condominio=row["nome_condominio"],
            endereco=row["endereco"],
            responsavel_id=row["responsavel_id"],
            numero_contrato=row["numero_contrato"],
            contrato=row["contrato"],
            dt_ativacao=parse_date(row["dt_ativacao"]),
            dt_vigencia_inicio=parse_date(row["dt_vigencia_inicio"]),
            dt_vigencia_fim=parse_date(row["dt_vigencia_fim"]),
            status=row["status"] or "ativo",
            observacoes=row["observacoes"],
            correlation_id=row["correlation_id"],
            dt_criado_em=parse_datetime(row["dt_criado_em"]),
            dt_atualizado_em=parse_datetime(row["dt_atualizado_em"]),
        )

    # ──────────────────────────────────────────────────────
    # CONVERSAO: OBJETO → BANCO
    # ──────────────────────────────────────────────────────

    def to_db_dict(self) -> dict:
        """Converte para dicionario pronto para INSERT/UPDATE."""
        return {
            "codigo_condominio": self.codigo_condominio,
            "nome_condominio": self.nome_condominio,
            "endereco": self.endereco,
            "responsavel_id": self.responsavel_id,
            "numero_contrato": self.numero_contrato,
            "contrato": self.contrato,
            "dt_ativacao": str(self.dt_ativacao) if self.dt_ativacao else None,
            "dt_vigencia_inicio": str(self.dt_vigencia_inicio) if self.dt_vigencia_inicio else None,
            "dt_vigencia_fim": str(self.dt_vigencia_fim) if self.dt_vigencia_fim else None,
            "status": self.status,
            "observacoes": self.observacoes,
            "correlation_id": self.correlation_id,
        }

    # ──────────────────────────────────────────────────────
    # METODOS DE EXIBICAO
    # ──────────────────────────────────────────────────────

    @property
    def status_texto(self) -> str:
        """Retorna status formatado."""
        mapa = {
            "ativo": "Ativo",
            "pendente": "Pendente",
            "vencido": "VENCIDO",
            "cancelado": "Cancelado",
        }
        return mapa.get(self.status, self.status)

    @property
    def vigencia_texto(self) -> str:
        """Retorna periodo de vigencia legivel."""
        inicio = str(self.dt_vigencia_inicio) if self.dt_vigencia_inicio else "?"
        fim = str(self.dt_vigencia_fim) if self.dt_vigencia_fim else "sem prazo"
        return f"{inicio} ate {fim}"

    def resumo(self) -> str:
        """Retorna um resumo de uma linha."""
        return (
            f"[{self.id or 'NOVO'}] {self.nome_condominio} ({self.codigo_condominio}) | "
            f"Contrato: {self.numero_contrato} | "
            f"{self.status_texto} | Vigencia: {self.vigencia_texto}"
        )


# ──────────────────────────────────────────────────────────
# EXEMPLO DE USO (execute este arquivo para testar!)
#   python src/core/models/assinatura_condominio.py
# ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import hashlib

    print("=" * 60)
    print("  TESTANDO O MODELO AssinaturaCondominio")
    print("=" * 60)

    # 1. Assinatura ativa
    cid = hashlib.sha256(b"assinatura:COND-001").hexdigest()
    a = AssinaturaCondominio(
        codigo_condominio="COND-001",
        nome_condominio="Residencial Palmeiras",
        numero_contrato="CONTRATO-2026-001",
        dt_vigencia_inicio=date(2026, 1, 1),
        dt_vigencia_fim=date(2027, 12, 31),
        responsavel_id=1,
        correlation_id=cid,
    )
    print(f"\n1. Assinatura criada:")
    print(f"   {a.resumo()}")
    print(f"   Vigencia: {a.vigencia_texto}")

    # 2. Dicionario para INSERT
    dados = a.to_db_dict()
    print(f"\n2. Dicionario para INSERT:")
    for chave, valor in dados.items():
        print(f"   {chave}: {valor}")

    # 3. Validacoes
    print(f"\n3. Testando validacoes:")
    try:
        AssinaturaCondominio(
            codigo_condominio="X", nome_condominio="X",
            numero_contrato="X", status="expirado",
            correlation_id="x"
        )
    except ValueError as e:
        print(f"   OK! Status invalido: {e}")

    try:
        AssinaturaCondominio(
            codigo_condominio="X", nome_condominio="X",
            numero_contrato="X",
            dt_vigencia_inicio=date(2027, 1, 1),
            dt_vigencia_fim=date(2026, 1, 1),
            correlation_id="x"
        )
    except ValueError as e:
        print(f"   OK! Data invalida: {e}")

    print(f"\n{'=' * 60}")
    print("  TUDO FUNCIONANDO!")
    print("=" * 60)
