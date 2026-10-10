import json
import time
import random
from cromosoma import CromosomaGrafo
from algoritmo_genetico import AlgoritmoGenetico
from aptitud import calcular_aptitud
from docente import evaluar

SEMILLAS = [11, 22, 33, 44, 55]
AGENTES = ['B1', 'U1', 'A1']
MAX_EVALUACIONES = 1000
MAX_CONTRAEJEMPLOS = 6

def ejecutar_busqueda_aleatoria(semilla):
    random.seed(semilla)
    mejor_grafo = None
    mejor_aptitud = -1
    hallazgo_evaluacion_num = -1

    for num_evaluacion in range(1, MAX_EVALUACIONES + 1):
        individuo = CromosomaGrafo()
        individuo.generar_aleatorio()
        aptitud = calcular_aptitud(individuo)

        if aptitud > mejor_aptitud:
            mejor_aptitud = aptitud
            mejor_grafo = individuo
            if aptitud >= 1000 and hallazgo_evaluacion_num == -1:
                hallazgo_evaluacion_num = num_evaluacion

    return mejor_grafo, mejor_aptitud, hallazgo_evaluacion_num

def registro(semilla, mejor_grafo, mejor_aptitud, hallazgo, tiempo):
    return {
        "semilla": semilla,
        "mejor_aptitud": mejor_aptitud,
        "evaluacion_primer_hallazgo": hallazgo,
        "n_aristas": len(mejor_grafo.aristas) if mejor_grafo else 0,
        "grafo": mejor_grafo.a_formato_evaluador() if mejor_grafo else None,
        "tiempo_s": round(tiempo, 4),
    }

def ejecutar_experimentos():
    resultados_totales = {"genetico": [], "aleatorio": []}
    contraejemplos = []

    print("\n--- Iniciando Experimentos ---")
    for semilla in SEMILLAS:
        print(f"\nSemilla: {semilla}...")

        # --- 1. Algoritmo Genético ---
        inicio_tiempo_ag = time.time()
        ag = AlgoritmoGenetico(semilla, max_evaluaciones=MAX_EVALUACIONES)
        mejor_ag, aptitud_ag, hallazgo_ag = ag.ejecutar()
        tiempo_ag = time.time() - inicio_tiempo_ag
        resultados_totales["genetico"].append(registro(semilla, mejor_ag, aptitud_ag, hallazgo_ag, tiempo_ag))

        # --- 2. Búsqueda Aleatoria ---
        inicio_tiempo_ba = time.time()
        mejor_ba, aptitud_ba, hallazgo_ba = ejecutar_busqueda_aleatoria(semilla)
        tiempo_ba = time.time() - inicio_tiempo_ba
        resultados_totales["aleatorio"].append(registro(semilla, mejor_ba, aptitud_ba, hallazgo_ba, tiempo_ba))

        print(f"  AG:        aptitud={aptitud_ag}  hallazgo en eval {hallazgo_ag}")
        print(f"  Aleatorio: aptitud={aptitud_ba}  hallazgo en eval {hallazgo_ba}")

        # --- 3. Recolección de Contraejemplos ---
        for metodo, grafo, aptitud in (("genetico", mejor_ag, aptitud_ag), ("aleatorio", mejor_ba, aptitud_ba)):
            if aptitud >= 1000 and len(contraejemplos) < MAX_CONTRAEJEMPLOS:
                grafo_dict = grafo.a_formato_evaluador()
                informe = evaluar(grafo_dict)

                # Guardamos el contraejemplo indicando a qué agente rompió
                for agente in AGENTES:
                    if informe[agente]["verificacion"]["discrepancias"] and len(contraejemplos) < MAX_CONTRAEJEMPLOS:
                        contraejemplos.append({
                            "agente_roto": agente,
                            "metodo": metodo,
                            "semilla": semilla,
                            "aptitud": aptitud,
                            "grafo": grafo_dict,
                            "resultado_agente": informe[agente]["resultado"],
                            "discrepancias": informe[agente]["verificacion"]["discrepancias"],
                            "referencia": informe[agente]["verificacion"]["referencia"],
                        })
                        # Con que se registre para un agente roto es suficiente para no duplicar este grafo
                        break

    # --- 4. Guardar los registros ---
    with open('resultados_experimento.json', 'w', encoding='utf-8') as f:
        json.dump(resultados_totales, f, indent=2, ensure_ascii=False)

    with open('contraejemplos.json', 'w', encoding='utf-8') as f:
        json.dump(contraejemplos, f, indent=2, ensure_ascii=False)

    print("\nExperimentos completados. Resultados guardados.")

if __name__ == "__main__":
    ejecutar_experimentos()