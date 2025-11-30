# ------------------------------------------------------
# CONFIGURACIÓN PARA QUE LOS IMPORTS FUNCIONEN EN VS CODE
# ------------------------------------------------------
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------
# LIBRERÍAS PARA LA INTERFAZ
# ------------------------------------------------------
import tkinter as tk
from tkinter import ttk, messagebox

# ------------------------------------------------------
# IMPORTAR REPRESENTACIONES
# ------------------------------------------------------
from representacion.lista_ady import ListaAdyacencia
from representacion.matriz_ady import MatrizAdyacencia
from representacion.matriz_inc import MatrizIncidencia

# ------------------------------------------------------
# IMPORTAR ALGORITMOS
# ------------------------------------------------------

#Importación recorridos
from recorridos.dfs import dfs
from recorridos.bfs import bfs

#Importación árboles
from arboles.is_tree import is_tree
from arboles.is_tree import is_tree, is_tree_diagnosis

#Importación componentes conexas y SCC
from componentesconexos.tarjan import tarjan
from componentesconexos.kosaraju import kosaraju

#Importar representación de datos de componentes
from representacion.data_componentes import grafo_dirigido_scc, NODOS_GRAFO_SÓLO_DIRIGIDO

# ------------------------------------------------------
# FUNCIÓN PARA CREAR GRAFO DE DEMOSTRACIÓN
# ------------------------------------------------------
def crear_grafo_demo(representacion):
    n = 5

    if representacion == "Lista de Adyacencia":
        g = ListaAdyacencia(n)
    elif representacion == "Matriz de Adyacencia":
        g = MatrizAdyacencia(n)
    elif representacion == "Matriz de Incidencia":
        g = MatrizIncidencia(n)
    else:
        return None

    # Aristas del ejemplo
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)

    return g


# ------------------------------------------------------
# FUNCIÓN PARA EJECUTAR ALGORITMO SELECCIONADO
# ------------------------------------------------------
def ejecutar_algoritmo():
    rep_seleccionada = combo_representacion.get()
    alg_seleccionado = combo_algoritmo.get()

    if rep_seleccionada == "":
        messagebox.showerror("Error", "Selecciona una representación de grafo.")
        return

    if alg_seleccionado == "":
        messagebox.showerror("Error", "Selecciona un algoritmo.")
        return

    g = crear_grafo_demo(rep_seleccionada)
    g_display = g  # Por defecto, mostrar el grafo creado
    resultado = "Algoritmo no ejecutado."
    # Ejecutar algoritmo elegido
    if alg_seleccionado == "DFS":
        resultado = dfs(g, 0)

    elif alg_seleccionado == "BFS":
        resultado = bfs(g, 0)

    elif alg_seleccionado == "Es Árbol":
        diag = is_tree_diagnosis(g)
        resultado = (
            "Requisitos para ser Árbol:\n\n"
            f"- Conectado: {'Sí' if diag['conectado'] else 'No'}\n"
            f"- Tiene ciclos: {'Sí' if diag['tiene_ciclos'] else 'No'}\n"
            f"- |E| = n - 1: {'Sí' if diag['e_n_1'] else 'No'}\n\n"
            f"Resultado final: {'Es árbol' if diag['es_arbol'] else 'NO es árbol'}"
        )
    # 1. Componentes Conexas (No Dirigidas)
   # elif alg_seleccionado == "Comp. Conexas (No Dirigidas)":
    #    # Usa el diccionario de datos importado
     #   resultado = encontrar_componentes_conexas(grafo_no_dirigido_componentes)
      #  resultado = f"Componentes Encontradas: {resultado}"
       # g_display = grafo_no_dirigido_componentes
        #rep_seleccionada = "Lista de Adyacencia (Diccionario de Prueba)"

    # 2. Componentes Fuertemente Conexas (Kosaraju)
    elif alg_seleccionado == "Comp. Fuertemente Conexas (Kosaraju)":
        # Usa el diccionario de datos dirigido importado
        scc_list = kosaraju(grafo_dirigido_scc, NODOS_GRAFO_SÓLO_DIRIGIDO)
        resultado = f"SCC Encontradas (Kosaraju):\n{scc_list}"
        g_display = grafo_dirigido_scc
        rep_seleccionada = "Lista de Adyacencia (Dirigido de Prueba)"

    # 3. Componentes Fuertemente Conexas (Tarjan)
    elif alg_seleccionado == "Comp. Fuertemente Conexas (Tarjan)":
        # Usa el diccionario de datos dirigido importado
        scc_list = tarjan(grafo_dirigido_scc, NODOS_GRAFO_SÓLO_DIRIGIDO)
        resultado = f"SCC Encontradas (Tarjan):\n{scc_list}"
        g_display = grafo_dirigido_scc
        rep_seleccionada = "Lista de Adyacencia (Dirigido de Prueba)"


    else:
        resultado = "Algoritmo no implementado"
        g_display = g
    # Mostrar Resultado
    salida.configure(state="normal")
    salida.delete("1.0", tk.END)
    salida.insert(
        tk.END,
        f"Representación: {rep_seleccionada}\n"
        f"Algoritmo: {alg_seleccionado}\n\n"
        f"Resultado: {resultado}\n\n"
        f"Grafo interno:\n{g}"
    )
    salida.configure(state="disabled")


# ------------------------------------------------------
# CONFIGURACIÓN DE VENTANA
# ------------------------------------------------------
root = tk.Tk()
root.title("Proyecto de Grafos - Interfaz Completa")
root.geometry("600x560")

titulo = tk.Label(root, text="Proyecto de Estructuras - Grafos", font=("Arial", 18))
titulo.pack(pady=10)

# -------------------------
# Selección de Representación
# -------------------------
tk.Label(root, text="Representación del Grafo:", font=("Arial", 12)).pack()
combo_representacion = ttk.Combobox(
    root,
    values=[
        "Lista de Adyacencia",
        "Matriz de Adyacencia",
        "Matriz de Incidencia",
    ],
    state="readonly",
    width=30
)
combo_representacion.pack(pady=5)

# -------------------------
# Selección de Algoritmo
# -------------------------
tk.Label(root, text="Algoritmo:", font=("Arial", 12)).pack()
combo_algoritmo = ttk.Combobox(
    root,
    values=[
        "DFS",
        "BFS",
        "Es Árbol",
        "SCC - Kosaraju (Dirigido)",
        "SCC - Tarjan (Dirigido)",
    ],
    state="readonly",
    width=30
)
combo_algoritmo.pack(pady=5)

# -------------------------
# Botón Ejecutar
# -------------------------
btn = tk.Button(root, text="Ejecutar", command=ejecutar_algoritmo, font=("Arial", 12))
btn.pack(pady=10)

# -------------------------
# Cuadro de Salida
# -------------------------
salida = tk.Text(root, width=70, height=20, state="disabled")
salida.pack(pady=10)

# -------------------------
# Iniciar ventana
# -------------------------
root.mainloop()
