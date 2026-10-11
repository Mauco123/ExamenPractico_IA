# Informe del Proyecto: Cazador Genético de Errores de Búsqueda

## 1. Representación, aptitud y operadores genéticos

Para formular la generación de pruebas como un problema de optimización, diseñamos una representación cromosómica basada en grafos dirigidos sintéticos. 
*   **Representación:** Cada individuo (grafo) se codificó como una estructura que contiene un nodo de `inicio` (0-5), un nodo `meta` (0-5), y una lista de `aristas` definidas por tuplas `(origen, destino, costo)`. El validador estructural garantiza que no existan aristas duplicadas y que los costos sean estrictamente positivos, permitiendo grafos insolubles (sin ruta a la meta) como candidatos válidos.
*   **Función de aptitud (Fitness):** Se diseñó para maximizar la probabilidad de encontrar discrepancias entre los agentes evaluados (B1, U1, A1) y el evaluador docente de referencia. La función otorga una puntuación máxima al descubrir un contraejemplo confirmado. Para guiar la búsqueda antes de encontrar un error, premia a los grafos que obligan a los algoritmos a expandir más rutas (mayor estrés). Adicionalmente, incluye un criterio de simplicidad que penaliza levemente la cantidad de aristas, favoreciendo grafos más pequeños y comprensibles en caso de empate.
*   **Operadores genéticos:** Implementamos selección por torneo basada en la aptitud. El cruzamiento (crossover) combina el nodo de inicio de un progenitor, la meta del otro, y realiza una mezcla aleatoria de sus listas de aristas. La mutación introduce variabilidad agregando aristas nuevas, eliminando existentes o modificando pesos, asegurando mantener la integridad del dominio.

## 2. Comparación experimental

El experimento principal consistió en ejecutar tanto el algoritmo genético como una búsqueda aleatoria (línea base) utilizando un presupuesto de 1000 evaluaciones y 5 semillas controladas (11, 22, 33, 44 y 55).

**Tabla de Resultados:**
| Método | Objetivo | Ejecuciones con hallazgo | Mediana evals (solo éxitos) | Ejecuciones sin hallazgo | Grafos distintos | Incidencias | Tiempo total (s) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Genético | B1 | 5/5 | 26 | 0 | 4994 | 0 | 1.614 |
| Genético | U1 | 5/5 | 5 | 0 | 4994 | 0 | 1.614 |
| Genético | A1 | 5/5 | 5 | 0 | 4994 | 0 | 1.614 |
| Aleatorio | B1 | 5/5 | 26 | 0 | 4841 | 0 | 1.470 |
| Aleatorio | U1 | 5/5 | 5 | 0 | 4841 | 0 | 1.470 |
| Aleatorio | A1 | 5/5 | 5 | 0 | 4841 | 0 | 1.470 |

**Análisis:**
Los datos demuestran que ambos métodos lograron un 100% de éxito (5/5) detectando los fallos en B1, U1 y A1. Sorprendentemente, la mediana de evaluaciones necesarias para el primer hallazgo fue idéntica en ambos enfoques: 26 evaluaciones para B1 y apenas 5 evaluaciones para U1 y A1[cite: 2]. El algoritmo genético procesó ligeramente más grafos distintos (4994 frente a 4841 del aleatorio), pero tomó un poco más de tiempo debido a la sobrecarga computacional de la selección y cruzamiento[cite: 2]. Ninguno de los métodos presentó incidencias por límites de tiempo o errores de ejecución[cite: 2].

## 3. Contraejemplos representativos

Alcanzamos los tres objetivos planteados. Los contraejemplos guardados en la carpeta `contraejemplos/` demuestran los siguientes incumplimientos semánticos, capturados programáticamente por nuestro adaptador:
*   **Fallo en B1 (Búsqueda en Amplitud):** Requiere un poco más de exploración (mediana de 26 grafos) para ser revelado. Se detectaron discrepancias en la validación de rutas generadas frente al oráculo.
*   **Fallo en U1 y A1 (Costo Uniforme y A*):** Sus fallos son altamente densos en el espacio de problemas. Con solo generar aleatoriamente ~5 grafos válidos, se logran producir casos donde U1 y A1 retornan costos que no cumplen con la optimalidad frente a la referencia, o declaran costos que no coinciden con la suma real de las aristas del grafo.

## 4. Limitaciones y reflexión conceptual

El hecho de que la búsqueda aleatoria iguale el rendimiento del algoritmo genético expone una limitación importante: la densidad de los defectos en el espacio de grafos de 6 nodos es tan alta que los errores son descubiertos antes de que el proceso evolutivo tenga tiempo de converger o demostrar una ventaja selectiva. 

**Interpretación Conceptual:**
La evolución de grafos opera en el *espacio del problema* (generando configuraciones topológicas y de costos), lo cual es drásticamente diferente a lo que hacen los agentes evaluados, que operan en el *espacio de estados* buscando una ruta dentro de una topología ya dada. Al formular este proyecto como evolución, delegamos la inteligencia del descubrimiento a una función de aptitud ciega que recompensa discrepancias. 

Como advirtió John McCarthy, dotar a una máquina de un comportamiento formal no es lo mismo que dotarla de sentido común. Generar estos grafos que "rompen" los algoritmos demuestra que podemos optimizar heurísticamente una estructura para revelar fallos lógicos, pero no demuestra comprensión por parte de la IA. Similar al argumento de la Habitación China de John Searle, nuestro algoritmo genético manipula la sintaxis de las aristas y nodos basándose en retroalimentación matemática (fitness), pero "no sabe" qué es un camino óptimo ni entiende por qué B1 o A1 están fallando. La semántica del error solo existe en la interpretación que hacemos nosotros, los ingenieros, al analizar los registros.

## 5. Contribuciones y recursos

*   **Christopher Karol Trejo Ganzo:** Diseño de la representación cromosómica de grafos, implementación del adaptador de comunicación con el paquete docente y el validador de entradas estructurales.
*   **Misael Bahena Vargas:** Desarrollo central del proceso evolutivo, operadores genéticos (selección, cruzamiento y mutación) y diseño de la función de aptitud considerando simplicidad.
*   **Mauricio Rodríguez Gaytan:** Clasificación semántica de resultados, validación real de los costos de ruta y desarrollo de la línea base (búsqueda aleatoria) y casos de prueba.
*   **Luis Angel Arteaga Castillo:** Automatización del experimento mediante semillas fijas, exportación de registros CSV/JSON y extracción reproducible de la colección de contraejemplos.
*   **Yahir Rodríguez Zamora:** ejecución de pruebas del proyecto (`test_proyecto.py`), gestión de incidencias (manejo de límites alcanzados), exportación de registros CSV/JSON y extracción reproducible de contraejemplos.

**Recursos utilizados:**
*   Python 3 Standard Library (`random`, `json`, `csv`).
*   Paquete docente proporcionado para la evaluación de algoritmos `B1`, `U1`, `A1` y referencia.