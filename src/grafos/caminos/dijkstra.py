import heapq
import math

class Dijkstra:
    def __init__(self, grafo, lista_nodos):
        self.grafo = grafo
        self.lista_nodos = lista_nodos
        
    def encontrar_caminos(self, inicio):
        if inicio not in self.lista_nodos:
            return "Error: Nodo de inicio no existe."
            
        distancias = {nodo: math.inf for nodo in self.lista_nodos}
        distancias[inicio] = 0
        
        pq = [(0, inicio)] 
        
        while pq:
            distancia_actual, nodo_actual = heapq.heappop(pq)
            
            if distancia_actual > distancias[nodo_actual]:
                continue
            
            for vecino, peso in self.grafo.get(nodo_actual, []):
                distancia_nueva = distancia_actual + peso
                
                if distancia_nueva < distancias[vecino]:
                    distancias[vecino] = distancia_nueva
                    heapq.heappush(pq, (distancia_nueva, vecino))
                    
        return distancias

def dijkstra(grafo, lista_nodos, inicio='A'):
    solver = Dijkstra(grafo, lista_nodos)
    return solver.encontrar_caminos(inicio)
