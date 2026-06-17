import csv

from services.persistence import carregar_chamados


def test_carregar_csv_sem_coluna_ordem_chegada(
    monkeypatch,
    tmp_path,
):

    csv_path = tmp_path / "chamados.csv"

    with open(
        csv_path,
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

    monkeypatch.setattr(
        "services.persistence.ARQUIVO_CSV",
        str(csv_path),
    )

    chamados = carregar_chamados()

    assert len(chamados) == 2
    assert chamados[0].ordem_chegada == 1
    assert chamados[1].ordem_chegada == 2
