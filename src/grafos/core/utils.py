def vecinos_nodos(g, u):
    for item in g.vecinos(u):
        if getattr(g, "es_ponderado", False):
            yield item[0]
        else:
            yield item
