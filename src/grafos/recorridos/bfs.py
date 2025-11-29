from collections import deque

def bfs(g, start):
    visited = [False] * g.n
    orden = []                # lista de nodos en orden de visita
    q = deque([start])
    visited[start] = True

    while q:
        u = q.popleft()
        orden.append(u)

        for v in g.vecinos(u):
            if not visited[v]:
                visited[v] = True
                q.append(v)
    
    return orden
