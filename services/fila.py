from models.chamado import Chamado
import heapq

class FilaPrioridade :

    def __init__(self):

        self.heap = [] # Lista para armazenar os chamados como uma heap

    def adicionar_chamado(self, chamado: Chamado)-> None:

        heapq.heappush(self.heap, chamado) # Adiciona o chamado à heap
    
    def atender_proximo(self) -> Chamado|None:

        if not self.heap:
            raise Exception("Não há chamados para atender.")
        
        return heapq.heappop(self.heap) # Remove e retorna o chamado de maior prioridade (menor valor)
    
    def listar_fila(self) -> list[Chamado]:

        return sorted(self.heap) # Retorna a lista de chamados ordenada por prioridade (menor valor primeiro)
    
    def obter_tamanho_fila(self) -> int:

        return len(self.heap) # Retorna o número de chamados na fila
    
    def esta_vazia(self) -> bool:

        return len(self.heap) == 0 
    
    def visualizar_proximo(self) -> Chamado|None:

        if not self.heap:
            raise Exception("Não há chamados para visualizar.")
        
        return self.heap[0] # Retorna o chamado de maior prioridade (menor valor) sem removê-lo da fila
    
    