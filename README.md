# Cazador genético de defectos en agentes de búsqueda

Algoritmo genético que evoluciona grafos dirigidos de 6 nodos para encontrar incumplimientos de
especificación en B1 (BFS), U1 (UCS) y A1 (A*) del paquete docente, comparado con una búsqueda
aleatoria con el mismo presupuesto de 1000 evaluaciones por semilla.

## Integrantes

- Arteaga Castillo Luis Angel
- Bahena Vargas Misael
- Rodriguez Gaytan Mauricio
- Rodriguez Zamora Yahir
- Trejo Ganzo Christopher Karol

Equipo: `<identificador>`

## Requisitos

- Python 3.10 o superior. Probado con Python 3.14.4.
- Solo biblioteca estándar; no se instala nada con pip.
- Paquete docente `busqueda` versión 1.0.0, sin modificar.

## Paquete docente

Va en `material_docente/busqueda/` y se importa únicamente a través de `docente.py`.
Para usar otra copia del paquete, reemplace esa carpeta por la carpeta `busqueda/` del ZIP
de estudiantes. Huellas SHA-256 esperadas:

| Archivo | SHA-256 (inicio) |
|---|---|
| `__init__.py` | `3da8a1f30e96…` |
| `__main__.py` | `58758b871302…` |
| `objetivos.py` | `35b023d29061…` |

Comprobación: `sha256sum material_docente/busqueda/*.py`

## Estructura

| Archivo / carpeta | Contenido |
|---|---|
| `cromosoma.py` | Representación (`CromosomaGrafo`), adaptador al JSON docente y validador estructural |
| `docente.py` | Importa el paquete docente desde `material_docente/` |
| `verificacion.py` | Verificación semántica propia (referencia con BFS y Dijkstra) |
| `evaluador.py` | Evaluador común: presupuesto, caché, clasificación, incidencias, primer hallazgo por agente |
| `aptitud.py` | Función de aptitud sobre los tres agentes |
| `algoritmo_genetico.py` | Algoritmo genético (torneo, cruce, mutación, elitismo) |
| `busqueda_aleatoria.py` | Línea base aleatoria |
| `main.py` | Experimento principal y ejecuciones individuales |
| `contraejemplos.py` | Selección, explicación y reproducción de contraejemplos |
| `pruebas/` | Pruebas `unittest` y evidencia de ejecución |
| `resultados/` | Registros del experimento principal |
| `contraejemplos/` | Casos `caso_XX.json` e `INDICE.md` |
| `material_docente/` | Paquete docente sin modificar |

## Comandos

Todos se ejecutan desde la raíz del repositorio.

```bash
# Pruebas
python3 -m unittest discover -s pruebas -t . -v

# Una ejecución de cada método (se guarda en resultados/individuales/)
python3 main.py --metodo genetico --semilla 11
python3 main.py --metodo aleatorio --semilla 11

# Comparación principal: semillas 11, 22, 33, 44 y 55, ambos métodos
python3 main.py

# Volver a evaluar un contraejemplo fuera del ciclo evolutivo
python3 contraejemplos.py contraejemplos/caso_01.json
```

## Dónde se escriben los resultados

| Ruta | Contenido |
|---|---|
| `resultados/configuracion.json` | Semillas, presupuesto, límite de expansiones, tamaño de población, versiones |
| `resultados/<metodo>_s<semilla>.json` | Registro de cada una de las 10 ejecuciones principales: configuración, evaluaciones, grafos distintos, primer hallazgo por agente, incidencias, progreso |
| `resultados/progreso.csv` | Progreso de las 10 ejecuciones (AG por generación; aleatoria en los mismos puntos) |
| `resultados/resumen.csv` | Comparación por método y agente; la mediana se calcula solo entre ejecuciones con hallazgo |
| `contraejemplos/` | Hasta 6 casos reproducibles e índice |
| `resultados/individuales/` | Ejecuciones sueltas con `--metodo`; no forman parte de la comparación principal ni se suben al repositorio |

`python3 main.py` sobrescribe `resultados/` y `contraejemplos/`. Con semilla fija, todo se
regenera idéntico excepto los tiempos. Las 18 reevaluaciones de los contraejemplos se registran
en `contraejemplos/INDICE.md` y no cuentan en el presupuesto. No hay ejecuciones de desarrollo
mezcladas con la comparación principal.

## Pruebas

`pruebas/test_proyecto.py` usa datos controlados escritos a mano; no son los contraejemplos
descubiertos.

| Grupo | Qué comprueba |
|---|---|
| `Formato` | Adaptador ida y vuelta; el paquete docente acepta los grafos generados; el validador rechaza lazos, costos 0 y 10, duplicados, booleanos y nodos fuera de rango; un grafo sin ruta es válido |
| `Operadores` | El cruce solo usa aristas de los padres; cruce y mutación mantienen el dominio |
| `Clasificacion` | Ausencia de ruta, rutas alternativas de igual calidad, costo declarado incorrecto, ruta inválida, BFS juzgado por aristas y UCS por costo, límite no contado como contraejemplo |
| `Presupuesto` | Los candidatos repetidos consumen presupuesto; ambos métodos usan exactamente 1000 evaluaciones; la misma semilla reproduce la misma ejecución |

Evidencia: `pruebas/evidencia_ejecucion.txt`. Fallos pendientes: ninguno.

## Tiempo de ejecución

Medido en el equipo del equipo:

| Tarea | Tiempo |
|---|---|
| `python3 main.py` (10 ejecuciones + contraejemplos) | 7.2 s |
| Pruebas | 1.3 s |
