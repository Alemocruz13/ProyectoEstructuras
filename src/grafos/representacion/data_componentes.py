# =================================================================
# GRAFOS DE PRUEBA PARA COMPONENTES CONEXAS Y SCC
# =================================================================

# --- 1. Grafo No Dirigido (Para dfs_conexas.py) ---
# Componentes esperadas: {0, 1, 2, 3}, {4, 5}, {6}
grafo_no_dirigido_componentes = {
    0: [1, 2],
    1: [0, 3],
    2: [0],
    3: [1],
    
    4: [5],
    5: [4],
    
    6: []
}

# --- 2. Grafo Dirigido (Para kosaraju.py) ---
# SCC esperadas: {0, 1, 2}, {3, 4}, {5}
grafo_dirigido_scc = {
    0: [1],
    1: [2],
    2: [0],  # Ciclo (0-1-2)
    
    3: [4],
    4: [3, 5], # Ciclo (3-4) y arista saliente
    
    5: [],
}

# Lista de nodos para Kosaraju
NODOS_GRAFO_SÓLO_DIRIGIDO = list(grafo_dirigido_scc.keys())