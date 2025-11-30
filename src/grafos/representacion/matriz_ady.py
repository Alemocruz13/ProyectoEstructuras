class MatrizAdyacencia:
    def __init__(self, n, dirigido=False, ponderado=False):
        self.n = n
        self.es_dirigido = dirigido
        self.es_ponderado = ponderado
        self.matriz = [[0]*n for _ in range(n)]

    def add_edge(self, u, v, peso=None):
        if self.es_ponderado:
            self.matriz[u][v] = peso
            if not self.es_dirigido:
                self.matriz[v][u] = peso
        else:
            self.matriz[u][v] = 1
            if not self.es_dirigido:
                self.matriz[v][u] = 1

    def vecinos(self, u):
        lista = []
        for v in range(self.n):
            if self.matriz[u][v] != 0:
                if self.es_ponderado:
                    lista.append((v, self.matriz[u][v]))
                else:
                    lista.append(v)
        return lista

    def __str__(self):
        return "\n".join(str(fila) for fila in self.matriz)
