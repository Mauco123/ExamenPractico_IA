**INTEGRANTES**
- Arteaga Castillo Luis Angel
- Bahena Vargas Misael
- Rodriguez Gaytan Mauricio
- Rodriguez Zamora Yahir
- Trejo Ganzo Christopher Karol

**VERSIÓN DE PYTHON**
- Python 3.10 o superior. Probado con Python 3.14.4.

**ESTRUCTURA DEL PROYECTO**\
  cromosoma.py\
  docente.py\
  verificacion.py\
  evaluador.py\
  aptitud.py\
  algoritmo_genetico.py\
  busqueda_aleatoria.py\
  main.py\
  contraejemplo.py\
  pruebas/\
        _init_.py\
        evidencia_ejecucion.txt\
        test_proyecto.py\
  resultados/\
      resultado.json\
  contraejemplos/\
      casos.json


**COMANDOS PARA EJECUCIÓN DE PRUEBAS**

Todos se ejecutan desde la raíz del repositorio.

**Pruebas** -> python3 -m unittest discover -s pruebas -t . -v

**Ejecutar cada método** -> python3 main.py --metodo genetico --semilla 11, python3 main.py --metodo aleatorio --semilla 11

**Comparación principal: semillas 11, 22, 33, 44 y 55 en ambos métodos** -> python3 main.py

**Evaluar un contraejemplo fuera del ciclo evolutivo** -> python3 contraejemplos.py contraejemplos/caso_01.json


**DONDE COLOCAR EL PAQUETE DOCENTE**\
Falta


**DONDE SE GUARDAN LOS RESULTADOS**

resultados/configuracion.json -> Semillas, presupuesto, límite de expansiones, tamaño de población, versiones
resultados/<metodo>_s<semilla>.json -> Registro de las 10 ejecuciones principales
resultados/progreso.csv -> Progreso de las 10 ejecuciones  
resultados/resumen.csv -> Comparación por método y agente
contraejemplos/ ->  6 casos de prueba
resultados/individuales/ ->  Ejecuciones sueltas con --metodo

**TIEMPO DE EJECUCION**
python3 main.py -> (10 ejecuciones + contraejemplos) en 3.1 s 
Pruebas  en 1.3 s 
