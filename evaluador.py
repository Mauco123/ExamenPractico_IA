"""Evaluador común: único punto por el que el AG y la búsqueda aleatoria evalúan grafos."""
from collections import Counter

from docente import evaluar, AGENTES
from cromosoma import validar_estructura
from verificacion import clasificar


class PresupuestoAgotado(Exception):
    pass


class EvaluadorComun:
    def __init__(self, presupuesto=1000, limite_expansiones=100):
        self.presupuesto = presupuesto
        self.limite = limite_expansiones
        self.consumidas = 0
        self.cache = {}                       # ahorra cómputo, NO presupuesto
        self.distintos = set()
        self.incidencias = Counter()          # limite, error, desacuerdo, equipo
        self.primer_hallazgo = {a: None for a in AGENTES}
        self.hallazgos = {a: {} for a in AGENTES}   # clave del grafo -> nº de evaluación

    @property
    def restantes(self):
        return self.presupuesto - self.consumidas

    def evaluar(self, cromosoma):
        if self.consumidas >= self.presupuesto:
            raise PresupuestoAgotado()
        self.consumidas += 1                  # cuenta aunque el grafo esté repetido
        numero = self.consumidas
        clave = cromosoma.clave()
        self.distintos.add(clave)
        try:
            grafo = cromosoma.a_formato_evaluador()
            validar_estructura(grafo)
            if clave not in self.cache:
                self.cache[clave] = evaluar(grafo, self.limite)
            informe = self.cache[clave]
        except Exception as exc:              # fallo NUESTRO, no del agente
            self.incidencias[f"equipo:{type(exc).__name__}"] += 1
            return {"numero": numero, "agentes": None, "referencia": None,
                    "error_equipo": f"{type(exc).__name__}: {exc}"}
        agentes = {}
        for a in AGENTES:
            r = informe[a]["resultado"]
            ver = informe[a]["verificacion"]
            if r["estado"] in ("limite", "error"):
                clase, propias = r["estado"], []
            else:
                propias = clasificar(a, grafo, r)
                if propias != sorted(ver["discrepancias"]):
                    clase = "desacuerdo"          # no se cuenta como hallazgo
                else:
                    clase = "contraejemplo" if propias else "correcto"
            if clase in ("limite", "error", "desacuerdo"):
                self.incidencias[f"{a}:{clase}"] += 1
            if clase == "contraejemplo":
                if self.primer_hallazgo[a] is None:
                    self.primer_hallazgo[a] = numero
                self.hallazgos[a].setdefault(clave, numero)
            agentes[a] = {"clase": clase, "discrepancias": propias, "resultado": r}
        return {"numero": numero, "agentes": agentes, "error_equipo": None,
                "referencia": informe["B1"]["verificacion"]["referencia"]}

    def resumen(self):
        return {"evaluaciones": self.consumidas,
                "grafos_distintos": len(self.distintos),
                "primer_hallazgo": {a: n if n is not None else "no encontrado"
                                    for a, n in self.primer_hallazgo.items()},
                "incidencias": dict(self.incidencias)}
