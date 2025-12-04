from src.grafos.representacion.matriz_inc import MatrizIncidencia

def test_matriz_incidencia_basico():
    g = MatrizIncidencia(3)
    g.add_edge(0, 1)

    # La primera arista debe aparecer reflejada
    assert g.matriz[0][0] == 1
    assert g.matriz[1][0] == 1
    assert g.matriz[2][0] == 0

    assert sorted(g.vecinos(0)) == [1]
    assert sorted(g.vecinos(1)) == [0]
    assert g.vecinos(2) == []
