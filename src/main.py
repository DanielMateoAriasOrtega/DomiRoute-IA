import csv
import html
import math
import random
from pathlib import Path

try:
    import pandas as pd
except ImportError as error:
    pd = None
    ERROR_IMPORTACION_PANDAS = error
else:
    ERROR_IMPORTACION_PANDAS = None

from busqueda import buscar_ruta, buscar_rutas_alternativas
from conocimiento import GRAFO
from reglas import estacion_valida

# Cada conexión entre dos lugares equivale a 20 metros.
DISTANCIA_POR_TRAMO_METROS = 20

# Duración estimada en minutos para cada conexión del mapa.
TIEMPOS_POR_TRAMO = {
    ("Restaurante", "Calle 1"): 3,
    ("Calle 1", "Restaurante"): 3,
    ("Calle 1", "Calle 2"): 5,
    ("Calle 2", "Calle 1"): 5,
    ("Calle 1", "Calle 3"): 4,
    ("Calle 3", "Calle 1"): 4,
    ("Calle 2", "Calle 4"): 6,
    ("Calle 4", "Calle 2"): 6,
    ("Calle 3", "Calle 5"): 6,
    ("Calle 5", "Calle 3"): 6,
    ("Calle 4", "Cliente"): 5,
    ("Cliente", "Calle 4"): 5,
    ("Calle 5", "Cliente"): 5,
    ("Cliente", "Calle 5"): 5,
}

COLUMNAS_RESUMEN = [
    "recorrido",
    "distancia_metros",
    "tiempo_minutos",
    "cantidad_pedidos",
]
ARCHIVO_DATOS = Path(__file__).resolve().parent.parent / "datos_recorridos.csv"
ARCHIVO_GRAFICO = Path(__file__).resolve().parent.parent / "analisis_recorridos.svg"


def calcular_tiempo_ruta(ruta, tiempos_por_tramo):
    """Devuelve el tiempo total y el tiempo de cada conexión de la ruta."""
    if not ruta or len(ruta) < 2:
        return 0, []

    tiempo_total = 0
    detalle = []

    # Sumamos el tiempo estimado de cada par de lugares consecutivos.
    for origen, destino in zip(ruta, ruta[1:]):
        tiempo_tramo = tiempos_por_tramo.get(
            (origen, destino),
            tiempos_por_tramo.get((destino, origen), 1),
        )
        tiempo_total += tiempo_tramo
        detalle.append((origen, destino, tiempo_tramo))

    return tiempo_total, detalle


def registrar_pedido(ruta, tiempo_total, archivo=None):
    """Guarda la ruta en CSV o incrementa su cantidad de pedidos."""
    if archivo is None:
        archivo = ARCHIVO_DATOS

    recorrido = " -> ".join(ruta)
    distancia = (len(ruta) - 1) * DISTANCIA_POR_TRAMO_METROS

    if archivo.exists():
        if pd is not None:
            datos = pd.read_csv(archivo).to_dict(orient="records")
        else:
            with archivo.open("r", newline="", encoding="utf-8-sig") as csv_file:
                datos = list(csv.DictReader(csv_file))

        # Evita continuar con un CSV incompatible o editado con columnas faltantes.
        if datos and list(datos[0].keys()) != COLUMNAS_RESUMEN:
            raise ValueError(
                f"El archivo {archivo} debe tener estas columnas: "
                f"{', '.join(COLUMNAS_RESUMEN)}"
            )
        if not datos:
            with archivo.open("r", newline="", encoding="utf-8-sig") as csv_file:
                columnas = next(csv.reader(csv_file), [])
            if columnas and columnas != COLUMNAS_RESUMEN:
                raise ValueError(
                    f"El archivo {archivo} debe tener estas columnas: "
                    f"{', '.join(COLUMNAS_RESUMEN)}"
                )
    else:
        datos = []

    for fila in datos:
        for columna in ("distancia_metros", "tiempo_minutos", "cantidad_pedidos"):
            try:
                valor = float(fila[columna])
            except (KeyError, TypeError, ValueError) as error:
                raise ValueError(
                    f"El archivo {archivo} contiene un valor inválido "
                    f"en la columna {columna}."
                ) from error
            if columna == "cantidad_pedidos":
                if not valor.is_integer():
                    raise ValueError(
                        f"El archivo {archivo} debe tener cantidades de "
                        "pedidos enteras."
                    )
                fila[columna] = int(valor)
            else:
                fila[columna] = valor

    coincidencia = next(
        (fila for fila in datos if fila["recorrido"] == recorrido),
        None,
    )
    if coincidencia is not None:
        # Cada consulta de una ruta cuenta como un nuevo pedido de ese recorrido.
        coincidencia["cantidad_pedidos"] += 1
        # Actualizamos las métricas por si cambian los tiempos configurados.
        coincidencia["distancia_metros"] = distancia
        coincidencia["tiempo_minutos"] = tiempo_total
    else:
        datos.append(
            {
                "recorrido": recorrido,
                "distancia_metros": distancia,
                "tiempo_minutos": tiempo_total,
                "cantidad_pedidos": 1,
            }
        )

    if pd is not None:
        pd.DataFrame(datos, columns=COLUMNAS_RESUMEN).to_csv(
            archivo,
            index=False,
        )
    else:
        with archivo.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=COLUMNAS_RESUMEN)
            writer.writeheader()
            writer.writerows(datos)
    return datos


def crear_tabla_resumen(datos):
    """Ordena las rutas por tiempo, distancia y volumen de pedidos."""
    if pd is not None:
        return (
            pd.DataFrame(datos, columns=COLUMNAS_RESUMEN)
            .sort_values(
                by=["tiempo_minutos", "distancia_metros", "cantidad_pedidos"],
                ascending=[True, True, False],
                ignore_index=True,
            )
            .to_dict(orient="records")
        )

    return sorted(
        datos,
        key=lambda fila: (
            float(fila["tiempo_minutos"]),
            float(fila["distancia_metros"]),
            -float(fila["cantidad_pedidos"]),
        ),
    )



def imprimir_tabla(datos, columnas):
    """Muestra registros en una tabla alineada en la terminal."""

    filas = []

    for fila in datos:
        valores = []

        for columna in columnas:
            valor = fila[columna]

            if isinstance(valor, float) and valor.is_integer():
                valor = int(valor)

            valores.append(str(valor))

        filas.append(valores)

    anchos = [
        max(
            len(columna),
            max((len(fila[i]) for fila in filas), default=0)
        )
        for i, columna in enumerate(columnas)
    ]

    encabezado = " | ".join(
        columna.ljust(anchos[i])
        for i, columna in enumerate(columnas)
    )

    separador = "-+-".join("-" * ancho for ancho in anchos)

    print(encabezado)
    print(separador)

    for fila in filas:
        print(
            " | ".join(
                valor.ljust(anchos[i])
                for i, valor in enumerate(fila)
            )
        )


def _distancia_cuadrada(punto, centro):
    return sum((valor - referencia) ** 2 for valor, referencia in zip(punto, centro))



def _agrupar_kmeans(valores, cantidad_grupos):
    """Agrupa métricas con K-Means de forma reproducible."""

    if not valores or cantidad_grupos < 2:
        return None

    if any(len(fila) != len(valores[0]) for fila in valores):
        raise ValueError("Todas las filas deben tener las mismas métricas.")

    datos = [
        [float(valor) for valor in fila]
        for fila in valores
    ]

    if any(
        not math.isfinite(valor)
        for fila in datos
        for valor in fila
    ):
        raise ValueError("Las métricas deben ser números finitos.")

    puntos_unicos = sorted(set(tuple(fila) for fila in datos))

    # No puede haber más grupos que puntos diferentes.
    cantidad_grupos = min(cantidad_grupos, len(puntos_unicos))

    if cantidad_grupos < 2:
        return [0] * len(datos)

    cantidad_variables = len(datos[0])

    medias = [
        sum(fila[i] for fila in datos) / len(datos)
        for i in range(cantidad_variables)
    ]

    escalas = [
        math.sqrt(
            sum((fila[i] - medias[i]) ** 2 for fila in datos)
            / len(datos)
        ) or 1.0
        for i in range(cantidad_variables)
    ]

    escalados = [
        [(valor - medias[i]) / escalas[i] for i, valor in enumerate(fila)]
        for fila in datos
    ]

    puntos_escalados_unicos = sorted(set(tuple(fila) for fila in escalados))

    rng = random.Random(42)
    indices = sorted(
        rng.sample(
            range(len(puntos_escalados_unicos)),
            cantidad_grupos,
        )
    )

    centros = [
        list(puntos_escalados_unicos[indice])
        for indice in indices
    ]

    etiquetas = None

    for _ in range(100):
        nuevas_etiquetas = [
            min(
                range(cantidad_grupos),
                key=lambda indice: _distancia_cuadrada(
                    punto,
                    centros[indice],
                ),
            )
            for punto in escalados
        ]

        nuevos_centros = []

        for grupo in range(cantidad_grupos):
            miembros = [
                punto
                for punto, etiqueta in zip(escalados, nuevas_etiquetas)
                if etiqueta == grupo
            ]

            if miembros:
                centro = [
                    sum(punto[i] for punto in miembros) / len(miembros)
                    for i in range(cantidad_variables)
                ]
            else:
                # Evita eliminar un centro si un grupo queda vacío.
                centro = centros[grupo]

            nuevos_centros.append(centro)

        convergio = (
            nuevas_etiquetas == etiquetas
            and nuevos_centros == centros
        )

        etiquetas = nuevas_etiquetas
        centros = nuevos_centros

        if convergio:
            break

    return etiquetas



def analizar_recorridos(datos):
    """Calcula promedios, rutas extremas y grupos K-Means."""

    analisis = [
        {**fila, "grupo_kmeans": "Sin grupo"}
        for fila in datos
    ]

    if not datos:
        estadisticas = {
            "distancia_promedio": None,
            "tiempo_promedio": None,
            "pedidos_promedio": None,
            "recorrido_mas_rapido": None,
            "recorrido_mas_lento": None,
            "kmeans_disponible": False,
        }
        return analisis, estadisticas

    variables = [
        "distancia_metros",
        "tiempo_minutos",
        "cantidad_pedidos",
    ]

    valores = [
        [float(fila[variable]) for variable in variables]
        for fila in analisis
    ]

    vectores_unicos = {tuple(fila) for fila in valores}

    # No crear más grupos que recorridos distintos.
    cantidad_grupos = min(3, len(analisis), len(vectores_unicos))

    if cantidad_grupos >= 2:
        etiquetas = _agrupar_kmeans(valores, cantidad_grupos)

        for fila, etiqueta in zip(analisis, etiquetas):
            fila["grupo_kmeans"] = f"Grupo {etiqueta + 1}"

    def promedio(columna):
        return sum(
            float(fila[columna]) for fila in datos
        ) / len(datos)

    mas_rapido = min(
        datos,
        key=lambda fila: float(fila["tiempo_minutos"]),
    )

    mas_lento = max(
        datos,
        key=lambda fila: float(fila["tiempo_minutos"]),
    )

    estadisticas = {
        "distancia_promedio": promedio("distancia_metros"),
        "tiempo_promedio": promedio("tiempo_minutos"),
        "pedidos_promedio": promedio("cantidad_pedidos"),
        "recorrido_mas_rapido": mas_rapido,
        "recorrido_mas_lento": mas_lento,
        "kmeans_disponible": cantidad_grupos >= 2,
    }

    return analisis, estadisticas


def graficar_analisis(analisis):
    """Guarda una gráfica SVG de distancia y tiempo agrupada por K-Means."""
    if not analisis:
        return None

    ancho, alto = 900, 560
    margen = 90
    distancias = [float(fila["distancia_metros"]) for fila in analisis]
    tiempos = [float(fila["tiempo_minutos"]) for fila in analisis]
    min_x, max_x = min(distancias), max(distancias)
    min_y, max_y = min(tiempos), max(tiempos)
    rango_x = max(max_x - min_x, 1)
    rango_y = max(max_y - min_y, 1)
    colores = ["#2563eb", "#dc2626", "#16a34a"]
    grupos = sorted({fila["grupo_kmeans"] for fila in analisis})
    elementos = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{ancho}" height="{alto}" viewBox="0 0 {ancho} {alto}">',
        "<rect width=\"100%\" height=\"100%\" fill=\"white\"/>",
        '<text x="450" y="35" text-anchor="middle" font-size="20">'
        "Recorridos agrupados con K-Means</text>",
        f'<line x1="{margen}" y1="{alto - margen}" x2="{ancho - margen}" '
        f'y2="{alto - margen}" stroke="#333"/>',
        f'<line x1="{margen}" y1="{margen}" x2="{margen}" '
        f'y2="{alto - margen}" stroke="#333"/>',
        f'<text x="450" y="{alto - 22}" text-anchor="middle">'
        "Distancia (metros)</text>",
        f'<text x="22" y="280" text-anchor="middle" '
        'transform="rotate(-90 22 280)">Tiempo estimado (minutos)</text>',
    ]

    for index, grupo in enumerate(grupos):
        color = colores[index % len(colores)]
        elementos.append(
            f'<circle cx="{ancho - margen - 115}" cy="{65 + index * 24}" '
            f'r="6" fill="{color}"/>'
        )
        elementos.append(
            f'<text x="{ancho - margen - 100}" y="{70 + index * 24}" '
            f'font-size="13">{html.escape(grupo)}</text>'
        )

    for fila in analisis:
        distancia = float(fila["distancia_metros"])
        tiempo = float(fila["tiempo_minutos"])
        x = margen + (distancia - min_x) / rango_x * (ancho - 2 * margen)
        y = alto - margen - (tiempo - min_y) / rango_y * (alto - 2 * margen)
        grupo_index = grupos.index(fila["grupo_kmeans"])
        color = colores[grupo_index % len(colores)]
        radio = 6 + math.sqrt(max(float(fila["cantidad_pedidos"]), 0))
        elementos.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radio:.1f}" '
            f'fill="{color}" fill-opacity="0.75"/>'
        )
        elementos.append(
            f'<text x="{x + radio + 3:.1f}" y="{y:.1f}" '
            f'font-size="10">{html.escape(str(fila["recorrido"]))}</text>'
        )

    elementos.extend(
        [
            '<text x="450" y="540" text-anchor="middle" font-size="11">'
            "El tamaño de cada punto representa la cantidad de pedidos.</text>",
            "</svg>",
        ]
    )
    ARCHIVO_GRAFICO.write_text("\n".join(elementos), encoding="utf-8")
    return ARCHIVO_GRAFICO

#mejora se agrega mejor menu de selección de lugares y se agrega la función para buscar rutas alternativas y compararlas

def seleccionar_lugar(grafo, mensaje, excluido=None):
    """Permite seleccionar un lugar usando números."""

    lugares = [
        lugar for lugar in grafo
        if lugar != excluido
    ]

    while True:
        print(f"\n===== {mensaje.upper()} =====")

        for numero, lugar in enumerate(lugares, start=1):
            print(f"{numero}. {lugar}")

        opcion = input("\nSelecciona un numero: ").strip()

        if opcion.isdigit():
            indice = int(opcion) - 1

            if 0 <= indice < len(lugares):
                elegido = lugares[indice]
                print(f"Seleccionado: {elegido}")
                return elegido

        print("Opcion invalida. Intenta nuevamente.")


def main():
    if pd is None:
        print(
            "\nAviso: pandas no se pudo cargar "
            f"({ERROR_IMPORTACION_PANDAS}). "
            "El programa usará el respaldo CSV de Python."
        )

    # Presentamos el sistema y los puntos disponibles.
    print("=" * 45)
    print("          DOMIROUTE IA")
    print(" Sistema inteligente de rutas")
    print("=" * 45)
    print("\nLugares disponibles:")

    for lugar in GRAFO:
        print("-", lugar)

    # Solicitamos el origen y el destino del pedido.
    # Seleccion del origen mediante menu numerado.
    origen = seleccionar_lugar(
        GRAFO,
        "Seleccionar origen"
    )

    # Seleccion del destino, excluyendo el origen.
    destino = seleccionar_lugar(
        GRAFO,
        "Seleccionar destino",
        excluido=origen
    )

    print("\n===== PEDIDO CONFIGURADO =====")
    print(f"Origen: {origen}")
    print(f"Destino: {destino}")


    # Validamos los lugares antes de iniciar la búsqueda.
    if not estacion_valida(GRAFO, origen):
        print("\nEl origen no existe.")
        return
    if not estacion_valida(GRAFO, destino):
        print("\nEl destino no existe.")
        return
    if origen == destino:
        print("\nEl origen y el destino son iguales.")
        return

    # Buscamos la ruta y calculamos el tiempo y distancia estimados.
    ruta = buscar_ruta(GRAFO, origen, destino)
    if not ruta:
        print("\nNo se encontró una ruta.")
        return

    # agregamos la función para buscar rutas alternativas y compararlas
    
    # Buscar y comparar diferentes recorridos.
    rutas_alternativas = buscar_rutas_alternativas(
        GRAFO, origen, destino
    )

    comparacion = []

    for recorrido in rutas_alternativas:
        minutos, _ = calcular_tiempo_ruta(
            recorrido, TIEMPOS_POR_TRAMO
        )

        distancia = (
            len(recorrido) - 1
        ) * DISTANCIA_POR_TRAMO_METROS

        comparacion.append({
            "ruta": recorrido,
            "tiempo": minutos,
            "distancia": distancia
        })

    # Ordenar desde la ruta más rápida.
    comparacion.sort(
        key=lambda opcion: (
            opcion["tiempo"],
            opcion["distancia"]
        )
    )

    print("\n===== COMPARACION DE RUTAS =====")

    for numero, opcion in enumerate(comparacion, 1):
        print(f"\nRuta {numero}:")
        print(" -> ".join(opcion["ruta"]))
        print(f"Distancia: {opcion['distancia']} metros")
        print(f"Tiempo: {opcion['tiempo']} minutos")

        if numero == 1:
            print(">>> RUTA MAS RAPIDA <<<")

    if len(comparacion) > 1:
        ahorro = (
            comparacion[-1]["tiempo"]
            - comparacion[0]["tiempo"]
        )
        print(f"\nAhorro maximo estimado: {ahorro} minutos")

    print("\n===== FIN DE COMPARACION =====")
    #variable tiempo_total, detalle
    tiempo_total, detalle = calcular_tiempo_ruta(ruta, TIEMPOS_POR_TRAMO)
    datos = registrar_pedido(ruta, tiempo_total)
    tabla = crear_tabla_resumen(datos)
    analisis, estadisticas = analizar_recorridos(tabla)

    print("\nRuta seleccionada:")
    print(" -> ".join(ruta))
    print(f"Tramos: {len(ruta) - 1}")
    distancia = (len(ruta) - 1) * DISTANCIA_POR_TRAMO_METROS
    print(f"Distancia estimada: {distancia} metros")
    print(f"Tiempo estimado: {tiempo_total} minutos")

    # Mostramos las métricas calculadas para cada tramo.
    print("\nDetalle por tramo:")
    for origen_tramo, destino_tramo, tiempo_tramo in detalle:
        print(
            f"- {origen_tramo} -> {destino_tramo}: "
            f"{DISTANCIA_POR_TRAMO_METROS} metros, {tiempo_tramo} minutos"
        )

    # La tabla resume todos los recorridos consultados y sus pedidos acumulados.
    print("\nTabla resumen de recorridos:")
    imprimir_tabla(tabla, COLUMNAS_RESUMEN)

    # Comparamos las rutas mediante promedios y extremos de tiempo.
    print("\nAnálisis comparativo:")
    print(
        f"Distancia promedio: "
        f"{estadisticas['distancia_promedio']:.1f} metros"
    )
    print(f"Tiempo promedio: {estadisticas['tiempo_promedio']:.1f} minutos")
    print(f"Pedidos promedio por recorrido: {estadisticas['pedidos_promedio']:.1f}")
    print(
        "Recorrido más rápido: "
        f"{estadisticas['recorrido_mas_rapido']['recorrido']} "
        f"({estadisticas['recorrido_mas_rapido']['tiempo_minutos']} minutos)"
    )
    print(
        "Recorrido más lento: "
        f"{estadisticas['recorrido_mas_lento']['recorrido']} "
        f"({estadisticas['recorrido_mas_lento']['tiempo_minutos']} minutos)"
    )

    # Informamos si hay suficiente historial para que K-Means compare grupos.
    if estadisticas["kmeans_disponible"]:
        print("\nClasificación K-Means:")
        imprimir_tabla(analisis, ["recorrido", "grupo_kmeans"])
    else:
        print(
            "\nK-Means necesita al menos dos recorridos registrados con "
            "métricas diferentes. Consulta otras rutas para crear grupos."
        )

    archivo_grafico = graficar_analisis(analisis)
    if archivo_grafico:
        print(f"\nGráfico generado: {archivo_grafico}")
    print(f"Historial guardado en: {ARCHIVO_DATOS}")


if __name__ == "__main__":
    # Inicia el programa solo al ejecutar este archivo directamente.
    main()
