"""Función de aptitud sobre los tres agentes (mayor es mejor).

Niveles (nunca se traslapan porque el bono de simplicidad vale 0..30):
  1000 * k + simplicidad   k = agentes (B1, U1, A1) con contraejemplo confirmado, k >= 1
  100 + 10 * rutas + simp. sin hallazgo, pero hay ruta 0->5 (rutas = caminos simples, tope 10)
  simplicidad              sin hallazgo y sin ruta 0->5
  0                        error de nuestro propio código
simplicidad = 30 - número de aristas (criterio secundario: preferir grafos pequeños).
limite / error / desacuerdo no suman: no son evidencia de defecto.
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
