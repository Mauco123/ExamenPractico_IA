import random
from itertools import permutations

# Parámetros del dominio
N_NODOS = 6
INICIO = 0
META = 5
COSTO_MIN = 1
COSTO_MAX = 9

# Todos los pares dirigidos válidos (u, v) con u != v
PARES_VALIDOS = list(permutations(range(N_NODOS), 2))
MAX_ARISTAS = len(PARES_VALIDOS)  # 30


class CromosomaGrafo:
    def __init__(self):
        # Formato: {(origen, destino): costo}
        self.aristas = {}

    def generar_aleatorio(self):

        #Llena self.aristas con un grafo aleatorio válido
        self.aristas.clear()
        k = random.randint(0, MAX_ARISTAS)
        seleccion = random.sample(PARES_VALIDOS, k)
        for u, v in seleccion:
            self.aristas[(u, v)] = random.randint(COSTO_MIN, COSTO_MAX)
        return self

    def a_formato_evaluador(self):

        #Traduce el diccionario interno al formato JSON del paquete docente
        lista_aristas = [[u, v, costo] for (u, v), costo in sorted(self.aristas.items())]
        return {
            "n": N_NODOS,
            "inicio": INICIO,
            "meta": META,
            "aristas": lista_aristas,
        }

    def clave(self):

        #Identidad del grafo: sirve para detectar duplicados y para la caché
        return tuple(sorted(self.aristas.items()))

    def copia(self):
        c = CromosomaGrafo()
        c.aristas = dict(self.aristas)
        return c

    @classmethod
    def desde_grafo(cls, grafo):

       #Inverso de a_formato_evaluador (para reproducir contraejemplos)
        validar_estructura(grafo)
        c = cls()
        c.aristas = {(u, v): w for u, v, w in grafo["aristas"]}
        return c

    def __len__(self):
        return len(self.aristas)

    def __repr__(self):
        return f"CromosomaGrafo({len(self.aristas)} aristas)"


def validar_estructura(grafo):

    #Validador estructural propio. Lanza ValueError si el grafo sale del dominio.
    if not isinstance(grafo, dict) or set(grafo) != {"n", "inicio", "meta", "aristas"}:
        raise ValueError("se requieren exactamente n, inicio, meta y aristas")
    if (grafo["n"], grafo["inicio"], grafo["meta"]) != (N_NODOS, INICIO, META):
        raise ValueError("dominio obligatorio: n=6, inicio=0, meta=5")
    if not isinstance(grafo["aristas"], list) or len(grafo["aristas"]) > MAX_ARISTAS:
        raise ValueError("aristas debe ser una lista de 0 a 30 elementos")
    vistos = set()
    for e in grafo["aristas"]:
        if not isinstance(e, list) or len(e) != 3 or any(type(x) is not int for x in e):
            raise ValueError(f"arista mal formada: {e!r}")
        u, v, w = e
        if (u, v) not in PARES_VALIDOS or not COSTO_MIN <= w <= COSTO_MAX or (u, v) in vistos:
            raise ValueError(f"arista fuera de dominio o duplicada: {e!r}")
        vistos.add((u, v))
    return True


if __name__ == "__main__":
    from docente import validar
    random.seed(0)
    for i in range(20):
        c = CromosomaGrafo().generar_aleatorio()
        g = c.a_formato_evaluador()
        validar_estructura(g)   # validador propio
        validar(g)              # validador del paquete docente
        assert CromosomaGrafo.desde_grafo(g).clave() == c.clave()
        print(f"{i:2d}: {c}")
    print("OK: 20 cromosomas válidos (validador propio y paquete docente)")
