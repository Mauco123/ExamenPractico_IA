"""Línea base: grafos independientes con la misma distribución que la población inicial
del AG (generar_aleatorio), el mismo evaluador y el mismo presupuesto. Sin selección ni
reproducción; la aptitud solo se calcula para registrar el mejor valor visto."""
import random
from cromosoma import CromosomaGrafo
from aptitud import calcular_aptitud


def puntos_control(pop_size, presupuesto, elitismo=1):
    """Mismos puntos (evaluaciones acumuladas) en que el AG cierra cada generación."""
    paso = pop_size - elitismo
    puntos = list(range(pop_size, presupuesto, paso))
    return set(puntos + [presupuesto])


def ejecutar_busqueda_aleatoria(evaluador, semilla, pop_size=50):
    random.seed(semilla)
    puntos = puntos_control(pop_size, evaluador.presupuesto)
    mejor, mejor_aptitud, progreso = None, -1, []
    while evaluador.restantes > 0:
        individuo = CromosomaGrafo().generar_aleatorio()
        aptitud = calcular_aptitud(evaluador.evaluar(individuo), individuo)
        if aptitud > mejor_aptitud:
            mejor, mejor_aptitud = individuo, aptitud
        if evaluador.consumidas in puntos:
            progreso.append({"evaluaciones": evaluador.consumidas,
                             "mejor_aptitud_hasta_ahora": mejor_aptitud,
                             "grafos_distintos": len(evaluador.distintos),
                             "primer_hallazgo": dict(evaluador.primer_hallazgo)})
    return mejor, mejor_aptitud, progreso
