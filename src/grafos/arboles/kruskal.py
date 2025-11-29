# src/grafos/arboles/kruskal.py

from typing import List, Tuple


class DisjointSet:
    """Union-Find con path compression y union by rank."""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        rootX, rootY = self.find(x), self.find(y)

        if rootX == rootY:
            return False

        if self.rank[rootX] < self.rank[rootY]:
            self.parent[rootX] = rootY
        elif self.rank[rootX] > self.rank[rootY]:
            self.parent[rootY] = rootX
        else:
            self.parent[rootY] = rootX
            self.rank[rootX] += 1

        return True


def kruskal(
    num_vertices: int,
    edges: List[Tuple[int, int, int]],
    directed: bool = False,
    weighted: bool = True
) -> List[Tuple[int, int, int]]:
    """
    Kruskal universal:
    - Funciona con grafos dirigidos y no dirigidos.
    - Funciona con grafos ponderados y no ponderados.
    
    Parámetros:
        num_vertices: número de nodos
        edges: lista de aristas (u, v, w)
        directed: True para grafo dirigido
        weighted: False si las aristas no tienen peso
        
    Regresa:
        Lista de aristas del MST.
    """

    # Si NO es ponderado, asignamos peso 1
    if not weighted:
        edges = [(u, v, 1) for (u, v, _) in edges]

    # Si es dirigido, lo "convertimos" a no dirigido para un MST
    # Tomamos la arista con menor peso para cada par (u, v)
    if directed:
        undirected = {}
        for u, v, w in edges:
            a, b = sorted((u, v))
            if (a, b) not in undirected or w < undirected[(a, b)]:
                undirected[(a, b)] = w
        edges = [(a, b, w) for (a, b), w in undirected.items()]

    # Ordenamos por peso
    edges_sorted = sorted(edges, key=lambda x: x[2])

    dsu = DisjointSet(num_vertices)
    mst = []

    # Algoritmo de Kruskal
    for u, v, w in edges_sorted:
        if dsu.union(u, v):
            mst.append((u, v, w))
            if len(mst) == num_vertices - 1:
                break

    return mst


# ejemplo de uso
if __name__ == "__main__":
    # Ejemplo con grafo NO dirigido y NO ponderado
    edges = [
        (0, 1, 0),
        (1, 2, 0),
        (2, 0, 0),
        (2, 3, 0),
        (3, 4, 0),
    ]

    mst = kruskal(5, edges, directed=False, weighted=False)
    print("MST:", mst)
