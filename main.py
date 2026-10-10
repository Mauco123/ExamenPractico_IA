import json
import time
import random
from cromosoma import CromosomaGrafo
from algoritmo_genetico import AlgoritmoGenetico
from aptitud import calcular_aptitud
from busqueda import evaluar

# Semillas exigidas por el proyecto
SEMILLAS = [11, 22, 33, 44, 55]
AGENTES = ['B1', 'U1', 'A1']
MAX_EVALUACIONES = 1000
MAX_CONTRAEJEMPLOS = 6
CONTRAEJEMPLOS_POR_AGENTE = MAX_CONTRAEJEMPLOS // len(AGENTES)  # 2 por agente

def ejecutar_busqueda_aleatoria(agente, semilla):
    """
    Línea base: Genera y evalúa grafos completamente al azar sin cruza ni mutación.
    """
    random.seed(semilla)

    mejor_grafo = None
    mejor_aptitud = -1
    hallazgo_evaluacion_num = -1

    for num_evaluacion in range(1, MAX_EVALUACIONES + 1):
        individuo = CromosomaGrafo()
        individuo.generar_aleatorio()
        aptitud = calcular_aptitud(individuo, agente)

        if aptitud > mejor_aptitud:
            mejor_aptitud = aptitud
            mejor_grafo = individuo
            if aptitud >= 1000 and hallazgo_evaluacion_num == -1:
                hallazgo_evaluacion_num = num_evaluacion

    return mejor_grafo, mejor_aptitud, hallazgo_evaluacion_num

def registro(semilla, mejor_grafo, mejor_aptitud, hallazgo, tiempo):
    """Arma el diccionario que se guarda por cada corrida."""
    return {
        "semilla": semilla,
        "mejor_aptitud": mejor_aptitud,
        "evaluacion_primer_hallazgo": hallazgo,
        "n_aristas": len(mejor_grafo.aristas),
        "grafo": mejor_grafo.a_formato_evaluador(),
        "tiempo_s": round(tiempo, 4),
    }

def ejecutar_experimentos():
    """
    Ejecuta el Algoritmo Genético y la Búsqueda Aleatoria para todos los agentes y semillas.
    """
    resultados_totales = {
        "genetico": {agente: [] for agente in AGENTES},
        "aleatorio": {agente: [] for agente in AGENTES}
    }

    # Lista para almacenar los 6 contraejemplos representativos (Req. 11)
    contraejemplos = []

    for agente in AGENTES:
        print(f"\n--- Evaluando Agente: {agente} ---")
        contraejemplos_agente = 0

        for semilla in SEMILLAS:
            print(f"Semilla: {semilla}...")

            # --- 1. Ejecución del Algoritmo Genético ---
            inicio_tiempo_ag = time.time()
            ag = AlgoritmoGenetico(agente, semilla, max_evaluaciones=MAX_EVALUACIONES)
            mejor_ag, aptitud_ag, hallazgo_ag = ag.ejecutar()
            tiempo_ag = time.time() - inicio_tiempo_ag
            resultados_totales["genetico"][agente].append(
                registro(semilla, mejor_ag, aptitud_ag, hallazgo_ag, tiempo_ag))

            # --- 2. Ejecución de la Búsqueda Aleatoria ---
            inicio_tiempo_ba = time.time()
            mejor_ba, aptitud_ba, hallazgo_ba = ejecutar_busqueda_aleatoria(agente, semilla)
            tiempo_ba = time.time() - inicio_tiempo_ba
            resultados_totales["aleatorio"][agente].append(
                registro(semilla, mejor_ba, aptitud_ba, hallazgo_ba, tiempo_ba))

            print(f"  AG:        aptitud={aptitud_ag}  hallazgo en eval {hallazgo_ag}")
            print(f"  Aleatorio: aptitud={aptitud_ba}  hallazgo en eval {hallazgo_ba}")

            # --- 3. Recolección de Contraejemplos ---
            # Se guardan 2 por agente para que los 6 cubran a B1, U1 y A1.
            for metodo, grafo, aptitud in (("genetico", mejor_ag, aptitud_ag),
                                           ("aleatorio", mejor_ba, aptitud_ba)):
                if (aptitud >= 1000 and contraejemplos_agente < CONTRAEJEMPLOS_POR_AGENTE
                        and len(contraejemplos) < MAX_CONTRAEJEMPLOS):
                    grafo_dict = grafo.a_formato_evaluador()
                    datos = evaluar(grafo_dict)[agente]
                    contraejemplos.append({
                        "agente": agente,
                        "metodo": metodo,
                        "semilla": semilla,
                        "aptitud": aptitud,
                        "grafo": grafo_dict,
                        "resultado_agente": datos["resultado"],
                        "discrepancias": datos["verificacion"]["discrepancias"],
                        "referencia": datos["verificacion"]["referencia"],
                    })
                    contraejemplos_agente += 1

    # --- 4. Guardar los registros ---
    with open('resultados_experimento.json', 'w', encoding='utf-8') as f:
        json.dump(resultados_totales, f, indent=2, ensure_ascii=False)

    with open('contraejemplos.json', 'w', encoding='utf-8') as f:
        json.dump(contraejemplos, f, indent=2, ensure_ascii=False)

    print("\nExperimentos completados. Resultados guardados.")

if __name__ == "__main__":
    ejecutar_experimentos()