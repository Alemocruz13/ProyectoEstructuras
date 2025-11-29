def edge_count(g):
    c = 0
    for u in range(g.n):
        c += len(list(g.vecinos(u)))

    if g.es_dirigido:
        return c
    else:
        return c // 2


def edges_equal_n_minus_1(g):
    return edge_count(g) == max(0, g.n - 1)
