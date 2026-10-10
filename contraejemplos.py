"""Selección, explicación y reproducción de contraejemplos (fuera del ciclo evolutivo).

Uso para reproducir uno:  python3 contraejemplos.py contraejemplos/caso_01.json
"""
import json
import sys
from pathlib import Path

from docente import VERSION, AGENTES, ejecutar, verificar, heuristica, referencia
from cromosoma import CromosomaGrafo
from verificacion import clasificar

CARPETA = Path("contraejemplos")
MAX_CASOS = 6
REPETICIONES = 3


def explicar(agente, resultado, ref):
    ruta = resultado["ruta"]
    if resultado["estado"] == "sin_solucion":
        return f"{agente} dice que no hay ruta, pero la referencia sí encuentra una."
    if agente == "B1":
        return (f"BFS debe minimizar aristas: devolvió {ruta} con {len(ruta) - 1} aristas, "
                f"pero el mínimo es {ref['distancia_minima_aristas']}.")
    return (f"{agente} debe minimizar el costo: devolvió {ruta} con costo "
            f"{resultado['costo']}, pero el mínimo es {ref['costo_minimo']}.")


def reproducir(caso, repeticiones=REPETICIONES):
    """Vuelve a ejecutar el agente sobre el grafo guardado y compara."""
    ok = True
    for _ in range(repeticiones):
        r = ejecutar(caso["objetivo"], caso["grafo"], caso["limite_expansiones"])
        v = verificar(caso["objetivo"], caso["grafo"], r)
        ok &= (r == caso["resultado_objetivo"] and v["contraejemplo"]
               and clasificar(caso["objetivo"], caso["grafo"], r) == caso["discrepancias"])
    return ok


def guardar_contraejemplos(hallazgos, limite):
    """hallazgos: lista de (metodo, semilla, evaluador.hallazgos).
    Por agente: el grafo con menos aristas del AG y el de la aleatoria (sin duplicados)."""
    CARPETA.mkdir(exist_ok=True)
    for viejo in CARPETA.glob("caso_*.json"):
        viejo.unlink()
    usados, casos = set(), []
    for agente in AGENTES:
        for metodo in ("genetico", "aleatorio"):
            candidatos = sorted((len(clave), numero, semilla, clave)
                                for m, semilla, h in hallazgos if m == metodo
                                for clave, numero in h[agente].items())
            for _, numero, semilla, clave in candidatos:
                if clave in usados:
                    continue
                usados.add(clave)
                grafo = CromosomaGrafo()
                grafo.aristas = dict(clave)
                grafo = grafo.a_formato_evaluador()
                r = ejecutar(agente, grafo, limite)
                ref = referencia(grafo)
                caso = {"id": f"caso_{len(casos) + 1:02d}", "objetivo": agente,
                        "metodo": metodo, "semilla": semilla, "numero_evaluacion": numero,
                        "version_paquete": VERSION, "limite_expansiones": limite,
                        "grafo": grafo,
                        "heuristica": list(heuristica(grafo)) if agente == "A1" else "no aplica",
                        "referencia": ref, "resultado_objetivo": r,
                        "verificacion_docente": verificar(agente, grafo, r),
                        "discrepancias": clasificar(agente, grafo, r),
                        "explicacion": explicar(agente, r, ref)}
                caso["reproducido"] = reproducir(caso)
                (CARPETA / f"{caso['id']}.json").write_text(
                    json.dumps(caso, indent=2, ensure_ascii=False), encoding="utf-8")
                casos.append(caso)
                break
    lineas = ["# Índice de contraejemplos", "",
              "| Caso | Objetivo | Discrepancias | Método | Semilla | Evaluación | Reproducido |",
              "|---|---|---|---|---|---|---|"]
    lineas += [f"| {c['id']} | {c['objetivo']} | {', '.join(c['discrepancias'])} | {c['metodo']} "
               f"| {c['semilla']} | {c['numero_evaluacion']} | {'sí' if c['reproducido'] else 'NO'} |"
               for c in casos[:MAX_CASOS]]
    faltan = [a for a in AGENTES if a not in {c["objetivo"] for c in casos}]
    lineas += ["", "Sin contraejemplo: " + (", ".join(faltan) or "ninguno")]
    (CARPETA / "INDICE.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return casos[:MAX_CASOS]


if __name__ == "__main__":
    caso = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(caso["explicacion"])
    print("Reproducido:", "sí" if reproducir(caso) else "NO")
