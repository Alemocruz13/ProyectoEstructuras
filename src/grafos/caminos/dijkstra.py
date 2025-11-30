import heapq
import math
from representacion.data_caminos import grafo_dijkstra, NODOS_DIJKSTRA

class Dijkstra:
    def __init__(self, grafo, lista_nodos):
        self.grafo = grafo
        self.lista_nodos = lista_nodos
        
    def encontrar_caminos(self, inicio):
        """
        Encuentra la distancia más corta desde 'inicio' a todos los demás nodos.
        
        Complejidad de Tiempo: O((V + E) log V)
        """
        if inicio not in self.lista_nodos:
            return "Error: Nodo de inicio no existe."
            
        # Inicialización de distancias
        distancias = {nodo: math.inf for nodo in self.lista_nodos}
        distancias[inicio] = 0
        
        # Cola de prioridad: (distancia, nodo)
        pq = [(0, inicio)] 
        
        while pq:
            distancia_actual, nodo_actual = heapq.heappop(pq)
            
            # Optimización: Si encontramos un camino más largo al nodo_actual, lo ignoramos
            if distancia_actual > distancias[nodo_actual]:
                continue
            
            # Relajación de aristas
            for vecino, peso in self.grafo.get(nodo_actual, []):
                distancia_nueva = distancia_actual + peso
                
                if distancia_nueva < distancias[vecino]:
                    distancias[vecino] = distancia_nueva
                    heapq.heappush(pq, (distancia_nueva, vecino))
                    
        return distancias

def dijkstra(grafo, lista_nodos, inicio='A'):
    solver = Dijkstra(grafo, lista_nodos)
    return solver.encontrar_caminos(inicio)

if __name__ == "__main__":
    resultado = dijkstra(grafo_dijkstra, NODOS_DIJKSTRA, inicio='A')
    print("Dijkstra desde A:", resultado)