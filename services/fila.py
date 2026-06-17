from models.chamado import Chamado
import heapq


class FilaPrioridade:

    def __init__(self):
        """
        Inicializa a fila de prioridade vazia.
        """
        self.heap = []
        self.contador = 0  # Controla ordem de chegada

    def adicionar_chamado(self, chamado: Chamado) -> None:
        """
        Adiciona um chamado à fila.

        Se dois chamados tiverem a mesma prioridade,
        o mais antigo é atendido primeiro (FIFO).

        Args:
            chamado: Objeto Chamado.
        """

        self.contador += 1

        # Define ordem de chegada
        chamado.ordem_chegada = self.contador

        heapq.heappush(self.heap, chamado)

    def carregar_chamado(self, chamado: Chamado) -> None:
        """
        Carrega um chamado vindo do CSV sem alterar
        sua ordem original.

        Args:
            chamado: Objeto Chamado carregado.
        """

        heapq.heappush(self.heap, chamado)

        # Atualiza contador para continuar sequência
        self.contador = max(
            self.contador,
            chamado.ordem_chegada
        )

    def atender_proximo(self) -> Chamado | None:
        """
        Remove e retorna o chamado de maior prioridade.

        Returns:
            Chamado ou None se a fila estiver vazia.
        """

        if self.esta_vazia():
            return None

        return heapq.heappop(self.heap)

    def listar_fila(self) -> list[Chamado]:
        """
        Retorna os chamados ordenados por prioridade.

        Não altera a Heap original.

        Returns:
            Lista ordenada.
        """

        return sorted(self.heap)

    def obter_tamanho_fila(self) -> int:
        """
        Retorna a quantidade de chamados.
        """

        return len(self.heap)

    def esta_vazia(self) -> bool:
        """
        Verifica se a fila está vazia.
        """

        return len(self.heap) == 0

    def visualizar_proximo(self) -> Chamado | None:
        """
        Retorna o próximo chamado sem removê-lo.

        Returns:
            Chamado ou None se fila vazia.
        """

        if self.esta_vazia():
            return None

        return self.heap[0]

    def obter_todos(self) -> list[Chamado]:
        """
        Retorna cópia de todos os chamados.

        Returns:
            Lista com todos os chamados.
        """

        return self.heap.copy()