from src.grafos.arboles.kruskal import kruskal

class GrafoMock:
    def __init__(self, n, edges):
        self.n = n
        self.edges = edges              # lista (u, v, peso)
        self.nodos = list(range(n))
        self.es_ponderado = True
        self.es_dirigido = False

        # Necesario por tu implementación
        self.indice = {i: i for i in range(n)}
        self.reverso = {i: i for i in range(n)}

        # Construimos lista de vecinos: {u: [(v, peso), ...]}
        self._ady = {i: [] for i in range(n)}
        for u, v, w in edges:
            self._ady[u].append((v, w))
            self._ady[v].append((u, w))  # grafo NO dirigido

    def vecinos(self, u):
        return self._ady[u]


def test_kruskal_basico():
    edges = [
        (0, 1, 1),
        (1, 2, 2),
        (0, 2, 4)
    ]

    g = GrafoMock(3, edges)
    mst = kruskal(g)

    assert len(mst) == 2
    assert (0, 1, 1) in mst
    assert (1, 2, 2) in mst
