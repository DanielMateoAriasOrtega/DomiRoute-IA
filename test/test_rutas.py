import sys

sys.path.append("src")

from conocimiento import GRAFO
from reglas import estacion_valida
from busqueda import buscar_ruta
from main import calcular_tiempo_ruta, TIEMPOS_POR_TRAMO, crear_tabla_resumen


def test_lugar_existente():
    assert estacion_valida(GRAFO, "Restaurante")


def test_lugar_inexistente():
    assert not estacion_valida(GRAFO, "Aeropuerto")


def test_ruta_existente():
    ruta = buscar_ruta(
        GRAFO,
        "Restaurante",
        "Cliente"
    )

    assert ruta is not None


def test_ruta_comienza_correctamente():
    ruta = buscar_ruta(
        GRAFO,
        "Restaurante",
        "Cliente"
    )

    assert ruta[0] == "Restaurante"
    assert ruta[-1] == "Cliente"


def test_calcular_tiempo_ruta():
    ruta = ["Restaurante", "Calle 1", "Calle 3", "Calle 5", "Cliente"]
    tiempo_total, detalle = calcular_tiempo_ruta(ruta, TIEMPOS_POR_TRAMO)

    assert tiempo_total == 18
    assert detalle == [
        ("Restaurante", "Calle 1", 3),
        ("Calle 1", "Calle 3", 4),
        ("Calle 3", "Calle 5", 6),
        ("Calle 5", "Cliente", 5),
    ]


def test_crear_tabla_resumen():
    ruta = ["Restaurante", "Calle 1", "Calle 3", "Calle 5", "Cliente"]
    _, detalle = calcular_tiempo_ruta(ruta, TIEMPOS_POR_TRAMO)
    resumen = crear_tabla_resumen(ruta, detalle)

    assert list(resumen.columns) == [
        "ruta",
        "orden_tramo",
        "origen",
        "destino",
        "duracion_minutos",
    ]
    assert resumen["duracion_minutos"].sum() == 18