from models.chamado import Chamado
from services.fila import FilaPrioridade
from services.persistence import (
    carregar_chamados,
    salvar_chamados
)
from services.reports import top_chamados


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


def salvar_estado(
    fila: FilaPrioridade
) -> None:

    salvar_chamados(
        fila.obter_todos()
    )


def menu() -> None:

    fila = FilaPrioridade()

    chamados_salvos = carregar_chamados()

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
        print("0 - Sair")

        opcao = input(
            "\nEscolha: "
        ).strip()

        match opcao:

            case "1":

                chamado = criar_chamado()

                fila.adicionar_chamado(
                    chamado
                )

                salvar_estado(fila)

                print(
                    "\n✅ Chamado criado "
                    "com sucesso!"
                )

            case "2":

                atender_chamado(
                    fila
                )

                salvar_estado(
                    fila
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


if __name__ == "__main__":
    menu()