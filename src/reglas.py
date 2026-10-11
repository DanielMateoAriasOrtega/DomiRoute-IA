"""Reglas para consultar los lugares y conexiones del grafo."""


def estacion_valida(grafo, estacion):
    """Indica si la estación existe en la base de conocimiento."""
    return estacion in grafo


def existe_conexion(grafo, origen, destino):
    """Indica si hay una conexión directa entre dos estaciones."""
    return destino in grafo.get(origen, [])


def obtener_vecinos(grafo, estacion):
    """Devuelve las estaciones conectadas directamente."""
    return grafo.get(estacion, [])