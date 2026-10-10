from busqueda import evaluar

def calcular_aptitud(cromosoma, limite_expansiones=100):
    grafo_dict = cromosoma.a_formato_evaluador()
    informe = evaluar(grafo_dict, limite_expansiones)

    puntuacion_maxima = 0

    # Evaluamos la aptitud basándonos en si el grafo rompe a CUALQUIERA de los 3 agentes
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

        # Nos quedamos con el mejor impacto que tuvo este grafo
        if puntuacion_actual > puntuacion_maxima:
            puntuacion_maxima = puntuacion_actual

    # Criterio secundario de simplicidad (Desempate)
    if puntuacion_maxima > 0:
        puntuacion_maxima += 30 - len(cromosoma.aristas)

    return puntuacion_maxima