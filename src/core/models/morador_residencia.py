#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  MODELO DE DOMINIO: MoradorResidencia (JUNCTION TABLE)
  n7-portaria-ai | Aula 02
============================================================

Este arquivo mapeia a tabela 'morador_residencia' do banco
para uma classe Python usando @dataclass.

O QUE E UMA JUNCTION TABLE?
============================

Imagine dois grupos de coisas que se conectam de muitas formas:

  MORADORES                    RESIDENCIAS
  +--------+                   +----------+
  | Joao   | ---mora em----->  | Apto 101 |
  | Ana    | ---mora em----->  | Apto 104 |
  | Ana    | ---dona de-----> | Apto 101 |  (Ana tem 2 unidades!)
  +--------+                   +----------+

  Joao mora no 101.
  Ana mora no 104, MAS tambem e dona do 101 (herdou do pai).
  Isso e uma relacao MUITOS PARA MUITOS (N:N).

  O problema: se colocarmos residencia_id dentro de moradores,
  Ana so pode ter UMA residencia. Se colocarmos morador_id
  dentro de residencias, o 101 so pode ter UM morador.

  A SOLUCAO e uma tabela intermediaria — a JUNCTION TABLE:

  morador_residencia
  +----+-----------+---------------+--------------+
  | id | morador_id| residencia_id | tipo_morador |
  +----+-----------+---------------+--------------+
  |  1 |    1 Joao |     1 Apto101 | proprietario |
  |  2 |    2 Ana  |     4 Apto104 | proprietario |
  |  3 |    2 Ana  |     1 Apto101 | proprietario | ← Ana tem 2!
  +----+-----------+---------------+--------------+

  Cada LINHA desta tabela e um VINCULO entre um morador e uma residencia.

ANALOGIA DO HOSPITAL:
  Em um hospital, a tabela 'consultas' conecta PACIENTES a MEDICOS.
  Um paciente pode ir a varios medicos.
  Um medico atende varios pacientes.
  Cada consulta tem data, motivo, etc.

  Aqui e a mesma ideia:
  morador_residencia conecta MORADORES a RESIDENCIAS.
  Cada vinculo tem tipo (proprietario/inquilino) e data de inicio.

FOREIGN KEYS (CHAVES ESTRANGEIRAS):
====================================

  FOREIGN KEY (morador_id) REFERENCES moradores(id)
  Isso significa: morador_id DEVE existir na tabela moradores.
  Se tentar inserir morador_id=999 e nao existir morador 999,
  o banco RECUSA a insercao.

  E como um "link" entre tabelas — garante que os dados sao validos.

  No Python, armazenamos apenas o ID (numero inteiro).
  Para pegar o nome do morador, fazemos um JOIN no SQL
  ou buscamos separadamente.

MAPEAMENTO:
  +-----------------------+------------------+----------------+
  | Coluna SQL            | Atributo Python  | Tipo Python    |
  +-----------------------+------------------+----------------+
  | id                    | id               | Optional[int]  |
  | morador_id            | morador_id       | int            |
  | residencia_id         | residencia_id    | int            |
  | tipo_morador          | tipo_morador     | str            |
  | dt_inicio             | dt_inicio        | date           |
  | dt_fim                | dt_fim           | Optional[date] |
  | ativo                 | ativo            | bool           |
  | correlation_id        | correlation_id   | str            |
  | dt_criado_em          | dt_criado_em     | Optional[datetime]|
  +-----------------------+------------------+----------------+
============================================================
"""

from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


# ============================================================
# TIPOS VALIDOS DE MORADOR NO VINCULO
# ============================================================
# Um morador pode ser 'proprietario' ou 'inquilino' em cada unidade.
# A mesma pessoa pode ser proprietario de uma e inquilino de outra!

TIPOS_MORADOR_VALIDOS = ("proprietario", "inquilino")


@dataclass
class MoradorResidencia:
    """
    Representa o VINCULO entre um morador e uma residencia.

    NAO e um morador. NAO e uma residencia.
    E a CONEXAO entre os dois — com informacoes extras:
    tipo (proprietario/inquilino), data de inicio e fim.

    Exemplos de uso:
        >>> # Joao e proprietario do Apto 101 desde jan/2024
        >>> vinculo = MoradorResidencia(
        ...     morador_id=1,       # id do Joao na tabela moradores
        ...     residencia_id=1,    # id do Apto 101 na tabela residencias
        ...     tipo_morador="proprietario",
        ...     dt_inicio=date(2024, 1, 10),
        ...     correlation_id="abc123..."
        ... )

        >>> # Ana e co-proprietaria do Apto 101 (herdou do pai)
        >>> vinculo2 = MoradorResidencia(
        ...     morador_id=4,       # id da Ana
        ...     residencia_id=1,    # mesmo Apto 101!
        ...     tipo_morador="proprietario",
        ...     dt_inicio=date(2023, 3, 15),
        ...     correlation_id="def456..."
        ... )

    POR QUE tipo_morador ESTA AQUI E NAO EM MORADORES?
    Porque a mesma pessoa pode ser proprietario de um apto
    e inquilino de outro! O tipo pertence ao VINCULO, nao a pessoa.
    """

    # ──────────────────────────────────────────────────────
    # CAMPOS OBRIGATORIOS (NOT NULL no SQL)
    # ──────────────────────────────────────────────────────

    morador_id: int
    # SQL: morador_id INTEGER NOT NULL
    #      FOREIGN KEY (morador_id) REFERENCES moradores(id)
    #
    # FOREIGN KEY = este numero DEVE existir na tabela moradores.
    # Se morador_id=1, entao o morador com id=1 deve existir.
    #
    # No Python, guardamos apenas o numero (int).
    # Para saber o NOME do morador, fazemos:
    #   SELECT m.nome FROM moradores m WHERE m.id = ?

    residencia_id: int
    # SQL: residencia_id INTEGER NOT NULL
    #      FOREIGN KEY (residencia_id) REFERENCES residencias(id)
    #
    # Mesma logica: este numero DEVE existir na tabela residencias.
    # Para saber o NUMERO da residencia, fazemos:
    #   SELECT r.numero_residencia FROM residencias r WHERE r.id = ?

    correlation_id: str
    # SQL: correlation_id TEXT UNIQUE NOT NULL
    # Hash SHA-256 para sincronizacao.

    # ──────────────────────────────────────────────────────
    # CAMPOS COM VALOR PADRAO
    # ──────────────────────────────────────────────────────

    id: Optional[int] = None
    # SQL: id INTEGER PRIMARY KEY AUTOINCREMENT

    tipo_morador: str = "proprietario"
    # SQL: tipo_morador TEXT DEFAULT 'proprietario'
    #      CHECK(tipo_morador IN ('proprietario', 'inquilino'))
    #
    # POR QUE ESTA AQUI E NAO NA TABELA MORADORES?
    # Porque o tipo depende do VINCULO, nao da pessoa!
    #
    # Exemplo real:
    #   Ana e PROPRIETARIA do Apto 101 (herdou)
    #   Ana e PROPRIETARIA do Apto 104 (comprou)
    #   Mas Ana poderia ser INQUILINA de um e dona de outro!
    #
    # Se tipo_morador estivesse em moradores, Ana so poderia
    # ter UM tipo — e isso seria errado.

    dt_inicio: Optional[date] = None
    # SQL: dt_inicio DATE NOT NULL DEFAULT (DATE('now'))
    # Quando o morador comecou a morar nesta unidade.
    #
    # No Python, usamos None como padrao e preenchemos depois.
    # O banco preenche automaticamente com a data de hoje
    # se nao informarmos.

    dt_fim: Optional[date] = None
    # SQL: dt_fim DATE
    # Quando o morador SAIU desta unidade.
    # NULL = ainda mora aqui!
    #
    # Isso permite HISTORICO: a mesma pessoa pode sair e voltar
    # depois. O UNIQUE(morador_id, residencia_id, dt_inicio)
    # garante que nao haja duplicata no mesmo periodo.

    ativo: bool = True
    # SQL: ativo BOOLEAN DEFAULT 1 CHECK(ativo IN (0, 1))
    # True = vinculo ativo. False = soft delete.

    dt_criado_em: Optional[datetime] = None
    # SQL: dt_criado_em DATETIME DEFAULT CURRENT_TIMESTAMP

    # ──────────────────────────────────────────────────────
    # VALIDACOES
    # ──────────────────────────────────────────────────────

    def __post_init__(self):
        """Valida os dados assim que o objeto e criado."""
        self._validar_tipo_morador()
        self._validar_ids()
        self._validar_datas()

    def _validar_tipo_morador(self):
        """tipo_morador deve ser 'proprietario' ou 'inquilino'."""
        if self.tipo_morador not in TIPOS_MORADOR_VALIDOS:
            raise ValueError(
                f"tipo_morador invalido: '{self.tipo_morador}'. "
                f"Valores aceitos: {TIPOS_MORADOR_VALIDOS}"
            )

    def _validar_ids(self):
        """IDs de FK devem ser numeros positivos."""
        if self.morador_id is not None and self.morador_id <= 0:
            raise ValueError(f"morador_id deve ser positivo. Recebido: {self.morador_id}")
        if self.residencia_id is not None and self.residencia_id <= 0:
            raise ValueError(f"residencia_id deve ser positivo. Recebido: {self.residencia_id}")

    def _validar_datas(self):
        """dt_fim nao pode ser anterior a dt_inicio."""
        if self.dt_inicio and self.dt_fim:
            if self.dt_fim < self.dt_inicio:
                raise ValueError(
                    f"dt_fim ({self.dt_fim}) nao pode ser antes de "
                    f"dt_inicio ({self.dt_inicio})"
                )

    # ──────────────────────────────────────────────────────
    # CONVERSAO: BANCO → OBJETO
    # ──────────────────────────────────────────────────────

    @classmethod
    def from_db_row(cls, row) -> "MoradorResidencia":
        """
        Cria um MoradorResidencia a partir de uma linha do banco.

        Uso:
            cursor.execute("SELECT * FROM morador_residencia WHERE id = ?", (1,))
            linha = cursor.fetchone()
            vinculo = MoradorResidencia.from_db_row(linha)
        """
        return cls(
            id=row["id"],
            morador_id=row["morador_id"],
            residencia_id=row["residencia_id"],
            tipo_morador=row["tipo_morador"] or "proprietario",
            dt_inicio=_parse_date(row["dt_inicio"]),
            dt_fim=_parse_date(row["dt_fim"]) if row["dt_fim"] else None,
            ativo=bool(row["ativo"]),
            correlation_id=row["correlation_id"],
            dt_criado_em=_parse_datetime(row["dt_criado_em"]),
        )

    # ──────────────────────────────────────────────────────
    # CONVERSAO: OBJETO → BANCO
    # ──────────────────────────────────────────────────────

    def to_db_dict(self) -> dict:
        """
        Converte para dicionario pronto para INSERT/UPDATE.

        Uso:
            dados = vinculo.to_db_dict()
            colunas = ', '.join(dados.keys())
            placeholders = ', '.join(['?'] * len(dados))
            cursor.execute(
                f"INSERT INTO morador_residencia ({colunas}) VALUES ({placeholders})",
                tuple(dados.values())
            )
        """
        return {
            "morador_id": self.morador_id,
            "residencia_id": self.residencia_id,
            "tipo_morador": self.tipo_morador,
            "dt_inicio": str(self.dt_inicio) if self.dt_inicio else None,
            "dt_fim": str(self.dt_fim) if self.dt_fim else None,
            "ativo": 1 if self.ativo else 0,
            "correlation_id": self.correlation_id,
        }

    # ──────────────────────────────────────────────────────
    # METODOS DE EXIBICAO
    # ──────────────────────────────────────────────────────

    @property
    def ainda_mora(self) -> bool:
        """True se o morador AINDA mora nesta residencia."""
        return self.dt_fim is None and self.ativo

    @property
    def status_texto(self) -> str:
        """Retorna status legivel."""
        if not self.ativo:
            return "Inativo"
        if self.dt_fim:
            return f"Encerrado em {self.dt_fim}"
        return "Ativo"

    def resumo(self) -> str:
        """Retorna um resumo de uma linha."""
        desde = f"desde {self.dt_inicio}" if self.dt_inicio else "sem data"
        return (
            f"[{self.id or 'NOVO'}] "
            f"Morador #{self.morador_id} → Residencia #{self.residencia_id} | "
            f"{self.tipo_morador} | {desde} | {self.status_texto}"
        )


# ──────────────────────────────────────────────────────────
# FUNCOES AUXILIARES (privadas ao modulo)
# ──────────────────────────────────────────────────────────

def _parse_date(valor) -> Optional[date]:
    """Converte string 'YYYY-MM-DD' para date."""
    if valor is None:
        return None
    try:
        return datetime.strptime(str(valor), "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def _parse_datetime(valor) -> Optional[datetime]:
    """Converte string 'YYYY-MM-DD HH:MM:SS' para datetime."""
    if valor is None:
        return None
    try:
        return datetime.strptime(str(valor), "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return None


# ──────────────────────────────────────────────────────────
# EXEMPLO DE USO (execute este arquivo para testar!)
#   python -m src.core.models.morador_residencia
#   ou: python src/core/models/morador_residencia.py
# ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import hashlib

    print("=" * 60)
    print("  TESTANDO O MODELO MoradorResidencia")
    print("=" * 60)

    # 1. Joao e proprietario do Apto 101
    cid1 = hashlib.sha256(b"morador_residencia:mr_1_1").hexdigest()
    vinculo1 = MoradorResidencia(
        morador_id=1,
        residencia_id=1,
        tipo_morador="proprietario",
        dt_inicio=date(2024, 1, 10),
        correlation_id=cid1,
    )
    print(f"\n1. Vinculo criado:")
    print(f"   {vinculo1.resumo()}")
    print(f"   Ainda mora? {vinculo1.ainda_mora}")

    # 2. Ana e proprietaria de 2 unidades (demo N:N!)
    cid2 = hashlib.sha256(b"morador_residencia:mr_4_4").hexdigest()
    vinculo_ana_104 = MoradorResidencia(
        morador_id=4,
        residencia_id=4,
        tipo_morador="proprietario",
        dt_inicio=date(2023, 3, 15),
        correlation_id=cid2,
    )

    cid3 = hashlib.sha256(b"morador_residencia:mr_4_1").hexdigest()
    vinculo_ana_101 = MoradorResidencia(
        morador_id=4,
        residencia_id=1,
        tipo_morador="proprietario",
        dt_inicio=date(2023, 3, 15),
        correlation_id=cid3,
    )

    print(f"\n2. Ana Paula em 2 unidades (N:N):")
    print(f"   {vinculo_ana_104.resumo()}")
    print(f"   {vinculo_ana_101.resumo()}")

    # 3. Converter para dicionario (INSERT)
    dados = vinculo1.to_db_dict()
    print(f"\n3. Dicionario para INSERT:")
    for chave, valor in dados.items():
        print(f"   {chave}: {valor}")

    # 4. Testar validacao tipo_morador invalido
    print(f"\n4. Testando validacoes:")
    try:
        invalido = MoradorResidencia(
            morador_id=1, residencia_id=1,
            tipo_morador="visitante",  # invalido!
            correlation_id="x",
        )
    except ValueError as e:
        print(f"   OK! Tipo invalido: {e}")

    # 5. Testar validacao dt_fim < dt_inicio
    try:
        invalido = MoradorResidencia(
            morador_id=1, residencia_id=1,
            dt_inicio=date(2025, 6, 1),
            dt_fim=date(2024, 1, 1),  # fim antes do inicio!
            correlation_id="x",
        )
    except ValueError as e:
        print(f"   OK! Data invalida: {e}")

    print(f"\n{'=' * 60}")
    print("  TUDO FUNCIONANDO!")
    print("=" * 60)
