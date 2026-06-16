from models.chamado import Chamado
from services.fila import FilaPrioridade


def calcular_prioridade(severidade: int) -> int:

    return -(severidade * 100)


def criar_chamado() -> Chamado:

    print("\n=== Novo Chamado ===")

    cliente = input("Cliente: ")
    categoria = input("Categoria: ")

    while True:
        
        try:
            severidade = int(
                input("Severidade (1-5): ")
            )

            if 1 <= severidade <= 5:
                break

            print("A severidade deve estar entre 1 e 5.")

        except ValueError:
            print("Digite um número válido.")

    descricao = input("Descrição: ")

    prioridade = calcular_prioridade(severidade)

    return Chamado(
        prioridade=prioridade,
        cliente=cliente,
        categoria=categoria,
        severidade=severidade,
        descricao=descricao
    )


def exibir_fila(fila: FilaPrioridade):

    print("\n=== FILA DE CHAMADOS ===")

    if fila.esta_vazia():

        print("Nenhum chamado na fila.")
        return

    for chamado in fila.listar_fila():

        print(chamado)


def atender_chamado(fila: FilaPrioridade):

    chamado = fila.atender_proximo()

    if chamado is None:
        print("\nNenhum chamado disponível.")
        return

    print("\n=== ATENDENDO ===")
    print(chamado)


def menu():
    
    fila = FilaPrioridade()

    while True:

        print("\n===== SMARTQUEUE =====")
        print("1 - Criar chamado")
        print("2 - Atender próximo")
        print("3 - Listar fila")
        print("4 - Ver próximo")
        print("0 - Sair")

        opcao = input("\nEscolha: ")

        match opcao:

            case "1":
                chamado = criar_chamado()
                fila.adicionar_chamado(chamado)
                print("\nChamado criado com sucesso!")

            case "2":
                atender_chamado(fila)

            case "3":
                exibir_fila(fila)

            case "4":
                proximo = fila.visualizar_proximo()

                if proximo:
                    print("\nPróximo chamado:")
                    print(proximo)
                else:
                    print("\nFila vazia.")

            case "0":
                print("\nEncerrando sistema...")
                break

            case _:
                print("\nOpção inválida.")


if __name__ == "__main__":
    menu()