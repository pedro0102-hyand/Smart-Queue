from models.chamado import Chamado
from services.fila import FilaPrioridade
from services.logger import get_logger
from services.persistence import (
    carregar_chamados,
    salvar_chamados
)
from services.reports import (
    calcular_estatisticas,
    top_chamados,
)

logger = get_logger()


def calcular_prioridade(severidade: int) -> int:
    """
    Calcula a prioridade do chamado.

    Como o heapq implementa uma Min Heap,
    utilizamos valores negativos para simular
    uma Max Heap.
    """
    return -(severidade * 100)


def criar_chamado() -> Chamado:
    print("\n=== NOVO CHAMADO ===")

    cliente = input("Cliente: ").strip()
    categoria = input("Categoria: ").strip()

    while True:
        try:
            severidade = int(
                input("Severidade (1-5): ")
            )

            if 1 <= severidade <= 5:
                break

            print("❌ A severidade deve estar entre 1 e 5.")

        except ValueError:
            print("❌ Digite um número válido.")

    descricao = input("Descrição: ").strip()

    prioridade = calcular_prioridade(severidade)

    return Chamado(
        prioridade=prioridade,
        ordem_chegada=0,  # Será definido na fila
        cliente=cliente,
        categoria=categoria,
        severidade=severidade,
        descricao=descricao
    )


def exibir_fila(fila: FilaPrioridade) -> None:
    print("\n=== FILA DE CHAMADOS ===")

    if fila.esta_vazia():
        print("Nenhum chamado na fila.")
        return

    for i, chamado in enumerate(
        fila.listar_fila(),
        start=1
    ):
        print(f"{i}. {chamado}")

    print(
        f"\nTotal de chamados: "
        f"{fila.obter_tamanho_fila()}"
    )


def atender_chamado(
    fila: FilaPrioridade
) -> None:

    chamado = fila.atender_proximo()

    if chamado is None:
        print("\nNenhum chamado disponível.")
        return

    print("\n=== ATENDENDO CHAMADO ===")
    print(chamado)

    logger.info(
        "Chamado atendido: id=%s, cliente=%s",
        chamado.id,
        chamado.cliente,
    )


def visualizar_proximo(
    fila: FilaPrioridade
) -> None:

    proximo = fila.visualizar_proximo()

    if proximo is None:
        print("\nFila vazia.")
        return

    print("\n=== PRÓXIMO CHAMADO ===")
    print(proximo)


def exibir_top_chamados(
    fila: FilaPrioridade
) -> None:

    top = top_chamados(
        fila.obter_todos(),
        n=5
    )

    if not top:
        print("\nNenhum chamado na fila.")
        return

    print("\n=== TOP 5 CHAMADOS ===")

    for i, chamado in enumerate(
        top,
        start=1
    ):
        print(f"{i}. {chamado}")


def exibir_estatisticas(
    fila: FilaPrioridade,
) -> None:

    stats = calcular_estatisticas(
        fila.obter_todos()
    )

    print("\n=== ESTATÍSTICAS ===")
    print(
        f"Total de chamados: "
        f"{stats['total']}"
    )

    if stats["total"] == 0:
        print("Média de severidade: —")
        print("\nQuantidade por categoria:")
        print("  Nenhum chamado na fila.")
        return

    print(
        f"Média de severidade: "
        f"{stats['media_severidade']:.2f}"
    )

    print("\nQuantidade por categoria:")

    for categoria, quantidade in sorted(
        stats["por_categoria"].items()
    ):
        print(
            f"  {categoria}: "
            f"{quantidade}"
        )


def salvar_estado(
    fila: FilaPrioridade
) -> None:

    try:
        salvar_chamados(
            fila.obter_todos()
        )
    except OSError as erro:
        logger.error(
            "Erro ao salvar chamados: %s",
            erro,
        )
        print(
            "\n❌ Erro ao salvar os chamados."
        )


def menu() -> None:

    fila = FilaPrioridade()

    try:
        chamados_salvos = carregar_chamados()
    except (OSError, ValueError, KeyError) as erro:
        logger.error(
            "Erro ao carregar chamados: %s",
            erro,
        )
        chamados_salvos = []
        print(
            "\n❌ Erro ao carregar chamados salvos."
        )

    for chamado in chamados_salvos:
        fila.carregar_chamado(chamado)

    print(
        f"\n📂 {len(chamados_salvos)} "
        "chamado(s) carregado(s)."
    )

    while True:

        print("\n" + "=" * 35)
        print("         SMARTQUEUE")
        print("=" * 35)
        print("1 - Criar chamado")
        print("2 - Atender próximo")
        print("3 - Listar fila")
        print("4 - Ver próximo")
        print("5 - Quantidade de chamados")
        print("6 - Top chamados críticos")
        print("7 - Buscar chamado por ID")
        print("8 - Cancelar chamado")
        print("9 - Estatísticas")
        print("0 - Sair")

        opcao = input(
            "\nEscolha: "
        ).strip()

        match opcao:

            case "1":

                try:
                    chamado = criar_chamado()

                    fila.adicionar_chamado(
                        chamado
                    )

                    salvar_estado(fila)

                    logger.info(
                        "Chamado criado: id=%s, "
                        "cliente=%s",
                        chamado.id,
                        chamado.cliente,
                    )

                    print(
                        "\n✅ Chamado criado "
                        "com sucesso!"
                    )
                except Exception as erro:
                    logger.error(
                        "Erro ao criar chamado: %s",
                        erro,
                    )
                    print(
                        "\n❌ Erro ao criar chamado."
                    )

            case "2":

                try:
                    atender_chamado(
                        fila
                    )

                    salvar_estado(
                        fila
                    )
                except Exception as erro:
                    logger.error(
                        "Erro ao atender chamado: %s",
                        erro,
                    )
                    print(
                        "\n❌ Erro ao atender chamado."
                    )

            case "3":

                exibir_fila(
                    fila
                )

            case "4":

                visualizar_proximo(
                    fila
                )

            case "5":

                print(
                    f"\nHá "
                    f"{fila.obter_tamanho_fila()} "
                    f"chamado(s) na fila."
                )

            case "6":

                exibir_top_chamados(
                    fila
                )
            
            case "7":

                buscar_chamado(
                    fila
                )

            case "8":

                cancelar_chamado(
                    fila
                )

            case "9":

                exibir_estatisticas(
                    fila
                )

            case "0":

                salvar_estado(
                    fila
                )

                print(
                    "\n💾 Chamados "
                    "salvos com sucesso!"
                )

                print(
                    "Até logo! 👋"
                )

                break

            case _:

                print(
                    "\n❌ Opção inválida."
                )

def buscar_chamado(
    fila: FilaPrioridade
) -> None:

    id_chamado = input(
        "\nDigite o ID do chamado: "
    ).strip()

    chamado = fila.buscar_por_id(
        id_chamado
    )

    if chamado is None:
        print(
            "\n❌ Chamado não encontrado."
        )
        return

    print("\n=== CHAMADO ENCONTRADO ===")

    print(
        f"ID: {chamado.id}"
    )

    print(
        f"Cliente: {chamado.cliente}"
    )

    print(
        f"Categoria: {chamado.categoria}"
    )

    print(
        f"Severidade: "
        f"{chamado.severidade}"
    )

    print(
        f"Descrição: "
        f"{chamado.descricao}"
    )

    print(
        f"Criado em: "
        f"{chamado.criado_em}"
    )

def cancelar_chamado(
    fila: FilaPrioridade
) -> None:

    id_chamado = input(
        "\nDigite o ID do chamado: "
    ).strip()

    sucesso = fila.cancelar_chamado(
        id_chamado
    )

    if sucesso:

        salvar_estado(
            fila
        )

        print(
            "\n✅ Chamado cancelado "
            "com sucesso!"
        )

    else:

        print(
            "\n❌ Chamado não encontrado."
        )


if __name__ == "__main__":
    menu()