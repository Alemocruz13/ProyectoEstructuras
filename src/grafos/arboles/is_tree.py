from arboles.is_connected import is_connected
from arboles.has_cycle import has_cycle
from arboles.edge_condition import edges_equal_n_minus_1

def is_tree_diagnosis(g):
    conectado = is_connected(g)
    ciclos = has_cycle(g)
    edges_ok = edges_equal_n_minus_1(g)

    es_arbol = conectado and not ciclos and edges_ok

    return {
        "conectado": conectado,
        "tiene_ciclos": ciclos,
        "e_n_1": edges_ok,
        "es_arbol": es_arbol
    }

def is_tree(g):
    d = is_tree_diagnosis(g)
    return d["es_arbol"]
