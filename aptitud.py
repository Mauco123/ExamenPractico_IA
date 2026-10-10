from busqueda import evaluar
 
def calcular_aptitud(cromosoma, agente_objetivo='B1', limite_expansiones=100):
    grafo_dict = cromosoma.a_formato_evaluador()
    informe = evaluar(grafo_dict, limite_expansiones)
    datos_agente = informe[agente_objetivo]
    estado = datos_agente['resultado']['estado']
    verificacion = datos_agente['verificacion']
    discrepancias = verificacion['discrepancias']
    puntuacion = 0
    if estado in ('limite', 'error'):
        puntuacion = 0
    elif not discrepancias:
        puntuacion = 10
    else:
        puntuacion = 1000
    if puntuacion > 0:
        puntuacion += 30 - len(cromosoma.aristas)
    return puntuacion

