# core/utils.py
from collections import deque

def vecinos_nodos(g, u):
    """
    Iterador que devuelve los vecinos 'sin peso' (nodo) independientemente
    de si la representación está ponderada o no.
    Acepta tanto objetos que tienen metodo vecinos(u) como dicts.
    """
    # Si g tiene metodo vecinos, lo usamos
    if hasattr(g, "vecinos"):
        for item in g.vecinos(u):
            if getattr(g, "es_ponderado", False):
                yield item[0]
            else:
                yield item
        return

    # Si es dict: g[u] -> lista de vecinos o lista de (v,w)
    if isinstance(g, dict):
        for item in g.get(u, []):
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                yield item[0]
            else:
                yield item
        return

    # Fallback: intentar indexar con entero
    try:
        for item in g[u]:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                yield item[0]
            else:
                yield item
    except Exception:
        return


def grafo_a_dict(g):
    """
    Convierte un 'Grafo' (objeto) a dict: nodo -> lista de vecinos (v) o (v,w)
    Si g ya es dict, lo devuelve.
    """
    if isinstance(g, dict):
        return g

    if hasattr(g, "nodos") and hasattr(g, "vecinos"):
        out = {}
        for u in g.nodos:
            out[u] = list(g.vecinos(u))
        return out

    # Intentar por indices 0..n-1
    if hasattr(g, "n"):
        out = {}
        for u in range(g.n):
            try:
                out[u] = list(g.vecinos(u))
            except Exception:
                out[u] = []
        return out

    # No convertible
    raise TypeError("No se puede convertir grafo a dict")


def detectar_biparticion(g):
    """
    Comprueba si g es bipartito, retorna (U, V, True) o (None, None, False)
    g puede ser objeto Grafo o dict.
    Operamos en nodos numéricos 0..n-1 si es necesario.
    """
    # Intentar usar n y vecinos_nodos
    try:
        if hasattr(g, "n"):
            n = g.n
            color = {}
            for start in range(n):
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
    except Exception:
        pass

    # fallback: convertir a dict y usar llaves
    d = grafo_a_dict(g)
    color = {}
    for start in d.keys():
        if start not in color:
            color[start] = 0
            q = deque([start])
            while q:
                u = q.popleft()
                for v in vecinos_nodos(d, u):
                    if v not in color:
                        color[v] = 1 - color[u]
                        q.append(v)
                    else:
                        if color[v] == color[u]:
                            return None, None, False
    U = [n for n, c in color.items() if c == 0]
    V = [n for n, c in color.items() if c == 1]
    return U, V, True
