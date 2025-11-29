class MatrizIncidencia:
    def __init__(self, n):
        self.n = n
        self.aristas = []          # lista de tuplas (u, v)
        self.matriz = []           # se llenará dinámicamente

    def add_edge(self, u, v):
        self.aristas.append((u, v))
        self._reconstruir_matriz()

    def _reconstruir_matriz(self):
        # Crear matriz vacía
        m = len(self.aristas)
        self.matriz = [[0] * m for _ in range(self.n)]

        # Llenar matriz
        for i, (u, v) in enumerate(self.aristas):
            self.matriz[u][i] = 1
            self.matriz[v][i] = 1

    def vecinos(self, u):
        vecinos = []
        for i, (a, b) in enumerate(self.aristas):
            if a == u:
                vecinos.append(b)
            elif b == u:
                vecinos.append(a)
        return vecinos

    def __str__(self):
        return "\n".join(str(fila) for fila in self.matriz)
