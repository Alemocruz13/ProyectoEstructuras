from recorridos.dfs import dfs

def has_cycle(g):
    visited = [False] * g.n
    stack = [False] * g.n

    # -----------------------------
    # Caso 1: Grafo dirigido
    # -----------------------------
    def dfs_dir(u):
        visited[u] = True
        stack[u] = True

        for v in g.vecinos(u):
            if not visited[v]:
                if dfs_dir(v):
                    return True
            elif stack[v]:
                return True

        stack[u] = False
        return False

    # -----------------------------
    # Caso 2: Grafo NO dirigido
    # -----------------------------
    def dfs_undir(u, parent):
        visited[u] = True

        for v in g.vecinos(u):
            if not visited[v]:
                if dfs_undir(v, u):
                    return True
            elif v != parent:
                return True

        return False

    if g.es_dirigido:
        for i in range(g.n):
            if not visited[i]:
                if dfs_dir(i):
                    return True
        return False
    
    else:
        for i in range(g.n):
            if not visited[i]:
                if dfs_undir(i, -1):
                    return True
        return False
