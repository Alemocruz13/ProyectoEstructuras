from src.grafos.arboles.prim import prim

class GrafoMock:
    def __init__(self, g):
        self.g = g
        self.n = len(g)
        self.nodos = list(g.keys())
        self.es_ponderado = True
        self.es_dirigido = False

        # Requerido por prim()
        self.indice = {i: i for i in self.nodos}
        self.reverso = {i: i for i in self.nodos}

    def vecinos(self, u):
        return self.g[u]


def test_prim_basico():
    grafo = {
        0: [(1, 1), (2, 4)],
        1: [(0, 1), (2, 2)],
        2: [(0, 4), (1, 2)]
    }

    g = GrafoMock(grafo)
    mst = prim(g)

    # (0-1) y (1-2)
    pesos = sorted([p for (_, _, p) in mst])

    assert pesos == [1, 2]
    assert len(mst) == 2
