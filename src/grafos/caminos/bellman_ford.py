# caminos/bellman_ford.py

import math

def bellman_ford(g, inicio=0):
    """
    Bellman-Ford universal basado solo en:
      - g.n
      - g.vecinos(u)
      - g.es_ponderado
    """

    n = g.n
    dist = [math.inf] * n
    dist[inicio] = 0

    # Relajar n-1 veces
    for _ in range(n - 1):
        cambio = False
        for u in range(n):
            for item in g.vecinos(u):

                if g.es_ponderado:
                    v, peso = item
                else:
                    v = item
                    peso = 1

                if dist[u] != math.inf and dist[u] + peso < dist[v]:
                    dist[v] = dist[u] + peso
                    cambio = True

        if not cambio:
            break

    # Detectar ciclo negativo
    for u in range(n):
        for item in g.vecinos(u):

            if g.es_ponderado:
                v, peso = item
            else:
                v = item
                peso = 1

            if dist[u] != math.inf and dist[u] + peso < dist[v]:
                return {"error": "Ciclo negativo detectado."}

    return {i: dist[i] for i in range(n)}
