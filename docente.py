"""Importa el paquete docente (v1.0.0) sin modificarlo, desde material_docente/."""
import sys
from pathlib import Path

RUTA = Path(__file__).resolve().parent / "material_docente"
sys.path.insert(0, str(RUTA))

from busqueda import (VERSION, evaluar, ejecutar, verificar,  # noqa: E402
                      referencia, heuristica, validar)

AGENTES = ("B1", "U1", "A1")
