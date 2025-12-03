def matching_maximal_general(edges, dirigido=False, ponderado=False):
    """
    Encuentra un matching maximal en grafos dirigidos/no dirigidos y ponderados/no ponderados.

    edges: lista de aristas
        - No ponderado: [(u,v), ...]
        - Ponderado: [(u,v,w), ...] donde w es el peso
    dirigido: True si el grafo es dirigido, False si no
    ponderado: True si las aristas tienen peso, False si no

    Retorna un conjunto de aristas que forman un matching maximal.
    """
    matching = []
    emparejado = set()  # nodos que ya están emparejados

    for edge in edges:
        # Obtenemos los nodos
        u, v = edge[:2]

        # Si alguno ya está emparejado, ignoramos
        if u in emparejado or v in emparejado:
            continue

        # Agregamos la arista al matching
        matching.append(edge)
        emparejado.add(u)
        emparejado.add(v)

    return matching

# Ejemplo de uso:

# Grafo no dirigido, no ponderado
edges1 = [(0,1),(1,2),(2,3),(3,4)]
print("Matching maximal:", matching_maximal_general(edges1))

# Grafo dirigido, ponderado
edges2 = [(0,1,5),(1,2,3),(2,3,2),(3,0,4)]
print("Matching maximal ponderado dirigido:", matching_maximal_general(edges2, dirigido=True, ponderado=True))
