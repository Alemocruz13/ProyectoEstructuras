def matching_maximal_general(edges):
    usado = set()
    resultado = []

    for u, v in edges:
        if u not in usado and v not in usado:
            resultado.append((u, v))
            usado.add(u)
            usado.add(v)

    return resultado
