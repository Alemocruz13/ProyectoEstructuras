# ------------------------------------------------------
# CONFIGURACIÓN PARA QUE LOS IMPORTS FUNCIONEN EN VS CODE
# ------------------------------------------------------
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ------------------------------------------------------
# LIBRERÍAS
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
from recorridos.dfs import dfs
from recorridos.bfs import bfs
from arboles.is_tree import is_tree_diagnosis

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
            u, v, w = map(int, partes)
        else:
            if len(partes) != 2:
                raise ValueError(f"Formato incorrecto (u v): {linea}")
            u, v = map(int, partes)

        # VALIDAR NODOS
        if u < 0 or u >= n or v < 0 or v >= n:
            raise ValueError(
                f"Nodo fuera de rango en arista '{linea}'. "
                f"Nodos permitidos: 0 a {n-1}"
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
    cfg.geometry("500x550")

    # -------- Representación --------
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
        pop.geometry("220x220")

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
            u = e_u.get()
            v = e_v.get()
            if combo_pond.get() == "Sí":
                w = e_w.get()
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

    if alg == "DFS":
        resultado = dfs(g, 0)

    elif alg == "BFS":
        resultado = bfs(g, 0)

    elif alg == "Es Árbol":
        diag = is_tree_diagnosis(g)
        resultado = (
            "Requisitos para ser Árbol:\n\n"
            f"- Conectado: {'Sí' if diag['conectado'] else 'No'}\n"
            f"- Tiene ciclos: {'Sí' if diag['tiene_ciclos'] else 'No'}\n"
            f"- |E| = n - 1: {'Sí' if diag['e_n_1'] else 'No'}\n\n"
            f"Resultado final: {'ES Árbol' if diag['es_arbol'] else 'NO es Árbol'}"
        )

    else:
        resultado = "Algoritmo no implementado"

    salida.configure(state="normal")
    salida.delete("1.0", tk.END)
    salida.insert(tk.END, str(resultado) + "\n\nGrafo:\n" + str(g))
    salida.configure(state="disabled")



# ------------------------------------------------------
# INTERFAZ PRINCIPAL
# ------------------------------------------------------
root = tk.Tk()
root.title("Proyecto de Grafos")
root.geometry("600x500")

tk.Label(root, text="Proyecto de Estructuras - Grafos", font=("Arial", 18)).pack(pady=10)

tk.Label(root, text="Algoritmo:", font=("Arial", 12)).pack()

combo_alg = ttk.Combobox(
    root,
    values=["DFS", "BFS", "Es Árbol"],
    state="readonly",
    width=30
)
combo_alg.pack(pady=5)

tk.Button(root, text="Configurar Grafo", font=("Arial", 12), command=abrir_config_grafo).pack(pady=10)

tk.Button(root, text="Ejecutar Algoritmo", font=("Arial", 12), command=ejecutar_algoritmo).pack(pady=10)

salida = tk.Text(root, width=70, height=15, state="disabled")
salida.pack(pady=10)

root.mainloop()
