"""Experimento principal: AG y búsqueda aleatoria, semillas 11, 22, 33, 44, 55,
1000 evaluaciones por método y semilla. Escribe en resultados/ y contraejemplos/."""
import csv
import json
import platform
import time
from pathlib import Path
from statistics import median

from docente import VERSION, AGENTES
from evaluador import EvaluadorComun
from algoritmo_genetico import AlgoritmoGenetico
from busqueda_aleatoria import ejecutar_busqueda_aleatoria
from contraejemplos import guardar_contraejemplos

SEMILLAS = [11, 22, 33, 44, 55]
MAX_EVALUACIONES = 1000
LIMITE_EXPANSIONES = 100
POP_SIZE = 50
RESULTADOS = Path("resultados")


def guardar_json(ruta, datos):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(datos, indent=2, ensure_ascii=False), encoding="utf-8")


def una_ejecucion(metodo, semilla):
    ev = EvaluadorComun(MAX_EVALUACIONES, LIMITE_EXPANSIONES)
    t0 = time.perf_counter()
    if metodo == "genetico":
        ag = AlgoritmoGenetico(ev, semilla, pop_size=POP_SIZE)
        mejor, aptitud = ag.ejecutar()
        progreso, config = ag.progreso, ag.configuracion()
    else:
        mejor, aptitud, progreso = ejecutar_busqueda_aleatoria(ev, semilla, POP_SIZE)
        config = {"distribucion": "generar_aleatorio (igual que la población inicial del AG)"}
    registro = {"metodo": metodo, "semilla": semilla, "configuracion": config,
                **ev.resumen(), "mejor_aptitud": aptitud,
                "mejor_grafo": mejor.a_formato_evaluador(),
                "progreso": progreso,
                "tiempo_s": round(time.perf_counter() - t0, 3)}
    guardar_json(RESULTADOS / f"{metodo}_s{semilla}.json", registro)
    return registro, ev.hallazgos


def resumir(registros):
    filas = []
    for metodo in ("genetico", "aleatorio"):
        regs = [r for r in registros if r["metodo"] == metodo]
        for a in AGENTES:
            exitos = [r["primer_hallazgo"][a] for r in regs
                      if r["primer_hallazgo"][a] != "no encontrado"]
            filas.append({
                "metodo": metodo, "objetivo": a,
                "ejecuciones_con_hallazgo": f"{len(exitos)}/{len(regs)}",
                "mediana_evals_primer_hallazgo_solo_exitos": median(exitos) if exitos else "no aplica",
                "ejecuciones_sin_hallazgo": len(regs) - len(exitos),
                "grafos_distintos_total": sum(r["grafos_distintos"] for r in regs),
                "incidencias_total": sum(sum(r["incidencias"].values()) for r in regs),
                "tiempo_total_s": round(sum(r["tiempo_s"] for r in regs), 3)})
    return filas


def escribir_csv(ruta, filas):
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)


def ejecutar_experimentos():
    guardar_json(RESULTADOS / "configuracion.json", {
        "semillas": SEMILLAS, "presupuesto": MAX_EVALUACIONES,
        "limite_expansiones": LIMITE_EXPANSIONES, "pop_size": POP_SIZE,
        "version_paquete_docente": VERSION, "python": platform.python_version()})
    registros, hallazgos = [], []
    for metodo in ("genetico", "aleatorio"):
        for semilla in SEMILLAS:
            registro, h = una_ejecucion(metodo, semilla)
            registros.append(registro)
            hallazgos.append((metodo, semilla, h))
            print(f"{metodo:9s} semilla {semilla}: {registro['primer_hallazgo']}")
    filas = resumir(registros)
    escribir_csv(RESULTADOS / "resumen.csv", filas)
    escribir_csv(RESULTADOS / "progreso.csv", [
        {"metodo": r["metodo"], "semilla": r["semilla"], "generacion": p.get("generacion", ""),
         "evaluaciones": p["evaluaciones"],
         "mejor_aptitud": p.get("mejor_aptitud_generacion", p.get("mejor_aptitud_hasta_ahora")),
         **{f"primer_{a}": p["primer_hallazgo"][a] or "no encontrado" for a in AGENTES}}
        for r in registros for p in r["progreso"]])
    casos = guardar_contraejemplos(hallazgos, LIMITE_EXPANSIONES)
    for f in filas:
        print(f)
    print(f"Contraejemplos guardados: {len(casos)}")


if __name__ == "__main__":
    ejecutar_experimentos()
