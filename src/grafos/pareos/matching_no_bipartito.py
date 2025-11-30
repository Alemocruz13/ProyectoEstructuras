def matching_general(g):
    """
    Implementación compacta basada en Edmonds Blossom.
    g: grafo con vecinos(u)
    """
    from collections import deque

    # Construimos lista de aristas
    edges = []
    for u in range(g.n):
        for v in g.vecinos(u):
            if u < v:
                edges.append((u, v))

    # ---- Blossom Algorithm ----
    # Tomado de versión académica reducida (MIT)

    n = g.n
    match = [-1] * n
    base = list(range(n))
    p = [-1] * n
    q = deque()
    used = [False] * n
    blossom = [False] * n

    def lca(a, b):
        visited = [False] * n
        while True:
            a = base[a]
            visited[a] = True
            if match[a] == -1:
                break
            a = p[match[a]]
        while True:
            b = base[b]
            if visited[b]:
                return b
            b = p[match[b]]

    def mark_path(v, b, children):
        while base[v] != b:
            blossom[base[v]] = blossom[base[match[v]]] = True
            p[v] = children
            children = match[v]
            v = p[match[v]]

    def find_path(root):
        used[:] = [False]*n
        p[:] = [-1]*n
        q.clear()

        q.append(root)
        used[root] = True

        while q:
            v = q.popleft()
            for u in g.vecinos(v):
                if base[v] == base[u] or match[v] == u:
                    continue
                if u == root or (match[u] != -1 and p[match[u]] != -1):
                    cur = lca(v, u)
                    blossom[:] = [False]*n
                    mark_path(v, cur, u)
                    mark_path(u, cur, v)
                    for i in range(n):
                        if blossom[base[i]]:
                            base[i] = cur
                            if not used[i]:
                                used[i] = True
                                q.append(i)
                elif p[u] == -1:
                    p[u] = v
                    if match[u] == -1:
                        # aumentar matching
                        while u != -1:
                            v = p[u]
                            w = match[v]
                            match[v] = u
                            match[u] = v
                            u = w
                        return True
                    u2 = match[u]
                    used[u2] = True
                    q.append(u2)
        return False

    for i in range(n):
        if match[i] == -1:
            base = list(range(n))
            find_path(i)

    # convertir a conjunto de parejas
    result = set()
    for u in range(n):
        v = match[u]
        if u < v:
            result.add((u, v))

    return result


def matching_perfecto_general(matching, n):
    return len(matching) * 2 == n


def matching_maximal_general(g, matching):
    M = set(matching)
    matched_nodes = set()
    for u, v in M:
        matched_nodes.add(u)
        matched_nodes.add(v)

    for u in range(g.n):
        for v in g.vecinos(u):
            if u not in matched_nodes and v not in matched_nodes:
                return False
    return True
