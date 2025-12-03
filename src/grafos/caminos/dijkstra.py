# caminos/dijkstra.py

import heapq
import math

def dijkstra(g, inicio=0):
    """
    Implementación universal de Dijkstra usando solo:
      - g.n
      - g.vecinos(u)
      - g.es_ponderado
    """

    n = g.n
    dist = [math.inf] * n
    dist[inicio] = 0

    pq = [(0, inicio)]  # (distancia, nodo)

    while pq:
        d, u = heapq.heappop(pq)

        if d > dist[u]:
            continue

        for item in g.vecinos(u):
            if g.es_ponderado:
                v, peso = item
            else:
                v = item
                peso = 1

            nueva = d + peso

            if nueva < dist[v]:
                dist[v] = nueva
                heapq.heappush(pq, (nueva, v))

    # devolver dict SOLO para que la interfaz muestre algo bonito
    return {i: dist[i] for i in range(n)}
