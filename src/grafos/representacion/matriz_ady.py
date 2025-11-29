class MatrizAdyacencia:
    def __init__(self, n):
        self.n = n
        self.matriz = [[0 for _ in range(n)] for _ in range(n)]

    def add_edge(self, u, v):
        self.matriz[u][v] = 1
        self.matriz[v][u] = 1

    def vecinos(self, u):
        return [v for v in range(self.n) if self.matriz[u][v] == 1]

    def __str__(self):
        return "\n".join(str(fila) for fila in self.matriz)
