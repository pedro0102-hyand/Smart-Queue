import heapq
from models.chamado import Chamado

def heapsort(chamados: list[Chamado]) -> list[Chamado]:

   heap = chamados.copy() # Cria uma cópia da lista original para não modificar a original

   heapq.heapify(heap) # Converte a lista em uma heap

   ordenados = [] # Lista para armazenar os chamados ordenados

   while heap:
       ordenados.append(heapq.heappop(heap))

   return ordenados

def top_chamados(
        chamados: list[Chamado],
        n: int = 5
) -> list[Chamado]:
    
    ordenados = heapsort(chamados)
    return ordenados[:n] # Retorna os n primeiros chamados da lista ordenada