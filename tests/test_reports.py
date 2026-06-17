from services.reports import heapsort, top_chamados
from tests.conftest import criar_chamado_teste


def test_heapsort_por_prioridade():

    baixo = criar_chamado_teste(
        1,
        cliente="Baixa",
        ordem_chegada=1,
    )

    alto = criar_chamado_teste(
        5,
        cliente="Alta",
        ordem_chegada=2,
    )

    medio = criar_chamado_teste(
        3,
        cliente="Media",
        ordem_chegada=3,
    )

    chamados = [baixo, alto, medio]

    ordenados = heapsort(chamados)

    assert [c.cliente for c in ordenados] == [
        "Alta",
        "Media",
        "Baixa",
    ]


def test_heapsort_fifo_em_empate():

    primeiro = criar_chamado_teste(
        3,
        cliente="Lucas",
        ordem_chegada=1,
    )

    segundo = criar_chamado_teste(
        3,
        cliente="Rodrigo",
        ordem_chegada=2,
    )

    chamados = [segundo, primeiro]

    ordenados = heapsort(chamados)

    assert ordenados[0].cliente == "Lucas"
    assert ordenados[1].cliente == "Rodrigo"


def test_heapsort_nao_altera_lista_original():

    chamado = criar_chamado_teste(
        3,
        ordem_chegada=1,
    )

    chamados = [chamado]
    copia_antes = chamados.copy()

    heapsort(chamados)

    assert chamados == copia_antes


def test_top_chamados_limita_quantidade():

    chamados = [
        criar_chamado_teste(
            severidade,
            cliente=f"Cliente{severidade}",
            ordem_chegada=severidade,
        )
        for severidade in range(1, 7)
    ]

    top = top_chamados(chamados, n=3)

    assert len(top) == 3
    assert [c.severidade for c in top] == [6, 5, 4]


def test_top_chamados_lista_vazia():

    assert top_chamados([]) == []
