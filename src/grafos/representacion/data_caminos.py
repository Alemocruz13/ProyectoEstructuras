# Importación para valor infinito
import math

# =================================================================
# GRAFOS DE PRUEBA PARA CAMINOS MÁS CORTOS
# Formato: {nodo: [(vecino, peso), ...]}
# =================================================================

# --- 1. Grafo para Dijkstra (Pesos no negativos) ---
grafo_dijkstra = {
    'A': [('B', 4), ('C', 2)],
    'B': [('E', 3)],
    'C': [('D', 2), ('F', 4)],
    'D': [('E', 3)],
    'E': [('G', 1)],
    'F': [('G', 2)],
    'G': []
}
NODOS_DIJKSTRA = list(grafo_dijkstra.keys())


# --- 2. Grafo para Bellman-Ford (Con pesos negativos, SIN ciclo negativo) ---
grafo_bellman_ford = {
    'A': [('B', 6), ('C', 7)],
    'B': [('D', 5), ('E', -4)],
    'C': [('D', -3)],
    'D': [('E', -2)],
    'E': [('G', 2)],
    'G': []
}
NODOS_BELLMAN = list(grafo_bellman_ford.keys())


# --- 3. Grafo con Ciclo Negativo (Para detección en Bellman-Ford) ---
grafo_ciclo_negativo = {
    'A': [('B', 1)],
    'B': [('C', -10)],
    'C': [('D', 1)],
    'D': [('B', 5)] # Ciclo B-C-D con peso total 1 + (-10) + 5 = -4 (CICLO NEGATIVO)
}
NODOS_CICLO_NEG = list(grafo_ciclo_negativo.keys())