from src.grafos.caminos.dijkstra import dijkstra

class GrafoMock:
    def __init__(self, g):
        self.g = g
        self.n = len(g)
        self.es_ponderado = True

    def vecinos(self, u):
        return self.g[u]

def test_dijkstra_basico():
    g = {
        0: [(1, 1), (2, 4)],
        1: [(2, 2)],
        2: []
    }

    grafo = GrafoMock(g)
    dist = dijkstra(grafo, 0)

    assert dist[0] == 0
    assert dist[1] == 1
    assert dist[2] == 3
