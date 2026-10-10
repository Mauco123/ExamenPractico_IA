from busqueda import evaluar
 
def calcular_aptitud(cromosoma, agente_objetivo='B1', limite_expansiones=100):
    """
    Evalúa un cromosoma y le asigna una puntuación numérica.
    A mayor puntuación, más apto es el grafo para reproducirse.
    """
    # 1. Convertir tu objeto CromosomaGrafo al formato JSON del profesor
    grafo_dict = cromosoma.a_formato_evaluador()
 
    # 2. Llamar al evaluador del profesor
    informe = evaluar(grafo_dict, limite_expansiones)
 
    # 3. Extraer los resultados del agente que estamos atacando en este momento (B1, U1 o A1)
    datos_agente = informe[agente_objetivo]
    estado = datos_agente['resultado']['estado']
    verificacion = datos_agente['verificacion']
    discrepancias = verificacion['discrepancias']
 
    # 4. Asignar la puntuación base según las reglas del proyecto:
    puntuacion = 0
 
    if estado in ('limite', 'error'):
        # El profesor indica que no son concluyentes, no sirven como contraejemplos.
        puntuacion = 0
 
    elif not discrepancias:
        # El grafo fue procesado y el agente no falló.
        # Le damos una puntuación bajita (ej. 10 puntos) solo por ser un grafo válido que terminó la ejecución.
        puntuacion = 10
 
    else:
        # ¡PREMIO MAYOR! El agente falló (ruta_invalida, costo_incorrecto, falso_sin_solucion, no_optimo).
        # Este es un contraejemplo real.
        puntuacion = 1000
 
    # 5. Criterio secundario de simplicidad (Desempate)
    # Bono de 30 - número de aristas: 0 aristas -> +30, 30 aristas -> +0.
    # Ej.: contraejemplo con 3 aristas = 1027, con 15 aristas = 1015.
    # Como el bono máximo es 30, nunca cambia el nivel (10 + 30 < 1000).
    # Los casos no concluyentes se quedan en 0 (sin bono).
    if puntuacion > 0:
        puntuacion += 30 - len(cromosoma.aristas)
 
    return puntuacion
