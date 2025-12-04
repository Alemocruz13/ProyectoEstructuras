from src.grafos.pareos.matching_maximal import matching_maximal_general

def test_matching_maximal_general():
    edges = [(0,1), (1,2), (2,3)]
    result = matching_maximal_general(edges)

    # Un matching maximal posible:
    # [(0,1), (2,3)] o [(1,2)]
    assert len(result) >= 1
