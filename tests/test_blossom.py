from src.grafos.pareos.blossom import matching_maximo_general

def test_blossom_matching_general():
    edges = [(0, 1), (1, 2), (2, 0)]  # triángulo
    matching = matching_maximo_general(edges)

    # un matching válido en un triángulo es tamaño 1
    assert len(matching) == 1
