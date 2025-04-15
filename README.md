# Tp2-SIA_Image-Parser
Para ejecutar el motor de generacion de imagenes se debe correr:

``python3 main.py config.json``

Dentro del archivo ```config.json``` se encuentran todos los parametros que recibe. Dependiendo del parametro, solo soportan ciertos valores.


- selection: [ "elite", "roulette"," deterministic_tournament", "probabilistic_tournament", boltzmann, universal, "ranking" ] 
- crossover: [ "one_point", "uniform" ]
- mutation: [ "gen", "uniform" ]
- mutation_strategy: [ "new", "delta" ]
- criteria: [ "traditional", "young" ]

Para ejecutar múltiples archivos de configuración de forma paralela se debe correr:

``python3 batch_run.py``

Esto ejecutará todos los archivos de configuración dentro de la carpeta ``batch_config``
