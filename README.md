# DomiRoute IA

## Descripción

DomiRoute IA es un sistema inteligente desarrollado en Python que permite encontrar una ruta entre un punto de origen y un punto de destino.

El proyecto utiliza una base de conocimiento representada mediante conexiones entre diferentes lugares, reglas lógicas y el algoritmo de búsqueda heurística A*.

## Objetivo

Desarrollar un sistema basado en conocimiento que permita encontrar una ruta para la entrega de un domicilio entre un restaurante y un cliente.

## Tecnologías

* Python
* Algoritmo A*
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

## Pruebas

Para ejecutar las pruebas:

```bash
pytest
```

El proyecto incluye pruebas para verificar lugares existentes, lugares inexistentes y búsqueda de rutas.

## Autor

Daniel Mateo Arias Ortega
