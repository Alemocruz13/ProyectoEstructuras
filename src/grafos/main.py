print("Proyecto Grafos funcionando")
#estructura de datos para representar un grafo
grafo={
    'A': ['B','C'],
    'B':['D'],
    'C': ['E'],
    'D': ['F'],
    'E': ['F'],
    'F': []
}

#inician algoritmos de recorrido

#BFS
from collections import deque

def bfs(grafo, nodo_inicial):
    cola=deque([nodo_inicial])
    visitados={nodo_inicial}
    orden_recorrido=[]
    print(f"---Ejecutando BFS desde el nodo {nodo_inicial}---")
    while cola:
        nodo_actual=cola.popleft()
        orden_recorrido.append(nodo_actual)
        print(f"Visitando nodo: {nodo_actual}")
        
        #iterar sobre los vecinos
        for vecino in grafo.get(nodo_actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                #se afrega el vecino a la cola
                cola.append(vecino)
    return orden_recorrido
#ejecutar BFS
recorrido_bfs=bfs(grafo, 'A')
print(f"\nRecorrido BFS: {recorrido_bfs}")

#DFS
def dfs_iterativo(grafo, nodo_inicial):
    pila=[nodo_inicial]
    visitados=set()
    orden_recorrido=[]
    print(f"\n---Ejecutando DFS desde el nodo {nodo_inicial}---")
    while pila:
        nodo_actual=pila.pop()
        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            orden_recorrido.append(nodo_actual)
            print(f"Visitando nodo: {nodo_actual}")
            
            for vecino in reversed(grafo.get(nodo_actual,[])):
                if vecino not in visitados:
                    pila.append(vecino)
    return orden_recorrido
#ejecutar DFS
recorrido_dfs=dfs_iterativo(grafo,'A')
print(f"\nRecorrido DFS: {recorrido_dfs}")
#fin de los algoritmos de recorrido
