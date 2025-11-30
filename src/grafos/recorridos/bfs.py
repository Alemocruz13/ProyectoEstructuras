from collections import deque

def bfs(g, start):
    visited = [False] * g.n
    q = deque([start])
    visited[start] = True

    recorrido = []

    while q:
        u = q.popleft()
        recorrido.append(u)

        for v in g.vecinos(u):
            if g.es_ponderado:
                v = v[0]

            if not visited[v]:
                visited[v] = True
                q.append(v)

    return recorrido
