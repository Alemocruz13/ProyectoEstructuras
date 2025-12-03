class TarjanSCC:
    def __init__(self, g):
        self.g = g
        self.nodos = g.nodos

        self.tiempo = 0
        self.ids = {n: -1 for n in self.nodos}
        self.low = {n: -1 for n in self.nodos}
        self.en_pila = {n: False for n in self.nodos}

        self.pila = []
        self.scc = []

    def dfs(self, u):
        self.ids[u] = self.low[u] = self.tiempo
        self.tiempo += 1

        self.pila.append(u)
        self.en_pila[u] = True

        for v in self.g.vecinos(u):
            if self.g.es_ponderado:
                v = v[0]

            if self.ids[v] == -1:
                self.dfs(v)
                self.low[u] = min(self.low[u], self.low[v])

            elif self.en_pila[v]:
                self.low[u] = min(self.low[u], self.ids[v])

        # ¿Es raíz de una SCC?
        if self.low[u] == self.ids[u]:
            comp = []

            while True:
                v = self.pila.pop()
                self.en_pila[v] = False
                comp.append(v)
                if v == u:
                    break

            self.scc.append(comp)

    def encontrar_scc(self):
        for nodo in self.nodos:
            if self.ids[nodo] == -1:
                self.dfs(nodo)

        return self.scc


def tarjan(g):
    return TarjanSCC(g).encontrar_scc()
