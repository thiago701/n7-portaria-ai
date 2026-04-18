#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  MODELO DE DOMINIO: Veiculo
  n7-portaria-ai | Aula 02
============================================================

Este arquivo mapeia a tabela 'veiculos' do banco de dados
para uma classe Python usando @dataclass.

O QUE E UM VEICULO?
  Carro, moto ou qualquer veiculo que entra no condominio.
  Pode pertencer a um MORADOR, FUNCIONARIO ou VISITANTE.

  >> CONTRIBUICAO DO ADEMILSON (v3.0):
  Ele sugeriu 'carro' e 'placa' diretamente na tabela moradores.
  O raciocinio estava certo! Refinamos para uma tabela separada
  que tambem serve funcionarios e visitantes.

REGRA IMPORTANTE (3 FKs mutuamente exclusivas):
  morador_id, funcionario_id, visitante_id — apenas UM deve
  ser preenchido. Os outros ficam NULL.
  Isso indica a QUEM o veiculo pertence.

  Exemplos:
    morador_id=1, funcionario_id=NULL, visitante_id=NULL → carro do morador 1
    morador_id=NULL, funcionario_id=3, visitante_id=NULL → carro do porteiro 3
    morador_id=NULL, funcionario_id=NULL, visitante_id=5 → carro do visitante 5

MAPEAMENTO:
  +-----------------------+------------------+-----------------+
  | Coluna SQL            | Atributo Python  | Tipo Python     |
  +-----------------------+------------------+-----------------+
  | id                    | id               | Optional[int]   |
  | placa                 | placa            | str             |
  | modelo                | modelo           | Optional[str]   |
  | cor                   | cor              | Optional[str]   |
  | morador_id            | morador_id       | Optional[int]   |
  | funcionario_id        | funcionario_id   | Optional[int]   |
  | visitante_id          | visitante_id     | Optional[int]   |
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


@dataclass
class Veiculo:
    """
    Representa um veiculo cadastrado no condominio.

    Exemplos de uso:
        >>> # Carro de um morador
        >>> carro = Veiculo(
        ...     placa="ABC1D23",
        ...     modelo="Onix",
        ...     cor="Prata",
        ...     morador_id=1,
        ...     correlation_id="abc123..."
        ... )

        >>> # Moto de um visitante
        >>> moto = Veiculo(
        ...     placa="XYZ9876",
        ...     modelo="Biz 125",
        ...     cor="Vermelha",
        ...     visitante_id=3,
        ...     correlation_id="def456..."
        ... )
    """

    # ──────────────────────────────────────────────────────
    # CAMPOS OBRIGATORIOS (NOT NULL no SQL)
    # ──────────────────────────────────────────────────────

    placa: str
    # SQL: placa TEXT UNIQUE NOT NULL CHECK(length(placa) >= 7)
    # Formato antigo: 'ABC-1234' (8 chars)
    # Formato Mercosul: 'ABC1D23' (7 chars)
    # UNIQUE = cada placa e unica no sistema.

    correlation_id: str
    # SQL: correlation_id TEXT UNIQUE NOT NULL

    # ──────────────────────────────────────────────────────
    # CAMPOS OPCIONAIS (com valor padrao)
    # ──────────────────────────────────────────────────────

    id: Optional[int] = None
    # SQL: id INTEGER PRIMARY KEY AUTOINCREMENT

    modelo: Optional[str] = None
    # SQL: modelo TEXT
    # Ex: 'Onix', 'Corolla', 'Biz 125', 'HB20'

    cor: Optional[str] = None
    # SQL: cor TEXT
    # Ex: 'Prata', 'Preto', 'Branco', 'Vermelho'

    # ── FKs mutuamente exclusivas ────────────────────────
    # Apenas UMA deve ser preenchida — as outras ficam None.
    # Isso indica a QUEM o veiculo pertence.

    morador_id: Optional[int] = None
    # SQL: morador_id INTEGER
    #      FOREIGN KEY (morador_id) REFERENCES moradores(id)
    # Se preenchido → veiculo pertence a este morador.

    funcionario_id: Optional[int] = None
    # SQL: funcionario_id INTEGER
    #      FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
    # Se preenchido → veiculo pertence a este funcionario.

    visitante_id: Optional[int] = None
    # SQL: visitante_id INTEGER
    #      FOREIGN KEY (visitante_id) REFERENCES visitantes(id)
    # Se preenchido → veiculo pertence a este visitante.

    ativo: bool = True
    # SQL: ativo BOOLEAN DEFAULT 1 CHECK(ativo IN (0, 1))

    dt_criado_em: Optional[datetime] = None
    # SQL: dt_criado_em DATETIME DEFAULT CURRENT_TIMESTAMP

    # ──────────────────────────────────────────────────────
    # VALIDACOES
    # ──────────────────────────────────────────────────────

    def __post_init__(self):
        """Valida os dados assim que o objeto e criado."""
        self._validar_placa()
        self._validar_proprietario()

    def _validar_placa(self):
        """Placa deve ter pelo menos 7 caracteres."""
        placa_limpa = self.placa.strip().upper().replace("-", "")
        if len(placa_limpa) < 7:
            raise ValueError(
                f"Placa deve ter pelo menos 7 caracteres. "
                f"Recebido: '{self.placa}' ({len(placa_limpa)} chars)"
            )
        self.placa = self.placa.strip().upper()  # normaliza

    def _validar_proprietario(self):
        """Exatamente UM proprietario deve ser informado (morador, funcionario ou visitante)."""
        preenchidos = sum([
            self.morador_id is not None,
            self.funcionario_id is not None,
            self.visitante_id is not None,
        ])
        if preenchidos == 0:
            raise ValueError(
                "Veiculo deve ter um proprietario: "
                "preencha morador_id, funcionario_id ou visitante_id"
            )
        if preenchidos > 1:
            raise ValueError(
                "Veiculo deve ter apenas UM proprietario. "
                "Preencha apenas morador_id OU funcionario_id OU visitante_id"
            )

    # ──────────────────────────────────────────────────────
    # CONVERSAO: BANCO → OBJETO
    # ──────────────────────────────────────────────────────

    @classmethod
    def from_db_row(cls, row) -> "Veiculo":
        """
        Cria um Veiculo a partir de uma linha do banco.

        Uso:
            cursor.execute("SELECT * FROM veiculos WHERE id = ?", (1,))
            linha = cursor.fetchone()
            veiculo = Veiculo.from_db_row(linha)
        """
        return cls(
            id=row["id"],
            placa=row["placa"],
            modelo=row["modelo"],
            cor=row["cor"],
            morador_id=row["morador_id"],
            funcionario_id=row["funcionario_id"],
            visitante_id=row["visitante_id"],
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
            "placa": self.placa,
            "modelo": self.modelo,
            "cor": self.cor,
            "morador_id": self.morador_id,
            "funcionario_id": self.funcionario_id,
            "visitante_id": self.visitante_id,
            "ativo": 1 if self.ativo else 0,
            "correlation_id": self.correlation_id,
        }

    # ──────────────────────────────────────────────────────
    # METODOS DE EXIBICAO
    # ──────────────────────────────────────────────────────

    @property
    def proprietario_texto(self) -> str:
        """Retorna quem e o dono do veiculo."""
        if self.morador_id:
            return f"Morador #{self.morador_id}"
        if self.funcionario_id:
            return f"Funcionario #{self.funcionario_id}"
        if self.visitante_id:
            return f"Visitante #{self.visitante_id}"
        return "Sem proprietario"

    @property
    def descricao_curta(self) -> str:
        """Ex: 'ABC1D23 (Onix Prata)' ou 'ABC1D23'."""
        partes = [self.placa]
        detalhes = []
        if self.modelo:
            detalhes.append(self.modelo)
        if self.cor:
            detalhes.append(self.cor)
        if detalhes:
            partes.append(f"({' '.join(detalhes)})")
        return " ".join(partes)

    @property
    def status_texto(self) -> str:
        """Retorna 'Ativo' ou 'Inativo'."""
        return "Ativo" if self.ativo else "Inativo"

    def resumo(self) -> str:
        """Retorna um resumo de uma linha."""
        return (
            f"[{self.id or 'NOVO'}] {self.descricao_curta} | "
            f"{self.proprietario_texto} | {self.status_texto}"
        )


# ──────────────────────────────────────────────────────────
# EXEMPLO DE USO (execute este arquivo para testar!)
#   python src/core/models/veiculo.py
# ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import hashlib

    print("=" * 60)
    print("  TESTANDO O MODELO Veiculo")
    print("=" * 60)

    # 1. Carro de morador
    cid = hashlib.sha256(b"veiculos:ABC1D23").hexdigest()
    carro = Veiculo(
        placa="ABC1D23",
        modelo="Onix",
        cor="Prata",
        morador_id=1,
        correlation_id=cid,
    )
    print(f"\n1. Veiculo criado:")
    print(f"   {carro.resumo()}")
    print(f"   Descricao: {carro.descricao_curta}")

    # 2. Moto de visitante
    cid2 = hashlib.sha256(b"veiculos:XYZ9876").hexdigest()
    moto = Veiculo(
        placa="XYZ-9876",
        modelo="Biz 125",
        cor="Vermelha",
        visitante_id=3,
        correlation_id=cid2,
    )
    print(f"\n2. Moto de visitante:")
    print(f"   {moto.resumo()}")

    # 3. Dicionario para INSERT
    dados = carro.to_db_dict()
    print(f"\n3. Dicionario para INSERT:")
    for chave, valor in dados.items():
        print(f"   {chave}: {valor}")

    # 4. Validacoes
    print(f"\n4. Testando validacoes:")
    try:
        Veiculo(placa="AB1", correlation_id="x", morador_id=1)
    except ValueError as e:
        print(f"   OK! Placa curta: {e}")

    try:
        Veiculo(placa="ABC1D23", correlation_id="x")  # sem proprietario
    except ValueError as e:
        print(f"   OK! Sem dono: {e}")

    try:
        Veiculo(placa="ABC1D23", correlation_id="x",
                morador_id=1, visitante_id=2)  # 2 donos
    except ValueError as e:
        print(f"   OK! 2 donos: {e}")

    print(f"\n{'=' * 60}")
    print("  TUDO FUNCIONANDO!")
    print("=" * 60)
