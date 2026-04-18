#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  MODELO DE DOMINIO: Visitante
  n7-portaria-ai | Aula 02
============================================================

Este arquivo mapeia a tabela 'visitantes' do banco de dados
para uma classe Python usando @dataclass.

O QUE E UM VISITANTE?
  Qualquer pessoa que NAO e morador e quer entrar no condominio.
  Ex: entregador, parente, prestador de servico.

  O visitante pode ser BLOQUEADO — nesse caso o porteiro e
  alertado e a cancela/portao nao abre.

  Tambem pode ter uma JANELA DE VALIDADE:
  - dt_validade_inicio = a partir de quando pode entrar
  - dt_validade_fim    = ate quando pode entrar
  Isso e util para visitantes regulares (ex: diarista toda sexta).

MAPEAMENTO:
  +-----------------------+--------------------+-----------------+
  | Coluna SQL            | Atributo Python    | Tipo Python     |
  +-----------------------+--------------------+-----------------+
  | id                    | id                 | Optional[int]   |
  | nome                  | nome               | str             |
  | documento             | documento          | str             |
  | tipo_documento        | tipo_documento     | str             |
  | telefone              | telefone           | Optional[str]   |
  | foto                  | foto               | Optional[bytes] |
  | bloqueado             | bloqueado          | bool            |
  | motivo_bloqueio       | motivo_bloqueio    | Optional[str]   |
  | dt_validade_inicio    | dt_validade_inicio | Optional[date]  |
  | dt_validade_fim       | dt_validade_fim    | Optional[date]  |
  | correlation_id        | correlation_id     | str             |
  | dt_criado_em          | dt_criado_em       | Optional[datetime]|
  +-----------------------+--------------------+-----------------+
============================================================
"""

from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

from src.core.models.base import parse_date, parse_datetime


# ============================================================
# TIPOS DE DOCUMENTO ACEITOS
# ============================================================
# O banco aceita apenas estes valores (CHECK constraint).
# RG e o padrao se nao informar nada.

TIPOS_DOCUMENTO_VALIDOS = ("RG", "CNH", "PASSAPORTE", "OUTRO")


@dataclass
class Visitante:
    """
    Representa um visitante do condominio.

    Exemplos de uso:
        >>> visitante = Visitante(
        ...     nome="Carlos Entregador",
        ...     documento="12345678",
        ...     correlation_id="abc123..."
        ... )
        >>> print(visitante.bloqueado)  # False
        >>> print(visitante.tipo_documento)  # 'RG'
    """

    # ──────────────────────────────────────────────────────
    # CAMPOS OBRIGATORIOS (NOT NULL no SQL)
    # ──────────────────────────────────────────────────────

    nome: str
    # SQL: nome TEXT NOT NULL
    # Nome completo do visitante.

    documento: str
    # SQL: documento TEXT NOT NULL
    # Numero do documento (RG, CNH, etc).
    # TEXT porque documentos podem ter letras (ex: passaporte).

    correlation_id: str
    # SQL: correlation_id TEXT UNIQUE NOT NULL
    # Hash SHA-256 para sincronizacao.

    # ──────────────────────────────────────────────────────
    # CAMPOS OPCIONAIS (com valor padrao)
    # ──────────────────────────────────────────────────────

    id: Optional[int] = None
    # SQL: id INTEGER PRIMARY KEY AUTOINCREMENT

    tipo_documento: str = "RG"
    # SQL: tipo_documento TEXT DEFAULT 'RG'
    #      CHECK(tipo_documento IN ('RG','CNH','PASSAPORTE','OUTRO'))
    # O tipo do documento apresentado na portaria.

    telefone: Optional[str] = None
    # SQL: telefone TEXT
    # Telefone de contato do visitante.

    foto: Optional[bytes] = None
    # SQL: foto BLOB
    # Foto do visitante. Util para reconhecimento facial futuro.

    bloqueado: bool = False
    # SQL: bloqueado BOOLEAN DEFAULT 0 CHECK(bloqueado IN (0, 1))
    # True = BLOQUEADO! Porteiro e alertado, portao nao abre.
    # Motivo do bloqueio fica em 'motivo_bloqueio'.

    motivo_bloqueio: Optional[str] = None
    # SQL: motivo_bloqueio TEXT
    # Se bloqueado=True, por que? Ex: "Tentativa de furto em 10/03"
    # Se bloqueado=False, este campo deve ser None.

    dt_validade_inicio: Optional[date] = None
    # SQL: dt_validade_inicio DATE
    # A partir de quando o visitante pode entrar.
    # None = sem restricao de data.

    dt_validade_fim: Optional[date] = None
    # SQL: dt_validade_fim DATE CHECK(dt_validade_fim IS NULL
    #                                OR dt_validade_fim >= dt_validade_inicio)
    # Ate quando pode entrar. None = sem prazo.
    # O CHECK garante que a data fim nao seja antes do inicio.

    dt_criado_em: Optional[datetime] = None
    # SQL: dt_criado_em DATETIME DEFAULT CURRENT_TIMESTAMP

    # ──────────────────────────────────────────────────────
    # VALIDACOES
    # ──────────────────────────────────────────────────────

    def __post_init__(self):
        """Valida os dados assim que o objeto e criado."""
        self._validar_tipo_documento()
        self._validar_datas()
        self._validar_bloqueio()

    def _validar_tipo_documento(self):
        """tipo_documento deve ser um dos valores aceitos."""
        if self.tipo_documento not in TIPOS_DOCUMENTO_VALIDOS:
            raise ValueError(
                f"tipo_documento invalido: '{self.tipo_documento}'. "
                f"Valores aceitos: {TIPOS_DOCUMENTO_VALIDOS}"
            )

    def _validar_datas(self):
        """dt_validade_fim nao pode ser anterior a dt_validade_inicio."""
        if self.dt_validade_inicio and self.dt_validade_fim:
            if self.dt_validade_fim < self.dt_validade_inicio:
                raise ValueError(
                    f"dt_validade_fim ({self.dt_validade_fim}) nao pode ser "
                    f"antes de dt_validade_inicio ({self.dt_validade_inicio})"
                )

    def _validar_bloqueio(self):
        """Se bloqueado, deve ter motivo."""
        if self.bloqueado and not self.motivo_bloqueio:
            raise ValueError(
                "Visitante bloqueado deve ter motivo_bloqueio preenchido"
            )

    # ──────────────────────────────────────────────────────
    # CONVERSAO: BANCO → OBJETO
    # ──────────────────────────────────────────────────────

    @classmethod
    def from_db_row(cls, row) -> "Visitante":
        """
        Cria um Visitante a partir de uma linha do banco.

        Uso:
            cursor.execute("SELECT * FROM visitantes WHERE id = ?", (1,))
            linha = cursor.fetchone()
            visitante = Visitante.from_db_row(linha)
        """
        return cls(
            id=row["id"],
            nome=row["nome"],
            documento=row["documento"],
            tipo_documento=row["tipo_documento"] or "RG",
            telefone=row["telefone"],
            foto=row["foto"],
            bloqueado=bool(row["bloqueado"]),
            motivo_bloqueio=row["motivo_bloqueio"],
            dt_validade_inicio=parse_date(row["dt_validade_inicio"]),
            dt_validade_fim=parse_date(row["dt_validade_fim"]),
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
            "documento": self.documento,
            "tipo_documento": self.tipo_documento,
            "telefone": self.telefone,
            "foto": self.foto,
            "bloqueado": 1 if self.bloqueado else 0,
            "motivo_bloqueio": self.motivo_bloqueio,
            "dt_validade_inicio": str(self.dt_validade_inicio) if self.dt_validade_inicio else None,
            "dt_validade_fim": str(self.dt_validade_fim) if self.dt_validade_fim else None,
            "correlation_id": self.correlation_id,
        }

    # ──────────────────────────────────────────────────────
    # METODOS DE EXIBICAO
    # ──────────────────────────────────────────────────────

    @property
    def status_texto(self) -> str:
        """Retorna status legivel."""
        if self.bloqueado:
            return f"BLOQUEADO ({self.motivo_bloqueio or 'sem motivo'})"
        return "Liberado"

    @property
    def validade_texto(self) -> str:
        """Retorna periodo de validade legivel."""
        if not self.dt_validade_inicio and not self.dt_validade_fim:
            return "Sem restricao de data"
        inicio = str(self.dt_validade_inicio) if self.dt_validade_inicio else "?"
        fim = str(self.dt_validade_fim) if self.dt_validade_fim else "sem prazo"
        return f"{inicio} ate {fim}"

    def resumo(self) -> str:
        """Retorna um resumo de uma linha."""
        doc = f"{self.tipo_documento}: {self.documento}"
        return (
            f"[{self.id or 'NOVO'}] {self.nome} | "
            f"{doc} | {self.status_texto}"
        )


# ──────────────────────────────────────────────────────────
# EXEMPLO DE USO (execute este arquivo para testar!)
#   python src/core/models/visitante.py
# ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import hashlib

    print("=" * 60)
    print("  TESTANDO O MODELO Visitante")
    print("=" * 60)

    # 1. Visitante normal
    cid = hashlib.sha256(b"visitantes:12345678").hexdigest()
    v = Visitante(
        nome="Roberto Almeida",
        documento="12345678",
        tipo_documento="RG",
        telefone="83999887766",
        correlation_id=cid,
    )
    print(f"\n1. Visitante criado:")
    print(f"   {v.resumo()}")
    print(f"   Validade: {v.validade_texto}")

    # 2. Visitante bloqueado
    cid2 = hashlib.sha256(b"visitantes:99887766").hexdigest()
    vb = Visitante(
        nome="Joao Problema",
        documento="99887766",
        bloqueado=True,
        motivo_bloqueio="Tentativa de acesso nao autorizado",
        correlation_id=cid2,
    )
    print(f"\n2. Visitante bloqueado:")
    print(f"   {vb.resumo()}")

    # 3. Dicionario para INSERT
    dados = v.to_db_dict()
    print(f"\n3. Dicionario para INSERT:")
    for chave, valor in dados.items():
        print(f"   {chave}: {valor}")

    # 4. Validacoes
    print(f"\n4. Testando validacoes:")
    try:
        Visitante(nome="X", documento="1", tipo_documento="CPF", correlation_id="x")
    except ValueError as e:
        print(f"   OK! Tipo invalido: {e}")

    try:
        Visitante(
            nome="X", documento="1", correlation_id="x",
            dt_validade_inicio=date(2026, 6, 1),
            dt_validade_fim=date(2026, 1, 1),
        )
    except ValueError as e:
        print(f"   OK! Data invalida: {e}")

    print(f"\n{'=' * 60}")
    print("  TUDO FUNCIONANDO!")
    print("=" * 60)
