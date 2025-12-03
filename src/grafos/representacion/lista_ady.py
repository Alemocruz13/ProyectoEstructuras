class ListaAdyacencia:
    def __init__(self, n, dirigido=False, ponderado=False):
        self.n = n
        self.es_dirigido = dirigido
        self.es_ponderado = ponderado

        # Nodos estándar → 0..n-1
        self.nodos = list(range(n))

        # Mapas requeridos por el sistema modular
        self.indice = {i: i for i in range(n)}       # nodo → índice
        self.reverso = {i: i for i in range(n)}      # índice → nodo

        # Lista de adyacencia
        self.lista = [[] for _ in range(n)]

        # Contador de aristas (solo las lógicas)
        self.num_aristas = 0

    def add_edge(self, u, v, peso=None):
        """Añade una arista al grafo, manejando pesos y dirección."""

        if u < 0 or u >= self.n or v < 0 or v >= self.n:
            raise ValueError("Nodo fuera de rango (0 a n-1)")

        # ----------------------------
        #  NO PONDERADO
        # ----------------------------
        if not self.es_ponderado:

            # evitar duplicados
            if v not in self.lista[u]:
                self.lista[u].append(v)
                self.num_aristas += 1

            if not self.es_dirigido:
                if u not in self.lista[v]:
                    self.lista[v].append(u)

        # ----------------------------
        #  PONDERADO
        # ----------------------------
        else:
            if (v, peso) not in self.lista[u]:
                self.lista[u].append((v, peso))
                self.num_aristas += 1

            if not self.es_dirigido:
                if (u, peso) not in self.lista[v]:
                    self.lista[v].append((u, peso))

    def get_num_aristas(self):
        return self.num_aristas

    def vecinos(self, u):
        """Devuelve lista de vecinos (v) o (v, peso)."""
        return self.lista[u]

    def __str__(self):
        resultado = "Lista de Adyacencia:\n"
        for i in range(self.n):
            resultado += f"{i}: {self.lista[i]}\n"
        resultado += f"Total nodos: {self.n}\n"
        resultado += f"Aristas: {self.num_aristas}\n"
        return resultado
