# 📘 Proyecto Estructuras --- Laboratorio de Grafos

Este proyecto implementa un laboratorio interactivo de grafos
utilizando Python y Tkinter. Permite cargar, visualizar y ejecutar
múltiples algoritmos clásicos de grafos, incluyendo recorridos, caminos
mínimos, componentes, árboles de expansión y algoritmos avanzados de
matching.

## 👥 Integrantes del Equipo

-   Alexis Moreno Cruz
-   Karol Antonio Perea Reyes
-   Luis David Villalobos Cuellar

## 🧰 Tecnologías Utilizadas

-   Python 3.10+
-   Tkinter (interfaz gráfica)
-   Git / GitHub (control de versiones y trabajo colaborativo)

# 🚀 Ejecución del Proyecto

### Requisitos

-   Python 3.10 o superior
-   Tkinter instalado (viene por defecto en Windows y Linux)

### Ejecutar la aplicación

``` bash
python main.py
```

La interfaz gráfica se abrirá automáticamente.

# 📂 Estructura del Proyecto

    ProyectoEstructuras/
    │
    ├── src/
    │   ├── grafos/
    │   │   ├── bfs.py
    │   │   ├── dfs.py
    │   │   ├── dijkstra.py
    │   │   ├── bellman_ford.py
    │   │   ├── tarjan.py
    │   │   ├── kosaraju.py
    │   │   ├── hopcroft_karp.py
    │   │   ├── blossom.py
    │   │   ├── kruskal.py
    │   │   ├── prim.py
    │   │   └── ...
    │   ├── core/
    │   │   ├── crear_grafo.py
    │   │   ├── config.py
    │   │   └── utils.py
    │   └── interfaz/
    │       └── ui.py
    │
    ├── tests/
    │   └── pruebas unitarias
    │
    ├── README.md
    └── main.py

# 🧪 Algoritmos Implementados

### 🔹 Representación de grafos

-   Matriz de adyacencia
-   Lista de adyacencia
-   Matriz de incidencia

### 🔹 Recorridos

-   BFS
-   DFS

### 🔹 Componentes

-   Kosaraju (SCC)
-   Tarjan (SCC)

### 🔹 Caminos mínimos

-   Dijkstra
-   Bellman--Ford

### 🔹 Verificación de árbol

-   Conectividad
-   Detección de ciclos
-   Condición `m = n - 1`

### 🔹 Árboles de expansión

-   Kruskal
-   Prim

### 🔹 Bipartición

-   Verificación de grafo bipartito

### 🔹 Matching (pareo)

-   Matching Greedy
-   Hopcroft--Karp
-   Blossom Algorithm

# 🧩 Funcionalidades Principales

-   Visualización gráfica de nodos y aristas
-   Carga de configuraciones de grafos
-   Ejecución de algoritmos en tiempo real
-   Panel de información con resultados detallados
-   Comparación entre múltiples algoritmos
-   Módulos independientes y mantenibles


# 📜 Licencia

Proyecto académico de la Universidad Autónoma de Aguascalientes. Uso
permitido exclusivamente con fines educativos.
