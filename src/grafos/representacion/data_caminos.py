# Grafo para Dijkstra
grafo_dijkstra = {
    'A': [('B', 4), ('C', 1)],
    'B': [('E', 4)],
    'C': [('B', 2), ('D', 4)],
    'D': [('E', 4)],
    'E': []
}
NODOS_DIJKSTRA = ['A', 'B', 'C', 'D', 'E']


# Grafo para Bellman-Ford sin ciclos negativos
grafo_bellman_ford = {
    'A': [('B', 4), ('C', 5)],
    'B': [('C', -3), ('D', 6)],
    'C': [('D', 2)],
    'D': []
}
NODOS_BELLMAN = ['A', 'B', 'C', 'D']


# Grafo para Bellman-Ford con ciclo negativo
grafo_ciclo_negativo = {
    'A': [('B', 1)],
    'B': [('C', -1)],
    'C': [('A', -1)]
}
NODOS_CICLO_NEG = ['A', 'B', 'C']