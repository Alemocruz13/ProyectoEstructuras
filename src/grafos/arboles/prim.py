import heapq

def prim(g):
    """
    Prim compatible con el objeto Grafo.
    Requiere grafo no dirigido y ponderado.
    """

    if not g.es_ponderado:
        return {"error": "Prim requiere grafo ponderado"}

    n = g.n
    visitado = [False] * n

    # Iniciar desde el primer nodo
    start = g.nodos[0]
    start_i = g.indice[start]
    visitado[start_i] = True

    heap = []
    mst = []

    # Insertar aristas iniciales
    for v, w in g.vecinos(start):
        heapq.heappush(heap, (w, start_i, g.indice[v]))

    # Procesar
    while heap and len(mst) < n - 1:
        w, u_i, v_i = heapq.heappop(heap)

        if visitado[v_i]:
            continue

        visitado[v_i] = True
        mst.append((g.reverso[u_i], g.reverso[v_i], w))

        for nxt, peso in g.vecinos(g.reverso[v_i]):
            nxt_i = g.indice[nxt]
            if not visitado[nxt_i]:
                heapq.heappush(heap, (peso, v_i, nxt_i))

    return mst
