import random
from itertools import permutations
N_NODOS = 6
INICIO = 0
META = 5
COSTO_MIN = 1
COSTO_MAX = 9
PARES_VALIDOS = list(permutations(range(N_NODOS), 2))
MAX_ARISTAS = len(PARES_VALIDOS)  # 30
class CromosomaGrafo:
    def __init__(self):
        self.aristas = {}
    def generar_aleatorio(self):
        self.aristas.clear()
        k = random.randint(0, MAX_ARISTAS)
        seleccion = random.sample(PARES_VALIDOS, k)
        for u, v in seleccion:
            self.aristas[(u, v)] = random.randint(COSTO_MIN, COSTO_MAX)
        return self
    def a_formato_evaluador(self):
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
    try:
        from validador import validar
    except ImportError:
        validar = None
    for i in range(20):
        c = CromosomaGrafo().generar_aleatorio()
        g = c.a_formato_evaluador()
        pares = [(u, v) for u, v, _ in g["aristas"]]
        assert 0 <= len(pares) <= MAX_ARISTAS
        assert len(pares) == len(set(pares)), "aristas duplicadas"
        for u, v, costo in g["aristas"]:
            assert 0 <= u < N_NODOS and 0 <= v < N_NODOS and u != v

            assert COSTO_MIN <= costo <= COSTO_MAX
        if validar is not None:
            validar(g)
        print(f"{i:2d}: {c}")
    print("OK: 20 cromosomas válidos" + (" (validados con el paquete docente)" if validar else ""))