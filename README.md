**Integrantes**

* Arteaga Castillo Luis Angel
* Bahena Vargas Misael
* Rodriguez Gaytan Mauricio
* Rodriguez Zamora Yahir
* Trejo Ganzo Christopher Karol
---
**Versión de Python**

* Python 3.10 o superior. Probado con Python 3.14.4.
---
**Estructura del proyecto**\
cromosoma.py\
docente.py\
verificacion.py\
evaluador.py\
aptitud.py\
algoritmo_genetico.py\
busqueda_aleatoria.py\
main.py\
contraejemplos.py\
uso_ia.md\
informe.md
pruebas/\
init.py\
evidencia_ejecucion.txt\
test_proyecto.py\
resultados/
resultado.json\
contraejemplos/
casos.json
material_docente/busqueda/\
_init_.py
_main_.py
objetivos




---
**Comandos para ejecución de pruebas**

* Pruebas -> python3 -m unittest discover -s pruebas -t . -v

* Ejecutar cada método -> python3 main.py --metodo genetico --semilla 11, python3 main.py --metodo aleatorio --semilla 11

* Comparación principal: semillas 11, 22, 33, 44 y 55 en ambos métodos -> python3 main.py

* Evaluar un contraejemplo fuera del ciclo evolutivo -> python3 contraejemplos.py contraejemplos/caso_01.json

---
**Dónde colocar el paquete docente**\
El paquete docente busqueda versión 1.0.0, sin modificar va en la carpeta material_docente/busqueda/ 

---
**Dónde se guardan los resultados**

* resultados/configuracion.json -> Semillas, presupuesto, límite de expansiones, tamaño de población, versiones
* resultados/_s.json -> Registro de las 10 ejecuciones principales
* resultados/progreso.csv -> Progreso de las 10 ejecuciones
* resultados/resumen.csv -> Comparación por método y agente
* contraejemplos/ ->  6 casos de prueba
* resultados/individuales/ ->  Ejecuciones sueltas con --metodo

---

**Tiempo de ejecución**
* python3 main.py -> (10 ejecuciones + contraejemplos) en 3.1 s
* Pruebas  en 1.3 s
