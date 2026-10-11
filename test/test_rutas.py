import sys

import pandas as pd

sys.path.append("src")

from conocimiento import GRAFO
from reglas import estacion_valida
from busqueda import buscar_ruta
from main import (
    DISTANCIA_POR_TRAMO_METROS,
    TIEMPOS_POR_TRAMO,
    analizar_recorridos,
    calcular_tiempo_ruta,
    crear_tabla_resumen,
    registrar_pedido,
)


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


def test_registrar_pedido_guarda_distancia_y_acumula_pedidos(tmp_path):
    archivo = tmp_path / "datos_recorridos.csv"
    ruta = ["Restaurante", "Calle 1", "Calle 3", "Calle 5", "Cliente"]

    datos = registrar_pedido(ruta, 18, archivo)
    datos = registrar_pedido(ruta, 18, archivo)

    assert datos.iloc[0]["distancia_metros"] == 4 * DISTANCIA_POR_TRAMO_METROS
    assert datos.iloc[0]["tiempo_minutos"] == 18
    assert datos.iloc[0]["cantidad_pedidos"] == 2


def test_crear_tabla_resumen_ordena_por_tiempo():
    datos = pd.DataFrame(
        [
            ["Ruta larga", 80, 19, 1],
            ["Ruta corta", 60, 15, 3],
        ],
        columns=[
            "recorrido",
            "distancia_metros",
            "tiempo_minutos",
            "cantidad_pedidos",
        ],
    )

    resumen = crear_tabla_resumen(datos)

    assert resumen.iloc[0]["recorrido"] == "Ruta corta"
    assert list(resumen.columns) == [
        "recorrido",
        "distancia_metros",
        "tiempo_minutos",
        "cantidad_pedidos",
    ]


def test_analizar_recorridos_calcula_promedio_y_grupos():
    datos = pd.DataFrame(
        [
            ["Ruta corta", 40, 8, 2],
            ["Ruta larga", 100, 25, 5],
        ],
        columns=[
            "recorrido",
            "distancia_metros",
            "tiempo_minutos",
            "cantidad_pedidos",
        ],
    )

    analisis, estadisticas = analizar_recorridos(datos)

    assert estadisticas["distancia_promedio"] == 70
    assert estadisticas["tiempo_promedio"] == 16.5
    assert estadisticas["recorrido_mas_rapido"]["recorrido"] == "Ruta corta"
    assert estadisticas["recorrido_mas_lento"]["recorrido"] == "Ruta larga"
    assert estadisticas["kmeans_disponible"]
    assert analisis["grupo_kmeans"].nunique() == 2