import sys
import logging
from PIL import Image

from src.config import init_config, config
from src.individual import Individual
from src.selections import selection
from src.crossovers import crossover
from src.mutations import mutate
from src.generations import next_generation
import os
import pickle

from multiprocessing import Pool, cpu_count

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
  image = Image.open(image_path)
  width, height = image.size
  block_width, block_height = int(width * quality_factor), int(height * quality_factor)

  # save the image on our config
  config["image"] = image.resize((block_width, block_height))
  config["max_coordinate"] = max(2 * width, 2 * height)

  os.makedirs("images", exist_ok=True)

  # generate the initial population
  population: list[Individual] = []

  continue_latest: bool = config["continue_latest"]
  if continue_latest and os.path.isfile("images/latest.pkl"):
    with open("images/latest.pkl", "rb") as latest_file:
      logger.info("Using the latest generation as the initial population...")
      population = pickle.load(latest_file)
  else:
    logger.info("Generating a new population...")
    with Pool(processes=cpu_count()) as pool:
      individuals = pool.map(Individual.generate_random_individual, [N] * population_amount)
    population.extend(individuals)

  # apply the method
  max_generations: int = config["max_generations"]

  for generation in range(max_generations):
    logger.info(f"Generation %s", generation)
    selected_individuals = selection(population)
    selected_individuals[0].get_current_image(width, height).save(f"images/generation-{generation}.png")
    children = crossover(selected_individuals)
    mutate(children)
    population = next_generation(population, children)

  # save the latest generation
  with open("images/latest.pkl", "wb") as latest_file:
    pickle.dump(population, latest_file)

  image.close()

if __name__ == "__main__":
  main()