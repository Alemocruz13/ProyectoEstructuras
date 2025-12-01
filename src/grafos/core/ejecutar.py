from core.crear_grafo import crear_grafo_desde_config
from core.biparticion import detectar_biparticion

from recorridos.bfs import bfs
from recorridos.dfs import dfs
from arboles.is_tree import is_tree_diagnosis

from pareos.bipartito import hopcroft_karp
from pareos.no_bipartito import matching_general

from componentesconexos.kosaraju import kosaraju
from componentesconexos.tarjan import tarjan

# Datos de SCC (tu archivo ya existente)
from representacion.data_componentes import grafo_dirigido_scc, NODOS_GRAFO_SÓLO_DIRIGIDO

# --- NUEVO ---
from caminos.dijkstra import dijkstra
from caminos.bellman_ford import bellman_ford
from representacion.data_caminos import (
    grafo_dijkstra,
    NODOS_DIJKSTRA,
    grafo_bellman_ford,
    NODOS_BELLMAN,
)


def ejecutar_algoritmo(nombre, config):
    g = crear_grafo_desde_config(config)

    # --- Recorridos ---
    if nombre == "DFS":
        return dfs(g, 0)

    if nombre == "BFS":
        return bfs(g, 0)

    # --- Árbol ---
    if nombre == "Es Árbol":
        return is_tree_diagnosis(g)

    # --- Componentes Conexos (Dirigidos) ---
    if nombre == "SCC - Kosaraju (Dirigido)":
        return kosaraju(grafo_dirigido_scc, NODOS_GRAFO_SÓLO_DIRIGIDO)

    if nombre == "SCC - Tarjan (Dirigido)":
        return tarjan(grafo_dirigido_scc, NODOS_GRAFO_SÓLO_DIRIGIDO)

    # --- Matching ---
    if nombre == "Matching Bipartito":
        U, V, ok = detectar_biparticion(g)
        if not ok:
            return "El grafo no es bipartito."
        m, pairU, pairV = hopcroft_karp(g, U, V)
        return f"Matching máximo = {m}\nPareos: {pairU}"

    if nombre == "Matching General":
        M = matching_general(g)
        return f"Matching general máximo: {M}"

    # --- NUEVOS ALGORITMOS DE CAMINOS ---
    if nombre == "Dijkstra":
        return dijkstra(grafo_dijkstra, NODOS_DIJKSTRA, inicio="A")

    if nombre == "Bellman-Ford":
        return bellman_ford(grafo_bellman_ford, NODOS_BELLMAN, inicio="A")

    return "Algoritmo no implementado."
