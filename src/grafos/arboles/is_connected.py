from recorridos.bfs import bfs

def is_connected(g):
    if g.n == 0:
        return True

    # Verificar ida (del nodo 0 hacia todos)
    visitados = bfs(g, 0)
    if len(visitados) != g.n:
        return False

    # Si es no dirigido, ahí acaba
    if not g.es_dirigido:
        return True

    # Si es dirigido → verificar conectividad al invertir aristas
    gr = reverse_graph(g)
    visitados_rev = bfs(gr, 0)

    return len(visitados_rev) == g.n


def reverse_graph(g):
    """Construye un grafo con todas las aristas invertidas."""
    from representacion.lista_ady import ListaAdyacencia
    gr = ListaAdyacencia(g.n, dirigido=True)

    for u in range(g.n):
        for v in g.vecinos(u):
            gr.add_edge(v, u)
    return gr
