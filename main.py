import random
import sys
import logging
from typing import Callable

from PIL import Image
import numpy as np

from src.config import init_config, config
from src.individual import Individual
from src.selections import selection
from src.crossovers import crossover
from src.mutations import mutate
from src.generations import next_generation
import os
import pickle
from multiprocessing import Pool, cpu_count

def apply_algorithm(logger: logging.Logger, population: list[Individual], width: int, height: int, func: Callable[[Individual, int, int, int], None]):
  max_generations: int = config["max_generations"]
  latest_gen: int = 0
  latest_gen_individual: Individual = None
  max_fitness: float = 0
  convergence_counter: int = 0
  convergence_max = 20
  mutation_counter: int = 0
  mutation_max = 20
  for generation in range(max_generations):
    logger.info(f"Generation %s", generation)
    selected_individuals = selection(population)
    latest_gen = generation
    latest_gen_individual = max(selected_individuals, key=lambda inf:inf.fitness)
    current_fitness = latest_gen_individual.fitness
    convergence_counter += 1
    if mutation_counter == mutation_max:
      mutation_counter = 0
      convergence_max += 5
    if convergence_counter == convergence_max:
      convergence_counter = 0
      new_mutation = random.uniform(0, 1)
      mutation_counter += 1
      logger.info(f"Changing the mutation chance to {new_mutation}")
      config["mutation_chance"] = new_mutation
    if current_fitness > max_fitness:
      convergence_counter = 0
      max_fitness = current_fitness
      logger.info(f"New max fitness: {current_fitness}")
      latest_gen_individual.get_current_image(width, height).save(config["output_folder"] + f"/best_current_individual.png")
    func(latest_gen_individual, generation, width, height)
    children = crossover(selected_individuals)
    mutate(children)
    population = next_generation(population, children)
    logger.info("Stopping the algorithm...")
    if latest_gen is not None:
      logger.info(f"Reached generation {latest_gen}")
    if latest_gen_individual:
      logger.info(f"Last fitness {latest_gen_individual.fitness}")
      latest_gen_individual.get_current_image(width, height).save(config["output_folder"] + f"/generation-{latest_gen}.png")
    logger.info("Saving latest generation...")
    with open(config["output_folder"] + "/latest.pkl", "wb") as latest_file:
      pickle.dump(population, latest_file)


def save_individual(individual: Individual, generation: int, width: int, height: int):
  individual.get_current_image(width, height).save(config["output_folder"] + f"/generation-{generation}.png")

def noop(individual: Individual, generation: int, width: int, height: int):
  pass

def main():

  if len(sys.argv) < 2:
    print("Missing 'config.json' as parameter")
    exit(1)

  # init the logger
  logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  logger = logging.getLogger("SIA_G8")

  # init the config
  init_config(sys.argv[1])

  # read the config
  N: int = config["triangles"]
  image_path: str = config["image_path"]
  population_amount: int = config["population"]
  quality_factor: float = config["quality_factor"]

  # read the original image
  image = Image.open(image_path).convert("RGBA")
  width, height = image.size
  width, height = int(width * quality_factor), int(height * quality_factor)

  # save the image on our config
  image = image.resize((width, height))
  config["image"] = image
  config["image_array"] = np.array(image.convert("RGB"), dtype=np.float32)
  config["max_coordinate"] = max(3 * width // 2, 3 * height // 2)

  os.makedirs(config["output_folder"], exist_ok=True)

  # generate the initial population
  population: list[Individual] = []

  continue_latest: bool = config["continue_latest"]
  if continue_latest and os.path.isfile(config["output_folder"] + "/latest.pkl"):
    with open(config["output_folder"] + "/latest.pkl", "rb") as latest_file:
      logger.info("Using the latest generation as the initial population...")
      population = pickle.load(latest_file)
      if len(population) < population_amount:
        with Pool(processes=cpu_count()) as pool:
          extension = pool.map(Individual.get_current_image, [N] * (population_amount - len(population)))
        population.extend(extension)
      elif len(population) > population_amount:
        population = population[:population_amount]
  else:
    logger.info("Generating a new population...")
    with Pool(processes=cpu_count()) as pool:
      individuals = pool.map(Individual.generate_random_individual, [N] * population_amount)
    population.extend(individuals)

  # apply the method

  save_progress: bool = config["save_progress"]
  if save_progress:
    func = save_individual
  else:
    func = noop
  apply_algorithm(logger, population, width, height, func)

  image.close()

if __name__ == "__main__":
  main()