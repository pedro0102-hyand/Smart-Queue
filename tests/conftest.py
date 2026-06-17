import pytest

from models.chamado import Chamado


@pytest.fixture
def csv_temporario(monkeypatch, tmp_path):

    csv_path = tmp_path / "chamados.csv"

    monkeypatch.setattr(
        "services.persistence.ARQUIVO_CSV",
        str(csv_path),
    )

    return csv_path


def criar_chamado_teste(
    severidade: int,
    cliente: str = "Teste",
    ordem_chegada: int = 0,
    id_chamado: str = "teste123",
    categoria: str = "Teste",
) -> Chamado:

    return Chamado(
        prioridade=-(severidade * 100),
        ordem_chegada=ordem_chegada,
        id=id_chamado,
        cliente=cliente,
        categoria=categoria,
        severidade=severidade,
        descricao="Descrição de teste",
        criado_em="2026-06-17 10:00:00",
    )
