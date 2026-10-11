# Declaración de uso de inteligencia artificial

**Sí hubo uso de IA.**

## Herramienta y modelo

- Herramienta: Claude (aplicación de escritorio, modo Cowork), de Anthropic.
- Modelo: `claude-opus-5-5` (identificador configurado en la sesión).
- Fecha de uso: 10 de octubre de 2026.
- Integrante que hizo las consultas: Trejo Ganzo Christopher Karol.

## Finalidad

1. Revisar el repositorio frente al enunciado del examen e identificar incumplimientos. Por
   ejemplo: un AG por agente, que gastaba 3000 evaluaciones por semilla; una aptitud que
   favorecía grafos vacíos; la falta de registros, pruebas y verificación propia.
2. Obtener una guía paso a paso con fragmentos de código para corregirlos: `docente.py`,
   validador en `cromosoma.py`, `verificacion.py`, `evaluador.py`, la nueva `aptitud.py`, los
   cambios en `algoritmo_genetico.py`, `busqueda_aleatoria.py`, `main.py`, `contraejemplos.py`
   y `pruebas/test_proyecto.py`.
3. Redactar el `README.md`.

Las ideas de base son del equipo: la representación `CromosomaGrafo`, el cruce por unión de
aristas, la mutación de agregar/eliminar/cambiar costo, la selección por torneo y la aptitud
por niveles con bono de simplicidad. La IA propuso cómo integrarlas con un evaluador común.
La IA no tuvo acceso para modificar el repositorio: los cambios los aplicó el equipo en su
terminal, paso por paso, revisando la salida de cada uno.

## Partes revisadas por el equipo

<Completar: qué archivo revisó cada integrante, qué entendió o cambió respecto de la propuesta.>

## Observaciones relevantes

- La IA señaló que, con una población de 50, casi todos los hallazgos ocurren en la población
  inicial, que es idéntica en ambos métodos. Por eso el AG y la búsqueda aleatoria dan
  resultados casi iguales. Lo reportamos en el informe sin forzar una ventaja del AG.
- La IA advirtió que la carpeta `docente/` del material del profesor contiene soluciones
  reservadas. No se usó.
- Las explicaciones de los contraejemplos se generan automáticamente a partir de la ruta
  devuelta y de la referencia; en el informe se explican con nuestras palabras.

## Verificaciones realizadas por el equipo

- Se ejecutaron las 13 pruebas propias (`pruebas/evidencia_ejecucion.txt`).
- Se ejecutó `python3 main.py`: cada ejecución usa exactamente 1000 evaluaciones y los
  resultados coinciden al repetir con las mismas semillas.
- Se reprodujeron los contraejemplos con `python3 contraejemplos.py contraejemplos/caso_XX.json`.
- Se comprobó con `sha256sum` que el paquete docente no fue modificado.
- <Completar: por ejemplo, verificar a mano en papel la ruta y el costo de un contraejemplo.>

## Registro acotado de consultas

| # | Consulta (resumen) | Resultado |
|---|---|---|
| 1 | Revisar si el repositorio cumple el enunciado | Lista de incumplimientos por requisito |
| 2 | Revisar los cambios de "Prueba1" (una corrida por semilla) | Presupuesto corregido; se pierde el primer hallazgo por agente y faltan casos de A1 |
| 3 | Guía paso a paso en terminal para cumplir con lo pedido | Pasos 1 a 9 con código, probados por la IA en una copia del repositorio |
| 4 | Instalar VS Code para correr las pruebas | Instrucciones de instalación; las pruebas se corrieron en terminal |
| 5 | Qué entregables faltan | Lista: README, informe, contribuciones, uso de IA, ZIP |
| 6 | Redactar el README | README con comandos, estructura, pruebas y tiempos medidos |
