import tkinter as tk
from tkinter import ttk, messagebox

from core.config import grafo_config
from core.ejecutar import ejecutar_algoritmo


def iniciar_app():
    root = tk.Tk()
    root.title("Proyecto de Grafos")
    root.geometry("740x620")

    tk.Label(root, text="Proyecto de Estructuras - Grafos",
             font=("Arial", 18)).pack(pady=10)

    # Combo de algoritmos
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
            "Dijkstra",
            "Bellman-Ford"
        ],
        state="readonly",
        width=40
    )
    combo_alg.pack(pady=8)

    # ===== CONFIGURAR GRAFO =====
    def abrir_config_grafo():
        cfg = tk.Toplevel(root)
        cfg.title("Configurar Grafo")
        cfg.geometry("520x560")

        tk.Label(cfg, text="Representación del grafo:",
                 font=("Arial", 12)).pack(pady=5)
        combo_rep = ttk.Combobox(
            cfg,
            values=[
                "Lista de Adyacencia",
                "Matriz de Adyacencia",
                "Matriz de Incidencia"
            ],
            state="readonly",
            width=35
        )
        combo_rep.pack()

        frame_p = tk.LabelFrame(cfg, text="Propiedades",
                                padx=10, pady=10)
        frame_p.pack(pady=10, fill="x")

        tk.Label(frame_p, text="Dirigido:").grid(row=0, column=0)
        combo_dir = ttk.Combobox(
            frame_p, values=["Sí", "No"],
            state="readonly", width=10)
        combo_dir.grid(row=0, column=1)

        tk.Label(frame_p, text="Ponderado:").grid(row=1, column=0)
        combo_pond = ttk.Combobox(
            frame_p, values=["Sí", "No"],
            state="readonly", width=10)
        combo_pond.grid(row=1, column=1)

        tk.Label(frame_p, text="Número de nodos:").grid(row=2, column=0)
        entry_n = tk.Entry(frame_p, width=10)
        entry_n.grid(row=2, column=1)

        frame_ar = tk.LabelFrame(cfg, text="Aristas",
                                 padx=10, pady=10)
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

        tk.Button(frame_ar, text="Agregar arista",
                  command=popup_arista).pack(pady=5)
        tk.Button(frame_ar, text="Limpiar aristas",
                  command=lambda: text_ar.delete("1.0", tk.END)).pack(pady=5)

        # Pre-cargar config
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

        tk.Button(cfg, text="Guardar configuración",
                  font=("Arial", 12), command=guardar).pack(pady=10)

    tk.Button(root, text="Configurar Grafo", font=("Arial", 12),
              command=abrir_config_grafo).pack(pady=4)

    # CARGAR DEMO
    def cargar_grafo_demo():
        grafo_config["representacion"] = "Lista de Adyacencia"
        grafo_config["dirigido"] = False
        grafo_config["ponderado"] = False
        grafo_config["n"] = 6
        grafo_config["aristas"] = "0 1\n0 2\n1 3\n2 3\n3 4\n4 5"
        messagebox.showinfo(
            "Demo", "Grafo demo cargado (nodos 0..5).")

    tk.Button(root, text="Cargar Grafo Demo",
              font=("Arial", 12),
              command=cargar_grafo_demo).pack(pady=4)

    # EJECUTAR ALGORITMO
    salida = tk.Text(root, width=90, height=22, state="disabled")
    salida.pack(pady=10, padx=10)

    def ejecutar():
        alg = combo_alg.get()
        try:
            resultado = ejecutar_algoritmo(alg, grafo_config)

            salida.configure(state="normal")
            salida.delete("1.0", tk.END)
            salida.insert(tk.END, f"{resultado}\n")
            salida.configure(state="disabled")

        except Exception as e:
            messagebox.showerror("Error ejecutando", str(e))

    tk.Button(root, text="Ejecutar Algoritmo",
              font=("Arial", 12),
              command=ejecutar).pack(pady=8)

    root.mainloop()
