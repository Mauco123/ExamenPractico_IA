from docente import evaluar

def calcular_aptitud(cromosoma, limite_expansiones=100):
    """
    Evalúa un cromosoma contra los 3 agentes y le asigna una puntuación.
    """
    grafo_dict = cromosoma.a_formato_evaluador()
    informe = evaluar(grafo_dict, limite_expansiones)

    puntuacion_maxima = 0

    # Buscamos si el grafo rompe a CUALQUIERA de los 3 agentes
    for agente in ['B1', 'U1', 'A1']:
        estado = informe[agente]['resultado']['estado']
        discrepancias = informe[agente]['verificacion']['discrepancias']

        puntuacion_actual = 0
        if estado in ('limite', 'error'):
            puntuacion_actual = 0
        elif not discrepancias:
            puntuacion_actual = 10
        else:
            puntuacion_actual = 1000

        if puntuacion_actual > puntuacion_maxima:
            puntuacion_maxima = puntuacion_actual

    # Criterio secundario de simplicidad (Desempate)
    # Bono de 30 - número de aristas
    if puntuacion_maxima > 0:
        puntuacion_maxima += 30 - len(cromosoma.aristas)

    return puntuacion_maxima