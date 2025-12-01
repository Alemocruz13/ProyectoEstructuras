class MatrizIncidencia:
    def __init__(self, n, dirigido=False, ponderado=False):
        self.n = n
        self.es_dirigido = dirigido
        self.es_ponderado = ponderado
        self.matriz = [[] for _ in range(n)]
        self.aristas = 0

    def add_edge(self, u, v, peso=None):
        peso_val = peso if self.es_ponderado else 1

        # Nueva columna
        for i in range(self.n):
            self.matriz[i].append(0)

        if self.es_dirigido:
            self.matriz[u][self.aristas] = -peso_val
            self.matriz[v][self.aristas] = peso_val
        else:
            self.matriz[u][self.aristas] = peso_val
            self.matriz[v][self.aristas] = peso_val

        self.aristas += 1

    def vecinos(self, u):
        vecinos = []
        for col in range(self.aristas):
            if self.matriz[u][col] != 0:
                for v in range(self.n):
                    if v != u and self.matriz[v][col] != 0:
                        if self.es_ponderado:
                            vecinos.append((v, abs(self.matriz[u][col])))
                        else:
                            vecinos.append(v)
        return vecinos

    def __str__(self):
        return "\n".join(str(fila) for fila in self.matriz)
