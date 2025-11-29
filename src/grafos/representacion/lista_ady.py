class ListaAdyacencia:
    def __init__(self, n, dirigido=False):
        self.n = n
        self.es_dirigido = dirigido
        self.lista = [[] for _ in range(n)]

    def add_edge(self, u, v):
        self.lista[u].append(v)
        if not self.es_dirigido:
            self.lista[v].append(u)

    def vecinos(self, u):
        return self.lista[u]

    def __str__(self):
        resultado = ""
        for i in range(self.n):
            resultado += f"{i}: {self.lista[i]}\n"
        return resultado
