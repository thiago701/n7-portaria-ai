#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  MODELO DE DOMINIO: Acesso
  n7-portaria-ai | Aula 02
============================================================

Este arquivo mapeia a tabela 'acessos' do banco de dados
para uma classe Python usando @dataclass.

O QUE E UM ACESSO?
  E o LOG de cada entrada/saida no condominio.
  NUNCA deletar registros desta tabela — e historico!

  Cada acesso registra:
  - QUEM entrou (visitante_id → visitantes)
  - QUEM foi visitado (morador_id → moradores)
  - QUEM liberou (funcionario_id → funcionarios)
  - COMO chegou (veiculo_id → veiculos, ou a pe)
  - POR ONDE entrou (tipo_acesso: 'pedestre' ou 'garagem')
  - COMO se autenticou (2FA: senha, digital, facial)

AUTENTICACAO 2FA (Dois Fatores):
  O sistema exige pelo menos 1 fator de autenticacao:
  - auth_senha   = porteiro liberou com senha manual
  - auth_digital = leitor biometrico confirmou digital
  - auth_facial  = camera reconheceu o rosto

  CHECK(auth_senha + auth_digital + auth_facial >= 1)
  → Nenhum acesso pode ser registrado sem autenticacao!

  Em config_acesso_morador, o morador pode exigir 2 fatores
  (ex: digital + facial) para maior seguranca.

MAPEAMENTO:
  +-----------------------+------------------+-----------------+
  | Coluna SQL            | Atributo Python  | Tipo Python     |
  +-----------------------+------------------+-----------------+
  | id                    | id               | Optional[int]   |
  | visitante_id          | visitante_id     | int             |
  | morador_id            | morador_id       | Optional[int]   |
  | funcionario_id        | funcionario_id   | Optional[int]   |
  | veiculo_id            | veiculo_id       | Optional[int]   |
  | tipo_acesso           | tipo_acesso      | str             |
  | auth_senha            | auth_senha       | bool            |
  | auth_digital          | auth_digital     | bool            |
  | auth_facial           | auth_facial      | bool            |
  | motivo                | motivo           | str             |
  | dt_entrada_em         | dt_entrada_em    | datetime        |
  | dt_saida_em           | dt_saida_em      | Optional[datetime]|
  | porteiro              | porteiro         | Optional[str]   |
  | observacoes           | observacoes      | Optional[str]   |
  | correlation_id        | correlation_id   | str             |
  +-----------------------+------------------+-----------------+
============================================================
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.core.models.base import parse_datetime


# ============================================================
# TIPOS DE ACESSO
# ============================================================
# 'pedestre' = portao principal (a pe)
# 'garagem'  = cancela do estacionamento (de carro/moto)

TIPOS_ACESSO_VALIDOS = ("pedestre", "garagem")


@dataclass
class Acesso:
    """
    Representa um registro de entrada/saida no condominio.

    REGRA: NUNCA deletar acessos — e historico de seguranca!

    Exemplos de uso:
        >>> from datetime import datetime
        >>> acesso = Acesso(
        ...     visitante_id=1,
        ...     morador_id=3,
        ...     funcionario_id=1,
        ...     motivo="Entrega de encomenda",
        ...     auth_senha=True,
        ...     correlation_id="abc123..."
        ... )
        >>> print(acesso.esta_dentro)  # True (dt_saida_em e None)
    """

    # ──────────────────────────────────────────────────────
    # CAMPOS OBRIGATORIOS (NOT NULL no SQL)
    # ──────────────────────────────────────────────────────

    visitante_id: int
    # SQL: visitante_id INTEGER NOT NULL
    #      FOREIGN KEY (visitante_id) REFERENCES visitantes(id)
    # QUEM entrou. Todo acesso e de um visitante.

    motivo: str
    # SQL: motivo TEXT NOT NULL
    # POR QUE veio. Ex: "Entrega de encomenda", "Visita familiar"

    correlation_id: str
    # SQL: correlation_id TEXT UNIQUE NOT NULL

    # ──────────────────────────────────────────────────────
    # CAMPOS OPCIONAIS / COM PADRAO
    # ──────────────────────────────────────────────────────

    id: Optional[int] = None
    # SQL: id INTEGER PRIMARY KEY AUTOINCREMENT

    morador_id: Optional[int] = None
    # SQL: morador_id INTEGER
    #      FOREIGN KEY (morador_id) REFERENCES moradores(id)
    # QUEM foi visitado. None = servico geral sem morador especifico.

    funcionario_id: Optional[int] = None
    # SQL: funcionario_id INTEGER
    #      FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
    # Porteiro que registrou este acesso.

    veiculo_id: Optional[int] = None
    # SQL: veiculo_id INTEGER
    #      FOREIGN KEY (veiculo_id) REFERENCES veiculos(id)
    # Veiculo usado. None = veio a pe.

    tipo_acesso: str = "pedestre"
    # SQL: tipo_acesso TEXT DEFAULT 'pedestre'
    #      CHECK(tipo_acesso IN ('pedestre', 'garagem'))
    # 'pedestre' = portao principal
    # 'garagem'  = cancela do estacionamento

    # ── 2FA — Fatores de Autenticacao ────────────────────
    # Pelo menos 1 deve ser True!
    # CHECK(auth_senha + auth_digital + auth_facial >= 1)

    auth_senha: bool = False
    # SQL: auth_senha BOOLEAN DEFAULT 0
    # True = porteiro liberou com senha/codigo manual.

    auth_digital: bool = False
    # SQL: auth_digital BOOLEAN DEFAULT 0
    # True = leitor biometrico confirmou a digital.

    auth_facial: bool = False
    # SQL: auth_facial BOOLEAN DEFAULT 0
    # True = camera reconheceu o rosto.

    dt_entrada_em: Optional[datetime] = None
    # SQL: dt_entrada_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    # Quando entrou. Preenchido automaticamente pelo banco.

    dt_saida_em: Optional[datetime] = None
    # SQL: dt_saida_em DATETIME
    # Quando saiu. NULL = pessoa AINDA ESTA DENTRO do condominio!

    porteiro: Optional[str] = None
    # SQL: porteiro TEXT
    # Nome do porteiro em texto livre (compatibilidade).

    observacoes: Optional[str] = None
    # SQL: observacoes TEXT
    # Anotacoes livres sobre o acesso.

    # ──────────────────────────────────────────────────────
    # VALIDACOES
    # ──────────────────────────────────────────────────────

    def __post_init__(self):
        """Valida os dados assim que o objeto e criado."""
        self._validar_tipo_acesso()
        self._validar_autenticacao()

    def _validar_tipo_acesso(self):
        """tipo_acesso deve ser 'pedestre' ou 'garagem'."""
        if self.tipo_acesso not in TIPOS_ACESSO_VALIDOS:
            raise ValueError(
                f"tipo_acesso invalido: '{self.tipo_acesso}'. "
                f"Valores aceitos: {TIPOS_ACESSO_VALIDOS}"
            )

    def _validar_autenticacao(self):
        """Pelo menos 1 fator de autenticacao deve estar ativo."""
        total = int(self.auth_senha) + int(self.auth_digital) + int(self.auth_facial)
        if total < 1:
            raise ValueError(
                "Pelo menos 1 fator de autenticacao e obrigatorio: "
                "auth_senha, auth_digital ou auth_facial"
            )

    # ──────────────────────────────────────────────────────
    # CONVERSAO: BANCO → OBJETO
    # ──────────────────────────────────────────────────────

    @classmethod
    def from_db_row(cls, row) -> "Acesso":
        """
        Cria um Acesso a partir de uma linha do banco.

        Uso:
            cursor.execute("SELECT * FROM acessos WHERE id = ?", (1,))
            linha = cursor.fetchone()
            acesso = Acesso.from_db_row(linha)
        """
        return cls(
            id=row["id"],
            visitante_id=row["visitante_id"],
            morador_id=row["morador_id"],
            funcionario_id=row["funcionario_id"],
            veiculo_id=row["veiculo_id"],
            tipo_acesso=row["tipo_acesso"] or "pedestre",
            auth_senha=bool(row["auth_senha"]),
            auth_digital=bool(row["auth_digital"]),
            auth_facial=bool(row["auth_facial"]),
            motivo=row["motivo"],
            dt_entrada_em=parse_datetime(row["dt_entrada_em"]),
            dt_saida_em=parse_datetime(row["dt_saida_em"]),
            porteiro=row["porteiro"],
            observacoes=row["observacoes"],
            correlation_id=row["correlation_id"],
        )

    # ──────────────────────────────────────────────────────
    # CONVERSAO: OBJETO → BANCO
    # ──────────────────────────────────────────────────────

    def to_db_dict(self) -> dict:
        """Converte para dicionario pronto para INSERT/UPDATE."""
        return {
            "visitante_id": self.visitante_id,
            "morador_id": self.morador_id,
            "funcionario_id": self.funcionario_id,
            "veiculo_id": self.veiculo_id,
            "tipo_acesso": self.tipo_acesso,
            "auth_senha": 1 if self.auth_senha else 0,
            "auth_digital": 1 if self.auth_digital else 0,
            "auth_facial": 1 if self.auth_facial else 0,
            "motivo": self.motivo,
            "dt_entrada_em": str(self.dt_entrada_em) if self.dt_entrada_em else None,
            "dt_saida_em": str(self.dt_saida_em) if self.dt_saida_em else None,
            "porteiro": self.porteiro,
            "observacoes": self.observacoes,
            "correlation_id": self.correlation_id,
        }

    # ──────────────────────────────────────────────────────
    # METODOS DE EXIBICAO
    # ──────────────────────────────────────────────────────

    @property
    def esta_dentro(self) -> bool:
        """True se a pessoa AINDA esta dentro do condominio."""
        return self.dt_saida_em is None

    @property
    def fatores_usados(self) -> list:
        """Retorna lista dos fatores de autenticacao usados."""
        fatores = []
        if self.auth_senha:
            fatores.append("senha")
        if self.auth_digital:
            fatores.append("digital")
        if self.auth_facial:
            fatores.append("facial")
        return fatores

    @property
    def status_texto(self) -> str:
        """Retorna status legivel."""
        if self.esta_dentro:
            return "DENTRO"
        return f"Saiu em {self.dt_saida_em}"

    def resumo(self) -> str:
        """Retorna um resumo de uma linha."""
        auth = "+".join(self.fatores_usados)
        via = f"via {self.tipo_acesso}"
        return (
            f"[{self.id or 'NOVO'}] Visitante #{self.visitante_id} "
            f"→ Morador #{self.morador_id or '?'} | "
            f"{via} | Auth: {auth} | {self.status_texto}"
        )


# ──────────────────────────────────────────────────────────
# EXEMPLO DE USO (execute este arquivo para testar!)
#   python src/core/models/acesso.py
# ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import hashlib

    print("=" * 60)
    print("  TESTANDO O MODELO Acesso")
    print("=" * 60)

    # 1. Acesso com senha
    cid = hashlib.sha256(b"acessos:1").hexdigest()
    a = Acesso(
        visitante_id=1,
        morador_id=3,
        funcionario_id=1,
        motivo="Entrega de encomenda",
        auth_senha=True,
        correlation_id=cid,
    )
    print(f"\n1. Acesso criado:")
    print(f"   {a.resumo()}")
    print(f"   Esta dentro? {a.esta_dentro}")
    print(f"   Fatores: {a.fatores_usados}")

    # 2. Acesso 2FA (digital + facial)
    cid2 = hashlib.sha256(b"acessos:2").hexdigest()
    a2 = Acesso(
        visitante_id=2,
        morador_id=1,
        motivo="Visita familiar",
        tipo_acesso="garagem",
        auth_digital=True,
        auth_facial=True,
        veiculo_id=1,
        correlation_id=cid2,
    )
    print(f"\n2. Acesso 2FA:")
    print(f"   {a2.resumo()}")
    print(f"   Fatores: {a2.fatores_usados}")

    # 3. Validacoes
    print(f"\n3. Testando validacoes:")
    try:
        Acesso(visitante_id=1, motivo="X", correlation_id="x",
               tipo_acesso="escada")
    except ValueError as e:
        print(f"   OK! Tipo invalido: {e}")

    try:
        Acesso(visitante_id=1, motivo="X", correlation_id="x")  # sem auth
    except ValueError as e:
        print(f"   OK! Sem autenticacao: {e}")

    print(f"\n{'=' * 60}")
    print("  TUDO FUNCIONANDO!")
    print("=" * 60)
