class ListaAdyacencia:
    def __init__(self, n):
        self.n = n
        self.grafo = [[] for _ in range(n)]

    def add_edge(self, u, v):
        self.grafo[u].append(v)
        self.grafo[v].append(u)

    def vecinos(self, u):
        return self.grafo[u]

    def __str__(self):
        texto = ""
        for i in range(self.n):
            texto += f"{i}: {self.grafo[i]}\n"
        return texto
