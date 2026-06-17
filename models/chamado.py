import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(order=True)
class Chamado:

    prioridade: int
    ordem_chegada: int = field(default=0)

    id: str = field(
        default_factory=lambda: str(uuid.uuid4())[:8],
        compare=False
    )

    cliente: str = field(
        compare=False,
        default=""
    )

    categoria: str = field(
        compare=False,
        default=""
    )

    severidade: int = field(
        compare=False,
        default=0
    )

    descricao: str = field(
        compare=False,
        default=""
    )

    criado_em: str = field(
        default_factory=lambda:
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        compare=False
    )

    def __str__(self):
        return (
            f"Chamado("
            f"id={self.id}, "
            f"cliente={self.cliente}, "
            f"categoria={self.categoria}, "
            f"severidade={self.severidade}, "
            f"prioridade={self.prioridade}, "
            f"criado_em={self.criado_em})"
        )
    
