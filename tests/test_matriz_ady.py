from src.grafos.representacion.matriz_ady import MatrizAdyacencia

def test_matriz_ady_basico():
    g = MatrizAdyacencia(3)
    g.add_edge(0, 1)

    assert g.matriz[0][1] == 1
    assert g.matriz[1][0] == 1   # No dirigido por defecto
    assert g.vecinos(0) == [1]

def test_matriz_ady_dirigido():
    g = MatrizAdyacencia(3, dirigido=True)
    g.add_edge(0, 1)

    assert g.matriz[0][1] == 1
    assert g.matriz[1][0] == 0   # Ya no añade arista opuesta
    assert g.vecinos(0) == [1]
