"""
Función de aptitud (fitness) para evaluar a los agentes (B1, U1, A1)
Entre más alto, mejor el grafo.

La dividimos por niveles fijos para que los puntajes no se encimen, 
usando la simplicidad (30 - número de aristas) como un pequeño bono secundario:
  - 1000 * k + simplicidad: Si encontramos un contraejemplo confirmado en 'k' agentes (k >= 1)
  - 100 + (10 * rutas) + simplicidad: Si no hubo error, pero al menos el grafo tiene caminos válidos de inicio a meta (hasta 10 rutas)
  - simplicidad: Si no hay hallazgos ni ruta válida; aquí solo gana puntos tener un grafo chiquito y simple
  - 0: Si nuestro propio código tronó o falló

cuidado: Los límites alcanzados, errores o desacuerdos raros no suman puntos porque no demuestran un fallo real de los agentes
"""
from cromosoma import INICIO, META, MAX_ARISTAS

TOPE_RUTAS = 10


def contar_rutas_simples(cromosoma, tope=TOPE_RUTAS):
    vecinos = {}
    for (u, v) in cromosoma.aristas:
        vecinos.setdefault(u, []).append(v)
    cuenta, pila = 0, [(INICIO, {INICIO})]
    while pila and cuenta < tope:
        u, visitados = pila.pop()
        if u == META:
            cuenta += 1
            continue
        for v in vecinos.get(u, []):
            if v not in visitados:
                pila.append((v, visitados | {v}))
    return cuenta


def calcular_aptitud(evaluacion, cromosoma):
    if evaluacion["agentes"] is None:          # error del equipo
        return 0
    simplicidad = MAX_ARISTAS - len(cromosoma.aristas)
    k = sum(1 for d in evaluacion["agentes"].values() if d["clase"] == "contraejemplo")
    if k > 0:
        return 1000 * k + simplicidad
    if evaluacion["referencia"]["existe_ruta"]:
        return 100 + 10 * contar_rutas_simples(cromosoma) + simplicidad
    return simplicidad
