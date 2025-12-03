class MatrizAdyacencia:
    def __init__(self, n, dirigido=False, ponderado=False):
        self.n = n
        self.es_dirigido = dirigido
        self.es_ponderado = ponderado

        # Nodos estándar 0..n-1
        self.nodos = list(range(n))
        self.indice = {i: i for i in range(n)}     # nodo → índice
        self.reverso = {i: i for i in range(n)}    # índice → nodo

        # Matriz NxN
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
        vec = []
        for v in range(self.n):
            if self.matriz[u][v] != 0:
                if self.es_ponderado:
                    vec.append((v, self.matriz[u][v]))
                else:
                    vec.append(v)
        return vec

    def __str__(self):
        res = "Matriz de Adyacencia:\n"
        for fila in self.matriz:
            res += f"{fila}\n"
        return res
