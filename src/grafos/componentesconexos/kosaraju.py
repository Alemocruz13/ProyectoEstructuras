class KosarajuSCC:
    def __init__(self, g):
        self.g = g               # Objeto Grafo
        self.nodos = g.nodos     # Lista de nodos originales
        self.visitados = set()
        self.pila_orden = []
        self.scc_encontradas = []

    # --------- Crear grafo traspuesto ---------
    def crear_traspuesto(self):
        trans = {nodo: [] for nodo in self.nodos}

        for u in self.nodos:
            for v in self.g.vecinos(u):
                if self.g.es_ponderado:
                    v = v[0]
                trans[v].append(u)

        return trans

    # --------- Paso 1: Orden de finalización ---------
    def dfs1(self, u):
        self.visitados.add(u)

        for v in self.g.vecinos(u):
            if self.g.es_ponderado:
                v = v[0]

            if v not in self.visitados:
                self.dfs1(v)

        self.pila_orden.append(u)

    # --------- Paso 2: DFS en el traspuesto ---------
    def dfs2(self, u, trans, comp):
        self.visitados.add(u)
        comp.append(u)

        for v in trans.get(u, []):
            if v not in self.visitados:
                self.dfs2(v, trans, comp)

    # --------- Función principal ---------
    def encontrar_scc(self):
        self.visitados.clear()
        self.pila_orden = []
        self.scc_encontradas = []

        # Paso 1
        for nodo in self.nodos:
            if nodo not in self.visitados:
                self.dfs1(nodo)

        # Paso 2
        trans = self.crear_traspuesto()
        self.visitados.clear()

        while self.pila_orden:
            u = self.pila_orden.pop()

            if u not in self.visitados:
                comp = []
                self.dfs2(u, trans, comp)
                self.scc_encontradas.append(comp)

        return self.scc_encontradas


def kosaraju(g):
    return KosarajuSCC(g).encontrar_scc()
