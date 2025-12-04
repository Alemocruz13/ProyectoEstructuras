from src.grafos.caminos.bellman_ford import bellman_ford

# Grafo que cumple la interfaz requerida por tu función:
#   g.n
#   g.es_ponderado
#   g.vecinos(u)
class GrafoMock:
    def __init__(self):
        self.n = 3
        self.es_ponderado = True
    
    def vecinos(self, u):
        """
        Grafo:
            0 → 1 (4)
            0 → 2 (5)
            1 → 2 (-2)
        """
        if u == 0:
            return [(1, 4), (2, 5)]
        if u == 1:
            return [(2, -2)]
        if u == 2:
            return []
        return []


def test_bellman_ford_camino_correcto():
    g = GrafoMock()
    distancias = bellman_ford(g, inicio=0)

    assert distancias[0] == 0
    assert distancias[1] == 4
    assert distancias[2] == 2  # 0→1 (4), 1→2 (-2)


def test_bellman_ford_no_ciclo_negativo():
    g = GrafoMock()
    distancias = bellman_ford(g, inicio=0)

    assert "error" not in distancias
