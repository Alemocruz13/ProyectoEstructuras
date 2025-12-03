import heapq

class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False

        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True


def kruskal(g):
    """
    Kruskal compatible con el objeto Grafo.
    Requiere que el grafo sea NO dirigido y PONDERADO.
    """

    if not g.es_ponderado:
        return {"error": "Kruskal requiere grafo ponderado"}

    # Convertimos aristas en formato plano (u_i, v_i, peso)
    edges = []
    for u in g.nodos:
        u_i = g.indice[u]
        for v, peso in g.vecinos(u):
            v_i = g.indice[v]

            # Evitar duplicados → solo agregar si u_i < v_i
            if u_i < v_i:
                edges.append((u_i, v_i, peso))

    # Ordenar aristas por peso
    edges.sort(key=lambda x: x[2])

    dsu = DisjointSet(g.n)
    mst = []

    # Aplicar Kruskal
    for u_i, v_i, w in edges:
        if dsu.union(u_i, v_i):
            mst.append((g.reverso[u_i], g.reverso[v_i], w))

        if len(mst) == g.n - 1:
            break

    return mst
