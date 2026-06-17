import csv

from services.fila import FilaPrioridade
from services.persistence import carregar_chamados
from tests.conftest import criar_chamado_teste


def test_fila_inicia_vazia():

    fila = FilaPrioridade()

    assert fila.esta_vazia() is True
    assert fila.obter_tamanho_fila() == 0


def test_adicionar_chamado():

    fila = FilaPrioridade()

    chamado = criar_chamado_teste(3)

    fila.adicionar_chamado(chamado)

    assert fila.esta_vazia() is False
    assert fila.obter_tamanho_fila() == 1


def test_visualizar_proximo():

    fila = FilaPrioridade()

    chamado = criar_chamado_teste(
        4,
        "Pedro"
    )

    fila.adicionar_chamado(chamado)

    proximo = fila.visualizar_proximo()

    assert proximo.cliente == "Pedro"
    assert proximo.severidade == 4


def test_prioridade_maior_sai_primeiro():

    fila = FilaPrioridade()

    baixo = criar_chamado_teste(
        1,
        "Baixa"
    )

    alto = criar_chamado_teste(
        5,
        "Alta"
    )

    fila.adicionar_chamado(baixo)
    fila.adicionar_chamado(alto)

    atendido = fila.atender_proximo()

    assert atendido.cliente == "Alta"
    assert atendido.severidade == 5


def test_atender_fila_vazia():

    fila = FilaPrioridade()

    resultado = fila.atender_proximo()

    assert resultado is None


def test_remover_reduz_tamanho():

    fila = FilaPrioridade()

    fila.adicionar_chamado(
        criar_chamado_teste(3)
    )

    fila.atender_proximo()

    assert fila.obter_tamanho_fila() == 0


def test_fifo_em_empate():

    fila = FilaPrioridade()

    primeiro = criar_chamado_teste(
        2,
        "Lucas"
    )

    segundo = criar_chamado_teste(
        2,
        "Rodrigo"
    )

    fila.adicionar_chamado(primeiro)
    fila.adicionar_chamado(segundo)

    atendido = fila.atender_proximo()

    assert atendido.cliente == "Lucas"


def test_busca_por_id():

    fila = FilaPrioridade()

    chamado = criar_chamado_teste(
        3,
        "Pedro"
    )

    fila.adicionar_chamado(chamado)

    encontrado = fila.buscar_por_id(
        chamado.id
    )

    assert encontrado is not None
    assert encontrado.id == chamado.id
    assert encontrado.cliente == "Pedro"


def test_busca_por_id_inexistente():

    fila = FilaPrioridade()

    encontrado = fila.buscar_por_id(
        "id_inexistente"
    )

    assert encontrado is None


def test_cancelar_chamado():

    fila = FilaPrioridade()

    chamado = criar_chamado_teste(
        4,
        "João"
    )

    fila.adicionar_chamado(chamado)

    sucesso = fila.cancelar_chamado(
        chamado.id
    )

    assert sucesso is True
    assert fila.esta_vazia() is True


def test_cancelar_chamado_inexistente():

    fila = FilaPrioridade()

    sucesso = fila.cancelar_chamado(
        "id_inexistente"
    )

    assert sucesso is False


def test_carregar_chamado_preserva_ordem_chegada():

    fila = FilaPrioridade()

    chamado = criar_chamado_teste(
        3,
        cliente="Pedro",
        ordem_chegada=7,
    )

    fila.carregar_chamado(chamado)

    assert chamado.ordem_chegada == 7
    assert fila.contador == 7


def test_carregar_chamado_atualiza_contador():

    fila = FilaPrioridade()

    fila.carregar_chamado(
        criar_chamado_teste(
            2,
            ordem_chegada=5,
        )
    )

    fila.carregar_chamado(
        criar_chamado_teste(
            4,
            ordem_chegada=3,
        )
    )

    assert fila.contador == 5

    fila.adicionar_chamado(
        criar_chamado_teste(1)
    )

    assert fila.contador == 6


def test_fifo_apos_carregar_chamados():

    fila = FilaPrioridade()

    fila.carregar_chamado(
        criar_chamado_teste(
            3,
            cliente="Ana",
            ordem_chegada=1,
        )
    )

    fila.carregar_chamado(
        criar_chamado_teste(
            3,
            cliente="Bruno",
            ordem_chegada=2,
        )
    )

    primeiro = fila.atender_proximo()
    segundo = fila.atender_proximo()

    assert primeiro.cliente == "Ana"
    assert segundo.cliente == "Bruno"


def test_carregar_csv_legado_na_fila(
    csv_temporario,
):

    with open(
        csv_temporario,
        mode="w",
        newline="",
        encoding="utf-8",
    ) as arquivo:

        writer = csv.writer(arquivo)

        writer.writerow([
            "id",
            "cliente",
            "categoria",
            "severidade",
            "descricao",
            "prioridade",
            "criado_em",
        ])

        writer.writerow([
            "aaa11111",
            "Ana",
            "Suporte",
            3,
            "Problema A",
            -300,
            "2026-06-17 10:00:00",
        ])

        writer.writerow([
            "bbb22222",
            "Bruno",
            "Suporte",
            3,
            "Problema B",
            -300,
            "2026-06-17 10:01:00",
        ])

    fila = FilaPrioridade()

    for chamado in carregar_chamados():
        fila.carregar_chamado(chamado)

    primeiro = fila.atender_proximo()
    segundo = fila.atender_proximo()

    assert primeiro.cliente == "Ana"
    assert segundo.cliente == "Bruno"
    assert fila.contador == 2