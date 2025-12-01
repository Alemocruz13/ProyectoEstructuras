# ------------------------------------------------------
# main.py (versión corregida: Opción B)
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

# networkx solo para matching general; si falta, mostramos error al usarlo
try:
    import networkx as nx
    HAS_NETWORKX = True
except Exception:
    HAS_NETWORKX = False

# ------------------------------------------------------
# IMPORTAR REPRESENTACIONES
# ------------------------------------------------------
from representacion.lista_ady import ListaAdyacencia
from representacion.matriz_ady import MatrizAdyacencia
from representacion.matriz_inc import MatrizIncidencia

# ------------------------------------------------------
# IMPORTAR ALGORITMOS (tus módulos)
# ------------------------------------------------------
from recorridos.dfs import dfs
from recorridos.bfs import bfs
from arboles.is_tree import is_tree_diagnosis, is_tree

# Componentes conexas
# Si no tienes estos archivos, coméntalos o añade los módulos correspondientes.
try:
    from componentesconexos.tarjan import tarjan
    from componentesconexos.kosaraju import kosaraju
    from representacion.data_componentes import grafo_dirigido_scc, NODOS_GRAFO_SÓLO_DIRIGIDO
    HAS_SCC_EXTRAS = True
except Exception:
    HAS_SCC_EXTRAS = False

# ------------------------------------------------------
# VARIABLES GLOBALES
# ------------------------------------------------------
grafo_config = {
    "representacion": None,
    "dirigido": False,
    "ponderado": False,
    "n": 0,
    "aristas": ""
}

# ------------------------------------------------------
# UTIL: obtener vecinos como nodos (ignorar pesos)
# ------------------------------------------------------
def vecinos_nodos(g, u):
    """
    Devuelve un iterable de enteros: los vecinos (nodos) de u,
    manejando tanto grafos ponderados (vecino = (v, peso)) como no ponderados (v).
    """
    for v in g.vecinos(u):
        if g.es_ponderado:
            yield v[0]
        else:
            yield v

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

    # Crear grafo
    if rep == "Lista de Adyacencia":
        g = ListaAdyacencia(n, dirigido=dirigido, ponderado=ponderado)
    elif rep == "Matriz de Adyacencia":
        g = MatrizAdyacencia(n, dirigido=dirigido, ponderado=ponderado)
    elif rep == "Matriz de Incidencia":
        g = MatrizIncidencia(n, dirigido=dirigido, ponderado=ponderado)
    else:
        raise ValueError("Representación inválida")

    lineas = texto.strip().split("\n")
    for linea in lineas:
        if linea.strip() == "":
            continue

        partes = linea.split()

        if ponderado:
            if len(partes) != 3:
                raise ValueError(f"Formato incorrecto (u v peso): {linea}")
            u, v = int(partes[0]), int(partes[1])
            # peso puede ser float; almacenar como number
            try:
                w = float(partes[2])
            except:
                raise ValueError(f"Peso inválido en línea: {linea}")
        else:
            if len(partes) != 2:
                raise ValueError(f"Formato incorrecto (u v): {linea}")
            u, v = int(partes[0]), int(partes[1])
            w = None

        # VALIDAR NODOS
        if u < 0 or u >= n or v < 0 or v >= n:
            raise ValueError(
                f"Nodo fuera de rango en arista '{linea}'. Nodos permitidos: 0 a {n-1}"
            )

        # Ahora sí agregamos la arista
        if ponderado:
            g.add_edge(u, v, w)
        else:
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

    # -------- Propiedades --------
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

    # -------- Aristas --------
    frame_ar = tk.LabelFrame(cfg, text="Aristas", padx=10, pady=10)
    frame_ar.pack(pady=10, fill="both", expand=True)

    text_ar = tk.Text(frame_ar, height=12, width=50)
    text_ar.pack()

    # -------- MINI POPUP: Agregar arista --------
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

    # -------- PRE-CARGAR CONFIGURACIÓN SI EXISTE --------
    if grafo_config["representacion"]:
        combo_rep.set(grafo_config["representacion"])

    combo_dir.set("Sí" if grafo_config["dirigido"] else "No")
    combo_pond.set("Sí" if grafo_config["ponderado"] else "No")

    if grafo_config["n"] > 0:
        entry_n.insert(0, str(grafo_config["n"]))

    text_ar.insert("1.0", grafo_config["aristas"])

    # -------- GUARDAR --------
    def guardar():
        try:
            grafo_config["representacion"] = combo_rep.get()
            grafo_config["dirigido"] = (combo_dir.get() == "Sí")
            grafo_config["ponderado"] = (combo_pond.get() == "Sí")
            grafo_config["n"] = int(entry_n.get())
            grafo_config["aristas"] = text_ar.get("1.0", tk.END).strip()

            if grafo_config["representacion"] == "":
                raise ValueError("Selecciona una representación.")

            messagebox.showinfo("Guardado", "Configuración guardada.")
            cfg.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(cfg, text="Guardar configuración", font=("Arial", 12), command=guardar).pack(pady=10)

# ------------------------------------------------------
# DETECCIÓN AUTOMÁTICA DE BIPARTICIÓN (BFS)
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

    U = [nodo for nodo, col in color.items() if col == 0]
    V = [nodo for nodo, col in color.items() if col == 1]
    return U, V, True

# ------------------------------------------------------
# HOPCROFT–KARP ADAPTADO (usa vecinos_nodos)
# ------------------------------------------------------
INF = 10**9

def hopcroft_karp(grafo, U, V):
    # pairU/pairV: mapping node->partner or None
    pairU = {u: None for u in U}
    pairV = {v: None for v in V}
    dist = {}

    def bfs_level():
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
                if v not in pairV:
                    continue
                if pairV[v] is None:
                    found = True
                else:
                    u2 = pairV[v]
                    if dist.get(u2, INF) == INF:
                        dist[u2] = dist[u] + 1
                        q.append(u2)
        return found

    def dfs_try(u):
        for v in vecinos_nodos(grafo, u):
            if v not in pairV:
                continue
            if pairV[v] is None or (dist.get(pairV[v], INF) == dist[u] + 1 and dfs_try(pairV[v])):
                pairU[u] = v
                pairV[v] = u
                return True
        dist[u] = INF
        return False

    matching = 0
    while bfs_level():
        for u in U:
            if pairU[u] is None:
                if dfs_try(u):
                    matching += 1

    return matching, pairU, pairV

# ------------------------------------------------------
# Matching general (usa networkx)
# ------------------------------------------------------
def matching_general(g):
    if not HAS_NETWORKX:
        raise RuntimeError("Falta 'networkx'. Instálalo con: pip install networkx")
    G = nx.Graph()
    G.add_nodes_from(range(g.n))
    # Añadir aristas (sin duplicar)
    seen = set()
    for u in range(g.n):
        for v in vecinos_nodos(g, u):
            if u == v:  # evitar loops
                continue
            a = (u, v) if u <= v else (v, u)
            if a in seen:
                continue
            seen.add(a)
            G.add_edge(a[0], a[1])
    matching = nx.max_weight_matching(G, maxcardinality=True)
    return matching

# ------------------------------------------------------
# EJECUTAR ALGORITMO
# ------------------------------------------------------
def ejecutar_algoritmo():
    if grafo_config["representacion"] is None:
        messagebox.showerror("Error", "Primero configura un grafo.")
        return

    try:
        g = crear_grafo_desde_config()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    alg = combo_alg.get()
    resultado = None

    if alg == "DFS":
        res = dfs(g, 0)
        resultado = "Recorrido DFS: " + " → ".join(map(str, res))

    elif alg == "BFS":
        res = bfs(g, 0)
        resultado = "Recorrido BFS: " + " → ".join(map(str, res))

    elif alg == "Es Árbol":
        diag = is_tree_diagnosis(g)
        resultado = (
            "Requisitos para ser Árbol:\n\n"
            f"- Conectado: {'Sí' if diag['conectado'] else 'No'}\n"
            f"- Tiene ciclos: {'Sí' if diag['tiene_ciclos'] else 'No'}\n"
            f"- |E| = n - 1: {'Sí' if diag['e_n_1'] else 'No'}\n\n"
            f"Resultado final: {'ES Árbol' if diag['es_arbol'] else 'NO es Árbol'}"
        )

    elif alg == "SCC - Kosaraju (Dirigido)":
        if not HAS_SCC_EXTRAS:
            resultado = "SCC (Kosaraju) no disponible: faltan módulos adicionales."
        else:
            # usar datos de ejemplo importados
            scc_list = kosaraju(grafo_dirigido_scc, NODOS_GRAFO_SÓLO_DIRIGIDO)
            resultado = f"SCC Encontradas (Kosaraju):\n{scc_list}"

    elif alg == "SCC - Tarjan (Dirigido)":
        if not HAS_SCC_EXTRAS:
            resultado = "SCC (Tarjan) no disponible: faltan módulos adicionales."
        else:
            scc_list = tarjan(grafo_dirigido_scc, NODOS_GRAFO_SÓLO_DIRIGIDO)
            resultado = f"SCC Encontradas (Tarjan):\n{scc_list}"

    elif alg == "Matching Bipartito":
        # detectar U/V automáticamente y mostrar popup con resultado
        U, V, ok = detectar_biparticion(g)
        if not ok:
            messagebox.showinfo("Matching Bipartito", "El grafo NO es bipartito. No se puede ejecutar Hopcroft–Karp.")
            return
        # ejecutar matching
        try:
            m, pairU, pairV = hopcroft_karp(g, U, V)
            # mostrar en popup
            win = tk.Toplevel(root)
            win.title("Matching Bipartito - Resultado")
            txt = tk.Text(win, width=60, height=20)
            txt.pack()
            txt.insert(tk.END, f"El grafo es bipartito.\nU = {U}\nV = {V}\n\n")
            txt.insert(tk.END, f"Matching máximo = {m}\n\nPareos (U -> V):\n{pairU}\n")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Error en Hopcroft–Karp:\n{e}")
            return

    elif alg == "Matching General":
        try:
            match = matching_general(g)
            resultado = f"Matching máximo general (pares):\n{match}"
        except Exception as e:
            resultado = f"Error (matching general): {e}"

    else:
        resultado = "Algoritmo no implementado"

    # Mostrar resultado y el grafo interno
    salida.configure(state="normal")
    salida.delete("1.0", tk.END)
    salida.insert(tk.END, str(resultado) + "\n\nGrafo:\n" + str(g))
    salida.configure(state="disabled")

# ------------------------------------------------------
# INTERFAZ PRINCIPAL
# ------------------------------------------------------
root = tk.Tk()
root.title("Proyecto de Grafos")
root.geometry("700x600")

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
        "Matching General"
    ],
    state="readonly",
    width=40
)
combo_alg.pack(pady=8)

tk.Button(root, text="Configurar Grafo", font=("Arial", 12), command=abrir_config_grafo).pack(pady=6)
tk.Button(root, text="Ejecutar Algoritmo", font=("Arial", 12), command=ejecutar_algoritmo).pack(pady=6)

salida = tk.Text(root, width=90, height=20, state="disabled")
salida.pack(pady=10, padx=10)

root.mainloop()

