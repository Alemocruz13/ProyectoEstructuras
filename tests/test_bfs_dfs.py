from src.grafos.recorridos.bfs import bfs
from src.grafos.recorridos.dfs import dfs

# Grafo compatible con tu implementación BFS/DFS
class GrafoMock:
    def __init__(self):
        # nodo real → índice interno
        self.indice = {0: 0, 1: 1, 2: 2, 3: 3}

        # índice interno → nodo real
        self.reverso = {0: 0, 1: 1, 2: 2, 3: 3}

        self.n = 4

        # Lista de adyacencia SIN pesos
        self.lista = {
            0: [1, 2],
            1: [3],
            2: [],
            3: []
        }

        # BFS/DFS lo necesitan
        self.es_ponderado = False

    def vecinos(self, u):
        return self.lista[u]


def test_bfs_recorrido():
    g = GrafoMock()
    visitados = bfs(g, 0)
    assert visitados == [0, 1, 2, 3]


def test_dfs_recorrido():
    g = GrafoMock()
    visitados = dfs(g, 0)
    assert visitados == [0, 1, 3, 2]
