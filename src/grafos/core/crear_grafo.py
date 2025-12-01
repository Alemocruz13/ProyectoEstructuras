from core.config import grafo_config
from representacion.lista_ady import ListaAdyacencia
from representacion.matriz_ady import MatrizAdyacencia
from representacion.matriz_inc import MatrizIncidencia


def crear_grafo_desde_config(config):
    rep = config["representacion"]
    dirigido = config["dirigido"]
    ponderado = config["ponderado"]
    n = config["n"]
    texto = config["aristas"]

    if rep == "Lista de Adyacencia":
        g = ListaAdyacencia(n, dirigido=dirigido, ponderado=ponderado)
    elif rep == "Matriz de Adyacencia":
        g = MatrizAdyacencia(n, dirigido=dirigido, ponderado=ponderado)
    elif rep == "Matriz de Incidencia":
        g = MatrizIncidencia(n, dirigido=dirigido, ponderado=ponderado)
    else:
        raise ValueError("Representación inválida.")

    for linea in texto.strip().split("\n"):
        if not linea.strip():
            continue
        datos = linea.split()

        if ponderado:
            u, v, w = datos
            g.add_edge(int(u), int(v), float(w))
        else:
            u, v = datos
            g.add_edge(int(u), int(v))

    return g
