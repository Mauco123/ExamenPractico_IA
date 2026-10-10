import random
from itertools import permutations

# Parámetros del dominio
N_NODOS = 6
INICIO = 0
META = 5
COSTO_MIN = 1
COSTO_MAX = 9

# Todos los pares dirigidos válidos (u, v) con u != v.
PARES_VALIDOS = list(permutations(range(N_NODOS), 2))
MAX_ARISTAS = len(PARES_VALIDOS)  # 30

class CromosomaGrafo:
    def __init__(self):
        # Formato: {(origen, destino): costo}
        self.aristas = {}

    def generar_aleatorio(self):
        """Llena self.aristas con un grafo aleatorio válido."""
        self.aristas.clear()
        k = random.randint(0, MAX_ARISTAS)
        seleccion = random.sample(PARES_VALIDOS, k)
        for u, v in seleccion:
            self.aristas[(u, v)] = random.randint(COSTO_MIN, COSTO_MAX)
        return self

    def a_formato_evaluador(self):
        """Traduce el diccionario interno al formato JSON del paquete docente."""
        lista_aristas = [[u, v, costo] for (u, v), costo in sorted(self.aristas.items())]
        return {
            "n": N_NODOS,
            "inicio": INICIO,
            "meta": META,
            "aristas": lista_aristas,
        }

    def __len__(self):
        return len(self.aristas)

    def __repr__(self):
        return f"CromosomaGrafo({len(self.aristas)} aristas)"