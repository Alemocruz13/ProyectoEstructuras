def dfs(g, start):
    start_i = g.indice[start]
    visited = [False] * g.n
    recorrido = []

    def _dfs(u_i):
        visited[u_i] = True
        u = g.reverso[u_i]
        recorrido.append(u)

        for v in g.vecinos(u):
            if g.es_ponderado:
                v = v[0]

            v_i = g.indice[v]

            if not visited[v_i]:
                _dfs(v_i)

    _dfs(start_i)
    return recorrido
