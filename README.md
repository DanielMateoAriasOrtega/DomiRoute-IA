# DomiRoute IA

## Descripción

DomiRoute IA es un sistema inteligente desarrollado en Python que permite encontrar una ruta entre un punto de origen y un punto de destino.

El proyecto utiliza una base de conocimiento representada mediante conexiones entre diferentes lugares, reglas lógicas y el algoritmo de búsqueda heurística A*.

## Objetivo

Desarrollar un sistema basado en conocimiento que permita encontrar una ruta para la entrega de un domicilio entre un restaurante y un cliente.

## Tecnologías

* Python
* Algoritmo A*
* pandas
* Matplotlib
* scikit-learn (K-Means)
* Pytest
* Git
* GitHub

## Funcionamiento

El sistema recibe un lugar de origen y un lugar de destino.

Primero verifica que los lugares existan en la base de conocimiento.

Después utiliza el algoritmo A* para encontrar una ruta entre los dos puntos.

## Base de conocimiento

El sistema representa los lugares y sus conexiones mediante un grafo.

Ejemplo:

Restaurante → Calle 1

Calle 1 → Calle 2

Calle 1 → Calle 3

## Reglas lógicas

El sistema utiliza reglas para:

* Comprobar si un lugar existe.
* Comprobar si existe una conexión.
* Obtener los lugares conectados.

## Búsqueda heurística

Se utiliza el algoritmo A*.

La función de evaluación utiliza:

**f(n) = g(n) + h(n)**

Donde:

* **g(n)** representa el costo acumulado.
* **h(n)** representa una estimación del costo restante.
* **f(n)** representa el costo estimado de la ruta.

## Ejecución

Desde la terminal ejecutar:

```bash
python src/main.py
```

## Análisis de recorridos

Cada tramo del mapa se considera de 20 metros. Los tiempos se estiman con los
valores definidos en `src/main.py`. Cada vez que se consulta una ruta válida,
el sistema cuenta esa consulta como un pedido y guarda o actualiza el recorrido
en `datos_recorridos.csv`.

El resumen compara los recorridos registrados por distancia, tiempo y cantidad
de pedidos; además muestra promedios y las rutas más rápida y más lenta. K-Means
agrupa los recorridos usando esas tres métricas normalizadas. Se requieren al
menos dos recorridos distintos para formar grupos. El gráfico relaciona
distancia y tiempo, distingue los grupos por color y representa la cantidad de
pedidos con el tamaño de cada punto; se guarda como `analisis_recorridos.png`.

Instala las dependencias del proyecto con:

```bash
python -m pip install -r requirements.txt
```

## Pruebas

Para ejecutar las pruebas:

```bash
pytest
```

El proyecto incluye pruebas para verificar lugares existentes, lugares inexistentes y búsqueda de rutas.

## Autor

Daniel Mateo Arias Ortega
