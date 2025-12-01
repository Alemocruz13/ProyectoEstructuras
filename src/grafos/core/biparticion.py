from collections import deque

def detectar_biparticion(g):
    color = {}
    for start in range(g.n):
        if start not in color:
            color[start] = 0
            q = deque([start])

            while q:
                u = q.popleft()
                for v in g.vecinos(u):
                    if v not in color:
                        color[v] = 1 - color[u]
                        q.append(v)
                    else:
                        if color[v] == color[u]:
                            return None, None, False

    U = [n for n, c in color.items() if c == 0]
    V = [n for n, c in color.items() if c == 1]
    return U, V, True
