from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class Cargo(str, Enum):
    PORTEIRO = "porteiro"
    ZELADOR = "zelador"        # ← era "Zelador" (inconsistente)
    ADMINISTRADOR = "administrador"
    OUTRO = "outro"

    