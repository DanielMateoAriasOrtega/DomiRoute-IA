import heapq


def heuristica(actual, destino):
    """
    Estimación sencilla de la distancia entre dos puntos.
    """
    posiciones = {
        "Restaurante": 0,
        "Calle 1": 1,
        "Calle 2": 2,
        "Calle 3": 2,
        "Calle 4": 3,
        "Calle 5": 3,
        "Cliente": 4
    }

    return abs(posiciones[actual] - posiciones[destino])


def buscar_ruta(grafo, inicio, destino):
    """
    Busca la ruta utilizando el algoritmo A*.
    """

    cola = []

    heapq.heappush(cola, (0, inicio))

    costos = {
        inicio: 0
    }

    anteriores = {
        inicio: None
    }

    while cola:

        _, actual = heapq.heappop(cola)

        if actual == destino:
            break

        for vecino in grafo.get(actual, []):

            nuevo_costo = costos[actual] + 1

            if vecino not in costos or nuevo_costo < costos[vecino]:

                costos[vecino] = nuevo_costo

                prioridad = (
                    nuevo_costo
                    + heuristica(vecino, destino)
                )

                heapq.heappush(
                    cola,
                    (prioridad, vecino)
                )

                anteriores[vecino] = actual

    if destino not in anteriores:
        return None

    ruta = []

    actual = destino

    while actual is not None:

        ruta.append(actual)

        actual = anteriores[actual]

    ruta.reverse()

    return ruta