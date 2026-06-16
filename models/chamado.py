import uuid
from dataclasses import dataclass, field
from datetime import datetime

@dataclass(order=True)

class Chamado:

    prioridade: int
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8], compare=False)
    cliente : str = field(compare=False, default="")
    categoria : str = field(compare=False, default="")
    severidade : int = field(compare=False, default="")
    descricao : str = field(compare=False, default="")
    criado_em: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"), compare=False)

    def __str__(self):
        return f"Chamado(id={self.id}, cliente={self.cliente}, categoria={self.categoria}, severidade={self.severidade}, prioridade={self.prioridade}, criado_em={self.criado_em})"
    
