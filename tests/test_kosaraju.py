from src.grafos.componentesconexos.kosaraju import kosaraju

class GrafoMock:
    def __init__(self, g):
        self.g = g
        self.nodos = list(g.keys())
        self.n = len(g)
        self.es_ponderado = False
        self.es_dirigido = True

    def vecinos(self, u):
        return self.g[u]


def test_kosaraju_scc():
    g = {
        0: [1],
        1: [2],
        2: [0],
        3: [4],
        4: []
    }

    G = GrafoMock(g)
    scc = kosaraju(G)

    scc_sets = [set(c) for c in scc]

    assert {0, 1, 2} in scc_sets
    assert {3} in scc_sets
    assert {4} in scc_sets
