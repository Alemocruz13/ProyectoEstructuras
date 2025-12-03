# Archivo: src/componentesconexos/kosaraju.py

# Importación corregida a las nuevas variables de prueba base
from representacion.data_componentes import grafo_dirigido_scc_base, NODOS_SÓLO_DIRIGIDO_BASE

class KosarajuSCC:
    def __init__(self, grafo, lista_nodos):
        self.grafo = grafo
        self.lista_nodos = lista_nodos
        self.visitados = set()
        self.pila_orden = []
        self.scc_encontradas = []

    def crear_grafo_traspuesto(self):
        """ Invierte la dirección de todas las aristas: O(V + E). """
        grafo_traspuesto = {nodo: [] for nodo in self.lista_nodos}
        
        for nodo in self.grafo:
            for vecino in self.grafo[nodo]:
                grafo_traspuesto[vecino].append(nodo)
                
        return grafo_traspuesto

    # --- PASO 1: Obtener Orden de Finalización ---
    def dfs_paso1(self, nodo):
        """ Recorrido en el grafo original para ordenar los nodos. """
        self.visitados.add(nodo)
        
        for vecino in self.grafo.get(nodo, []):
            if vecino not in self.visitados:
                self.dfs_paso1(vecino)
        
        # Una vez que el nodo y todos sus descendientes son visitados, se apila.
        self.pila_orden.append(nodo) 

    # --- PASO 2: Encontrar SCC en el Traspuesto ---
    def dfs_paso2(self, nodo, grafo_traspuesto, componente_actual):
        """ Recorrido en el grafo traspuesto para agrupar nodos. """
        self.visitados.add(nodo)
        componente_actual.append(nodo)
        
        for vecino in grafo_traspuesto.get(nodo, []):
            if vecino not in self.visitados:
                self.dfs_paso2(vecino, grafo_traspuesto, componente_actual)

    # --- Función Principal ---
    def encontrar_scc(self):
        # Reiniciar variables
        self.visitados.clear()
        self.pila_orden = []
        self.scc_encontradas = []

        # 1. Obtener orden de finalización (Paso 1)
        for nodo in self.lista_nodos:
            if nodo not in self.visitados:
                self.dfs_paso1(nodo)
                
        # 2. Crear el grafo traspuesto
        grafo_traspuesto = self.crear_grafo_traspuesto()
        
        # 3. Recorrer el traspuesto en el orden inverso de la pila (Paso 2)
        self.visitados.clear()
        while self.pila_orden:
            nodo = self.pila_orden.pop()
            
            if nodo not in self.visitados:
                componente_actual = []
                self.dfs_paso2(nodo, grafo_traspuesto, componente_actual)
                self.scc_encontradas.append(componente_actual)
                
        return self.scc_encontradas

def kosaraju(grafo, lista_nodos):
    """ Función de llamada simple para la interfaz. """
    solver = KosarajuSCC(grafo, lista_nodos)
    return solver.encontrar_scc()

if __name__ == "__main__":
    # Usando las nuevas variables de prueba BASE
    scc = kosaraju(grafo_dirigido_scc_base, NODOS_SÓLO_DIRIGIDO_BASE)
    print("SCC Kosaraju:", scc)