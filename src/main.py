from conocimiento import GRAFO
from reglas import estacion_valida
from busqueda import buscar_ruta


def main():

    print("=" * 45)
    print("          DOMIROUTE IA")
    print(" Sistema inteligente de rutas")
    print("=" * 45)

    print("\nLugares disponibles:")

    for lugar in GRAFO:
        print("-", lugar)

    origen = input("\nIngrese el origen: ")
    destino = input("Ingrese el destino: ")

    if not estacion_valida(GRAFO, origen):
        print("\nEl origen no existe.")
        return

    if not estacion_valida(GRAFO, destino):
        print("\nEl destino no existe.")
        return

    if origen == destino:
        print("\nEl origen y el destino son iguales.")
        return

    ruta = buscar_ruta(GRAFO, origen, destino)

    if ruta:

        print("\nRuta encontrada:")
        print(" -> ".join(ruta))

        print(
            f"\nNúmero de tramos: {len(ruta) - 1}"
        )

    else:

        print("\nNo se encontró una ruta.")


if __name__ == "__main__":
    main()