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
        random.seed(self.semilla)

    def inicializar_poblacion(self):
        poblacion = []
        for _ in range(self.pop_size):
            individuo = CromosomaGrafo()
            individuo.generar_aleatorio()
            poblacion.append(individuo)
        return poblacion

    def seleccion_torneo(self, poblacion, aptitudes, k=3):

        indices = random.sample(range(len(poblacion)), min(k, len(poblacion)))
        # El ganador es el de mayor aptitud entre los elegidos
        ganador = max(indices, key=lambda i: aptitudes[i])
        return poblacion[ganador]

    def cruzar(self, padre1, padre2):
        hijo = CromosomaGrafo()

        union = dict(padre1.aristas)
        for par, costo in padre2.aristas.items():
            if par not in union or random.random() < 0.5:
                union[par] = costo

        n1, n2 = len(padre1.aristas), len(padre2.aristas)
        k = random.randint(min(n1, n2), max(n1, n2))
        k = min(k, len(union), MAX_ARISTAS)

        for par in random.sample(list(union), k):
            hijo.aristas[par] = union[par]

        return hijo

    def mutar(self, cromosoma, prob_mutacion=0.2):

        if random.random() < prob_mutacion:
            aristas = cromosoma.aristas

            opciones = []
            if len(aristas) < MAX_ARISTAS:
                opciones.append('agregar')
            if len(aristas) > 0:
                opciones.extend(['eliminar', 'cambiar_costo'])

            tipo = random.choice(opciones)

            if tipo == 'agregar':
                libres = [par for par in PARES_VALIDOS if par not in aristas]
                aristas[random.choice(libres)] = random.randint(COSTO_MIN, COSTO_MAX)

            elif tipo == 'eliminar':
                del aristas[random.choice(list(aristas))]

            else:
                par = random.choice(list(aristas))
                aristas[par] = random.randint(COSTO_MIN, COSTO_MAX)

    def ejecutar(self):
        poblacion = self.inicializar_poblacion()
        mejor_global = None
        mejor_aptitud_global = -1
        hallazgo_evaluacion_num = -1

        while self.evaluaciones_consumidas < self.max_evaluaciones:
            aptitudes = []

            for ind in poblacion:
                if self.evaluaciones_consumidas >= self.max_evaluaciones:
                    break

                aptitud = calcular_aptitud(ind, self.agente_objetivo)
                aptitudes.append(aptitud)
                self.evaluaciones_consumidas += 1

                if aptitud > mejor_aptitud_global:
                    mejor_aptitud_global = aptitud
                    mejor_global = ind
                    if aptitud >= 1000 and hallazgo_evaluacion_num == -1:
                        hallazgo_evaluacion_num = self.evaluaciones_consumidas

            if self.evaluaciones_consumidas >= self.max_evaluaciones:
                break

            nueva_poblacion = []

            nueva_poblacion.append(mejor_global)

            while len(nueva_poblacion) < self.pop_size:

                padre1 = self.seleccion_torneo(poblacion, aptitudes)
                padre2 = self.seleccion_torneo(poblacion, aptitudes)

                hijo = self.cruzar(padre1, padre2)

                self.mutar(hijo)

                nueva_poblacion.append(hijo)

            poblacion = nueva_poblacion

        return mejor_global, mejor_aptitud_global, hallazgo_evaluacion_num
