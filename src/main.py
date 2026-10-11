from pathlib import Path

import matplotlib

# Permite guardar gráficos en equipos sin interfaz gráfica.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from busqueda import buscar_ruta
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
ARCHIVO_GRAFICO = Path(__file__).resolve().parent.parent / "analisis_recorridos.png"


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


def registrar_pedido(ruta, tiempo_total, archivo=ARCHIVO_DATOS):
    """Guarda la ruta en CSV o incrementa su cantidad de pedidos."""
    recorrido = " -> ".join(ruta)
    distancia = (len(ruta) - 1) * DISTANCIA_POR_TRAMO_METROS

    if archivo.exists():
        datos = pd.read_csv(archivo)
        # Evita continuar con un CSV incompatible o editado con columnas faltantes.
        if list(datos.columns) != COLUMNAS_RESUMEN:
            raise ValueError(
                f"El archivo {archivo} debe tener estas columnas: "
                f"{', '.join(COLUMNAS_RESUMEN)}"
            )
    else:
        datos = pd.DataFrame(columns=COLUMNAS_RESUMEN)

    coincidencia = datos["recorrido"] == recorrido
    if coincidencia.any():
        # Cada consulta de una ruta cuenta como un nuevo pedido de ese recorrido.
        indice = datos.index[coincidencia][0]
        datos.loc[indice, "cantidad_pedidos"] += 1
        # Actualizamos las métricas por si cambian los tiempos configurados.
        datos.loc[indice, "distancia_metros"] = distancia
        datos.loc[indice, "tiempo_minutos"] = tiempo_total
    else:
        nuevo_registro = pd.DataFrame(
            [{
                "recorrido": recorrido,
                "distancia_metros": distancia,
                "tiempo_minutos": tiempo_total,
                "cantidad_pedidos": 1,
            }]
        )
        datos = pd.concat([datos, nuevo_registro], ignore_index=True)

    datos = datos[COLUMNAS_RESUMEN]
    datos.to_csv(archivo, index=False)
    return datos


def crear_tabla_resumen(datos):
    """Ordena las rutas por tiempo, distancia y volumen de pedidos."""
    if datos.empty:
        return pd.DataFrame(columns=COLUMNAS_RESUMEN)

    return datos.sort_values(
        by=["tiempo_minutos", "distancia_metros", "cantidad_pedidos"],
        ascending=[True, True, False],
        ignore_index=True,
    )


def analizar_recorridos(datos):
    """Calcula promedios, rutas extremas y grupos K-Means."""
    analisis = datos.copy()
    analisis["grupo_kmeans"] = "Sin grupo"

    # K-Means compara distancias, tiempos y pedidos; normalizamos sus escalas
    # porque los metros y la cantidad de pedidos tienen magnitudes diferentes.
    variables = ["distancia_metros", "tiempo_minutos", "cantidad_pedidos"]
    valores = analisis[variables].astype(float)
    cantidad_grupos = min(3, len(analisis), len(valores.drop_duplicates()))

    # Se requieren al menos dos recorridos con valores distintos para agrupar.
    if cantidad_grupos >= 2:
        escalados = StandardScaler().fit_transform(valores)
        modelo = KMeans(n_clusters=cantidad_grupos, random_state=42, n_init=10)
        etiquetas = modelo.fit_predict(escalados)
        analisis["grupo_kmeans"] = [f"Grupo {etiqueta + 1}" for etiqueta in etiquetas]

    estadisticas = {
        "distancia_promedio": datos["distancia_metros"].mean(),
        "tiempo_promedio": datos["tiempo_minutos"].mean(),
        "pedidos_promedio": datos["cantidad_pedidos"].mean(),
        "recorrido_mas_rapido": datos.loc[datos["tiempo_minutos"].idxmin()],
        "recorrido_mas_lento": datos.loc[datos["tiempo_minutos"].idxmax()],
        "kmeans_disponible": cantidad_grupos >= 2,
    }
    return analisis, estadisticas


def graficar_analisis(analisis):
    """Guarda una gráfica de distancia y tiempo; el tamaño representa pedidos."""
    if analisis.empty:
        return None

    fig, ax = plt.subplots(figsize=(10, 6))
    grupos = analisis["grupo_kmeans"].unique()

    # Cada color representa un grupo; cada punto es un recorrido registrado.
    for grupo in grupos:
        seleccion = analisis[analisis["grupo_kmeans"] == grupo]
        ax.scatter(
            seleccion["distancia_metros"],
            seleccion["tiempo_minutos"],
            s=80 + seleccion["cantidad_pedidos"] * 25,
            alpha=0.75,
            label=grupo,
        )

        # Etiquetamos los puntos para poder identificar cada ruta comparada.
        for _, fila in seleccion.iterrows():
            ax.annotate(
                fila["recorrido"],
                (fila["distancia_metros"], fila["tiempo_minutos"]),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=7,
            )

    ax.set_title("Comparación de recorridos agrupados con K-Means")
    ax.set_xlabel("Distancia (metros)")
    ax.set_ylabel("Tiempo estimado (minutos)")
    ax.grid(axis="both", linestyle="--", alpha=0.35)
    ax.legend(title="Grupo")
    ax.text(
        0.01,
        0.01,
        "El tamaño de cada punto representa la cantidad de pedidos.",
        transform=ax.transAxes,
        fontsize=8,
    )
    fig.tight_layout()
    fig.savefig(ARCHIVO_GRAFICO, dpi=200)
    plt.close(fig)
    return ARCHIVO_GRAFICO


def main():
    # Presentamos el sistema y los puntos disponibles.
    print("=" * 45)
    print("          DOMIROUTE IA")
    print(" Sistema inteligente de rutas")
    print("=" * 45)
    print("\nLugares disponibles:")

    for lugar in GRAFO:
        print("-", lugar)

    # Solicitamos el origen y el destino del pedido.
    origen = input("\nIngrese el origen: ")
    destino = input("Ingrese el destino: ")

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

    tiempo_total, detalle = calcular_tiempo_ruta(ruta, TIEMPOS_POR_TRAMO)
    datos = registrar_pedido(ruta, tiempo_total)
    tabla = crear_tabla_resumen(datos)
    analisis, estadisticas = analizar_recorridos(tabla)

    print("\nRuta seleccionada:")
    print(" -> ".join(ruta))
    print(f"Tramos: {len(ruta) - 1}")
    print(f"Distancia estimada: {(len(ruta) - 1) * DISTANCIA_POR_TRAMO_METROS} metros")
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
    print(tabla.to_string(index=False))

    # Comparamos las rutas mediante promedios y extremos de tiempo.
    print("\nAnálisis comparativo:")
    print(f"Distancia promedio: {estadisticas['distancia_promedio']:.1f} metros")
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
        print(analisis[["recorrido", "grupo_kmeans"]].to_string(index=False))
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
