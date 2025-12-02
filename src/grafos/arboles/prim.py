import heapq

def prim(num_vertices, edges, dirigidos=False, ponderado=True):
    """
    Algoritmo de Prim generalizado.
    Acepta grafos dirigidos/no dirigidos, ponderados/no ponderados.
    Siempre construye un grafo NO dirigido para que Prim funcione.
    """

    # Construcción del grafo
    graph = [[] for _ in range(num_vertices)]

    for edge in edges:
        if ponderado:
            u, v, w = edge
        else:
            u, v = edge
            w = 1  # Peso por defecto

        # Siempre agregamos ambas direcciones (Prim requiere grafo no dirigido)
        graph[u].append((v, w))
        graph[v].append((u, w))

    # Estructuras necesarias
    visitado = [False] * num_vertices
    heap = []

    # Iniciar desde el vértice 0
    visitado[0] = True
    for v, w in graph[0]:
        heapq.heappush(heap, (w, 0, v))

    mst = []

    # Algoritmo de Prim
    while heap and len(mst) < num_vertices - 1:
        w, u, v = heapq.heappop(heap)

        if visitado[v]:
            continue

        visitado[v] = True
        mst.append((u, v, w))

        for nxt, peso in graph[v]:
            if not visitado[nxt]:
                heapq.heappush(heap, (peso, v, nxt))

    return mst


# Ejemplo de uso
if __name__ == "__main__":
    num_vertices = 5
    edges = [
        (0, 1, 2),
        (0, 3, 6),
        (1, 3, 8),
        (1, 2, 3),
        (1, 4, 5),
        (2, 4, 7)
    ]
    
    resultado = prim(num_vertices, edges, dirigidos=False, ponderado=True)
    print("MST:", resultado)
    