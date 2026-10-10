import random
from cromosoma import CromosomaGrafo, PARES_VALIDOS, COSTO_MIN, COSTO_MAX, MAX_ARISTAS
from aptitud import calcular_aptitud


class AlgoritmoGenetico:
    def __init__(self, evaluador, semilla, pop_size=50, prob_mutacion=0.2,
                 torneo_k=3, reintentos_duplicado=3):
        self.evaluador = evaluador
        self.semilla = semilla
        self.pop_size = pop_size
        self.prob_mutacion = prob_mutacion
        self.torneo_k = torneo_k
        self.reintentos_duplicado = reintentos_duplicado
        self.progreso = []
        random.seed(self.semilla)

    def configuracion(self):
        return {"pop_size": self.pop_size, "seleccion": f"torneo k={self.torneo_k}",
                "cruce": "unión de aristas de ambos padres y muestreo de k aristas",
                "prob_mutacion_por_hijo": self.prob_mutacion,
                "mutacion": "agregar / eliminar / cambiar costo de una arista",
                "elitismo": 1, "reemplazo": "generacional con elitismo",
                "duplicados": f"mutación forzada hasta {self.reintentos_duplicado} veces",
                "parada": "presupuesto de evaluaciones agotado"}

    def inicializar_poblacion(self):
        poblacion = []
        for _ in range(self.pop_size):
            individuo = CromosomaGrafo()
            individuo.generar_aleatorio()
            poblacion.append(individuo)
        return poblacion

    def seleccion_torneo(self, poblacion, aptitudes, k=3):
        indices = random.sample(range(len(poblacion)), min(k, len(poblacion)))
        # Gana la mayor aptitud; en empate, el primero sorteado (desempate aleatorio)
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

    def evaluar(self, individuo):
        evaluacion = self.evaluador.evaluar(individuo)
        return calcular_aptitud(evaluacion, individuo)

    def registrar(self, generacion, aptitudes):
        self.progreso.append({
            "generacion": generacion,
            "evaluaciones": self.evaluador.consumidas,
            "mejor_aptitud_generacion": max(aptitudes),
            "aptitud_media": round(sum(aptitudes) / len(aptitudes), 2),
            "grafos_distintos": len(self.evaluador.distintos),
            "primer_hallazgo": dict(self.evaluador.primer_hallazgo)})

    def ejecutar(self):
        poblacion = self.inicializar_poblacion()
        aptitudes = [self.evaluar(ind) for ind in poblacion]   # cuenta en el presupuesto
        self.registrar(0, aptitudes)
        generacion = 0
        while self.evaluador.restantes > 0:
            generacion += 1
            # Elitismo 1: el mejor pasa sin volver a evaluarse (empate: menor índice)
            i_mejor = max(range(len(poblacion)), key=lambda i: aptitudes[i])
            nueva, nuevas_apt = [poblacion[i_mejor]], [aptitudes[i_mejor]]
            vistos = {ind.clave() for ind in poblacion}
            while len(nueva) < self.pop_size and self.evaluador.restantes > 0:
                padre1 = self.seleccion_torneo(poblacion, aptitudes, self.torneo_k)
                padre2 = self.seleccion_torneo(poblacion, aptitudes, self.torneo_k)
                hijo = self.cruzar(padre1, padre2)
                self.mutar(hijo, self.prob_mutacion)
                for _ in range(self.reintentos_duplicado):   # evitar clones
                    if hijo.clave() not in vistos:
                        break
                    self.mutar(hijo, prob_mutacion=1.0)
                vistos.add(hijo.clave())
                nueva.append(hijo)
                nuevas_apt.append(self.evaluar(hijo))
            poblacion, aptitudes = nueva, nuevas_apt
            self.registrar(generacion, aptitudes)
        i_mejor = max(range(len(poblacion)), key=lambda i: aptitudes[i])
        return poblacion[i_mejor], aptitudes[i_mejor]
