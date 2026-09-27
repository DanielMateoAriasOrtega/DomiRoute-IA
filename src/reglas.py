# Reglas lógicas de DomiRoute IA


def estacion_valida(grafo, estacion):
    """
    Comprueba si el lugar existe en la base de conocimiento.
    """
    return estacion in grafo


def existe_conexion(grafo, origen, destino):
    """
    Comprueba si existe una conexión directa.
    """
    return destino in grafo.get(origen, [])


def obtener_vecinos(grafo, estacion):
    """
    Obtiene los lugares conectados directamente.
    """
    return grafo.get(estacion, [])