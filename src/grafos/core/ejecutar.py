from core.config import grafo_config
from core.crear_grafo import crear_grafo_desde_config
from core.utils import vecinos_nodos, grafo_a_dict, detectar_biparticion


# ============================================================
#  IMPORTACIONES DE ALGORITMOS
# ============================================================

# Recorridos
try:
    from recorridos.bfs import bfs
except Exception:
    bfs = None

try:
    from recorridos.dfs import dfs
except Exception:
    dfs = None


# Árboles
try:
    from arboles.is_tree import is_tree_diagnosis
except Exception:
    is_tree_diagnosis = None

try:
    from arboles.kruskal import kruskal as kruskal_old
except Exception:
    kruskal_old = None

# >>> INTEGRACIÓN PRIM
try:
    from arboles.prim import prim as prim_fn
except Exception:
    prim_fn = None
# <<< FIN INTEGRACIÓN PRIM


# SCC
try:
    from componentesconexos.kosaraju import kosaraju as kosaraju_fn
except Exception:
    kosaraju_fn = None

try:
    from componentesconexos.tarjan import tarjan as tarjan_fn
except Exception:
    tarjan_fn = None


# Caminos (NUEVOS Y COMPATIBLES)
try:
    from caminos.dijkstra import dijkstra as dijkstra_fn
except Exception:
    dijkstra_fn = None

try:
    from caminos.bellman_ford import bellman_ford as bellman_fn
except Exception:
    bellman_fn = None


# Matching externo
try:
    from pareos.bipartito import hopcroft_karp as hopcroft_karp_ext
except Exception:
    hopcroft_karp_ext = None

# Matching bipartito (Hopcroft–Karp)
try:
    from pareos.bipartito import hopcroft_karp as hopcroft_karp_ext
except Exception:
    hopcroft_karp_ext = None

# Matching máximo general (Blossom)
try:
    from pareos.blossom import matching_maximo_general as blossom_ext
except Exception:
    blossom_ext = None

# Matching maximal (greedy)
try:
    from pareos.matching_maximal import matching_maximal_general as maximal_ext
except Exception:
    maximal_ext = None




# ============================================================
#   EJECUTAR ALGORITMO SELECCIONADO
# ============================================================
def ejecutar_algoritmo_seleccionado(nombre_alg, extra=None):

    # Crear grafo desde configuración
    try:
        g = crear_grafo_desde_config()
    except Exception as e:
        return False, f"Error creando grafo: {e}"

    inicio = extra.get("inicio", 0) if extra else 0

    # ----------------------------------------------------
    # DFS
    # ----------------------------------------------------
    if nombre_alg == "DFS (Depth-First Search)":
        if dfs is None:
            return False, "DFS no implementado."

        try:
            r = dfs(g, 0)
        except TypeError:
            try:
                r = dfs(g)
            except Exception as e:
                return False, f"DFS falló: {e}"

        return True, "DFS: " + " → ".join(map(str, r))

    # ----------------------------------------------------
    # BFS
    # ----------------------------------------------------
    if nombre_alg == "BFS (Breadth-First Search)":
        if bfs is None:
            return False, "BFS no implementado."

        try:
            r = bfs(g, 0)
        except TypeError:
            try:
                r = bfs(g)
            except Exception as e:
                return False, f"BFS falló: {e}"

        return True, "BFS: " + " → ".join(map(str, r))

    # ----------------------------------------------------
    # Es Árbol
    # ----------------------------------------------------
    if nombre_alg == "Es Árbol (Conected + Ciclos + |E|=n-1)":
        if is_tree_diagnosis is None:
            return False, "Diagnóstico de árbol no implementado."

        try:
            diag = is_tree_diagnosis(g)
        except Exception as e:
            return False, f"Error en is_tree: {e}"

        texto = (
            f"Conectado: {diag.get('conectado')}\n"
            f"Tiene ciclos: {diag.get('tiene_ciclos')}\n"
            f"|E| = n - 1: {diag.get('e_n_1')}\n"
            f"Resultado final: {'ÁRBOL' if diag.get('es_arbol') else 'NO ES ÁRBOL'}"
        )
        return True, texto

    # ----------------------------------------------------
    # SCC - Kosaraju / Tarjan (CORRECCIÓN: Se pasa solo 'g')
    # ----------------------------------------------------
    if nombre_alg.startswith("SCC"):

        if "Kosaraju" in nombre_alg:
            if kosaraju_fn is None:
                return False, "Kosaraju no disponible."

            try:
                # CORREGIDO: Se pasa solo el objeto Grafo 'g'
                res = kosaraju_fn(g)
            except Exception as e:
                return False, f"Kosaraju falló: {e}"

            return True, f"SCC (Kosaraju):\n{res}"

        if "Tarjan" in nombre_alg:
            if tarjan_fn is None:
                return False, "Tarjan no disponible."

            try:
                # CORREGIDO: Se pasa solo el objeto Grafo 'g'
                res = tarjan_fn(g)
            except Exception as e:
                return False, f"Tarjan falló: {e}"

            return True, f"SCC (Tarjan):\n{res}"

    # ----------------------------------------------------
    # DIJKSTRA (NUEVO Y YA ESTÁNDAR)
    # ----------------------------------------------------
    if nombre_alg == "Camino Más Corto (Dijkstra)":
        if dijkstra_fn is None:
            return False, "Dijkstra no disponible."

        try:
            r = dijkstra_fn(g, inicio)
        except Exception as e:
            return False, f"Dijkstra falló: {e}"

        return True, f"Dijkstra (inicio {inicio}):\n{r}"

    # ----------------------------------------------------
    # BELLMAN-FORD (NUEVO Y YA ESTÁNDAR)
    # ----------------------------------------------------
    if nombre_alg == "Camino Más Corto (Bellman-Ford)":
        if bellman_fn is None:
            return False, "Bellman-Ford no disponible."

        try:
            r = bellman_fn(g, inicio)
        except Exception as e:
            return False, f"Bellman-Ford falló: {e}"

        return True, f"Bellman-Ford (inicio {inicio}):\n{r}"

    # ----------------------------------------------------
    # MATCHING BIPARTITO
    # ----------------------------------------------------
    if nombre_alg == "Matching Bipartito (Hopcroft–Karp)":
        U, V, ok = detectar_biparticion(g)
        if not ok:
            return False, "El grafo NO es bipartito."

        if hopcroft_karp_ext:
            try:
                m, pairU, pairV = hopcroft_karp_ext(g, U, V)
            except Exception as e:
                return False, f"Hopcroft-Karp falló: {e}"
        else:
            try:
                from pareos.bipartito import hopcroft_karp
                m, pairU, pairV = hopcroft_karp(g, U, V)
            except Exception:
                return False, "No hay implementación disponible para Hopcroft-Karp."

        return True, f"Matching bipartito máximo = {m}\nPareos U→V:\n{pairU}"

    # ----------------------------------------------------
    # MATCHING GENERAL (CORRECCIÓN: INDENTACIÓN)
    # ----------------------------------------------------
    if nombre_alg == "Matching General (Blossom - Edmonds)":
        if blossom_ext is None:
            return False, "Matching general (Blossom) no disponible."

        try:
            # Convertir g a lista de aristas estándar
            edges = []
            for u in range(g.n):
                for v in vecinos_nodos(g, u):
                    v_idx = v[0] if g.es_ponderado else v
                    if u < v_idx:
                        edges.append((u, v_idx))
            mat = blossom_ext(edges)
        except Exception as e:
            return False, f"Blossom falló: {e}"

        return True, f"Matching general máximo (Blossom):\n{mat}"

    # ----------------------------------------------------
    # MATCHING MAXIMAL (CORRECCIÓN: INDENTACIÓN)
    # ----------------------------------------------------
    if nombre_alg == "Matching Maximal (Greedy)":
        if maximal_ext is None:
            return False, "Matching maximal no disponible."
        try:
            edges = []
            for u in range(g.n):
                for v in vecinos_nodos(g, u):
                    v_idx = v[0] if g.es_ponderado else v
                    if u < v_idx:
                        edges.append((u, v_idx))
            mat = maximal_ext(edges)
        except Exception as e:
            return False, f"Matching Maximal falló: {e}"

        return True, f"Matching maximal:\n{mat}"


    # ----------------------------------------------------
    # KRUSKAL
    # ----------------------------------------------------
    if nombre_alg == "Kruskal (MST - Kruskal)":
        if kruskal_old is None:
            return False, "Kruskal no disponible."

        # Intento directo
        try:
            res = kruskal_old(g)
            return True, f"MST (Kruskal):\n{res}"
        except Exception:
            pass

        # Construir aristas (u, v, w)
        edges = []
        for u in range(g.n):
            for v in vecinos_nodos(g, u):
                if g.es_ponderado:
                    v_idx, peso = v
                else:
                    v_idx = v
                    peso = 1
                if u <= v_idx:
                    edges.append((u, v_idx, peso))

        try:
            res = kruskal_old(
                g.n, edges,
                directed=g.es_dirigido,
                weighted=g.es_ponderado
            )
            return True, f"MST (Kruskal):\n{res}"
        except Exception as e:
            return False, f"Kruskal falló: {e}"
            
    # ----------------------------------------------------
    # PRIM (MST) (NUEVO BLOQUE)
    # ----------------------------------------------------
    if nombre_alg == "Prim (MST - Prim)":
        if prim_fn is None:
            return False, "Prim no disponible."
        
        # Validación: Prim requiere grafo no dirigido y ponderado
        if g.es_dirigido:
            return False, "Prim requiere un grafo NO dirigido."
        if not g.es_ponderado:
            return False, "Prim requiere un grafo PONDERADO."

        try:
            mst = prim_fn(g)
            
            # Formatear la salida
            total_costo = sum(w for u, v, w in mst)
            res_str = "\n".join([f"({u}, {v}) Peso: {w}" for u, v, w in mst])

            return True, f"MST (Prim) - Costo Total: {total_costo}\nAristas:\n{res_str}"
        except Exception as e:
            return False, f"Prim falló: {e}"


    # ----------------------------------------------------
    return False, "Algoritmo no reconocido."