# ------------------------------------------------------
# main.py — Interfaz completa con matching externo/interno
# ------------------------------------------------------
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------
# LIBRERÍAS
# ------------------------------------------------------
import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque

# networkx opcional (no obligatorio porque preferimos usar matching_no_bipartito.py si existe)
try:
    import networkx as nx
    HAS_NETWORKX = True
except Exception:
    HAS_NETWORKX = False

# ------------------------------------------------------
# IMPORTAR REPRESENTACIONES (tus archivos)
# ------------------------------------------------------
from representacion.lista_ady import ListaAdyacencia
from representacion.matriz_ady import MatrizAdyacencia
from representacion.matriz_inc import MatrizIncidencia

# ------------------------------------------------------
# IMPORTAR TUS ALGORITMOS (recorridos y árbol)
# ------------------------------------------------------
from recorridos.dfs import dfs
from recorridos.bfs import bfs
from arboles.is_tree import is_tree_diagnosis
from arboles.kruskal import kruskal

# Componentes conexas / SCC (opcional)
try:
    from componentesconexos.tarjan import tarjan
    from componentesconexos.kosaraju import kosaraju
    from representacion.data_componentes import grafo_dirigido_scc, NODOS_GRAFO_SÓLO_DIRIGIDO
    HAS_SCC_EXTRAS = True
except Exception:
    HAS_SCC_EXTRAS = False

# ------------------------------------------------------
# INTENTAR IMPORTAR MÓDULOS DE MATCHING EXTERNOS
# ------------------------------------------------------
EXT_HOPCROFT = None
EXT_MATCHING_GENERAL = None

try:
    from matching_bipartito import hopcroft_karp as EXT_HOPCROFT
except Exception:
    EXT_HOPCROFT = None

try:
    from matching_no_bipartito import matching_general as EXT_MATCHING_GENERAL
except Exception:
    EXT_MATCHING_GENERAL = None

# ------------------------------------------------------
# VARIABLES GLOBALES DEL GRAFO
# ------------------------------------------------------
grafo_config = {
    "representacion": None,
    "dirigido": False,
    "ponderado": False,
    "n": 0,
    "aristas": ""
}

# ------------------------------------------------------
# UTIL: extraer solo vecinos (ignorando peso)
# ------------------------------------------------------
def vecinos_nodos(g, u):
    """
    Extrae los vecinos en forma de enteros, tanto si g.vecinos(u) devuelve
    v o (v, peso). Usa atributo g.es_ponderado.
    """
    for item in g.vecinos(u):
        if getattr(g, "es_ponderado", False):
            # item esperado: (v, peso)
            yield item[0]
        else:
            yield item

# ------------------------------------------------------
# IMPLEMENTACIÓN INTERNA HOPCROFT–KARP (fallback)
# ------------------------------------------------------
INF = 10**9

def _hopcroft_karp_internal(grafo, U, V):
    pairU = {u: None for u in U}
    pairV = {v: None for v in V}
    dist = {}

    def bfs():
        q = deque()
        for u in U:
            if pairU[u] is None:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = INF
        found = False
        while q:
            u = q.popleft()
            for v in vecinos_nodos(grafo, u):
                if v in pairV:
                    if pairV[v] is None:
                        found = True
                    else:
                        u2 = pairV[v]
                        if dist.get(u2, INF) == INF:
                            dist[u2] = dist[u] + 1
                            q.append(u2)
        return found

    def dfs(u):
        for v in vecinos_nodos(grafo, u):
            if v in pairV:
                if pairV[v] is None or (dist.get(pairV[v], INF) == dist[u] + 1 and dfs(pairV[v])):
                    pairU[u] = v
                    pairV[v] = u
                    return True
        dist[u] = INF
        return False

    matching = 0
    while bfs():
        for u in U:
            if pairU[u] is None:
                if dfs(u):
                    matching += 1
    return matching, pairU, pairV

# ------------------------------------------------------
# IMPLEMENTACIÓN INTERNA MATCHING GENERAL (fallback Blossom compacta)
# ------------------------------------------------------
def _matching_general_internal(g):
    from collections import deque
    edges = []
    for u in range(g.n):
        for v in vecinos_nodos(g, u):
            if u < v:
                edges.append((u, v))

    # Blossom (versión compacta)
    n = g.n
    match = [-1] * n
    base = list(range(n))
    p = [-1] * n
    q = deque()
    used = [False] * n
    blossom = [False] * n

    def lca(a, b):
        visited = [False] * n
        while True:
            a = base[a]
            visited[a] = True
            if match[a] == -1:
                break
            a = p[match[a]]
        while True:
            b = base[b]
            if visited[b]:
                return b
            b = p[match[b]]

    def mark_path(v, b, children):
        while base[v] != b:
            blossom[base[v]] = blossom[base[match[v]]] = True
            p[v] = children
            children = match[v]
            v = p[match[v]]

    def find_path(root):
        used[:] = [False]*n
        p[:] = [-1]*n
        q.clear()
        q.append(root)
        used[root] = True

        while q:
            v = q.popleft()
            for u in vecinos_nodos(g, v):
                if base[v] == base[u] or match[v] == u:
                    continue
                if u == root or (match[u] != -1 and p[match[u]] != -1):
                    cur = lca(v, u)
                    blossom[:] = [False]*n
                    mark_path(v, cur, u)
                    mark_path(u, cur, v)
                    for i in range(n):
                        if blossom[base[i]]:
                            base[i] = cur
                            if not used[i]:
                                used[i] = True
                                q.append(i)
                elif p[u] == -1:
                    p[u] = v
                    if match[u] == -1:
                        # aumentar matching
                        uu = u
                        while uu != -1:
                            vv = p[uu]
                            ww = match[vv] if vv != -1 else -1
                            match[uu] = vv
                            match[vv] = uu
                            uu = ww
                        return True
                    u2 = match[u]
                    used[u2] = True
                    q.append(u2)
        return False

    for i in range(n):
        if match[i] == -1:
            base = list(range(n))
            find_path(i)

    result = set()
    for u in range(n):
        v = match[u]
        if v != -1 and u < v:
            result.add((u, v))
    return result

# ------------------------------------------------------
# CREAR GRAFO DESDE CONFIGURACIÓN
# ------------------------------------------------------
def crear_grafo_desde_config():
    if grafo_config["representacion"] is None:
        raise ValueError("No hay configuración de grafo guardada.")

    rep = grafo_config["representacion"]
    dirigido = grafo_config["dirigido"]
    ponderado = grafo_config["ponderado"]
    n = grafo_config["n"]
    texto = grafo_config["aristas"]

    if rep == "Lista de Adyacencia":
        g = ListaAdyacencia(n, dirigido=dirigido, ponderado=ponderado)
    elif rep == "Matriz de Adyacencia":
        g = MatrizAdyacencia(n, dirigido=dirigido, ponderado=ponderado)
    elif rep == "Matriz de Incidencia":
        g = MatrizIncidencia(n, dirigido=dirigido, ponderado=ponderado)
    else:
        raise ValueError("Representación inválida")

    for linea in texto.strip().split("\n"):
        if linea.strip() == "":
            continue
        partes = linea.split()
        if ponderado:
            if len(partes) != 3:
                raise ValueError(f"Formato incorrecto (u v peso): {linea}")
            u, v = int(partes[0]), int(partes[1])
            try:
                w = float(partes[2])
            except:
                raise ValueError(f"Peso inválido: {linea}")
            g.add_edge(u, v, w)
        else:
            if len(partes) != 2:
                raise ValueError(f"Formato incorrecto (u v): {linea}")
            u, v = int(partes[0]), int(partes[1])
            g.add_edge(u, v)
    return g

# ------------------------------------------------------
# VENTANA DE CONFIGURACIÓN DEL GRAFO
# ------------------------------------------------------
def abrir_config_grafo():
    cfg = tk.Toplevel(root)
    cfg.title("Configurar Grafo")
    cfg.geometry("520x560")

    tk.Label(cfg, text="Representación del grafo:", font=("Arial", 12)).pack(pady=5)
    combo_rep = ttk.Combobox(
        cfg,
        values=["Lista de Adyacencia", "Matriz de Adyacencia", "Matriz de Incidencia"],
        state="readonly",
        width=35
    )
    combo_rep.pack()

    frame_p = tk.LabelFrame(cfg, text="Propiedades", padx=10, pady=10)
    frame_p.pack(pady=10, fill="x")

    tk.Label(frame_p, text="Dirigido:").grid(row=0, column=0)
    combo_dir = ttk.Combobox(frame_p, values=["Sí", "No"], state="readonly", width=10)
    combo_dir.grid(row=0, column=1)

    tk.Label(frame_p, text="Ponderado:").grid(row=1, column=0)
    combo_pond = ttk.Combobox(frame_p, values=["Sí", "No"], state="readonly", width=10)
    combo_pond.grid(row=1, column=1)

    tk.Label(frame_p, text="Número de nodos:").grid(row=2, column=0)
    entry_n = tk.Entry(frame_p, width=10)
    entry_n.grid(row=2, column=1)

    frame_ar = tk.LabelFrame(cfg, text="Aristas", padx=10, pady=10)
    frame_ar.pack(pady=10, fill="both", expand=True)

    text_ar = tk.Text(frame_ar, height=12, width=50)
    text_ar.pack()

    def popup_arista():
        pop = tk.Toplevel(cfg)
        pop.title("Agregar Arista")
        pop.geometry("260x240")

        tk.Label(pop, text="Nodo U:").pack()
        e_u = tk.Entry(pop)
        e_u.pack()

        tk.Label(pop, text="Nodo V:").pack()
        e_v = tk.Entry(pop)
        e_v.pack()

        if combo_pond.get() == "Sí":
            tk.Label(pop, text="Peso:").pack()
            e_w = tk.Entry(pop)
            e_w.pack()
        else:
            e_w = None

        def agregar():
            u = e_u.get().strip()
            v = e_v.get().strip()
            if combo_pond.get() == "Sí":
                w = e_w.get().strip()
                text_ar.insert(tk.END, f"{u} {v} {w}\n")
            else:
                text_ar.insert(tk.END, f"{u} {v}\n")
            pop.destroy()

        tk.Button(pop, text="Agregar", command=agregar).pack(pady=5)

    tk.Button(frame_ar, text="Agregar arista", command=popup_arista).pack(pady=5)
    tk.Button(frame_ar, text="Limpiar aristas", command=lambda: text_ar.delete("1.0", tk.END)).pack(pady=5)

    # Pre-cargar config si existe
    if grafo_config["representacion"]:
        combo_rep.set(grafo_config["representacion"])
    combo_dir.set("Sí" if grafo_config["dirigido"] else "No")
    combo_pond.set("Sí" if grafo_config["ponderado"] else "No")
    if grafo_config["n"] > 0:
        entry_n.insert(0, str(grafo_config["n"]))
    text_ar.insert("1.0", grafo_config["aristas"])

    def guardar():
        try:
            grafo_config["representacion"] = combo_rep.get()
            grafo_config["dirigido"] = combo_dir.get() == "Sí"
            grafo_config["ponderado"] = combo_pond.get() == "Sí"
            grafo_config["n"] = int(entry_n.get())
            grafo_config["aristas"] = text_ar.get("1.0", tk.END).strip()
            if not grafo_config["representacion"]:
                raise ValueError("Selecciona una representación.")
            messagebox.showinfo("Guardado", "Configuración guardada.")
            cfg.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(cfg, text="Guardar configuración", font=("Arial", 12), command=guardar).pack(pady=10)

# ------------------------------------------------------
# CARGAR GRAFO DEMO
# ------------------------------------------------------
def cargar_grafo_demo():
    # demo que funciona para pruebas: no dirigido, no ponderado, 6 nodos
    grafo_config["representacion"] = "Lista de Adyacencia"
    grafo_config["dirigido"] = False
    grafo_config["ponderado"] = False
    grafo_config["n"] = 6
    grafo_config["aristas"] = "0 1\n0 2\n1 3\n2 3\n3 4\n4 5"
    messagebox.showinfo("Demo", "Grafo demo cargado (nodos 0..5).")

# ------------------------------------------------------
# DETECCIÓN BIPARTICIÓN
# ------------------------------------------------------
def detectar_biparticion(g):
    color = {}
    for start in range(g.n):
        if start not in color:
            color[start] = 0
            q = deque([start])
            while q:
                u = q.popleft()
                for v in vecinos_nodos(g, u):
                    if v not in color:
                        color[v] = 1 - color[u]
                        q.append(v)
                    else:
                        if color[v] == color[u]:
                            return None, None, False
    U = [n for n, c in color.items() if c == 0]
    V = [n for n, c in color.items() if c == 1]
    return U, V, True

# ------------------------------------------------------
# EJECUTAR ALGORITMO (VALIDACIONES + LLAMADAS)
# ------------------------------------------------------
def ejecutar_algoritmo():
    if grafo_config["representacion"] is None:
        messagebox.showerror("Error", "Primero configura o carga un grafo.")
        return

    try:
        g = crear_grafo_desde_config()
    except Exception as e:
        messagebox.showerror("Error al crear grafo", str(e))
        return

    alg = combo_alg.get()

    # Validaciones previas
    if alg.startswith("SCC") and not g.es_dirigido:
        messagebox.showerror("Requisito", "SCC requiere grafo DIRIGIDO.")
        return

    if alg == "Matching Bipartito" and g.es_dirigido:
        messagebox.showerror("Requisito", "Matching Bipartito requiere grafo NO dirigido.")
        return

    if alg.startswith("Matching") and g.es_ponderado:
        messagebox.showerror("Requisito", "Matching no soporta grafos ponderados.")
        return

    # Ejecutar
    try:
        if alg == "DFS":
            res = dfs(g, 0)
            resultado = "DFS: " + " → ".join(map(str, res))

        elif alg == "BFS":
            res = bfs(g, 0)
            resultado = "BFS: " + " → ".join(map(str, res))

        elif alg == "Es Árbol":
            diag = is_tree_diagnosis(g)
            resultado = (
                f"Conectado: {diag['conectado']}\n"
                f"Tiene ciclos: {diag['tiene_ciclos']}\n"
                f"|E| = n - 1: {diag['e_n_1']}\n"
                f"Resultado final: {'ÁRBOL' if diag['es_arbol'] else 'NO ES ÁRBOL'}"
            )

        elif alg == "SCC - Kosaraju (Dirigido)":
            if not HAS_SCC_EXTRAS:
                resultado = "Kosaraju no disponible (módulos faltantes)."
            else:
                resultado = kosaraju(grafo_dirigido_scc, NODOS_GRAFO_SÓLO_DIRIGIDO)

        elif alg == "SCC - Tarjan (Dirigido)":
            if not HAS_SCC_EXTRAS:
                resultado = "Tarjan no disponible (módulos faltantes)."
            else:
                resultado = tarjan(grafo_dirigido_scc, NODOS_GRAFO_SÓLO_DIRIGIDO)

        elif alg == "Matching Bipartito":
            U, V, ok = detectar_biparticion(g)
            if not ok:
                messagebox.showerror("Requisito", "El grafo NO es bipartito.")
                return
            # preferir módulo externo si existe
            if EXT_HOPCROFT:
                m, pairU, pairV = EXT_HOPCROFT(g, U, V)
            else:
                m, pairU, pairV = _hopcroft_karp_internal(g, U, V)
            resultado = f"Matching bipartito máximo = {m}\nPareos (U->V):\n{pairU}"

        elif alg == "Matching General":
            # preferir módulo externo si existe
            if EXT_MATCHING_GENERAL:
                mat = EXT_MATCHING_GENERAL(g)
            else:
                # si networkx está disponible, usarlo como opción alternativa:
                if HAS_NETWORKX:
                    # crear graph y usar nx
                    G = nx.Graph()
                    G.add_nodes_from(range(g.n))
                    seen = set()
                    for u in range(g.n):
                        for v in vecinos_nodos(g, u):
                            a = tuple(sorted((u, v)))
                            if a not in seen and u != v:
                                seen.add(a)
                                G.add_edge(*a)
                    mat = nx.max_weight_matching(G, maxcardinality=True)
                else:
                    mat = _matching_general_internal(g)
            resultado = f"Matching general máximo:\n{mat}"
            
        elif alg == "Kruskal (MST)":
            edges = []
            for u in range(g.n):
                for v in g.vecinos(u):
                    if g.es_ponderado:
                        try:
                            nodo, peso = v
                        except TypeError:
                            nodo = v
                            peso = 1
                    else:
                        nodo = v
                        peso = 1
                    if u < nodo or g.es_dirigido:
                        edges.append((u, nodo, peso))
            mst = kruskal(g.n, edges, directed=g.es_dirigido, weighted=g.es_ponderado)
            resultado = f"MST (Kruskal): \n{mst}"

        else:
            resultado = "Algoritmo no implementado."

    except Exception as e:
        resultado = f"Error ejecutando algoritmo: {e}"

    # Mostrar resultado
    salida.configure(state="normal")
    salida.delete("1.0", tk.END)
    salida.insert(tk.END, f"{resultado}\n\nGrafo interno:\n{g}")
    salida.configure(state="disabled")

# ------------------------------------------------------
# INTERFAZ PRINCIPAL (coloca esto al final)
# ------------------------------------------------------
root = tk.Tk()
root.title("Proyecto de Grafos")
root.geometry("740x620")

tk.Label(root, text="Proyecto de Estructuras - Grafos", font=("Arial", 18)).pack(pady=10)

tk.Label(root, text="Algoritmo:", font=("Arial", 12)).pack()
combo_alg = ttk.Combobox(
    root,
    values=[
        "DFS",
        "BFS",
        "Es Árbol",
        "SCC - Kosaraju (Dirigido)",
        "SCC - Tarjan (Dirigido)",
        "Matching Bipartito",
        "Matching General",
        "Kruskal (MST)"
    ],
    state="readonly",
    width=40
)
combo_alg.pack(pady=8)

tk.Button(root, text="Configurar Grafo", font=("Arial", 12), command=abrir_config_grafo).pack(pady=4)
tk.Button(root, text="Cargar Grafo Demo", font=("Arial", 12), command=cargar_grafo_demo).pack(pady=4)
tk.Button(root, text="Ejecutar Algoritmo", font=("Arial", 12), command=ejecutar_algoritmo).pack(pady=8)

salida = tk.Text(root, width=90, height=22, state="disabled")
salida.pack(pady=10, padx=10)

root.mainloop()
