def has_cycle(g):
    """Detecta ciclos en grafos dirigidos y no dirigidos, ponderados o no."""

    visited = [False] * g.n
    parent = [-1] * g.n

    # -----------------------------
    # CICLOS EN GRAFO NO DIRIGIDO
    # -----------------------------
    def dfs_undir(u):
        visited[u] = True

        for v in g.vecinos(u):

            # Si es ponderado, v es (nodo, peso)
            if g.es_ponderado:
                v = v[0]

            if not visited[v]:
                parent[v] = u
                if dfs_undir(v):
                    return True

            # Si ya está visitado y no es el padre, hay ciclo
            elif parent[u] != v:
                return True

        return False

    # -----------------------------
    # CICLOS EN GRAFO DIRIGIDO
    # -----------------------------
    in_stack = [False] * g.n

    def dfs_dir(u):
        visited[u] = True
        in_stack[u] = True

        for v in g.vecinos(u):

            # Extraer nodo si es ponderado
            if g.es_ponderado:
                v = v[0]

            if not visited[v]:
                if dfs_dir(v):
                    return True

            elif in_stack[v]:
                return True  # ciclo dirigido encontrado

        in_stack[u] = False
        return False

    # -----------------------------
    # EJECUTAR CORRESPONDIENTE
    # -----------------------------
    if g.es_dirigido:
        for i in range(g.n):
            if not visited[i] and dfs_dir(i):
                return True
    else:
        for i in range(g.n):
            if not visited[i] and dfs_undir(i):
                return True

    return False
