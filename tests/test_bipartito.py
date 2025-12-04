from src.grafos.pareos.bipartito import hopcroft_karp

class GrafoMock:
    def __init__(self):
        self.ady = {
            0: [3],
            1: [3, 4],
            2: [4],
            3: [0, 1],
            4: [1, 2]
        }

    def vecinos(self, u):
        return self.ady[u]

def test_es_bipartito_con_hopcroft():
    g = GrafoMock()
    U = [0, 1, 2]
    V = [3, 4]

    matching, pairU, pairV = hopcroft_karp(g, U, V)

    assert matching == 2
