def dfs(g, start):
    visited = [False] * g.n
    recorrido = []

    def _dfs(u):
        visited[u] = True
        recorrido.append(u)

        for v in g.vecinos(u):
            # Si el grafo es ponderado, v es una tupla (nodo, peso)
            if g.es_ponderado:
                v = v[0]

            if not visited[v]:
                _dfs(v)

    _dfs(start)
    return recorrido
