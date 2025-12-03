# core/crear_grafo.py
from core.config import grafo_config

# Intentamos importar las clases de representación que están en tu repo.
try:
    from representacion.lista_ady import ListaAdyacencia
except Exception:
    ListaAdyacencia = None

try:
    from representacion.matriz_ady import MatrizAdyacencia
except Exception:
    MatrizAdyacencia = None

try:
    from representacion.matriz_inc import MatrizIncidencia
except Exception:
    MatrizIncidencia = None

def crear_grafo_desde_config():
    """
    Crea y devuelve una instancia de la representación elegida
    utilizando grafo_config. Lanza ValueError si hay problemas.
    """
    cfg = grafo_config
    if cfg.representacion is None:
        raise ValueError("No hay configuración de grafo guardada.")

    rep = cfg.representacion
    dirigido = cfg.dirigido
    ponderado = cfg.ponderado
    n = cfg.n
    texto = cfg.aristas or ""

    # Elegir clase de representación
    if rep == "Lista de Adyacencia":
        if ListaAdyacencia is None:
            raise ImportError("Falta representacion.lista_ady.ListaAdyacencia")
        g = ListaAdyacencia(n, dirigido=dirigido, ponderado=ponderado)
    elif rep == "Matriz de Adyacencia":
        if MatrizAdyacencia is None:
            raise ImportError("Falta representacion.matriz_ady.MatrizAdyacencia")
        g = MatrizAdyacencia(n, dirigido=dirigido, ponderado=ponderado)
    elif rep == "Matriz de Incidencia":
        if MatrizIncidencia is None:
            raise ImportError("Falta representacion.matriz_inc.MatrizIncidencia")
        g = MatrizIncidencia(n, dirigido=dirigido, ponderado=ponderado)
    else:
        raise ValueError("Representación inválida")

    # Rellenar aristas desde texto; se asume nodos numerados como enteros
    for linea in texto.strip().splitlines():
        linea = linea.strip()
        if not linea:
            continue
        partes = linea.split()
        if ponderado:
            if len(partes) != 3:
                raise ValueError(f"Formato incorrecto (u v peso): {linea}")
            u, v = int(partes[0]), int(partes[1])
            try:
                w = float(partes[2])
            except Exception:
                raise ValueError(f"Peso inválido: {linea}")
            g.add_edge(u, v, w)
        else:
            if len(partes) != 2:
                raise ValueError(f"Formato incorrecto (u v): {linea}")
            u, v = int(partes[0]), int(partes[1])
            g.add_edge(u, v)

    return g
