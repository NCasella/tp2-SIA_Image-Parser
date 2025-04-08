import sys
from PIL import Image

from src.config import init_config, config
from src.individual import Individual
from src.selections import selection
from src.crossovers import crossover
from src.mutations import mutate
from src.generations import next_generation
import os

def main():

  if len(sys.argv) < 2:
    print("Missing 'config.json' as parameter")
    exit(1)

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
  config["max_coordinate"] = max(2*width, 2*height)

  # generate the initial population
  population: list[Individual] = []
  for _ in range(population_amount):
    population.append(Individual.generate_random_individual(chromosome_amount=N))

  # apply the method
  max_generations: int = config["max_generations"]

  os.makedirs("images", exist_ok=True)

  for generation in range(max_generations):
    print(f"Generation {generation}")
    selected_individuals = selection(population)
    selected_individuals[0].get_current_image(width, height).save(f"images/generation-{generation}.png")
    children = crossover(selected_individuals)
    mutate(children)
    population = next_generation(population, children)
    print(len(population))

  image.close()

if __name__ == "__main__":
  main()