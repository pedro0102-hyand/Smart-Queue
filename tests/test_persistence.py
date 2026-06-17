import csv

from services.persistence import (
    carregar_chamados,
    salvar_chamados,
)
from tests.conftest import criar_chamado_teste


def test_carregar_arquivo_inexistente(
    csv_temporario,
):

    chamados = carregar_chamados()

    assert chamados == []


def test_salvar_chamados_cria_csv_com_colunas(
    csv_temporario,
):

    chamado = criar_chamado_teste(
        4,
        cliente="Maria",
        ordem_chegada=1,
        id_chamado="abc12345",
    )

    salvar_chamados([chamado])

    with open(
        csv_temporario,
        mode="r",
        encoding="utf-8",
    ) as arquivo:

        reader = csv.DictReader(arquivo)

        assert reader.fieldnames == [
            "id",
            "cliente",
            "categoria",
            "severidade",
            "descricao",
            "prioridade",
            "ordem_chegada",
            "criado_em",
        ]

        linha = next(reader)

        assert linha["id"] == "abc12345"
        assert linha["cliente"] == "Maria"
        assert linha["severidade"] == "4"
        assert linha["prioridade"] == "-400"
        assert linha["ordem_chegada"] == "1"


def test_round_trip_preserva_dados(
    csv_temporario,
):

    original = [
        criar_chamado_teste(
            5,
            cliente="Alta",
            ordem_chegada=1,
            id_chamado="id000001",
        ),
        criar_chamado_teste(
            2,
            cliente="Baixa",
            ordem_chegada=2,
            id_chamado="id000002",
        ),
    ]

    salvar_chamados(original)
    carregados = carregar_chamados()

    assert len(carregados) == 2

    assert carregados[0].id == "id000001"
    assert carregados[0].cliente == "Alta"
    assert carregados[0].severidade == 5
    assert carregados[0].prioridade == -500
    assert carregados[0].ordem_chegada == 1
    assert carregados[0].criado_em == "2026-06-17 10:00:00"

    assert carregados[1].id == "id000002"
    assert carregados[1].cliente == "Baixa"
    assert carregados[1].ordem_chegada == 2


def test_carregar_csv_com_coluna_ordem_chegada(
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
            "ordem_chegada",
            "criado_em",
        ])

        writer.writerow([
            "aaa11111",
            "Ana",
            "Suporte",
            3,
            "Problema A",
            -300,
            10,
            "2026-06-17 10:00:00",
        ])

        writer.writerow([
            "bbb22222",
            "Bruno",
            "Suporte",
            3,
            "Problema B",
            -300,
            20,
            "2026-06-17 10:01:00",
        ])

    chamados = carregar_chamados()

    assert chamados[0].ordem_chegada == 10
    assert chamados[1].ordem_chegada == 20


def test_carregar_csv_sem_coluna_ordem_chegada(
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

    chamados = carregar_chamados()

    assert len(chamados) == 2
    assert chamados[0].ordem_chegada == 1
    assert chamados[1].ordem_chegada == 2
