from dataclasses import dataclass
from typing import Optional

@dataclass
class Produto:
    id: Optional[int] = None
    nome: Optional[str] = None
    preco: Optional[int] = None
    descricao: Optional[str] = None