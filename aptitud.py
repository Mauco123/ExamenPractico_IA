from busqueda import evaluar


def calcular_aptitud(cromosoma, agente_objetivo='B1', limite_expansiones=100):
    """
    Evalúa un cromosoma y le asigna una puntuación numérica.
    A mayor puntuación, más apto es el grafo para reproducirse.
    """
    # 1. Convertir el objeto CromosomaGrafo al formato JSON del profesor
    grafo_dict = cromosoma.a_formato_evaluador()

    # 2. Llamar al evaluador del profesor
    informe = evaluar(grafo_dict, limite_expansiones)

    # 3. Extraer resultados del agente objetivo (B1, U1 o A1)
    datos_agente = informe[agente_objetivo]
    estado = datos_agente['resultado']['estado']
    verificacion = datos_agente['verificacion']
    discrepancias = verificacion['discrepancias']

    # 4. Puntuación base según las reglas del proyecto
    if estado in ('limite', 'error'):
        # No concluyentes: no sirven como contraejemplos.
        puntuacion = 0
    elif not discrepancias:
        # Grafo válido y el agente no falló.
        puntuacion = 10
    else:
        # El agente falló: contraejemplo real.
        puntuacion = 1000

    # 5. Desempate por simplicidad: bono de 30 - número de aristas.
    # Máximo 30, así que nunca cambia de nivel (10 + 30 < 1000).
    # Los casos no concluyentes se quedan en 0 (sin bono).
    if puntuacion > 0:
        puntuacion += 30 - len(cromosoma.aristas)

    return puntuacion
