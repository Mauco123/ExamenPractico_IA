# Verificación semántica propia (independiente del verificador docente)
from collections import deque
from heapq import heappush, heappop

from cromosoma import N_NODOS, INICIO, META


def referencia_propia(grafo):
    #BFS (mínimo de aristas) y Dijkstra (mínimo costo) de INICIO a META
    ady = {u: [] for u in range(N_NODOS)}
    for u, v, w in grafo["aristas"]:
        ady[u].append((v, w))
    saltos = {INICIO: 0}
    cola = deque([INICIO])
    while cola:
        u = cola.popleft()
        for v, _ in ady[u]:
            if v not in saltos:
                saltos[v] = saltos[u] + 1
                cola.append(v)
    costo = {INICIO: 0}
    heap = [(0, INICIO)]
    while heap:
        c, u = heappop(heap)
        if c > costo[u]:
            continue
        for v, w in ady[u]:
            if c + w < costo.get(v, float("inf")):
                costo[v] = c + w
                heappush(heap, (c + w, v))
    existe = META in saltos
    return {"existe_ruta": existe,
            "distancia_minima_aristas": saltos.get(META),
            "costo_minimo": costo.get(META)}


def clasificar(agente, grafo, resultado):

    """Devuelve la lista ordenada de discrepancias que encontramos nosotros.
    Solo para estados 'solucion' y 'sin_solucion' (limite/error no se juzgan)"""
    
    ref = referencia_propia(grafo)
    pesos = {(u, v): w for u, v, w in grafo["aristas"]}
    fallos = []
    if resultado["estado"] == "sin_solucion":
        if ref["existe_ruta"]:
            fallos.append("falso_sin_solucion")
    elif resultado["estado"] == "solucion":
        ruta = resultado["ruta"]
        valida = (isinstance(ruta, list) and len(ruta) >= 2 and ruta[0] == INICIO
                  and ruta[-1] == META and all(p in pesos for p in zip(ruta, ruta[1:])))
        if not valida:
            fallos.append("ruta_invalida")
        else:
            real = sum(pesos[p] for p in zip(ruta, ruta[1:]))
            if resultado["costo"] != real or type(resultado["costo"]) is not int:
                fallos.append("costo_incorrecto")
            if agente == "B1":   # BFS se juzga por número de aristas
                optimo, obtenido = ref["distancia_minima_aristas"], len(ruta) - 1
            else:                # UCS y A* por costo real
                optimo, obtenido = ref["costo_minimo"], real
            if obtenido != optimo:
                fallos.append("no_optimo")
    return sorted(fallos)
