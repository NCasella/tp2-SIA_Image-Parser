# Tp2-SIA_Image-Parser
Para ejecutar el motor de generacion de imagenes se debe correr:

``python3 main.py config.json``

Dentro del archivo ```config.json``` se encuentran todos los parametros que recibe. Dependiendo del parametro, solo soportan ciertos valores.

- continue_latest: [true, false]
- save_progress: [true, false]
- polygon_amount: integer
- vertices: integer (3 para triangulo, 4 para cuadrilatero, etc...)
- image_path: path a la imagen original
- output_folder: path
- population: integer
- quality_factor: float [0.0-1.0]
- max_generations: integer
- selection: [ "elite", "roulette"," deterministic_tournament", "probabilistic_tournament", boltzmann, universal, "ranking" ]
- selection_amount: integer
- probabilistic_threshold: float [0.5-1.0]
- crossover: [ "one_point", "uniform" ]
- crossover_chance: float
- mutation_strategy: [ "new", "delta" ]
- mutation: [ "gen", "uniform" ]
- mutation_chance: float [0.0-1.0]
- criteria: [ "traditional", "young" ]
- generation_gap: float [0.0-1.0]
- initial_temperature: float [0.0-1.0]
- min_temperature: float

Para ejecutar múltiples archivos de configuración de forma paralela se debe correr:

``python3 batch_run.py``

Esto ejecutará todos los archivos de configuración dentro de la carpeta ``batch_config``
