"""Pruebas del trabajo propio. Ejecutar desde la raíz: python3 -m unittest discover -s pruebas -t . -v
Los grafos y resultados de estas pruebas son datos CONTROLADOS escritos a mano,
no contraejemplos descubiertos por el experimento."""
import random
import unittest

from docente import validar
from cromosoma import CromosomaGrafo, validar_estructura
from verificacion import clasificar
from evaluador import EvaluadorComun, PresupuestoAgotado
from algoritmo_genetico import AlgoritmoGenetico
from busqueda_aleatoria import ejecutar_busqueda_aleatoria


def grafo(aristas):
    return {"n": 6, "inicio": 0, "meta": 5, "aristas": aristas}


def sol(ruta, costo):
    return {"estado": "solucion", "ruta": ruta, "costo": costo, "expansiones": 1, "error": None}


SIN = {"estado": "sin_solucion", "ruta": None, "costo": None, "expansiones": 1, "error": None}
EMPATE = grafo([[0, 1, 2], [1, 5, 3], [0, 2, 4], [2, 5, 1]])      # 0-1-5 y 0-2-5 cuestan 5
CORTA_CARA = grafo([[0, 5, 9], [0, 1, 1], [1, 2, 1], [2, 5, 1]])  # 0-5 (9) vs 0-1-2-5 (3)


class Formato(unittest.TestCase):
    def test_adaptador_ida_y_vuelta(self):
        random.seed(1)
        for _ in range(300):
            c = CromosomaGrafo().generar_aleatorio()
            g = c.a_formato_evaluador()
            validar_estructura(g)
            validar(g)                                   # el paquete lo acepta
            self.assertEqual(CromosomaGrafo.desde_grafo(g).clave(), c.clave())

    def test_rechaza_fuera_de_dominio(self):
        for aristas in ([[0, 0, 1]], [[0, 1, 0]], [[0, 1, 10]], [[0, 1, 1], [0, 1, 2]],
                        [[True, 1, 2]], [[0, 6, 1]]):
            with self.assertRaises(ValueError):
                validar_estructura(grafo(aristas))

    def test_sin_ruta_es_valido(self):
        self.assertTrue(validar_estructura(grafo([[0, 1, 1], [1, 0, 1]])))


class Operadores(unittest.TestCase):
    def test_cruce_y_mutacion_preservan_dominio(self):
        ag = AlgoritmoGenetico(EvaluadorComun(1), semilla=7)
        for _ in range(500):
            p1 = CromosomaGrafo().generar_aleatorio()
            p2 = CromosomaGrafo().generar_aleatorio()
            hijo = ag.cruzar(p1, p2)
            self.assertTrue(set(hijo.aristas) <= set(p1.aristas) | set(p2.aristas))
            ag.mutar(hijo, prob_mutacion=1.0)
            validar_estructura(hijo.a_formato_evaluador())


class Clasificacion(unittest.TestCase):
    def test_ausencia_de_ruta(self):
        self.assertEqual(clasificar("U1", grafo([[0, 1, 1]]), SIN), [])
        self.assertEqual(clasificar("U1", EMPATE, SIN), ["falso_sin_solucion"])

    def test_rutas_alternativas_de_igual_calidad(self):
        for a in ("B1", "U1", "A1"):
            self.assertEqual(clasificar(a, EMPATE, sol([0, 1, 5], 5)), [])
            self.assertEqual(clasificar(a, EMPATE, sol([0, 2, 5], 5)), [])

    def test_costo_declarado_incorrecto(self):
        self.assertEqual(clasificar("U1", EMPATE, sol([0, 1, 5], 4)), ["costo_incorrecto"])

    def test_ruta_invalida(self):
        self.assertEqual(clasificar("B1", EMPATE, sol([0, 5], 5)), ["ruta_invalida"])

    def test_bfs_por_aristas_ucs_por_costo(self):
        self.assertEqual(clasificar("B1", CORTA_CARA, sol([0, 5], 9)), [])
        self.assertEqual(clasificar("U1", CORTA_CARA, sol([0, 5], 9)), ["no_optimo"])

    def test_limite_no_es_contraejemplo(self):
        ev = EvaluadorComun(presupuesto=1, limite_expansiones=0)
        e = ev.evaluar(CromosomaGrafo.desde_grafo(EMPATE))
        self.assertTrue(all(d["clase"] == "limite" for d in e["agentes"].values()))
        self.assertEqual(ev.primer_hallazgo, {"B1": None, "U1": None, "A1": None})


class Presupuesto(unittest.TestCase):
    def test_repetidos_consumen_presupuesto(self):
        ev = EvaluadorComun(presupuesto=3)
        c = CromosomaGrafo.desde_grafo(EMPATE)
        for _ in range(3):
            ev.evaluar(c)
        self.assertEqual((ev.consumidas, len(ev.distintos)), (3, 1))
        with self.assertRaises(PresupuestoAgotado):
            ev.evaluar(c)

    def test_metodos_usan_exactamente_1000(self):
        ev1, ev2 = EvaluadorComun(1000), EvaluadorComun(1000)
        AlgoritmoGenetico(ev1, 11).ejecutar()
        ejecutar_busqueda_aleatoria(ev2, 11)
        self.assertEqual((ev1.consumidas, ev2.consumidas), (1000, 1000))

    def test_semilla_fija_reproduce(self):
        corridas = []
        for _ in range(2):
            ev = EvaluadorComun(1000)
            ag = AlgoritmoGenetico(ev, 22)
            ag.ejecutar()
            corridas.append((ev.resumen(), ag.progreso))
        self.assertEqual(corridas[0], corridas[1])


if __name__ == "__main__":
    unittest.main()
