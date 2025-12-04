from src.grafos.representacion.lista_ady import ListaAdyacencia

def test_lista_adyacencia_simple():
    g = ListaAdyacencia(3)

    # Detectar el nombre del método real
    if hasattr(g, "agregar_arista"):
        g.agregar_arista(0, 1)
        g.agregar_arista(1, 2)
    elif hasattr(g, "añadir_arista"):
        g.añadir_arista(0, 1)
        g.añadir_arista(1, 2)
    elif hasattr(g, "add_edge"):
        g.add_edge(0, 1)
        g.add_edge(1, 2)
    else:
        raise AssertionError("ListaAdyacencia no tiene método para agregar aristas")

    # Validar vecinos
    assert sorted(g.vecinos(0)) == [1]
    assert sorted(g.vecinos(1)) == [0, 2]
    assert sorted(g.vecinos(2)) == [1]
