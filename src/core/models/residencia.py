#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  MODELO DE DOMINIO: Residencia
  n7-portaria-ai | Aula 02
============================================================

Este arquivo mapeia a tabela 'residencias' do banco de dados
para uma classe Python usando @dataclass.

ANALOGIA:
  Pense no condominio como um ARMARIO DE GAVETAS.
  Cada RESIDENCIA e uma gaveta — tem numero, andar, bloco.
  Os MORADORES sao as pessoas que usam essas gavetas.
  A mesma pessoa pode ter VARIAS gavetas (proprietario de 2 aptos).
  A mesma gaveta pode ser usada por VARIAS pessoas (familia).

  Por isso, moradores e residencias estao em TABELAS SEPARADAS,
  conectadas pela tabela intermediaria 'morador_residencia'.

MAPEAMENTO:
  +-----------------------+------------------+----------------+
  | Coluna SQL            | Atributo Python  | Tipo Python    |
  +-----------------------+------------------+----------------+
  | id                    | id               | Optional[int]  |
  | codigo_condominio     | codigo_condominio| str            |
  | numero_residencia     | numero_residencia| str            |
  | bloco                 | bloco            | Optional[str]  |
  | quadra                | quadra           | Optional[str]  |
  | andar                 | andar            | Optional[int]  |
  | tipo_moradia          | tipo_moradia     | str            |
  | interfone             | interfone        | Optional[str]  |
  | observacao            | observacao       | Optional[str]  |
  | ativo                 | ativo            | bool           |
  | correlation_id        | correlation_id   | str            |
  | dt_criado_em          | dt_criado_em     | Optional[datetime]|
  | dt_atualizado_em      | dt_atualizado_em | Optional[datetime]|
  +-----------------------+------------------+----------------+

CAMPOS DO ADEMILSON (v5.0):
  O Ademilson sugeriu 3 campos que fazem total sentido:
  - tipo_moradia  → o porteiro precisa saber se e casa ou apto!
  - interfone     → como chamar o morador na portaria!
  - observacao    → anotacoes livres (ex: "cobertura, acesso especial")
============================================================
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.core.models.base import parse_datetime


# ============================================================
# TIPOS VALIDOS DE MORADIA
# ============================================================
# Estes sao os valores que o banco aceita (CHECK constraint).
# Se tentar salvar outro valor, o SQLite recusa!
#
# Usamos uma lista simples aqui — em Python avancado,
# poderiamos usar Enum, mas nao e necessario agora.

TIPOS_MORADIA_VALIDOS = ("apartamento", "casa", "comercial", "outro")


@dataclass
class Residencias:
    __tablename__ = "residencias"

    """
    Representa uma unidade habitacional do condominio.

    Cada residencia e um "lugar" onde moradores vivem:
    apartamento, casa, sala comercial, etc.

    Exemplos de uso:
        >>> # Apartamento 101, Bloco A, 1o andar
        >>> apto = Residencia(
        ...     codigo_condominio="COND-001",
        ...     numero_residencia="101",
        ...     bloco="A",
        ...     andar=1,
        ...     tipo_moradia="apartamento",
        ...     interfone="101",
        ...     correlation_id="abc123..."
        ... )

        >>> # Casa no lote 08, quadra 03 (condominio horizontal)
        >>> casa = Residencia(
        ...     codigo_condominio="COND-001",
        ...     numero_residencia="08",
        ...     quadra="03",
        ...     tipo_moradia="casa",
        ...     observacao="Lote 08 da Quadra 03",
        ...     correlation_id="def456..."
        ... )

    NOTA: Uma Residencia NAO sabe quem mora nela!
    Essa informacao esta na tabela morador_residencia.
    """

    # ──────────────────────────────────────────────────────
    # CAMPOS OBRIGATORIOS (NOT NULL no SQL)
    # ──────────────────────────────────────────────────────

    codigo_condominio: str
    # SQL: codigo_condominio TEXT NOT NULL
    # Codigo do condominio. Ex: 'COND-001'.
    # Permite que o sistema funcione para varios condominios.

    numero_residencia: str
    # SQL: numero_residencia TEXT NOT NULL
    # Numero da unidade: '101', '101-A', '08' (lote), 'Cobertura'.
    # TEXT (nao INTEGER) porque pode ter letras!

    correlation_id: str
    # SQL: correlation_id TEXT UNIQUE NOT NULL
    # Hash SHA-256 para sincronizacao.
    # Gerado por: hashlib.sha256(f'residencias:{chave}'.encode()).hexdigest()

    # ──────────────────────────────────────────────────────
    # CAMPOS OPCIONAIS (podem ser NULL no SQL)
    # ──────────────────────────────────────────────────────

    id: Optional[int] = None
    # SQL: id INTEGER PRIMARY KEY AUTOINCREMENT
    # Gerado pelo banco. None quando ainda nao foi salvo.

    bloco: Optional[str] = None
    # SQL: bloco TEXT
    # Ex: 'A', 'B', 'Torre 1'.
    # NULL em condominios HORIZONTAIS (casas/lotes).
    #
    # COMO SABER? Se o condominio tem predios → tem bloco.
    #             Se so tem casas → bloco e None.

    quadra: Optional[str] = None
    # SQL: quadra TEXT
    # Ex: '01', '05'.
    # NULL em condominios VERTICAIS (predios).
    #
    # E o oposto do bloco: casas tem quadra, aptos tem bloco.

    andar: Optional[int] = None
    # SQL: andar INTEGER
    # Numero do andar. None em casas.
    # Note: INTEGER no SQL → int no Python (nao str!).

    tipo_moradia: str = "apartamento"
    # SQL: tipo_moradia TEXT DEFAULT 'apartamento'
    #      CHECK(tipo_moradia IN ('apartamento','casa','comercial','outro'))
    #
    # SUGESTAO DO ADEMILSON! Ele percebeu que o porteiro
    # precisa saber se e casa ou apartamento para saber
    # como chamar o morador (interfone vs ir ate a porta).
    #
    # Valores validos: 'apartamento', 'casa', 'comercial', 'outro'

    interfone: Optional[str] = None
    # SQL: interfone TEXT
    # Codigo do interfone. Ex: '101', '1-A'.
    #
    # SUGESTAO DO ADEMILSON! Campo fundamental para a
    # portaria chamar o morador. Sem isso o porteiro
    # teria que procurar o numero na lista.

    observacao: Optional[str] = None
    # SQL: observacao TEXT
    # Anotacoes livres. Ex: 'Cobertura — acesso especial'.
    #
    # SUGESTAO DO ADEMILSON! O porteiro precisa de um
    # campo para anotar coisas que nao tem campo proprio.

    # ── Controle do registro ─────────────────────────────

    ativo: bool = True
    # SQL: ativo BOOLEAN DEFAULT 1 CHECK(ativo IN (0, 1))
    # True = ativa. False = soft delete.
    # Nunca deletamos dados — apenas desativamos!

    dt_criado_em: Optional[datetime] = None
    # SQL: dt_criado_em DATETIME DEFAULT CURRENT_TIMESTAMP

    dt_atualizado_em: Optional[datetime] = None
    # SQL: dt_atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP

    # ──────────────────────────────────────────────────────
    # VALIDACOES
    # ──────────────────────────────────────────────────────

    def __post_init__(self):
        """Valida os dados assim que o objeto e criado."""
        self._validar_tipo_moradia()

    def _validar_tipo_moradia(self):
        """tipo_moradia deve ser um dos valores aceitos pelo banco."""
        if self.tipo_moradia not in TIPOS_MORADIA_VALIDOS:
            raise ValueError(
                f"tipo_moradia invalido: '{self.tipo_moradia}'. "
                f"Valores aceitos: {TIPOS_MORADIA_VALIDOS}"
            )

    # ──────────────────────────────────────────────────────
    # CONVERSAO: BANCO → OBJETO
    # ──────────────────────────────────────────────────────

    @classmethod
    def from_db_row(cls, row) -> "Residencia":
        """
        Cria uma Residencia a partir de uma linha do banco.

        Uso:
            cursor.execute("SELECT * FROM residencias WHERE id = ?", (1,))
            linha = cursor.fetchone()
            res = Residencia.from_db_row(linha)
        """
        return cls(
            id=row["id"],
            codigo_condominio=row["codigo_condominio"],
            numero_residencia=row["numero_residencia"],
            bloco=row["bloco"],
            quadra=row["quadra"],
            andar=row["andar"],
            tipo_moradia=row["tipo_moradia"] or "apartamento",
            interfone=row["interfone"],
            observacao=row["observacao"],
            ativo=bool(row["ativo"]),
            correlation_id=row["correlation_id"],
            dt_criado_em=parse_datetime(row["dt_criado_em"]),
            dt_atualizado_em=parse_datetime(row["dt_atualizado_em"]),
        )

    # ──────────────────────────────────────────────────────
    # CONVERSAO: OBJETO → BANCO
    # ──────────────────────────────────────────────────────

    def to_db_dict(self) -> dict:
        """
        Converte para dicionario pronto para INSERT/UPDATE.

        Uso:
            dados = residencia.to_db_dict()
            colunas = ', '.join(dados.keys())
            placeholders = ', '.join(['?'] * len(dados))
            cursor.execute(
                f"INSERT INTO residencias ({colunas}) VALUES ({placeholders})",
                tuple(dados.values())
            )
        """
        return {
            "codigo_condominio": self.codigo_condominio,
            "numero_residencia": self.numero_residencia,
            "bloco": self.bloco,
            "quadra": self.quadra,
            "andar": self.andar,
            "tipo_moradia": self.tipo_moradia,
            "interfone": self.interfone,
            "observacao": self.observacao,
            "ativo": 1 if self.ativo else 0,
            "correlation_id": self.correlation_id,
        }

    # ──────────────────────────────────────────────────────
    # METODOS DE EXIBICAO
    # ──────────────────────────────────────────────────────

    @property
    def descricao_curta(self) -> str:
        """
        Retorna descricao legivel: 'Apto 101 (Bloco A, 1o andar)'
        ou 'Casa Lote 08 (Quadra 03)'.
        """
        tipo = "Apto" if self.tipo_moradia == "apartamento" else self.tipo_moradia.capitalize()
        partes = [f"{tipo} {self.numero_residencia}"]

        detalhes = []
        if self.bloco:
            detalhes.append(f"Bloco {self.bloco}")
        if self.quadra:
            detalhes.append(f"Quadra {self.quadra}")
        if self.andar is not None:
            detalhes.append(f"{self.andar}o andar")

        if detalhes:
            partes.append(f"({', '.join(detalhes)})")

        return " ".join(partes)

    @property
    def status_texto(self) -> str:
        """Retorna 'Ativa' ou 'Inativa'."""
        return "Ativa" if self.ativo else "Inativa"

    def resumo(self) -> str:
        """Retorna um resumo de uma linha."""
        inter = f" | Interfone: {self.interfone}" if self.interfone else ""
        return (
            f"[{self.id or 'NOVA'}] {self.descricao_curta}"
            f"{inter} | {self.status_texto}"
        )


# ──────────────────────────────────────────────────────────
# EXEMPLO DE USO (execute este arquivo para testar!)
#   python -m src.core.models.residencia
#   ou: python src/core/models/residencia.py
# ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import hashlib

    print("=" * 60)
    print("  TESTANDO O MODELO Residencia")
    print("=" * 60)

    # 1. Criar um apartamento
    cid = hashlib.sha256(b"residencias:res_101_A").hexdigest()
    apto = Residencia(
        codigo_condominio="COND-001",
        numero_residencia="101",
        bloco="A",
        andar=1,
        tipo_moradia="apartamento",
        interfone="101",
        correlation_id=cid,
    )
    print(f"\n1. Apartamento criado:")
    print(f"   {apto.resumo()}")
    print(f"   Descricao: {apto.descricao_curta}")

    # 2. Criar uma casa (condominio horizontal)
    cid2 = hashlib.sha256(b"residencias:res_lote08_Q03").hexdigest()
    casa = Residencia(
        codigo_condominio="COND-001",
        numero_residencia="08",
        quadra="03",
        tipo_moradia="casa",
        observacao="Lote 08 da Quadra 03",
        correlation_id=cid2,
    )
    print(f"\n2. Casa criada:")
    print(f"   {casa.resumo()}")
    print(f"   Descricao: {casa.descricao_curta}")

    # 3. Testar conversao para dicionario
    dados = apto.to_db_dict()
    print(f"\n3. Dicionario para INSERT:")
    for chave, valor in dados.items():
        print(f"   {chave}: {valor}")

    # 4. Testar validacao de tipo_moradia invalido
    print(f"\n4. Testando validacao:")
    try:
        invalido = Residencia(
            codigo_condominio="X",
            numero_residencia="1",
            tipo_moradia="garagem",  # valor invalido!
            correlation_id="x",
        )
    except ValueError as e:
        print(f"   OK! Tipo invalido detectado: {e}")

    print(f"\n{'=' * 60}")
    print("  TUDO FUNCIONANDO!")
    print("=" * 60)
