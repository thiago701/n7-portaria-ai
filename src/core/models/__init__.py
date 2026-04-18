"""
Modelos de domínio do n7-portaria-ai.

Cada tabela do banco de dados tem um modelo Python correspondente.
Veja GUIA_MAPEAMENTO.md para aprender a criar novos modelos!

TABELAS MAPEADAS (9/9):
  moradores           → Morador
  residencias         → Residencia
  morador_residencia  → MoradorResidencia
  visitantes          → Visitante
  funcionarios        → Funcionario
  veiculos            → Veiculo
  acessos             → Acesso
  config_acesso_morador → ConfigAcessoMorador
  assinatura_condominio → AssinaturaCondominio
"""

from src.core.models.morador import Morador
from src.core.models.residencia import Residencia
from src.core.models.morador_residencia import MoradorResidencia
from src.core.models.visitante import Visitante
from src.core.models.funcionario import Funcionario
from src.core.models.veiculo import Veiculo
from src.core.models.acesso import Acesso
from src.core.models.config_acesso_morador import ConfigAcessoMorador
from src.core.models.assinatura_condominio import AssinaturaCondominio

__all__ = [
    "Morador",
    "Residencia",
    "MoradorResidencia",
    "Visitante",
    "Funcionario",
    "Veiculo",
    "Acesso",
    "ConfigAcessoMorador",
    "AssinaturaCondominio",
]
