"""
Modelos de domínio do n7-portaria-ai.

Cada tabela do banco de dados tem um modelo Python correspondente.
Veja GUIA_MAPEAMENTO.md para aprender a criar novos modelos!
"""

from src.core.models.morador import Morador
from src.core.models.residencia import Residencia
from src.core.models.morador_residencia import MoradorResidencia

__all__ = ["Morador", "Residencia", "MoradorResidencia"]
