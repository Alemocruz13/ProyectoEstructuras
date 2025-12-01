class ListaAdyacencia:
    def __init__(self, n, dirigido=False, ponderado=False):
        self.n = n
        self.es_dirigido = dirigido
        self.es_ponderado = ponderado

        # Cada posición tendrá: 
        # - v (no ponderado)
        # - (v, peso) (ponderado)
        self.lista = [[] for _ in range(n)]

        # Contador de aristas lógicas (NO duplicamos en no dirigidos)
        self.num_aristas = 0

    def add_edge(self, u, v, peso=None):
        """Añade una arista al grafo, manejando pesos y dirección."""
        if u < 0 or u >= self.n or v < 0 or v >= self.n:
            raise ValueError("Nodo fuera de rango (0 a n-1)")

        # ----------------------------
        #  NO PONDERADO
        # ----------------------------
        if not self.es_ponderado:

            # Evitar duplicados
            if v not in self.lista[u]:
                self.lista[u].append(v)
                self.num_aristas += 1

            # Si es no dirigido, agregar la arista inversa SIN aumentar aristas
            if not self.es_dirigido:
                if u not in self.lista[v]:
                    self.lista[v].append(u)

        # ----------------------------
        #  PONDERADO
        # ----------------------------
        else:
            # Evitar duplicados ponderados
            if (v, peso) not in self.lista[u]:
                self.lista[u].append((v, peso))
                self.num_aristas += 1

            if not self.es_dirigido:
                if (u, peso) not in self.lista[v]:
                    self.lista[v].append((u, peso))

    def get_num_aristas(self):
        return self.num_aristas

    def vecinos(self, u):
        """Devuelve la lista interna (puede ser v o (v,peso))."""
        return self.lista[u]

    def __str__(self):
        resultado = "Lista de Adyacencia:\n"
        for i in range(self.n):
            resultado += f"Nodo {i}: {self.lista[i]}\n"

        resultado += f"Total de Nodos (n): {self.n}\n"
        resultado += f"Total de Aristas (|E|): {self.num_aristas}\n"
        return resultado
