import csv
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from busqueda import buscar_ruta
from conocimiento import GRAFO
from reglas import estacion_valida
import main as aplicacion
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
    ruta = buscar_ruta(GRAFO, "Restaurante", "Cliente")
    assert ruta is not None


def test_ruta_comienza_correctamente():
    ruta = buscar_ruta(GRAFO, "Restaurante", "Cliente")

    assert ruta is not None
    assert ruta[0] == "Restaurante"
    assert ruta[-1] == "Cliente"


def test_calcular_tiempo_ruta():
    ruta = [
        "Restaurante",
        "Calle 1",
        "Calle 3",
        "Calle 5",
        "Cliente",
    ]

    tiempo_total, detalle = calcular_tiempo_ruta(
        ruta, TIEMPOS_POR_TRAMO
    )

    assert tiempo_total == 18
    assert detalle == [
        ("Restaurante", "Calle 1", 3),
        ("Calle 1", "Calle 3", 4),
        ("Calle 3", "Calle 5", 6),
        ("Calle 5", "Cliente", 5),
    ]


def test_registrar_pedido_guarda_distancia_y_acumula_pedidos(
    tmp_path,
):
    archivo = tmp_path / "datos_recorridos.csv"

    ruta = [
        "Restaurante",
        "Calle 1",
        "Calle 3",
        "Calle 5",
        "Cliente",
    ]

    registrar_pedido(ruta, 18, archivo)
    datos = registrar_pedido(ruta, 18, archivo)

    assert datos[0]["distancia_metros"] == (
        4 * DISTANCIA_POR_TRAMO_METROS
    )
    assert datos[0]["tiempo_minutos"] == 18
    assert datos[0]["cantidad_pedidos"] == 2
    with archivo.open(newline="", encoding="utf-8") as archivo_csv:
        registros_csv = list(csv.DictReader(archivo_csv))
    assert registros_csv[0]["cantidad_pedidos"] == "2"


def test_crear_tabla_resumen_ordena_por_tiempo():
    datos = [
        {
            "recorrido": "Ruta larga",
            "distancia_metros": 80,
            "tiempo_minutos": 19,
            "cantidad_pedidos": 1,
        },
        {
            "recorrido": "Ruta corta",
            "distancia_metros": 60,
            "tiempo_minutos": 15,
            "cantidad_pedidos": 3,
        },
    ]

    resumen = crear_tabla_resumen(datos)

    assert resumen[0]["recorrido"] == "Ruta corta"
    assert list(resumen[0]) == [
        "recorrido", "distancia_metros", "tiempo_minutos", "cantidad_pedidos"
    ]


def test_analizar_recorridos_calcula_promedio_y_grupos():
    datos = [
        {
            "recorrido": "Ruta corta",
            "distancia_metros": 40,
            "tiempo_minutos": 8,
            "cantidad_pedidos": 2,
        },
        {
            "recorrido": "Ruta larga",
            "distancia_metros": 100,
            "tiempo_minutos": 25,
            "cantidad_pedidos": 5,
        },
    ]

    analisis, estadisticas = analizar_recorridos(datos)

    assert estadisticas["distancia_promedio"] == 70
    assert estadisticas["tiempo_promedio"] == 16.5
    assert (
        estadisticas["recorrido_mas_rapido"]["recorrido"]
        == "Ruta corta"
    )
    assert (
        estadisticas["recorrido_mas_lento"]["recorrido"]
        == "Ruta larga"
    )
    assert estadisticas["kmeans_disponible"]
    assert len({fila["grupo_kmeans"] for fila in analisis}) == 2


def test_analizar_recorridos_vacio_no_falla():
    datos = []

    analisis, estadisticas = analizar_recorridos(datos)

    assert analisis == []
    assert estadisticas["distancia_promedio"] is None
    assert estadisticas["tiempo_promedio"] is None
    assert estadisticas["pedidos_promedio"] is None
    assert estadisticas["recorrido_mas_rapido"] is None
    assert estadisticas["recorrido_mas_lento"] is None
    assert not estadisticas["kmeans_disponible"]


def test_aplicacion_completa_guarda_csv_y_grafica(tmp_path, monkeypatch):
    archivo_datos = tmp_path / "datos_recorridos.csv"
    archivo_grafico = tmp_path / "analisis_recorridos.svg"
    monkeypatch.setattr(aplicacion, "ARCHIVO_DATOS", archivo_datos)
    monkeypatch.setattr(aplicacion, "ARCHIVO_GRAFICO", archivo_grafico)
    respuestas = iter(["1", "6"])
    monkeypatch.setattr("builtins.input", lambda _: next(respuestas))

    aplicacion.main()

    assert archivo_datos.exists()
    assert archivo_grafico.exists()
    assert "<svg" in archivo_grafico.read_text(encoding="utf-8")