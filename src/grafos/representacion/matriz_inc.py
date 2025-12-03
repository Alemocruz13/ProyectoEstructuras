class MatrizIncidencia:
    def __init__(self, n, dirigido=False, ponderado=False):
        self.n = n
        self.es_dirigido = dirigido
        self.es_ponderado = ponderado

        # Nodos estándar 0..n-1
        self.nodos = list(range(n))
        self.indice = {i: i for i in range(n)}
        self.reverso = {i: i for i in range(n)}

        # Matriz n x m (m inicia en 0)
        self.matriz = [[] for _ in range(n)]
        self.aristas = 0

    def add_edge(self, u, v, peso=None):
        w = peso if self.es_ponderado else 1

        # Añadir nueva columna
        for i in range(self.n):
            self.matriz[i].append(0)

        if self.es_dirigido:
            # salida u: -w, entrada v: +w
            self.matriz[u][self.aristas] = -w
            self.matriz[v][self.aristas] = +w
        else:
            # no dirigido: ambos lados tienen w
            self.matriz[u][self.aristas] = w
            self.matriz[v][self.aristas] = w

        self.aristas += 1

    def vecinos(self, u):
        vec = []
        for col in range(self.aristas):
            if self.matriz[u][col] != 0:  # u participa
                for v in range(self.n):
                    if v != u and self.matriz[v][col] != 0:
                        if self.es_ponderado:
                            vec.append((v, abs(self.matriz[u][col])))
                        else:
                            vec.append(v)
        return vec

    def __str__(self):
        res = "Matriz de Incidencia:\n"
        for fila in self.matriz:
            res += f"{fila}\n"
        return res
