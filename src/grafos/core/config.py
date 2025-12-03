# core/config.py
"""
Configuración global del grafo. Este módulo almacena y expone
la estructura de configuración que usa la GUI y crear_grafo.py
"""
from dataclasses import dataclass, field

@dataclass
class GrafoConfig:
    representacion: str = None  # "Lista de Adyacencia" / "Matriz de Adyacencia" / "Matriz de Incidencia"
    dirigido: bool = False
    ponderado: bool = False
    n: int = 0
    aristas: str = ""  # texto con líneas "u v [w]"

# instancia global
grafo_config = GrafoConfig()
