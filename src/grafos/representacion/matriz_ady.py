class MatrizAdyacencia:
    def __init__(self, n, dirigido=False):
        self.n = n
        self.es_dirigido = dirigido
        self.matriz = [[0]*n for _ in range(n)]

    def add_edge(self, u, v):
        self.matriz[u][v] = 1
        if not self.es_dirigido:
            self.matriz[v][u] = 1


    def vecinos(self, u):
        return [i for i in range(self.n) if self.matriz[u][i] != 0]

    def __str__(self):
        return "\n".join(str(fila) for fila in self.matriz)
