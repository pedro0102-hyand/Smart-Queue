from models.chamado import Chamado
import heapq


class FilaPrioridade:

    def __init__(self):
        """Inicializa a fila de prioridade vazia."""
        self.heap = []

    def adicionar_chamado(self, chamado: Chamado) -> None:
        """
        Adiciona um chamado à fila.
        
        Args:
            chamado: Objeto Chamado a ser adicionado.
        """
        heapq.heappush(self.heap, chamado)
    
    def atender_proximo(self) -> Chamado | None:
        """
        Remove e retorna o chamado de maior prioridade.
        
        Returns:
            Chamado de maior prioridade ou None se fila vazia.
        """
        if not self.heap:
            return None
        
        return heapq.heappop(self.heap)
    
    def listar_fila(self) -> list[Chamado]:
        """
        Retorna lista de chamados ordenada por prioridade.
        
        Returns:
            Lista de chamados ordenada (maior prioridade primeiro).
        """
        return sorted(self.heap)
    
    def obter_tamanho_fila(self) -> int:
        """Retorna quantidade de chamados na fila."""
        return len(self.heap)
    
    def esta_vazia(self) -> bool:
        """Verifica se a fila está vazia."""
        return len(self.heap) == 0
    
    def visualizar_proximo(self) -> Chamado | None:
        """
        Retorna o próximo chamado sem remover da fila.
        
        Returns:
            Próximo chamado (maior prioridade) ou None se fila vazia.
        """
        if not self.heap:
            return None
        
        return self.heap[0]
    
    def obter_todos(self) -> list[Chamado]:
        """Retorna cópia de todos os chamados (sem ordenação de heap)."""
        return self.heap.copy()