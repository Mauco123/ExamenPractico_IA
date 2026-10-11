# Informe del Proyecto

## 1. Representación del dominio y validación de candidatos

Para formular la generación de pruebas como un problema de optimización, el primer paso consistió en distinguir claramente el espacio de grafos candidatos (el problema que resuelve el algoritmo genético) del espacio de rutas (el problema que intentan resolver los agentes evaluados). 

Diseñamos una representación cromosómica genotípica donde cada individuo es un grafo dirigido sintético. La estructura de datos elegida encapsula tres propiedades fundamentales: un nodo de `inicio` (representado por un entero del 0 al 5), un nodo `meta` (entero del 0 al 5), y una lista dinámica de `aristas`. Cada arista se codifica como una tupla `(origen, destino, costo)`. 

**Decisiones de factibilidad y reparación:** 
Un aspecto crítico del diseño fue garantizar que el algoritmo evolutivo explorara únicamente instancias válidas del dominio. Implementamos un validador estructural en el constructor del cromosoma. Durante la creación aleatoria inicial y tras la aplicación de cualquier operador genético, el sistema aplica políticas estrictas:
*   **Rechazo de costos inválidos:** Si una mutación genera un costo $\le 0$, el operador repara el gen asignando un costo mínimo positivo aleatorio.
*   **Eliminación de duplicados:** Se aplica un filtro de conjuntos (`set`) para asegurar que no existan múltiples aristas direccionales idénticas entre dos mismos nodos. 
*   **Grafos sin solución:** De acuerdo con los requerimientos, los grafos desconectados o donde no existe un camino del inicio a la meta no son reparados. Son considerados candidatos estructuralmente válidos y su evaluación es gestionada por la función de aptitud.

## 2. Operadores genéticos y proceso evolutivo

Para el ciclo evolutivo, decidimos prescindir de bibliotecas externas, implementando desde cero los mecanismos de selección, cruzamiento y mutación para tener control absoluto sobre la aleatoriedad.

*   **Selección:** Utilizamos un mecanismo de selección por torneo (tamaño de torneo = 3). Elegir este método sobre la "ruleta" nos permitió mantener una presión selectiva constante sin importar la escala de los valores de aptitud, evitando la convergencia prematura en las primeras generaciones.
*   **Cruzamiento (Crossover):** Diseñamos un cruzamiento multipunto adaptado a grafos. Dado un par de progenitores, el descendiente hereda el nodo de inicio del primer progenitor y el nodo meta del segundo. El conjunto de aristas se construye mediante la unión aleatoria de subconjuntos de aristas de ambos padres. El validador estructural interviene inmediatamente después para limpiar cualquier inconsistencia topológica generada por esta mezcla.
*   **Mutación:** Con una probabilidad controlada (tasa de mutación), el cromosoma sufre alteraciones para introducir diversidad. Las mutaciones posibles incluyen: adición de una arista completamente nueva, eliminación de una arista existente para fragmentar rutas, alteración drástica del peso de una arista para engañar a algoritmos heurísticos, o la reasignación de los nodos inicio/meta.

## 3. Función de aptitud y evaluación semántica

La función de aptitud (fitness) es el núcleo heurístico que guía la búsqueda hacia el hallazgo de discrepancias. Se estructuró como una función de evaluación multicriterio priorizada:

1.  **Prioridad Máxima (El Hallazgo):** Si la evaluación semántica detecta que un objetivo (B1, U1 o A1) incumple las garantías de su algoritmo (ej. devuelve un costo subóptimo frente al verificador docente, inventa una ruta que no existe, o declara un costo que no coincide con la suma de sus aristas), el individuo recibe una aptitud infinita o máxima, garantizando su preservación y marcando el final de la búsqueda para esa semilla.
2.  **Prioridad Secundaria (Estrés Computacional):** Para guiar a la población hacia grafos que pongan a prueba a los agentes, se recompensa a los individuos basándose en el número de nodos expandidos y la longitud de las rutas evaluadas. Un grafo que obliga a A* a explorar más nodos que BFS recibe un puntaje más alto, ya que representa un terreno más "engañoso" para las heurísticas.
3.  **Criterio de Simplicidad:** Entre dos candidatos que generen el mismo nivel de estrés, se aplica una penalización leve proporcional al número de aristas. Esto favorece la aparición de contraejemplos minimalistas y comprensibles, facilitando la depuración posterior.

Adicionalmente, se implementó un adaptador con aislamiento de fallos (`try/except`). Los estados de "límite alcanzado" o excepciones en los agentes se registran como incidencias separadas y se castigan en la función de aptitud, evitando que el genético evolucione grafos que simplemente rompen el programa por *timeout* en lugar de revelar un error lógico.

## 4. Comparación experimental y análisis de resultados

El diseño experimental comparó nuestro algoritmo genético con una línea base de búsqueda aleatoria, ambos con un presupuesto de 1000 evaluaciones y controlados por 5 semillas (11, 22, 33, 44, 55). Para garantizar equidad, implementamos una caché que registra grafos previamente evaluados; si el genético regenera un grafo conocido, consume presupuesto pero no tiempo de cómputo externo.

**Resumen de Resultados:**
Ambos métodos detectaron discrepancias en los tres objetivos (B1, U1, A1) en el 100% de las ejecuciones. Los registros demuestran que las ejecuciones tomaron alrededor de 1.6 segundos para el genético y 1.47 segundos para la búsqueda aleatoria, sin registrarse incidencias por *timeouts*.

**Análisis Crítico:**
El resultado más revelador del experimento es que la búsqueda aleatoria igualó el rendimiento mediano del algoritmo genético: se necesitaron 26 evaluaciones para revelar los fallos de B1, y solo 5 evaluaciones para U1 y A1. Esto indica empíricamente que la densidad de defectos inyectados en las implementaciones docentes es extraordinariamente alta en el subespacio de grafos de 6 nodos. Los errores son tan comunes que una selección estocástica sin presión evolutiva es suficiente para detonarlos antes de que la selección por torneo tenga oportunidad de mostrar ventaja competitiva.

## 5. Contraejemplos representativos y sus implicaciones

La colección de contraejemplos extraída del experimento ilustra claramente los fallos de especificación:
*   **B1 (Búsqueda en Amplitud):** Las discrepancias, halladas tras explorar en mediana 26 grafos, muestran fallos en la reconstrucción semántica de las rutas. El agente devuelve información que diverge de la topología real del grafo validada por el evaluador.
*   **U1 y A1 (Costo Uniforme y A*):** Con apenas 5 evaluaciones, se evidencia que estas implementaciones fallan en su garantía de optimalidad. Aceptan rutas iniciales de menor profundidad en lugar de minimizar el costo acumulado, o presentan cálculos donde el costo declarado de la ruta difiere de la suma aritmética de las aristas del grafo objetivo, rompiendo la admisibilidad que caracteriza teóricamente a estos algoritmos.

## 6. Reflexión conceptual sobre IA, evolución y comprensión

Este experimento subraya una diferencia fundamental en la inteligencia artificial: la disparidad entre la búsqueda de soluciones genéricas (nuestro algoritmo evolutivo) y la búsqueda de trayectorias (los agentes evaluados). Mientras BFS y A* buscan secuencias de acciones dentro de un entorno estático y predefinido, nuestra evolución de grafos navega en un meta-espacio de topologías complejas.

En un contexto filosófico, nuestro algoritmo fue altamente eficaz descubriendo errores sin saber qué es un error. John McCarthy argumentó que dotar a los programas con sentido común y capacidad de razonamiento declarativo era el verdadero objetivo de la IA. Nuestro algoritmo genético carece por completo de este razonamiento declarativo. 

Esta falta de verdadera "comprensión" se alinea con el argumento de la *Habitación China* de John Searle (1980) y contrasta fuertemente con la visión funcionalista de la Prueba de Turing (1950). El algoritmo genético manipula símbolos y estructuras sintácticas (nodos, pesos) para optimizar un número (la función de aptitud). Logra engañar y romper implementaciones complejas, produciendo pruebas de software de alta calidad, pero sin tener un modelo semántico interno de lo que significa "optimalidad", "ruta" o "defecto". La inteligencia de la prueba radica en nuestro diseño de la función de aptitud, no en una comprensión intrínseca de la máquina.

## 7. Contribuciones, revisiones cruzadas y recursos

*   **Integrante 1 [Cristopher Karol Trejo Ganzo]:** Desarrollo de la representación genotípica, validador estructural de grafos y el adaptador semántico. *Revisión cruzada:* Auditó la función de aptitud del Integrante 3 para asegurar compatibilidad de datos.
*   **Integrante 2 [Misael Bahena Vargas]:** Arquitectura del ciclo evolutivo y programación de operadores genéticos (selección, crossover y mutación). *Revisión cruzada:* Validó el mecanismo de control de semillas implementado por el Integrante 4.
*   **Integrante 3 [Mauricio Rodríguez Gaytan]:** Diseño matemático de la función de aptitud (criterios de simplicidad y penalización) y clasificación de resultados del verificador. *Revisión cruzada:* Revisó las pruebas unitarias del Integrante 5.
*   **Integrante 4 [Luis Angel Arteaga Castillo]:** Desarrollo del generador de línea base aleatoria, automatización del presupuesto estricto (1000 iteraciones) y gestión de la caché de evaluaciones. *Revisión cruzada:* Supervisó que los operadores del Integrante 2 no alteraran referencias en memoria de los cromosomas.
*   **Integrante 5 [Yahir Rodríguez Zamora]:** Pruebas automatizadas del proyecto (`test_proyecto.py`), manejo de incidencias y excepciones aisladas, exportación de resultados CSV/JSON y extracción de contraejemplos minimizados. *Revisión cruzada:* Probó la tolerancia a fallos del adaptador del Integrante 1.

**Recursos utilizados:**
*   Python 3 Standard Library (`random`, `json`, `csv`).
*   Paquete docente proporcionado para la evaluación de algoritmos `B1`, `U1`, `A1` y referencia.

**Bibliografía:**
*   Python Software Foundation. (2023). *Python Language Reference, version 3.x* (Librerías estándar `random`, `json`, `csv`).
*   Russell, S. J., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson. (Referencia para verificación teórica de propiedades de algoritmos BFS, UCS, A*).
*   Searle, J. R. (1980). *Minds, brains, and programs*. Behavioral and Brain Sciences, 3(3), 417-424.
*   Turing, A. M. (1950). *Computing Machinery and Intelligence*. Mind, 59(236), 433-460.


