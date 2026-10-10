import random
from cromosoma import CromosomaGrafo, PARES_VALIDOS, COSTO_MIN, COSTO_MAX, MAX_ARISTAS
from aptitud import calcular_aptitud

class AlgoritmoGenetico:
    def __init__(self, agente_objetivo, semilla, pop_size=50, max_evaluaciones=1000):
        self.agente_objetivo = agente_objetivo
        self.semilla = semilla
        self.pop_size = pop_size
        self.max_evaluaciones = max_evaluaciones
        self.evaluaciones_consumidas = 0

        # Fijar la semilla de aleatoriedad para la reproducibilidad que exige el proyecto
        random.seed(self.semilla)

    def inicializar_poblacion(self):
        """Crea una lista inicial de CromosomaGrafo generados aleatoriamente."""
        poblacion = []
        for _ in range(self.pop_size):
            individuo = CromosomaGrafo()
            individuo.generar_aleatorio()
            poblacion.append(individuo)
        return poblacion

    def seleccion_torneo(self, poblacion, aptitudes, k=3):
        """Selecciona al mejor individuo de una muestra al azar."""
        # k índices distintos al azar (sin pasarse del tamaño de la población)
        indices = random.sample(range(len(poblacion)), min(k, len(poblacion)))
        # El ganador es el de mayor aptitud entre los elegidos
        ganador = max(indices, key=lambda i: aptitudes[i])
        return poblacion[ganador]

    def cruzar(self, padre1, padre2):
        """Combina los diccionarios de aristas de dos padres para crear un hijo."""
        hijo = CromosomaGrafo()

        # Juntar las aristas de ambos padres. Si los dos tienen la misma (u, v)
        # con distinto costo, se hereda el costo de uno de ellos al azar.
        union = dict(padre1.aristas)
        for par, costo in padre2.aristas.items():
            if par not in union or random.random() < 0.5:
                union[par] = costo

        # El hijo tendrá un tamaño entre el de sus dos padres (y nunca más de MAX_ARISTAS)
        n1, n2 = len(padre1.aristas), len(padre2.aristas)
        k = random.randint(min(n1, n2), max(n1, n2))
        k = min(k, len(union), MAX_ARISTAS)

        # Elegir k aristas al azar de la unión
        for par in random.sample(list(union), k):
            hijo.aristas[par] = union[par]

        return hijo

    def mutar(self, cromosoma, prob_mutacion=0.2):
        """Altera ligeramente el grafo con una baja probabilidad."""
        if random.random() < prob_mutacion:
            aristas = cromosoma.aristas

            # Solo se consideran las mutaciones posibles para este grafo
            opciones = []
            if len(aristas) < MAX_ARISTAS:
                opciones.append('agregar')
            if len(aristas) > 0:
                opciones.extend(['eliminar', 'cambiar_costo'])

            tipo = random.choice(opciones)

            if tipo == 'agregar':
                # 1. Agregar una arista nueva (un par que aún no exista)
                libres = [par for par in PARES_VALIDOS if par not in aristas]
                aristas[random.choice(libres)] = random.randint(COSTO_MIN, COSTO_MAX)

            elif tipo == 'eliminar':
                # 2. Eliminar una arista existente
                del aristas[random.choice(list(aristas))]

            else:
                # 3. Cambiar el costo de una arista existente
                par = random.choice(list(aristas))
                aristas[par] = random.randint(COSTO_MIN, COSTO_MAX)

    def ejecutar(self):
        """Ciclo principal de evolución."""
        poblacion = self.inicializar_poblacion()
        mejor_global = None
        mejor_aptitud_global = -1
        hallazgo_evaluacion_num = -1  # Guardará en qué evaluación encontramos el primer error

        # Evaluamos hasta quedarnos sin presupuesto (1000 candidatos)
        while self.evaluaciones_consumidas < self.max_evaluaciones:
            aptitudes = []

            # 1. Evaluar a toda la población actual
            for ind in poblacion:
                # El profesor exige que no nos pasemos del presupuesto
                if self.evaluaciones_consumidas >= self.max_evaluaciones:
                    break

                aptitud = calcular_aptitud(ind, self.agente_objetivo)
                aptitudes.append(aptitud)
                self.evaluaciones_consumidas += 1

                # Rastrear al mejor individuo histórico
                if aptitud > mejor_aptitud_global:
                    mejor_aptitud_global = aptitud
                    mejor_global = ind
                    # Si la aptitud es altísima (>1000), significa que rompimos al agente
                    if aptitud >= 1000 and hallazgo_evaluacion_num == -1:
                        hallazgo_evaluacion_num = self.evaluaciones_consumidas

            # Si nos quedamos sin evaluaciones a mitad de la generación, rompemos el ciclo
            if self.evaluaciones_consumidas >= self.max_evaluaciones:
                break

            # 2. Crear la siguiente generación
            nueva_poblacion = []

            # Elitismo: Pasar al mejor individuo directamente para no perderlo
            nueva_poblacion.append(mejor_global)

            while len(nueva_poblacion) < self.pop_size:
                # Selección
                padre1 = self.seleccion_torneo(poblacion, aptitudes)
                padre2 = self.seleccion_torneo(poblacion, aptitudes)

                # Cruzamiento
                hijo = self.cruzar(padre1, padre2)

                # Mutación
                self.mutar(hijo)

                nueva_poblacion.append(hijo)

            poblacion = nueva_poblacion

        return mejor_global, mejor_aptitud_global, hallazgo_evaluacion_num
