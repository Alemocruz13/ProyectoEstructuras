class MatrizIncidencia:
    def __init__(self, n, dirigido=False):
        self.n = n
        self.es_dirigido = dirigido
        self.matriz = []   # cada columna representa una arista

    def add_edge(self, u, v):
        # Crear columna de arista
        col = [0] * self.n

        if not self.es_dirigido:
            # Grafo NO dirigido: 1 indica que el nodo toca esa arista
            col[u] = 1
            col[v] = 1

        else:
            # Grafo dirigido:
            # u → v  1 = salida, -1 = entrada
            col[u] = 1
            col[v] = -1

        self.matriz.append(col)

    def vecinos(self, u):
        vecinos = []

        # Recorremos cada arista (columna)
        for col in self.matriz:

            if not self.es_dirigido:
                # No dirigido: si col[u] = 1, buscar al otro extremo
                if col[u] == 1:
                    for i in range(self.n):
                        if i != u and col[i] == 1:
                            vecinos.append(i)

            else:
                # Dirigido: u → v si col[u] = 1 y col[v] = -1
                if col[u] == 1:
                    for i in range(self.n):
                        if col[i] == -1:
                            vecinos.append(i)

        return vecinos

    def __str__(self):
        # Imprime cada columna como vector de incidencia
        salida = ""
        for i, col in enumerate(self.matriz):
            salida += f"Arista {i}: {col}\n"
        return salida
