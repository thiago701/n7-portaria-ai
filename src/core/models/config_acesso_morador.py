#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  MODELO DE DOMINIO: ConfigAcessoMorador
  n7-portaria-ai | Aula 02
============================================================

Este arquivo mapeia a tabela 'config_acesso_morador' do banco
para uma classe Python usando @dataclass.

O QUE E CONFIG_ACESSO_MORADOR?
  E a POLITICA DE SEGURANCA individual de cada morador.
  Cada morador pode escolher quantos fatores de autenticacao
  exigir para liberar visitantes na sua unidade.

  RELACAO 1:1 com moradores:
  Cada morador tem NO MAXIMO 1 config (UNIQUE morador_id).
  Se nao tiver config, o sistema usa o padrao (1 fator).

  FATORES DE AUTENTICACAO:
    permite_senha   = porteiro pode liberar com codigo
    permite_digital = pode usar leitor biometrico
    permite_facial  = pode usar camera facial

  fatores_requeridos:
    1 = qualquer fator aceito (mais pratico)
    2 = dois fatores obrigatorios (mais seguro)
        Ex: digital + facial

  REGRA: pelo menos 1 tipo deve estar habilitado!
  CHECK(permite_senha + permite_digital + permite_facial >= 1)

MAPEAMENTO:
  +-----------------------+--------------------+-----------------+
  | Coluna SQL            | Atributo Python    | Tipo Python     |
  +-----------------------+--------------------+-----------------+
  | id                    | id                 | Optional[int]   |
  | morador_id            | morador_id         | int             |
  | fatores_requeridos    | fatores_requeridos | int             |
  | permite_senha         | permite_senha      | bool            |
  | permite_digital       | permite_digital    | bool            |
  | permite_facial        | permite_facial     | bool            |
  | correlation_id        | correlation_id     | str             |
  | dt_criado_em          | dt_criado_em       | Optional[datetime]|
  | dt_atualizado_em      | dt_atualizado_em   | Optional[datetime]|
  +-----------------------+--------------------+-----------------+
============================================================
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.core.models.base import parse_datetime


@dataclass
class ConfigAcessoMorador:
    """
    Politica de autenticacao individual de um morador.

    Exemplos de uso:
        >>> # Morador exige 2 fatores (digital + facial)
        >>> config = ConfigAcessoMorador(
        ...     morador_id=1,
        ...     fatores_requeridos=2,
        ...     permite_senha=False,
        ...     permite_digital=True,
        ...     permite_facial=True,
        ...     correlation_id="abc123..."
        ... )

        >>> # Config padrao (1 fator, apenas senha)
        >>> config_simples = ConfigAcessoMorador(
        ...     morador_id=5,
        ...     correlation_id="def456..."
        ... )
        >>> print(config_simples.fatores_requeridos)  # 1
        >>> print(config_simples.permite_senha)       # True
    """

    # ──────────────────────────────────────────────────────
    # CAMPOS OBRIGATORIOS
    # ──────────────────────────────────────────────────────

    morador_id: int
    # SQL: morador_id INTEGER UNIQUE NOT NULL
    #      FOREIGN KEY (morador_id) REFERENCES moradores(id)
    # UNIQUE: cada morador tem no maximo 1 config (relacao 1:1).

    correlation_id: str
    # SQL: correlation_id TEXT UNIQUE NOT NULL

    # ──────────────────────────────────────────────────────
    # CAMPOS COM VALOR PADRAO
    # ──────────────────────────────────────────────────────

    id: Optional[int] = None
    # SQL: id INTEGER PRIMARY KEY AUTOINCREMENT

    fatores_requeridos: int = 1
    # SQL: fatores_requeridos INTEGER DEFAULT 1
    #      CHECK(fatores_requeridos IN (1, 2))
    # 1 = qualquer fator aceito (padrao, mais pratico)
    # 2 = dois fatores obrigatorios (mais seguro)

    permite_senha: bool = True
    # SQL: permite_senha BOOLEAN DEFAULT 1
    # True = porteiro pode liberar com codigo/senha.

    permite_digital: bool = True
    # SQL: permite_digital BOOLEAN DEFAULT 1
    # True = pode usar leitor de digital.

    permite_facial: bool = False
    # SQL: permite_facial BOOLEAN DEFAULT 0
    # False por padrao: exige hardware de camera especial.
    # So habilitar se o condominio tiver a camera.

    dt_criado_em: Optional[datetime] = None
    # SQL: dt_criado_em DATETIME DEFAULT CURRENT_TIMESTAMP

    dt_atualizado_em: Optional[datetime] = None
    # SQL: dt_atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP

    # ──────────────────────────────────────────────────────
    # VALIDACOES
    # ──────────────────────────────────────────────────────

    def __post_init__(self):
        """Valida os dados assim que o objeto e criado."""
        self._validar_fatores()
        self._validar_pelo_menos_um_tipo()
        self._validar_fatores_vs_tipos()

    def _validar_fatores(self):
        """fatores_requeridos deve ser 1 ou 2."""
        if self.fatores_requeridos not in (1, 2):
            raise ValueError(
                f"fatores_requeridos deve ser 1 ou 2. "
                f"Recebido: {self.fatores_requeridos}"
            )

    def _validar_pelo_menos_um_tipo(self):
        """Pelo menos 1 tipo de autenticacao deve estar habilitado."""
        total = int(self.permite_senha) + int(self.permite_digital) + int(self.permite_facial)
        if total < 1:
            raise ValueError(
                "Pelo menos 1 tipo de autenticacao deve estar habilitado: "
                "permite_senha, permite_digital ou permite_facial"
            )

    def _validar_fatores_vs_tipos(self):
        """Se exige 2 fatores, pelo menos 2 tipos devem estar habilitados."""
        if self.fatores_requeridos == 2:
            total = int(self.permite_senha) + int(self.permite_digital) + int(self.permite_facial)
            if total < 2:
                raise ValueError(
                    f"Se fatores_requeridos=2, pelo menos 2 tipos devem "
                    f"estar habilitados. Apenas {total} habilitado(s)."
                )

    # ──────────────────────────────────────────────────────
    # CONVERSAO: BANCO → OBJETO
    # ──────────────────────────────────────────────────────

    @classmethod
    def from_db_row(cls, row) -> "ConfigAcessoMorador":
        """
        Cria uma ConfigAcessoMorador a partir de uma linha do banco.

        Uso:
            cursor.execute(
                "SELECT * FROM config_acesso_morador WHERE morador_id = ?", (1,)
            )
            linha = cursor.fetchone()
            config = ConfigAcessoMorador.from_db_row(linha)
        """
        return cls(
            id=row["id"],
            morador_id=row["morador_id"],
            fatores_requeridos=row["fatores_requeridos"] or 1,
            permite_senha=bool(row["permite_senha"]),
            permite_digital=bool(row["permite_digital"]),
            permite_facial=bool(row["permite_facial"]),
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
            "morador_id": self.morador_id,
            "fatores_requeridos": self.fatores_requeridos,
            "permite_senha": 1 if self.permite_senha else 0,
            "permite_digital": 1 if self.permite_digital else 0,
            "permite_facial": 1 if self.permite_facial else 0,
            "correlation_id": self.correlation_id,
        }

    # ──────────────────────────────────────────────────────
    # METODOS DE EXIBICAO
    # ──────────────────────────────────────────────────────

    @property
    def tipos_permitidos(self) -> list:
        """Retorna lista dos tipos de autenticacao habilitados."""
        tipos = []
        if self.permite_senha:
            tipos.append("senha")
        if self.permite_digital:
            tipos.append("digital")
        if self.permite_facial:
            tipos.append("facial")
        return tipos

    @property
    def nivel_seguranca(self) -> str:
        """Retorna nivel de seguranca legivel."""
        if self.fatores_requeridos == 2:
            return "Alto (2FA)"
        return "Padrao (1 fator)"

    def resumo(self) -> str:
        """Retorna um resumo de uma linha."""
        tipos = ", ".join(self.tipos_permitidos)
        return (
            f"[{self.id or 'NOVO'}] Morador #{self.morador_id} | "
            f"{self.nivel_seguranca} | Permite: {tipos}"
        )


# ──────────────────────────────────────────────────────────
# EXEMPLO DE USO (execute este arquivo para testar!)
#   python src/core/models/config_acesso_morador.py
# ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import hashlib

    print("=" * 60)
    print("  TESTANDO O MODELO ConfigAcessoMorador")
    print("=" * 60)

    # 1. Config padrao (1 fator, senha + digital)
    cid = hashlib.sha256(b"config:1").hexdigest()
    c1 = ConfigAcessoMorador(
        morador_id=1,
        correlation_id=cid,
    )
    print(f"\n1. Config padrao:")
    print(f"   {c1.resumo()}")

    # 2. Config 2FA (digital + facial)
    cid2 = hashlib.sha256(b"config:2").hexdigest()
    c2 = ConfigAcessoMorador(
        morador_id=2,
        fatores_requeridos=2,
        permite_senha=False,
        permite_digital=True,
        permite_facial=True,
        correlation_id=cid2,
    )
    print(f"\n2. Config 2FA:")
    print(f"   {c2.resumo()}")

    # 3. Dicionario para INSERT
    dados = c2.to_db_dict()
    print(f"\n3. Dicionario para INSERT:")
    for chave, valor in dados.items():
        print(f"   {chave}: {valor}")

    # 4. Validacoes
    print(f"\n4. Testando validacoes:")
    try:
        ConfigAcessoMorador(morador_id=1, fatores_requeridos=3, correlation_id="x")
    except ValueError as e:
        print(f"   OK! Fatores invalidos: {e}")

    try:
        ConfigAcessoMorador(
            morador_id=1, permite_senha=False,
            permite_digital=False, permite_facial=False,
            correlation_id="x"
        )
    except ValueError as e:
        print(f"   OK! Nenhum tipo: {e}")

    try:
        ConfigAcessoMorador(
            morador_id=1, fatores_requeridos=2,
            permite_senha=True, permite_digital=False,
            permite_facial=False, correlation_id="x"
        )
    except ValueError as e:
        print(f"   OK! 2FA com 1 tipo: {e}")

    print(f"\n{'=' * 60}")
    print("  TUDO FUNCIONANDO!")
    print("=" * 60)
