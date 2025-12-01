import math
from representacion.data_caminos import grafo_bellman_ford, NODOS_BELLMAN, grafo_ciclo_negativo, NODOS_CICLO_NEG

class BellmanFord:
    def __init__(self, grafo, lista_nodos):
        self.grafo = grafo
        self.lista_nodos = lista_nodos
        self.num_nodos = len(lista_nodos)
        
    def encontrar_caminos(self, inicio):
        """
        Encuentra el camino más corto y detecta ciclos negativos.
        
        Complejidad de Tiempo: O(V * E)
        """
        if inicio not in self.lista_nodos:
            return {"error": "Nodo de inicio no existe."}
            
        # 1. Inicialización
        distancias = {nodo: math.inf for nodo in self.lista_nodos}
        distancias[inicio] = 0
        
        # 2. Relajación de aristas |V| - 1 veces
        for i in range(self.num_nodos - 1):
            cambio = False
            # Recorremos todas las aristas
            for u in self.lista_nodos:
                for v, peso in self.grafo.get(u, []):
                    # Relajación
                    if distancias[u] != math.inf and distancias[u] + peso < distancias[v]:
                        distancias[v] = distancias[u] + peso
                        cambio = True
            
            # Optimización: si no hay cambios en una iteración, terminamos.
            if not cambio:
                break

        # 3. Detección de Ciclos Negativos
        for u in self.lista_nodos:
            for v, peso in self.grafo.get(u, []):
                if distancias[u] != math.inf and distancias[u] + peso < distancias[v]:
                    return {"error": "Ciclo Negativo detectado. No existe camino más corto."}

        return distancias

def bellman_ford(grafo, lista_nodos, inicio='A'):
    solver = BellmanFord(grafo, lista_nodos)
    return solver.encontrar_caminos(inicio)

if __name__ == "__main__":
    # Prueba 1: Sin ciclo negativo
    resultado1 = bellman_ford(grafo_bellman_ford, NODOS_BELLMAN, inicio='A')
    print("Bellman-Ford (Sin Ciclo):", resultado1) 
    
    # Prueba 2: Con ciclo negativo
    resultado2 = bellman_ford(grafo_ciclo_negativo, NODOS_CICLO_NEG, inicio='A')
    print("Bellman-Ford (Con Ciclo):", resultado2)