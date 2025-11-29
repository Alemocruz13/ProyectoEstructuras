def dfs(g, start):
    visited = [False] * g.n
    orden = []

    def _dfs(u):
        visited[u] = True
        orden.append(u)

        for v in g.vecinos(u):
            if not visited[v]:
                _dfs(v)

    _dfs(start)
    return orden
