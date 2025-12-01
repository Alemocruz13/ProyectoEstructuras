# Importación corregida
from representacion.data_componentes import grafo_dirigido_scc, NODOS_GRAFO_SÓLO_DIRIGIDO

class TarjanSCC:
    def __init__(self, grafo, lista_nodos):
        self.grafo = grafo
        self.lista_nodos = lista_nodos
        
        self.tiempo = 0
        
        # Inicialización de Diccionarios clave
        self.disc_time = {nodo: -1 for nodo in lista_nodos}      # Tiempo de Descubrimiento (descubrimiento)
        self.low_link_time = {nodo: -1 for nodo in lista_nodos}  # El tiempo más bajo alcanzable
        self.en_pila = {nodo: False for nodo in lista_nodos}      # ¿El nodo está en la pila actual?
        
        self.pila = []
        self.scc_encontradas = []

    def scc_dfs(self, u):
        """ La función central de DFS que encuentra las SCC. """
        
        # 1. Inicializar tiempos y agregar a la pila
        self.disc_time[u] = self.low_link_time[u] = self.tiempo
        self.tiempo += 1
        self.pila.append(u)
        self.en_pila[u] = True

        for v in self.grafo.get(u, []):
            if self.disc_time[v] == -1: # Caso 1: Vecino no visitado (Arista de árbol)
                self.scc_dfs(v)
                # Propagar el low_link_time del hijo
                self.low_link_time[u] = min(self.low_link_time[u], self.low_link_time[v])
            
            elif self.en_pila[v]: # Caso 2: Vecino visitado que está en la pila (Arista de retroceso)
                # Usar el tiempo de descubrimiento del vecino, no su low_link
                self.low_link_time[u] = min(self.low_link_time[u], self.disc_time[v])

        # 2. Si u es la raíz de una SCC
        if self.low_link_time[u] == self.disc_time[u]:
            scc_actual = []
            while True:
                v = self.pila.pop()
                self.en_pila[v] = False
                scc_actual.append(v)
                if u == v:
                    break
            self.scc_encontradas.append(scc_actual)

    def encontrar_scc(self):
        """ Función principal que inicia el recorrido. """
        
        # Recorrer todos los nodos para manejar grafos no conexos
        for nodo in self.lista_nodos:
            if self.disc_time[nodo] == -1: # Si no ha sido descubierto
                self.scc_dfs(nodo)
                
        return self.scc_encontradas

def tarjan(grafo, lista_nodos):
    """ Función de llamada simple para la interfaz. """
    solver = TarjanSCC(grafo, lista_nodos)
    return solver.encontrar_scc()


if __name__ == "__main__":
    scc = tarjan(grafo_dirigido_scc, NODOS_GRAFO_SÓLO_DIRIGIDO)
    print("SCC Tarjan:", scc)