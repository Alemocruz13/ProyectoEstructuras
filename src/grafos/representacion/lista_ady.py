class ListaAdyacencia:
    def __init__(self, n, dirigido=False):
        self.n = n
        self.es_dirigido = dirigido
        # La lista almacena listas de vecinos, por defecto NO PONDERADO
        self.lista = [[] for _ in range(n)] 
        # Variable para llevar conteo de aristas (necesario para is_tree)
        self.num_aristas = 0 

    def add_edge(self, u, v, peso=1):
        """ Añade una arista (u -> v). Ignoramos el peso para BFS/DFS simple. """
        
        if u < 0 or u >= self.n or v < 0 or v >= self.n:
            raise ValueError("Nodo fuera de rango (0 a n-1)")

        # Evitar duplicados antes de añadir (buena práctica)
        if v not in self.lista[u]:
            self.lista[u].append(v)
            self.num_aristas += 1

            if not self.es_dirigido:
                # La arista inversa (v -> u)
                if u not in self.lista[v]:
                    self.lista[v].append(u)
                    # No sumamos num_aristas aquí, ya que es la misma arista lógica
    
    def get_num_aristas(self):
        """ Devuelve el número total de aristas lógicas. """
        return self.num_aristas

    def vecinos(self, u):
        """ Devuelve la lista de nodos vecinos de u. """
        return self.lista[u]

    def __str__(self):
        """ Representación en string de la lista de adyacencia. """
        resultado = "Lista de Adyacencia:\n"
        for i in range(self.n):
            resultado += f"Nodo {i}: {self.lista[i]}\n"
        resultado += f"Total de Nodos (n): {self.n}\n"
        resultado += f"Total de Aristas (|E|): {self.num_aristas}"
        return resultado
