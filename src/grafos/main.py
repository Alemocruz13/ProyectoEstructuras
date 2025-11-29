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
from visualizacion.plot import plot_grafo


# ------------------------------------------------------
# IMPORTAR ALGORITMOS
# ------------------------------------------------------
from recorridos.dfs import dfs

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
    elif representacion == "Visualización Gráfica":
        g = ListaAdyacencia(n)
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

    # Ejecutar algoritmo elegido
    if alg_seleccionado == "DFS":
        resultado = dfs(g, 0)

    else:
        resultado = "Algoritmo no implementado"

    # Mostrar Resultado
    salida.configure(state="normal")
    salida.delete("1.0", tk.END)
    salida.insert(tk.END,
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
root.geometry("550x500")

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
        "Visualización Gráfica"
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
salida = tk.Text(root, width=65, height=15, state="disabled")
salida.pack(pady=10)

# -------------------------
# Iniciar ventana
# -------------------------
root.mainloop()
