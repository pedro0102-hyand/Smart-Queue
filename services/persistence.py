import os
import csv

from models.chamado import Chamado


ARQUIVO_CSV = "data/chamados.csv"


def salvar_chamados(
    chamados: list[Chamado]
) -> None:

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(
        ARQUIVO_CSV,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        writer = csv.writer(
            arquivo
        )

        writer.writerow([
            "id",
            "cliente",
            "categoria",
            "severidade",
            "descricao",
            "prioridade",
            "ordem_chegada",
            "criado_em"
        ])

        for chamado in chamados:

            writer.writerow([
                chamado.id,
                chamado.cliente,
                chamado.categoria,
                chamado.severidade,
                chamado.descricao,
                chamado.prioridade,
                chamado.ordem_chegada,
                chamado.criado_em
            ])


def carregar_chamados() -> list[Chamado]:

    chamados = []

    if not os.path.exists(
        ARQUIVO_CSV
    ):
        return chamados

    with open(
        ARQUIVO_CSV,
        mode="r",
        encoding="utf-8"
    ) as arquivo:

        reader = csv.DictReader(
            arquivo
        )

        tem_ordem_chegada = (
            reader.fieldnames is not None
            and "ordem_chegada" in reader.fieldnames
        )

        for indice, linha in enumerate(
            reader,
            start=1
        ):

            if tem_ordem_chegada:
                valor = linha.get(
                    "ordem_chegada",
                    ""
                ).strip()
                ordem_chegada = (
                    int(valor)
                    if valor
                    else indice
                )
            else:
                ordem_chegada = indice

            chamado = Chamado(
                prioridade=int(
                    linha["prioridade"]
                ),

                ordem_chegada=ordem_chegada,

                id=linha["id"],

                cliente=linha[
                    "cliente"
                ],

                categoria=linha[
                    "categoria"
                ],

                severidade=int(
                    linha["severidade"]
                ),

                descricao=linha[
                    "descricao"
                ],

                criado_em=linha[
                    "criado_em"
                ]
            )

            chamados.append(
                chamado
            )

    return chamados

