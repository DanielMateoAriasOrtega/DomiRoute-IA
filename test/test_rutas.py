import sys

sys.path.append("src")

from conocimiento import GRAFO
from reglas import estacion_valida
from busqueda import buscar_ruta


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