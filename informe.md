# Informe del Proyecto: Cazador Genético de Errores de Búsqueda

---

## §1 Representación del dominio y validación de candidatos

La formulación de la generación de pruebas como un problema de optimización se estructuró mediante una representación cromosómica basada en grafos dirigidos sintéticos. El dominio de búsqueda fija el nodo de inicio en 0 y la meta en 5. El genotipo de cada individuo almacena las aristas en un diccionario cuyas claves corresponden a pares dirigidos de nodos en formato de tupla y cuyos valores son costos numéricos generados del 1 al 9, con un límite máximo de 30 aristas. La tupla de tres elementos que incluye origen, destino y costo se reserva exclusivamente para la interfaz externa de comunicación con el evaluador.

Los operadores de variación producen individuos válidos por diseño, un comportamiento respaldado por la prueba unitaria `test_cruce_y_mutacion_preservan_dominio`. La función `validar_estructura` (`evaluador.py:37`, `cromosoma.py:56`) lanza un error ante anomalías estructurales; rechaza los lazos mediante `PARES_VALIDOS` y detecta duplicados guardando pares de aristas en un conjunto de control. Los ciclos y los grafos sin ruta ejecutable no se consideran cromosomas mal formados, sino candidatos válidos dentro del espacio de búsqueda.

---

## §2 Operadores genéticos y proceso evolutivo

El proceso evolutivo opera con una población de 50 individuos y se rige por una selección por torneo con un parámetro `k` de 3, donde los empates de aptitud se resuelven mediante el orden de índices derivado del muestreo estocástico previo. El operador de cruzamiento combina las colecciones de aristas de ambos progenitores sin alterar las constantes de inicio y meta, seleccionando un número `k` de aristas acotado entre los límites del padre menor y el mayor. Para las aristas compartidas, la resolución de conflictos de costos se realiza asignando una probabilidad del 50% de heredar el peso de cualquiera de los dos padres (`algoritmo_genetico.py:45`).

La mutación se aplica con una probabilidad del 20% (`prob_mutacion = 0.2`), eligiendo uniformemente entre reasignar el costo de una arista existente, insertar una nueva o eliminar una existente. Dado que la heurística provista por el paquete docente es nula con la tupla de ceros, el algoritmo A* opera sin ventaja informada, diferenciándose de la búsqueda de costo uniforme `U1` exclusivamente por su defecto lógico interno y no por alteraciones de admisibilidad. La población se actualiza mediante un reemplazo generacional con elitismo de 1, permitiendo la persistencia de clones tras tres reintentos de mutación forzada. La condición de parada se activa al agotar el presupuesto total de evaluaciones (`algoritmo_genetico.py:90`), operando bajo un límite operativo de 100 expansiones por agente.

---

## §3 Función de aptitud y evaluación semántica

La aptitud se estructura en un esquema jerárquico de tres niveles orientados a premiar el descubrimiento de fallos y guiar la optimización:

1. Nivel Principal: Multiplica 1000 por la cantidad `k` de agentes delatados, sumando el valor de simplicidad.
2. Nivel Intermedio: Suma 100 más 10 multiplicado por el número de rutas simples válidas, más la simplicidad. Se aplica cuando el grafo posee al menos una ruta ejecutable sin errores; premia aquellos grafos que presentan múltiples rutas alternativas, ya que es en estas topologías ramificadas donde los fallos de optimalidad tienden a manifestarse.
3. Nivel Base: Asigna un bono de simplicidad proporcional al límite de aristas menos las aristas actuales. Los grafos sin solución caen en este nivel. El bono de simplicidad actúa de forma transversal en todos los niveles como mecanismo de desempate.

El sistema de manejo de excepciones aísla los errores mediante bloques de captura: los fallos propios del adaptador se registran como incidencias de equipo con aptitud de cero, mientras que los errores internos de los agentes evaluados se gestionan directamente a través del paquete docente sin penalizar al cromosoma generador.

La evaluación semántica verifica que la ruta propuesta comience y termine en los nodos correctos, utilice aristas existentes, declare un costo aritméticamente consistente con la suma de las aristas y mantenga la optimalidad frente a una referencia propia basada en búsqueda en amplitud BFS y Dijkstra (`verificacion.py:8-34, 37-64`). El criterio de optimalidad se aplica según la naturaleza de cada agente: `B1` se juzga evaluando la minimización del número de aristas, mientras que `U1` y `A1` se evalúan bajo el criterio de costo mínimo. Además, el sistema acepta rutas alternativas de idéntica calidad mediante una comparación por valor numérico y no por identidad de ruta, respaldado por la prueba `test_rutas_alternativas_de_igual_calidad`. En las 10 ejecuciones principales, el clasificador registró cero desacuerdos frente al oráculo docente (`evaluador.py:52-56`).

---

## §4 Comparación experimental

El experimento evaluó el algoritmo genético frente a una línea base de búsqueda aleatoria utilizando un presupuesto estricto de 1,000 evaluaciones y 5 semillas controladas de 11, 22, 33, 44 y 55.

| Método | Objetivo | Ejec. con hallazgo | Mediana evals (éxitos) | Ejec. sin hallazgo | Grafos distintos | Incidencias | Tiempo total (s) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Genético | `B1` | 5/5 | 26 | 0 | 4,994 | 0 | 1.526 |
| Genético | `U1` | 5/5 | 5 | 0 | 4,994 | 0 | 1.526 |
| Genético | `A1` | 5/5 | 5 | 0 | 4,994 | 0 | 1.526 |
| Aleatorio | `B1` | 5/5 | 26 | 0 | 4,841 | 0 | 1.358 |
| Aleatorio | `U1` | 5/5 | 5 | 0 | 4,841 | 0 | 1.358 |
| Aleatorio | `A1` | 5/5 | 5 | 0 | 4,841 | 0 | 1.358 |

> **Nota metodológica y limitaciones:** Ambas estrategias comparten el flujo estocástico inicial durante las primeras cincuenta evaluaciones al invocar globalmente la misma semilla y generación base, lo que explica la coincidencia en el número de evaluaciones del primer hallazgo en 4 de las 5 semillas. Los valores de grafos distintos corresponden a la suma acumulada a lo largo de las 5 ejecuciones. Las cero incidencias se deben a que, con grafos de 6 nodos, el máximo de expansiones observado en nuestros registros fue 5, manteniéndose muy por debajo del límite operativo de 100.
> El algoritmo genético alcanza una aptitud final por semilla de 3,015 a 3,020 puntos con 10 a 15 aristas, frente a los 3,013 a 3,022 puntos de la búsqueda aleatoria con 8 a 17 aristas. La causa es que el cruzamiento muestrea `k` entre los límites de los padres, impidiendo reducir el tamaño por debajo del progenitor menor, y únicamente la mutación de eliminación reduce el tamaño en un 6.7%, mientras que la búsqueda aleatoria sortea `k` de forma uniforme entre 0 y 30.

---

## §5 Contraejemplos representativos

Los contraejemplos almacenados en la carpeta `contraejemplos/` documentan los incumplimientos semánticos capturados por el sistema:

| Caso | Objetivo | Método | Semilla | Evaluación | Aristas | Heurística | Referencia | Resultado | Discrepancia | Reproducido |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `caso_01` | `B1` | Genético | 33 | 12 | 10 | No aplica | Mínimo 2 aristas | 3 aristas (costo 10) | `no_optimo` | Sí |
| `caso_02` | `B1` | Aleatorio | 11 | 833 | 8 | No aplica | Mínimo 2 aristas | 3 aristas (costo 9) | `no_optimo` | Sí |
| `caso_03` | `U1` | Genético | 11 | 34 | 9 | No aplica | Costo mínimo 9 | Costo 11 | `no_optimo` | Sí |
| `caso_04` | `U1` | Aleatorio | 55 | 235 | 8 | No aplica | Costo mínimo 8 | Costo 9 | `no_optimo` | Sí |
| `caso_05` | `A1` | Genético | 44 | 111 | 9 | `(0,0,0,0,0,0)` | Costo mínimo 3 | Costo 9 | `no_optimo` | Sí |
| `caso_06` | `A1` | Aleatorio | 55 | 289 | 6 | `(0,0,0,0,0,0)` | Costo mínimo 19 | Costo 24 | `no_optimo` | Sí |

Un caso ilustrativo es el `caso_01` para `B1`, donde el número mínimo de aristas de referencia es 2, pero el agente devolvió un camino con 3 aristas cuyo costo total es 10; dado que el costo numérico coincide con el óptimo, el grafo delata al agente exclusivamente porque `B1` se evalúa bajo el criterio de conteo de aristas. En el `caso_05` para `A1`, el costo óptimo de referencia es 3 y el agente devuelve un costo de 9. Las causas raíz identificadas en el código docente dentro de `objetivos.py` son: `B1` extrae nodos mediante una pila en lugar de una cola (`objetivos.py:12`); `U1` retorna de forma prematura al generar el nodo meta sin comprobar la optimalidad de costos globales (`objetivos.py:37`); y `A1` descarta erróneamente nodos ya descubiertos bajo condiciones específicas de control (`objetivos.py:38-39`).

---

## §6 Reflexión conceptual y limitaciones

El proyecto opera sobre una distinción fundamental entre dos espacios de búsqueda: por un lado, el meta-espacio de topologías y costos explorado por el algoritmo evolutivo, donde cada grafo constituye un candidato evaluado mediante una función objetivo y manipulado por operadores estructurales; por el otro, el espacio de estados en el que opera cada agente, buscando una secuencia de nodos sobre una topología fija que no puede modificar.

Históricamente, la generación automática de contraejemplos se vincula con la tensión entre posturas opuestas. Por un lado, el criterio conductual de Alan Turing (1950) postula que si la conducta observable de un sistema es indistinguible de la de un humano, eso basta para atribuirle competencia. Por otro lado, el argumento de la Habitación China de John Searle (1980) sostiene que seguir reglas sintácticas puras no equivale a tener una comprensión real del significado. Esto contrasta con la propuesta clásica de John McCarthy (1959), quien defendía que la inteligencia artificial requiere representaciones declarativas y razonamiento basado en sentido común. Nuestro algoritmo evolutivo carece por completo de dicho razonamiento declarativo, funcionando como un optimizador de caja negra guiado por retroalimentación numérica.

El equipo seleccionó el enfoque evolutivo debido a que no requiere un modelo analítico formal del código objetivo; al tratar al sistema evaluado como una caja negra, únicamente necesita poder ejecutarlo y verificar sus salidas frente a un oráculo de referencia.

---

## §7 Contribuciones y recursos


* **Christopher Karol Trejo Ganzo:** Estructura cromosómica en `cromosoma.py`, validación y adaptador docente. Revisó la integración de Misael.
* **Misael Bahena Vargas:** Proceso evolutivo en `algoritmo_genetico.py`, operadores y función de aptitud en `aptitud.py`. Revisó los scripts de Mauricio.
* **Mauricio Rodríguez Gaytan:** Línea base aleatoria en `busqueda_aleatoria.py` y ejecución de pruebas en `test_proyecto.py`. Revisó las estructuras de Christopher.
* **Luis Angel Arteaga Castillo:** Procesamiento de registros JSON y CSV y colección de contraejemplos. Revisó la clasificación con Yahir.
* **Yahir Rodríguez Zamora:** Clasificación semántica y casos de prueba. Revisó la exportación con Luis Angel.

**Recursos externos y bibliografía:**

* Entorno de desarrollo y bibliotecas de la biblioteca estándar de Python 3 (`random`, `json`, `csv`, `collections`, `heapq`, `statistics`).
* McCarthy, J. (1959). Programs with Common Sense. Proceedings of a Symposium Held at the National Physical Laboratory.
* Russell, S., & Norvig, P. (2020). Inteligencia Artificial: Un Enfoque Moderno (4ª ed., Capítulo 3). Pearson.
* Searle, J. R. (1980). Minds, brains, and programs. Behavioral and Brain Sciences, 3(3), 417-424.
* Turing, A. M. (1950). Computing machinery and intelligence. Mind, 59(236), 433-460.