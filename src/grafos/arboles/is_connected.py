from collections import deque

def is_connected(g):
    """ Verifica si un grafo (dirigido o no) es fuertemente o débilmente conectado. """

    if g.n == 0:
        return True

    # Si es no dirigido, basta con 1 BFS
    if not g.es_dirigido:
        return bfs_check(g, 0)

    # Si es dirigido: verificar conectividad débil
    # 1) grafo original
    if not bfs_check(g, 0):
        return False

    # 2) grafo con aristas invertidas
    gr = reverse_graph(g)
    return bfs_check(gr, 0)


def bfs_check(g, start):
    visited = [False] * g.n
    q = deque([start])
    visited[start] = True

    while q:
        u = q.popleft()

        for v in g.vecinos(u):

            # Si es ponderado, v = (nodo, peso)
            if g.es_ponderado:
                v = v[0]

            if not visited[v]:
                visited[v] = True
                q.append(v)

    return all(visited)


def reverse_graph(g):
    """ Regresa un grafo con todas las aristas invertidas. """
    from representacion.lista_ady import ListaAdyacencia
    from representacion.matriz_ady import MatrizAdyacencia
    from representacion.matriz_inc import MatrizIncidencia

    # Crear un grafo nuevo del mismo tipo
    if isinstance(g, ListaAdyacencia):
        gr = ListaAdyacencia(g.n, dirigido=True, ponderado=g.es_ponderado)
    elif isinstance(g, MatrizAdyacencia):
        gr = MatrizAdyacencia(g.n, dirigido=True, ponderado=g.es_ponderado)
    elif isinstance(g, MatrizIncidencia):
        gr = MatrizIncidencia(g.n, dirigido=True, ponderado=g.es_ponderado)
    else:
        raise ValueError("Tipo de grafo no soportado.")

    # Invertir aristas
    for u in range(g.n):
        for v in g.vecinos(u):

            # extraer nodo real si es ponderado
            if g.es_ponderado:
                nodo = v[0]
                peso = v[1]
                gr.add_edge(nodo, u, peso=peso)
            else:
                gr.add_edge(v, u)

    return gr