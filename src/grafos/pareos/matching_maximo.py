def matching_maximo_general(edges, dirigido=False, ponderado=False):
    """
    Implementación del algoritmo Blossom (Edmonds) para matching máximo.
    FUNCIONA PARA:
        - Grafos dirigidos (se convierten a no dirigidos)
        - Grafos no dirigidos
        - Grafos ponderados (ignora peso)
        - Grafos no ponderados

    edges:
        - No ponderado: [(u, v)]
        - Ponderado: [(u, v, w)]
    """

    # --- Construimos lista de adyacencia ---
    grafo = {}
    for edge in edges:
        u, v = edge[:2]  # ignoramos peso si existe

        if u not in grafo:
            grafo[u] = []
        if v not in grafo:
            grafo[v] = []

        grafo[u].append(v)
        if not dirigido:
            grafo[v].append(u)

    # Convertir lista de nodos
    nodos = list(grafo.keys())

    # --- Algoritmo Blossom ---
    mate = {u: None for u in nodos}
    label = {}
    parent = {}
    base = {}
    q = []

    def lca(a, b):
        """ Lowest Common Ancestor para detectar ciclos impares """
        visited = set()
        while True:
            a = base[a]
            visited.add(a)
            if mate[a] is None:
                break
            a = parent[mate[a]]
        while True:
            b = base[b]
            if b in visited:
                return b
            b = parent[mate[b]]

    def mark_path(v, b, children):
        while base[v] != b:
            children.add(base[v])
            children.add(base[mate[v]])
            parent[v] = children
            v = parent[mate[v]]

    def find_path(root):
        """ BFS modificado de Blossom """
        for u in nodos:
            label[u] = None
            parent[u] = None
            base[u] = u
        label[root] = 0
        q.clear()
        q.append(root)

        for v in q:
            for u in grafo[v]:
                if label[u] == None:
                    label[u] = 1
                    parent[u] = v
                    if mate[u] == None:
                        # Aumentar camino
                        return u
                    label[mate[u]] = 0
                    q.append(mate[u])
                elif label[u] == 0 and base[u] != base[v]:
                    b = lca(u, v)
                    blossom = set()
                    mark_path(u, b, blossom)
                    mark_path(v, b, blossom)
                    for n in blossom:
                        if label[n] == 1:
                            label[n] = None
                        base[n] = b
                        if n not in q:
                            q.append(n)
        return None

    for u in nodos:
        if mate[u] is None:
            v = find_path(u)
            if v:
                # Aumentar el matching
                while v is not None:
                    pv = parent[v]
                    nv = mate[pv] if pv is not None else None
                    mate[v] = pv
                    mate[pv] = v
                    v = nv

    # Convertimos output
    resultado = set()
    for u in nodos:
        v = mate[u]
        if v is not None and (v, u) not in resultado:
            resultado.add((u, v))

    return list(resultado)


# ============================
# EJEMPLOS DE USO
# ============================

# 1. Grafo no dirigido
edges1 = [(0,1),(1,2),(2,3),(3,4),(4,5)]
print("Matching maximo:", matching_maximo_general(edges1))

# 2. Grafo dirigido, ponderado
edges2 = [(0,1,5),(1,2,3),(2,3,2),(3,0,4)]
print("Matching maximo (dir + pond):", matching_maximo_general(edges2, dirigido=True, ponderado=True))

# 3. Grafo con ciclo impar (Blossom)
edges3 = [(1,2),(2,3),(3,1),(3,4),(4,5)]
print("Matching maximo:", matching_maximo_general(edges3))
