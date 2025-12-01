import math

class BellmanFord:
    def __init__(self, grafo, lista_nodos):
        self.grafo = grafo
        self.lista_nodos = lista_nodos
        self.num_nodos = len(lista_nodos)
        
    def encontrar_caminos(self, inicio):
        if inicio not in self.lista_nodos:
            return {"error": "Nodo de inicio no existe."}
            
        distancias = {nodo: math.inf for nodo in self.lista_nodos}
        distancias[inicio] = 0
        
        for _ in range(self.num_nodos - 1):
            cambio = False
            for u in self.lista_nodos:
                for v, peso in self.grafo.get(u, []):
                    if distancias[u] != math.inf and distancias[u] + peso < distancias[v]:
                        distancias[v] = distancias[u] + peso
                        cambio = True
            if not cambio:
                break

        for u in self.lista_nodos:
            for v, peso in self.grafo.get(u, []):
                if distancias[u] != math.inf and distancias[u] + peso < distancias[v]:
                    return {"error": "Ciclo Negativo detectado. No existe camino más corto."}

        return distancias

def bellman_ford(grafo, lista_nodos, inicio='A'):
    solver = BellmanFord(grafo, lista_nodos)
    return solver.encontrar_caminos(inicio)
