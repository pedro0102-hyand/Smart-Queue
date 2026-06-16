from models.chamado import Chamado
from services.fila import FilaPrioridade
from services.persistence import (
    carregar_chamados,
    salvar_chamados
)


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
            severidade = int(input("Severidade (1-5): "))

            if 1 <= severidade <= 5:
                break

            print("❌ A severidade deve estar entre 1 e 5.")

        except ValueError:
            print("❌ Digite um número válido.")

    descricao = input("Descrição: ").strip()

    prioridade = calcular_prioridade(severidade)

    return Chamado(
        prioridade=prioridade,
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

    for i, chamado in enumerate(fila.listar_fila(), start=1):
        print(f"{i}. {chamado}")

    print(f"\nTotal de chamados: {fila.obter_tamanho_fila()}")


def atender_chamado(fila: FilaPrioridade) -> None:
    chamado = fila.atender_proximo()

    if chamado is None:
        print("\nNenhum chamado disponível.")
        return

    print("\n=== ATENDENDO CHAMADO ===")
    print(chamado)


def visualizar_proximo(fila: FilaPrioridade) -> None:
    proximo = fila.visualizar_proximo()

    if proximo is None:
        print("\nFila vazia.")
        return

    print("\n=== PRÓXIMO CHAMADO ===")
    print(proximo)


def menu() -> None:

    fila = FilaPrioridade()

    # Carrega chamados salvos
    chamados_salvos = carregar_chamados()

    for chamado in chamados_salvos:
        fila.adicionar_chamado(chamado)

    print(
        f"\n📂 {len(chamados_salvos)} chamado(s) carregado(s)."
    )

    while True:

        print("\n" + "=" * 30)
        print("         SMARTQUEUE")
        print("=" * 30)
        print("1 - Criar chamado")
        print("2 - Atender próximo")
        print("3 - Listar fila")
        print("4 - Ver próximo")
        print("5 - Quantidade de chamados")
        print("0 - Sair")

        opcao = input("\nEscolha: ").strip()

        match opcao:

            case "1":
                chamado = criar_chamado()
                fila.adicionar_chamado(chamado)

                print("\n✅ Chamado criado com sucesso!")

            case "2":
                atender_chamado(fila)

            case "3":
                exibir_fila(fila)

            case "4":
                visualizar_proximo(fila)

            case "5":
                print(
                    f"\nHá {fila.obter_tamanho_fila()} "
                    "chamado(s) na fila."
                )

            case "0":

                # Salva os chamados antes de sair
                salvar_chamados(
                    fila.obter_todos()
                )

                print("\n💾 Chamados salvos com sucesso!")
                print("Até logo! 👋")
                break

            case _:
                print("\n❌ Opção inválida.")


if __name__ == "__main__":
    menu()