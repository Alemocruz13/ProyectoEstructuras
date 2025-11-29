def dfs(grafo, inicio):
    visitados = [False] * grafo.n
    orden = []

    def dfs_rec(u):
        visitados[u] = True
        orden.append(u)

        for v in grafo.vecinos(u):
            if not visitados[v]:
                dfs_rec(v)

    dfs_rec(inicio)
    return orden
