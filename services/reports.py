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


def calcular_estatisticas(
    chamados: list[Chamado],
) -> dict:

    total = len(chamados)

    if total == 0:
        return {
            "total": 0,
            "media_severidade": 0.0,
            "por_categoria": {},
        }

    media_severidade = (
        sum(
            chamado.severidade
            for chamado in chamados
        )
        / total
    )

    por_categoria: dict[str, int] = {}

    for chamado in chamados:
        por_categoria[chamado.categoria] = (
            por_categoria.get(
                chamado.categoria,
                0,
            )
            + 1
        )

    return {
        "total": total,
        "media_severidade": media_severidade,
        "por_categoria": por_categoria,
    }