from collections import deque

INF = 10**9

def hopcroft_karp(g, U, V):
    pairU = {u: None for u in U}
    pairV = {v: None for v in V}
    dist = {}

    def bfs():
        cola = deque()
        for u in U:
            if pairU[u] is None:
                dist[u] = 0
                cola.append(u)
            else:
                dist[u] = INF

        found = False
        while cola:
            u = cola.popleft()
            for v in g.vecinos(u):
                if v in V:
                    if pairV[v] is None:
                        found = True
                    else:
                        u2 = pairV[v]
                        if dist.get(u2, INF) == INF:
                            dist[u2] = dist[u] + 1
                            cola.append(u2)
        return found

    def dfs(u):
        for v in g.vecinos(u):
            if v in V:
                if pairV[v] is None or (
                    dist.get(pairV[v], INF) == dist[u] + 1 and dfs(pairV[v])
                ):
                    pairU[u] = v
                    pairV[v] = u
                    return True
        dist[u] = INF
        return False

    matching = 0
    while bfs():
        for u in U:
            if pairU[u] is None and dfs(u):
                matching += 1

    return matching, pairU, pairV
