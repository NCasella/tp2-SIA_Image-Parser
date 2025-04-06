import json
import sys
from PIL import Image
from src.individual import Individual
import os
from src.selections import calculate_fitness

def main():

  if len(sys.argv) < 2:
    print("Missing 'config.json' as parameter")
    exit(1)

  with open(sys.argv[1]) as config_file:
    config = json.load(config_file)

  # read the config
  N: int = config["triangles"]
  image_path: str = config["image_path"]
  population_amount: int = config["population"]
  blocks: int = config["blocks"]
  selection_amount: int = config["selection_amount"]

  # read the original image
  global image
  image = Image.open(image_path)
  width, height = image.size
  block_width, block_height = width // blocks, height // blocks
  global resized_image
  resized_image = image.resize((block_width, block_height))

  # generate the initial population
  population: list[Individual] = list()
  for _ in range(population_amount):
    population.append(Individual.generate_random_individual(max_coordinate=max(width, height), chromosome_amount=N))
  
  print(calculate_fitness(image=image, individuals=population))

  # selection
  selection_methods:dict[str,callable] = {
    "elite":lambda: None,
    "roulette":lambda: None,
    "deterministic_tournament":lambda: None,
    "probabilistic_tournament":lambda: None,
    "boltzman":lambda: None,
    "universal":lambda: None,
    "ranking":lambda: None,
  }
  crossover_methods:dict[str,callable] = {
    "one_point":lambda: None,
    "two_points":lambda: None,
    "uniform":lambda: None,
    "annul":lambda:None
  }
  mutation_methods:dict[str,callable] = {
    "gen":lambda: None,
    "multi_gen":lambda: None,
    "uniform":lambda: None,
    "non_uniform":lambda:None
  }
  criteria_methods:dict[str,callable] = {
    "traditional":lambda: None,
    "young":lambda: None,
  }


  # save output
  os.makedirs("images", exist_ok=True)
  resized_image.save("./images/resized_output.png")

  image.close()
  
  ## selection,mutation crossover, etc


if __name__ == "__main__":
  main()