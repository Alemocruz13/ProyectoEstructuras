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

# -----------------------------------------------------------------
# GRAFOS DIRIGIDOS PARA KOSARAJU Y TARJAN
# -----------------------------------------------------------------

# --- 2. Grafo Dirigido Estándar (SCCs Varias) - AHORA LLAMADO BASE ---
# SCC esperadas: {0, 1, 2}, {3, 4}, {5}
grafo_dirigido_scc_base = {
    0: [1],
    1: [2],
    2: [0],  # Ciclo cerrado (SCC 1: 0-1-2)
    
    3: [4],
    4: [3, 5], # Ciclo cerrado (SCC 2: 3-4) y arista saliente a 5
    
    5: [],     # Nodo terminal (SCC 3: 5)
}


# --- 3. Grafo con una Única Gran SCC ---
# SCC esperadas: {0, 1, 2, 3}
grafo_dirigido_scc_unica = {
    0: [1],
    1: [2],
    2: [3],
    3: [0],
}


# --- 4. Grafo Dirigido Acíclico (DAG) ---
# SCC esperadas: {0}, {1}, {2}, {3}, {4}, {5}
grafo_dirigido_dag_sin_ciclos = {
    0: [1, 2],
    1: [3],
    2: [4],
    3: [5],
    4: [5],
    5: [],
}


# Listas de nodos
NODOS_SÓLO_DIRIGIDO_BASE = list(grafo_dirigido_scc_base.keys())
NODOS_SÓLO_DIRIGIDO_UNICA = list(grafo_dirigido_scc_unica.keys())
NODOS_SÓLO_DIRIGIDO_DAG = list(grafo_dirigido_dag_sin_ciclos.keys())