from collections import deque

def bfs(g, start):
    # Convertimos el nodo real a índice interno
    start_i = g.indice[start]

    visited = [False] * g.n
    q = deque([start_i])
    visited[start_i] = True

    recorrido = []

    while q:
        u_i = q.popleft()
        u = g.reverso[u_i]   # convertimos índice → nodo
        recorrido.append(u)

        for v in g.vecinos(u):
            if g.es_ponderado:
                v = v[0]  # extraemos solo el nodo

            v_i = g.indice[v]

            if not visited[v_i]:
                visited[v_i] = True
                q.append(v_i)

    return recorrido
