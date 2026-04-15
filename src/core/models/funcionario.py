from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Funcionario:
  
    nome: str
    documento: str
    correlation_id: str

    id: Optional[int] = None
    tipo_documento: str = "RG"
    telefone: Optional[str] = None
    bloqueado: bool = False
    dt_criado_em: Optional[datetime] = None