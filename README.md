# DomiRoute-IA 🚀

*Sistema inteligente para la búsqueda, el análisis y la agrupación de rutas de domicilios mediante Python.*

## 📌 Descripción del proyecto

DomiRoute-IA es un proyecto académico desarrollado en Python que permite encontrar rutas entre un restaurante y un cliente, registrar información sobre los recorridos y analizar sus características mediante técnicas de inteligencia artificial.

El sistema representa una red de lugares y conexiones mediante un grafo, utiliza reglas lógicas para validar la información y aplica el algoritmo de búsqueda heurística A* para encontrar recorridos entre un punto de origen y un destino.

Además, incorpora un módulo de análisis de recorridos que permite calcular estadísticas y aplicar el algoritmo K-Means para identificar agrupaciones de rutas con características similares.

El proyecto sirve como base para estudiar los métodos de búsqueda, el aprendizaje no supervisado y la integración de técnicas de aprendizaje automático en un problema de distribución de domicilios.

## 🎯 Objetivo general

Desarrollar un sistema basado en inteligencia artificial que permita encontrar y analizar rutas de entrega de domicilios mediante algoritmos de búsqueda, reglas lógicas y técnicas de agrupamiento.

## 🎯 Objetivos específicos

* Representar una red de recorridos mediante un grafo.
* Implementar el algoritmo A* para encontrar rutas entre diferentes puntos.
* Validar lugares y conexiones mediante una base de conocimiento y reglas lógicas.
* Registrar recorridos y analizar sus distancias, tiempos estimados y cantidades de pedidos.
* Aplicar K-Means para agrupar recorridos según sus características.
* Verificar el funcionamiento del sistema mediante pruebas automatizadas.
* Establecer una base para incorporar modelos de aprendizaje supervisado.

## 🛠️ Tecnologías utilizadas

| Tecnología   | Función                                                 |
| ------------ | ------------------------------------------------------- |
| Python       | Lenguaje principal del proyecto.                        |
| Algoritmo A* | Búsqueda heurística de rutas.                           |
| K-Means      | Agrupamiento de recorridos similares.                   |
| pandas       | Herramienta opcional para el manejo de datos tabulares. |
| CSV          | Almacenamiento de los recorridos registrados.           |
| SVG          | Generación de la gráfica de análisis.                   |
| pytest       | Ejecución de pruebas automatizadas.                     |
| Git          | Control de versiones.                                   |
| GitHub       | Alojamiento del repositorio y colaboración.             |

El agrupamiento K-Means y la generación de la gráfica SVG cuentan con implementaciones que no requieren bibliotecas externas. El programa también dispone de mecanismos alternativos para manejar los datos cuando pandas no está disponible.

## 🧠 Arquitectura del proyecto

El sistema está organizado en módulos para facilitar su mantenimiento y comprensión.

* *src/main.py*: coordina la ejecución, permite consultar rutas, registra recorridos y realiza el análisis estadístico y el agrupamiento.
* *src/conocimiento.py*: contiene la base de conocimiento utilizada para representar los lugares y sus conexiones.
* *src/reglas.py*: implementa las reglas lógicas para validar lugares y conexiones.
* *src/busqueda.py*: contiene la lógica del algoritmo de búsqueda de rutas.
* *test/test_rutas.py*: contiene pruebas automatizadas para comprobar diferentes comportamientos del sistema.
* *datos_recorridos.csv*: almacena los registros de los recorridos analizados.
* *analisis_recorridos.svg*: presenta una visualización de los resultados del análisis.
* *estadistica_ruta.png*: recurso gráfico adicional del proyecto.

## 🗺️ Base de conocimiento

La red de recorridos se representa mediante un grafo compuesto por lugares y conexiones entre ellos.

Un ejemplo simplificado de la estructura es:

text
Restaurante
     |
   Calle 1
   /     \
Calle 2  Calle 3
   |        |
Calle 4   Calle 5
   \        /
     Cliente


Esta representación permite explorar diferentes alternativas para llegar desde el restaurante hasta el cliente.

Cada conexión contiene información utilizada para estimar el costo del recorrido. En el escenario académico actual, cada tramo se considera de 20 metros.

## 📐 Reglas lógicas

El sistema utiliza reglas para validar la información antes de realizar una búsqueda.

Entre sus funciones se encuentran:

* Comprobar si un lugar existe en la base de conocimiento.
* Verificar si existe una conexión entre dos lugares.
* Obtener los lugares conectados con un punto determinado.
* Validar el origen y el destino antes de buscar una ruta.

Estas reglas permiten mantener organizada la información y reducir errores durante la ejecución.

## 🔎 Búsqueda heurística con A*

El algoritmo A* permite encontrar una ruta mediante la combinación del costo acumulado y una estimación del costo restante.

Su función de evaluación se expresa mediante la siguiente fórmula:

$$
f(n)=g(n)+h(n)
$$

Donde:

* *\(g(n)\)* representa el costo acumulado desde el punto de origen hasta el nodo actual.
* *\(h(n)\)* representa la estimación del costo restante hasta el destino.
* *\(f(n)\)* representa el costo estimado total de la ruta que pasa por el nodo actual.

El algoritmo evalúa las alternativas disponibles y utiliza esta función para orientar la búsqueda hacia el destino.

El resultado depende de la estructura del grafo, los costos de las conexiones y la heurística definida en la implementación.

## 📊 Análisis de recorridos

El proyecto registra información de los recorridos consultados y permite analizar sus características principales.

Las variables utilizadas incluyen:

* *Recorrido:* secuencia de lugares por los que pasa la ruta.
* *Distancia:* longitud estimada del recorrido, expresada en metros.
* *Tiempo:* duración estimada, expresada en minutos.
* *Cantidad de pedidos:* número de consultas o pedidos registrados para cada recorrido, según la lógica de la aplicación.

Cada vez que se consulta una ruta válida, el sistema contabiliza la consulta como un pedido y guarda o actualiza el registro correspondiente en datos_recorridos.csv.

El análisis permite obtener:

* Promedio de distancia.
* Promedio de tiempo estimado.
* Promedio de pedidos por recorrido.
* Recorrido con menor tiempo registrado.
* Recorrido con mayor tiempo registrado.
* Agrupaciones de recorridos según sus características.

Los valores representan estimaciones del escenario académico y no incorporan información de tráfico en tiempo real.

## 🤖 Aprendizaje no supervisado: K-Means

DomiRoute-IA implementa el algoritmo K-Means para identificar agrupaciones entre los recorridos registrados.

El algoritmo utiliza variables numéricas como la distancia, el tiempo estimado y la cantidad de pedidos. Estas variables se normalizan para reducir el efecto de las diferencias entre sus escalas.

El procedimiento general consiste en:

1. Obtener los datos de los recorridos.
2. Seleccionar las variables numéricas.
3. Validar y normalizar los valores.
4. Determinar la cantidad de grupos posible según los datos disponibles.
5. Ejecutar el agrupamiento.
6. Asignar cada recorrido a un grupo.
7. Mostrar y analizar los resultados.

Los grupos resultantes permiten identificar recorridos con características similares. Sin embargo, las etiquetas «Grupo 1», «Grupo 2» y otras equivalentes son identificadores, no posiciones de un ranking.

El agrupamiento requiere suficientes recorridos distintos para formar al menos dos grupos. Si los datos disponibles no permiten realizarlo, el sistema puede informar que no se encuentra disponible el análisis.

## 📈 Visualización de resultados

El sistema genera una gráfica en formato SVG que relaciona la distancia con el tiempo estimado de los recorridos.

La visualización utiliza elementos gráficos para distinguir los grupos y representar la cantidad de pedidos de cada registro.

El archivo generado es:

text
analisis_recorridos.svg


Esta gráfica facilita la comparación visual de los recorridos y permite observar posibles similitudes entre ellos.

## 📚 Relación con las actividades académicas

### Actividad 3. Métodos de aprendizaje supervisado

Esta actividad aborda el uso de datos etiquetados para entrenar modelos capaces de predecir una categoría conocida.

Para ampliar DomiRoute-IA con este enfoque, se propone incorporar un árbol de decisión que utilice variables como la distancia, el tiempo y la cantidad de pedidos para predecir una categoría previamente definida.

La implementación debe incluir un conjunto de datos etiquetado, entrenamiento, predicciones, evaluación del modelo y pruebas automatizadas. Si se utilizan etiquetas simuladas, deben identificarse como tales.

*Estado:* el modelo supervisado debe incorporarse y verificarse antes de presentar sus resultados como parte funcional del proyecto.

### Actividad 4. Métodos de aprendizaje no supervisado

Esta actividad se centra en el análisis de datos sin etiquetas previas.

DomiRoute-IA incorpora K-Means para agrupar recorridos según sus características numéricas, lo que permite explorar similitudes y diferencias entre las rutas registradas.

El análisis puede apoyarse en las estadísticas y en la gráfica SVG generada por el sistema.

## ▶️ Requisitos previos

Para ejecutar el proyecto se recomienda contar con:

* Python 3.13 o una versión compatible con el código.
* Una terminal como PowerShell.
* Git, si se desea clonar y gestionar el repositorio.
* pytest para ejecutar las pruebas automatizadas.
* pandas como dependencia opcional para el procesamiento tabular.

## ⚙️ Instalación

Clona el repositorio desde GitHub:

bash
git clone <URL_DEL_REPOSITORIO>


Ingresa en la carpeta del proyecto:

bash
cd DomiRoute-IA


Instala las dependencias declaradas:

bash
python -m pip install -r requirements.txt


Si se utiliza el lanzador de Python de Windows, también puede ejecutarse:

powershell
py -3.13 -m pip install -r requirements.txt


## 🚀 Ejecución del proyecto

Desde la carpeta principal del repositorio, ejecuta:

bash
python src/main.py


En Windows también puedes utilizar:

powershell
py -3.13 src/main.py


El programa solicitará los datos necesarios para consultar un recorrido y mostrará la información disponible según las opciones implementadas.

## 🧪 Pruebas automatizadas

El proyecto utiliza pytest para verificar el funcionamiento de sus componentes.

Para ejecutar las pruebas, utiliza:

bash
python -m pytest -v


En Windows también puedes utilizar:

powershell
py -3.13 -m pytest -v


Las pruebas existentes en test/test_rutas.py cubren comportamientos relacionados con la búsqueda y el análisis de rutas. La cobertura exacta debe revisarse en el código de las pruebas.

Para incorporar los modelos de aprendizaje automático, se recomienda agregar casos de prueba que comprueben el entrenamiento y las predicciones del árbol de decisión, así como la asignación de grupos de K-Means.

## 🛡️ Manejo de dependencias

El archivo requirements.txt declara las dependencias del proyecto.

Actualmente, pandas es opcional para el funcionamiento básico del sistema. Si Windows bloquea una dependencia binaria de pandas, el programa dispone de mecanismos alternativos basados en las herramientas incluidas en Python para trabajar con CSV, tablas y estadísticas.

La búsqueda de rutas, el agrupamiento K-Means y la generación de la gráfica SVG se encuentran implementados de forma que no requieren paquetes externos para esas funciones.

## ⚠️ Limitaciones del proyecto

DomiRoute-IA utiliza una red de recorridos simplificada y tiempos estimados definidos para el ejercicio académico.

El sistema no debe interpretarse como una plataforma comercial de navegación, ya que no incorpora necesariamente tráfico en tiempo real, cierres viales, clima ni otras condiciones externas.

La utilidad de los análisis de aprendizaje automático depende de la cantidad y calidad de los datos disponibles. Los resultados obtenidos con datos simulados deben interpretarse dentro de ese contexto.

## 🔮 Trabajo futuro

Entre las mejoras que podrían incorporarse se encuentran:

* Implementar y evaluar el árbol de decisión para el aprendizaje supervisado.
* Ampliar el conjunto de datos de recorridos.
* Agregar pruebas automatizadas específicas para cada modelo.
* Comparar distintas configuraciones de K-Means.
* Incorporar fuentes de datos reales, cuando estén disponibles.
* Evaluar la aplicación con escenarios de distribución más complejos.
* Documentar las métricas y evidencias de ejecución de los modelos.

## 📖 Referencias

Palma Méndez, J. T. (2008). Inteligencia artificial: métodos, técnicas y aplicaciones. McGraw-Hill España.

Python Software Foundation. (s. f.). Python documentation. https://docs.python.org/3/

pytest. (s. f.). pytest documentation. https://docs.pytest.org/

## 👥 Autoría y colaboración

*Autor:* Daniel Mateo Arias Ortega.

*Colaboradores del proyecto académico:* Esmeralda y Cristian.

*Repositorio:* [Agregar aquí la URL del repositorio de GitHub].

Las contribuciones de cada integrante deben reflejarse en el historial real de Git y GitHub, de acuerdo con el trabajo realizado por cada persona.
