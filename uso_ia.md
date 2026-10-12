**Declaración de uso de IA para Examen Parcial**


Sí hubo uso de IA, dentro de las modalidades permitidas las cuales fueron consultas conceptuales, orientación general y revisión del trabajo que revisó el equipo.

**Herramienta y modelo**

Dato             | Valor

Herramienta      | Claude

Modelo           | Somnet 4.6

Periodo de uso   | 9/Octubre/2026 al 11/Octubre/2026

Modalidad        | Interfaz de chat

---

**Consultas realizadas**

1. Consultas conceptuales: Aclarar conceptos de algoritmos genéticos y de búsqueda no informada e informada.  

2. Orientación en el diseño: Apoyar con alternativas de diseño antes de usarse, por ejemplo el cómo representar el grafo como cromosoma, cómo estructurar la función de aptitud por niveles y cómo hacer comparable la búsqueda aleatoria con el algoritmo genético.  

3. Revisión del trabajo ya elaborado: Revisar scripts ya escritos por el equipo para que señalar posibles errores, riesgos y puntos a comprobar.  

---

**Partes del trabajo revisadas por el agente**


Parte                                  | Archivo                 | Qué se revisó


Representación y validación del dom.   | cromosoma.py            | Que el adaptador al formato del paquete docente y el validador cubrieran lazos, costos fuera de [1, 9], duplicados y nodos fuera de rango.

Verificación propia                    | verificacion.py         | Que el criterio de optimalidad fuera el correcto por agente: BFS por número de aristas, U1 y A1 por costo.

Contabilidad del presupuesto           | evaluador.py            | Que la caché y los grafos repetidos no alterarán el conteo de las 1000 evaluaciones.

Función de aptitud                     | aptitud.py              | Separación de niveles y que limite, error y desacuerdo no se premiaran como hallazgos.

Operadores evolutivos                  | algoritmo_genetico.py   | Que cruce y mutación preservaran el dominio y que el manejo de duplicados no sesgara la búsqueda.

Comparabilidad de la línea base        | busqueda_aleatoria.py   | Que los puntos de control coincidieran con los del AG y que ambos métodos usaran el mismo evaluador y presupuesto.

Pruebas                                | pruebas/test_proyecto.py| Cobertura de casos límite y que las pruebas no dependieran de los contraejemplos descubiertos.

---

**Observaciones relevantes**

1. Presupuesto y grafos repetidos. Riesgo de que la caché de evaluaciones hiciera que un grafo ya visto no consumiera presupuesto, lo que habría dado al AG más evaluaciones efectivas que a la búsqueda aleatoria. Atendida: en EvaluadorComun.evaluar el contador se incrementa antes de consultar la caché; la caché ahorra cómputo, no presupuesto. Comprobado en test_repetidos_consumen_presupuesto.  

2. El límite no es evidencia de defecto. Agotar el límite de expansiones significa que el agente no terminó, no que se haya equivocado; contarlo como contraejemplo habría inflado los resultados. Atendida: verificacion.clasificar solo juzga los estados solucion y sin_solucion, y la aptitud no premia limite, error ni desacuerdo. Comprobado en test_limite_no_es_contraejemplo.  

3. Criterio de optimalidad distinto por agente. Riesgo de marcar como contraejemplo una ruta de B1 que no es la más barata, cuando BFS solo debe minimizar el número de aristas. Atendida: la referencia propia calcula BFS y Dijkstra por separado y cada agente se juzga contra el suyo. Comprobado en test_bfs_por_aristas_ucs_por_costo.  

4. Rutas alternativas de igual calidad. Riesgo de reportar un falso positivo cuando el agente devuelve una ruta distinta a la de la referencia pero con el mismo costo o la misma longitud. Atendida: la comparación es por valor, no por igualdad de ruta. Comprobado en test_rutas_alternativas_de_igual_calidad.  

5. Comparabilidad de la línea base. La comparación entre métodos solo es válida si la búsqueda aleatoria muestrea de la misma distribución que la población inicial del AG y se mide en los mismos puntos. Atendida: busqueda_aleatoria reutiliza generar_aleatorio y puntos_control reproduce los cortes de generación del AG.  

6. Separación de niveles en la aptitud. Riesgo de que el bono de simplicidad hiciera que un grafo sin hallazgo superara a uno con hallazgo. Atendida: el bono vale como máximo 30 y los niveles van de 1000 en 1000, por lo que no se traslapan.  

7. Reproducibilidad de los contraejemplos. Se señaló que un hallazgo no comprobado podría depender de un desempate aleatorio dentro del agente. Atendida: cada caso se reejecuta 3 veces fuera del presupuesto (contraejemplos.reproducir), 18 ejecuciones en total, todas consistentes.  

8. Errores propios frente a defectos del agente. Riesgo de atribuir al agente una excepción causada por nuestro propio adaptador. Atendida: las excepciones del equipo se registran aparte como equipo:<Tipo> y reciben aptitud 0. En las 10 ejecuciones principales el total de incidencias fue 0.

---

**Verificaciones realizadas por el equipo**

Ninguna indicación de la IA se incorporó sin comprobación. Las verificaciones fueron:

- Lectura y contraste con el paquete docente. Toda afirmación sobre el comportamiento esperado de B1, U1 y A1 se contrastó con el código de material_docente/busqueda/ y con la documentación del curso, no con la respuesta de la herramienta.  

- Verificación independiente. Se implementó verificacion.py con BFS y Dijkstra propios, de modo que la clasificación de contraejemplos no dependa del verificador docente ni de ninguna sugerencia externa.  

- Pruebas automatizadas. 13 pruebas en pruebas/test_proyecto.py, ejecutadas con python3 -m unittest discover -s pruebas -t . -v. Resultado: 13/13 correctas en 1.299 s. Evidencia en pruebas/evidencia_ejecucion.txt.  

- Reproducibilidad por semilla. test_semilla_fija_reproduce confirma que una misma semilla produce la misma ejecución, y test_metodos_usan_exactamente_1000 que ambos métodos consumen exactamente el presupuesto.  

- Reproducción de contraejemplos. Los 6 casos de contraejemplos/ se reejecutaron 3 veces cada uno fuera del ciclo evolutivo; los 6 quedaron marcados como reproducidos en contraejemplos/INDICE.md.  

- Revisión cruzada entre integrantes. Cada módulo revisado con apoyo de la herramienta fue leído además por al menos otro integrante del equipo antes de integrarse.

---

**Registro acotado de consultas**

  | Fecha aprox. | Tipo       | Tema de la consulta                                                                                  | Qué se hizo con la respuesta

1 | 9/10/2026    | Conceptual | Diferencia entre el criterio de optimalidad de BFS (número de aristas) y U1/A* (costo acumulado).    | Se contrastó con el paquete docente y se usó para referencia_propia.

2 | 9/10/2026    | Conceptual | Condiciones bajo las cuales A* deja de ser óptimo (heurística no admisible o inconsistente).         | Sirvió para entender qué tipo de grafo podía exponer un defecto en A1.

3 | 9/10/2026    | Orientación| Alternativas de representación de un grafo dirigido con costos como cromosoma de longitud variable.  | El equipo eligió el diccionario {(u,v): costo} e implementó cromosoma.py.

4 | 10/10/2026   | Orientación| Cómo estructurar una función de aptitud con objetivo principal y criterio de desempate.              | Se adoptó el esquema por niveles con bono de simplicidad acotado a 30.

5 | 10/10/2026   | Orientación| Qué hace comparable una línea base aleatoria frente a un algoritmo genético bajo el mismo pres.      | Se definieron los puntos de control comunes y el evaluador compartido.

6 | 10/10/2026   | Revisión   | Revisión de evaluador.py: contabilidad del presupuesto con caché y grafos repetidos.                 | Observación 1 de la sección 5; se añadió test_repetidos_consumen_presupuesto.

7 | 11/10/2026   | Revisión   | Revisión de verificacion.py: qué estados deben considerarse evidencia de defecto.                    | Observación 2; se añadió test_limite_no_es_contraejemplo.

8 | 11/10/2026   | Revisión   | Revisión de algoritmo_genetico.py: si cruce y mutación pueden salirse del dominio válido.            | Observación 6 / preservación de dominio; se añadió test_cruce_y_mutacion...

9 | 11/10/2026   | Revisión   | Revisión de la cobertura de las pruebas: casos límite faltantes.                                     | Se añadieron los casos de rutas alternativas y de grafo sin ruta.

---

**Partes Revisadas y Observaciones Relevantes**

- Arquitectura de archivos: La IA revisó nuestro árbol de directorios y confirmó que la separación entre cromosoma.py, evaluador.py y aptitud.py era adecuada para aislar las responsabilidades.

- Integración: Nos orientó conceptualmente sobre cómo el adaptador debe leer la estructura (diccionario) y pasarla a las funciones de material_docente sin modificar este último.

- Informe Final: Se utilizó un esqueleto sugerido por la IA para estructurar el reporte de 1000 a 1500 palabras, garantizando que cubriéramos todos los puntos de la rúbrica (factibilidad, evolución, experimentación y contraejemplos). 

- Formato documentación del proyecto: Se nos sugirió seguir un formato específico para la documentación del proyecto, lo que nos ayudó a organizar la información de manera clara y concisa. Así como darle un mejor aspecto a los archivos de tipo Markdown dándonos la manera en que los archivos de este tipo se organizan y como aplicar colores, negritas, etc. para que tenga una mejor estética.
