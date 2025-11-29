import matplotlib.pyplot as plt

def plot_grafo(grafo):
    """
    Graficar un grafo con matplotlib.
    Funciona para lista de adyacencia, matriz adyacencia o matriz incidencia.
    """

    # ---------------------------------------------
    # 1. Conseguir las aristas en formato (u, v)
    # ---------------------------------------------
    aristas = []

    # Caso: Lista de Adyacencia
    if hasattr(grafo, "grafo"):  
        for u in range(grafo.n):
            for v in grafo.grafo[u]:
                if (v, u) not in aristas:
                    aristas.append((u, v))

    # Caso: Matriz de Adyacencia
    elif hasattr(grafo, "matriz") and isinstance(grafo.matriz[0][0], int):
        for u in range(grafo.n):
            for v in range(grafo.n):
                if grafo.matriz[u][v] == 1 and (v, u) not in aristas:
                    aristas.append((u, v))

    # Caso: Matriz de Incidencia
    elif hasattr(grafo, "matriz") and isinstance(grafo.matriz[0][0], int):
        for c, (u, v) in enumerate(grafo.aristas):
            aristas.append((u, v))

    # ---------------------------------------------
    # 2. Crear posiciones circulares para los nodos
    # ---------------------------------------------
    import math
    posiciones = {}
    angulo = 2 * math.pi / grafo.n

    for i in range(grafo.n):
        posiciones[i] = (
            math.cos(i * angulo),
            math.sin(i * angulo)
        )

    # ---------------------------------------------
    # 3. Dibujar nodos
    # ---------------------------------------------
    for nodo, (x, y) in posiciones.items():
        plt.scatter(x, y, s=500, color="skyblue")
        plt.text(x, y, str(nodo), ha='center', va='center', fontsize=12, fontweight='bold')

    # ---------------------------------------------
    # 4. Dibujar aristas
    # ---------------------------------------------
    for u, v in aristas:
        x1, y1 = posiciones[u]
        x2, y2 = posiciones[v]
        plt.plot([x1, x2], [y1, y2], color="black")

    # ---------------------------------------------
    # 5. Mostrar
    # ---------------------------------------------
    plt.title("Visualización del Grafo")
    plt.axis('off')
    plt.show()
