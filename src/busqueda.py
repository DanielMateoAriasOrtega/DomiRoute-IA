import heapq


POSICIONES = {
    "Restaurante": 0,
    "Calle 1": 1,
    "Calle 2": 2,
    "Calle 3": 2,
    "Calle 4": 3,
    "Calle 5": 3,
    "Cliente": 4,
}


def heuristica(actual, destino):
    """Estima la distancia entre dos puntos conocidos."""
    if actual not in POSICIONES or destino not in POSICIONES:
        return 0
    return abs(POSICIONES[actual] - POSICIONES[destino])


def buscar_ruta(grafo, inicio, destino):
    """Busca la ruta de menor cantidad de tramos usando A*."""
    cola = [(0, inicio)]
    costos = {inicio: 0}
    anteriores = {inicio: None}

    while cola:
        _, actual = heapq.heappop(cola)
        if actual == destino:
            break

        for vecino in grafo.get(actual, []):
            nuevo_costo = costos[actual] + 1
            if vecino in costos and nuevo_costo >= costos[vecino]:
                continue

            costos[vecino] = nuevo_costo
            prioridad = nuevo_costo + heuristica(vecino, destino)
            heapq.heappush(cola, (prioridad, vecino))
            anteriores[vecino] = actual

    if destino not in anteriores:
        return None

    ruta = []
    actual = destino
    while actual is not None:
        ruta.append(actual)
        actual = anteriores[actual]

    return list(reversed(ruta))