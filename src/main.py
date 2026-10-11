import matplotlib

# Se usa el backend 'Agg' para que el gráfico pueda generarse en entornos sin GUI.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from conocimiento import GRAFO
from reglas import estacion_valida
from busqueda import buscar_ruta

# Definimos una tabla de tiempos estimados por tramo.
# Cada clave representa un recorrido entre dos estaciones y cada valor
# indica la duración en minutos de ese tramo específico.
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


def calcular_tiempo_ruta(ruta, tiempos_por_tramo):
    """
    Calcula el tiempo total de una ruta y devuelve además el detalle por tramo.
    La ruta se recibe como una lista como: ["A", "B", "C", "D"].
    """
    # Si la ruta está vacía o solo tiene un punto, no hay desplazamiento.
    if not ruta or len(ruta) < 2:
        return 0, []

    tiempo_total = 0
    detalle = []

    # Recorremos cada par consecutivo de la ruta para medir el tiempo de cada tramo.
    for origen, destino in zip(ruta, ruta[1:]):
        # Si el tramo está definido en el diccionario, usamos ese valor.
        # En caso contrario, se toma un tiempo mínimo por defecto para evitar errores.
        tiempo_tramo = tiempos_por_tramo.get(
            (origen, destino),
            tiempos_por_tramo.get((destino, origen), 1)
        )

        tiempo_total += tiempo_tramo
        detalle.append((origen, destino, tiempo_tramo))

    return tiempo_total, detalle


def crear_tabla_resumen(ruta, detalle):
    """
    Convierte el detalle de la ruta a un DataFrame ordenado y lo prepara
    para mostrarse como tabla resumen y para graficarlo.
    """
    # Si no hay detalle, devolvemos un DataFrame vacío con las columnas esperadas.
    if not detalle:
        return pd.DataFrame(columns=["ruta", "origen", "destino", "duracion_minutos"])

    # Convertimos la lista de tuplas a un DataFrame de pandas.
    resumen = pd.DataFrame(
        detalle,
        columns=["origen", "destino", "duracion_minutos"]
    )

    # Añadimos la ruta completa como columna para identificar el recorrido.
    resumen["ruta"] = " -> ".join(ruta)

    # Añadimos una columna de orden para dejar los tramos en el orden real del camino.
    resumen["orden_tramo"] = range(1, len(resumen) + 1)

    # Ordenamos el resumen por tiempo de mayor a menor para visualizar los tramos
    # más costosos primero. Esto facilita la lectura del análisis.
    resumen = resumen[["ruta", "orden_tramo", "origen", "destino", "duracion_minutos"]]
    resumen = resumen.sort_values(by="duracion_minutos", ascending=False, ignore_index=True)

    return resumen


def graficar_resumen_ruta(resumen, ruta):
    """
    Genera un gráfico de barras con la duración de cada tramo de la ruta.
    El gráfico se guarda como imagen en la carpeta del proyecto.
    """
    if resumen.empty:
        return None

    # Creamos la figura y el eje.
    fig, ax = plt.subplots(figsize=(8, 5))

    # Bar chart con la duración de cada tramo.
    ax.bar(
        resumen["destino"],
        resumen["duracion_minutos"],
        color=["#4C72B0", "#55A868", "#C44E52", "#8172B3", "#CCB974"]
    )

    # Etiquetas y título.
    ax.set_title(f"Duración por tramo: {ruta}")
    ax.set_xlabel("Destino")
    ax.set_ylabel("Tiempo (minutos)")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    # Ajustamos el texto para que salga legible en el eje X.
    plt.xticks(rotation=20)
    plt.tight_layout()

    # Guardamos la imagen del gráfico en la raíz del proyecto.
    archivo_grafico = "estadistica_ruta.png"
    plt.savefig(archivo_grafico, dpi=200)
    plt.close(fig)

    return archivo_grafico


def main():
    # Encabezado principal del sistema.
    print("=" * 45)
    print("          DOMIROUTE IA")
    print(" Sistema inteligente de rutas")
    print("=" * 45)

    print("\nLugares disponibles:")

    # Muestra todos los nodos del grafo para que el usuario elija un origen y destino.
    for lugar in GRAFO:
        print("-", lugar)

    # Lectura de entrada del usuario.
    origen = input("\nIngrese el origen: ")
    destino = input("Ingrese el destino: ")

    # Validación del origen.
    if not estacion_valida(GRAFO, origen):
        print("\nEl origen no existe.")
        return

    # Validación del destino.
    if not estacion_valida(GRAFO, destino):
        print("\nEl destino no existe.")
        return

    # Evita rutas vacías cuando el origen y destino son el mismo sitio.
    if origen == destino:
        print("\nEl origen y el destino son iguales.")
        return

    # Búsqueda de la ruta más eficiente entre origen y destino.
    ruta = buscar_ruta(GRAFO, origen, destino)

    if ruta:
        # Calcula la duración total y el detalle por tramo de la ruta encontrada.
        tiempo_total, detalle = calcular_tiempo_ruta(ruta, TIEMPOS_POR_TRAMO)

        # Creamos la tabla resumen usando pandas.
        tabla_resumen = crear_tabla_resumen(ruta, detalle)

        print("\nRuta encontrada:")
        print(" -> ".join(ruta))

        print(f"\nNúmero de tramos: {len(ruta) - 1}")

        # Muestra estadísticas del tiempo por cada tramo del camino.
        print("\nEstadística de duración por camino:")
        for origen_tramo, destino_tramo, tiempo_tramo in detalle:
            print(f"- {origen_tramo} -> {destino_tramo}: {tiempo_tramo} minutos")

        print(f"\nTiempo total estimado: {tiempo_total} minutos")

        # Mostramos la tabla resumen con pandas.
        print("\nTabla resumen (pandas):")
        print(tabla_resumen.to_string(index=False))

        # Generamos la gráfica estadística y guardamos la imagen.
        archivo_grafico = graficar_resumen_ruta(tabla_resumen, " -> ".join(ruta))
        if archivo_grafico:
            print(f"\nGráfico generado: {archivo_grafico}")
    else:
        # Si no existe ruta, se informa al usuario.
        print("\nNo se encontró una ruta.")


if __name__ == "__main__":
    # Ejecuta la aplicación solo cuando se corre directamente este archivo.
    main()