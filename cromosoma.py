import random

from itertools import permutations

# Parámetros del dominio

N_NODOS = 6

INICIO = 0

META = 5

COSTO_MIN = 1

COSTO_MAX = 9

# Todos los pares dirigidos válidos (u, v) con u != v.

# Con 6 nodos hay exactamente 6 * 5 = 30 pares, por eso el máximo es 30 aristas.

PARES_VALIDOS = list(permutations(range(N_NODOS), 2))

MAX_ARISTAS = len(PARES_VALIDOS)  # 30


class CromosomaGrafo:

    def __init__(self):
        # Usamos un diccionario para evitar aristas duplicadas por naturaleza.

        # Formato: {(origen, destino): costo}

        self.aristas = {}

    def generar_aleatorio(self):
        """

        Llena self.aristas con un grafo aleatorio válido.

        Reglas del dominio:

        - 0 a 30 aristas dirigidas únicas.

        - Costos entre 1 y 9.

        - Nodos del 0 al 5 (sin lazos al mismo nodo, es decir, u != v).

        """

        self.aristas.clear()

        # 1. Cuántas aristas tendrá este individuo (0 a 30)

        k = random.randint(0, MAX_ARISTAS)

        # 2. Elegir k pares distintos sin ciclos anidados:

        #    random.sample garantiza que no se repite ningún (u, v)

        #    y PARES_VALIDOS ya excluye los lazos u == v.

        seleccion = random.sample(PARES_VALIDOS, k)

        # 3. Asignar un costo aleatorio a cada arista

        for u, v in seleccion:
            self.aristas[(u, v)] = random.randint(COSTO_MIN, COSTO_MAX)

        return self

    def a_formato_evaluador(self):
        """

        Traduce el diccionario interno al formato exacto que exige el paquete docente.

        """

        # Se ordenan las aristas para que la salida sea determinista y fácil de comparar.

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


if __name__ == "__main__":

    # Prueba rápida: genera 20 cromosomas y revisa las reglas del dominio.

    # Si tienes el paquete del profesor a mano, cambia la importación por la real

    # (p. ej. `from material_busqueda.validador import validar`).

    try:

        from validador import validar  # ajustar a la ruta real del paquete docente

    except ImportError:

        validar = None

    for i in range(20):

        c = CromosomaGrafo().generar_aleatorio()

        g = c.a_formato_evaluador()

        # Verificación propia (independiente del validador docente)

        pares = [(u, v) for u, v, _ in g["aristas"]]

        assert 0 <= len(pares) <= MAX_ARISTAS

        assert len(pares) == len(set(pares)), "aristas duplicadas"

        for u, v, costo in g["aristas"]:
            assert 0 <= u < N_NODOS and 0 <= v < N_NODOS and u != v

            assert COSTO_MIN <= costo <= COSTO_MAX

        if validar is not None:
            validar(g)  # lanza ValueError si algo está mal

        print(f"{i:2d}: {c}")

    print("OK: 20 cromosomas válidos" + (" (validados con el paquete docente)" if validar else ""))