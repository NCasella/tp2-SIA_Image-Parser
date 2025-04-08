from PIL.Image import Image

from src.individual import Individual
from math import ceil
from src.config import config

from multiprocessing import Pool

def _calculate_fitness(individual: Individual):
    image: Image = config["image"]
    temp_fitness = 0
    width, height = image.size
    output_img = individual.get_current_image(width, height)
    for i in range(width):
        for j in range(height):
            output_r, output_g, output_b = output_img.getpixel((i, j))
            image_r, image_g, image_b = image.getpixel((i, j))
            r_diff = 255 - abs(output_r - image_r)
            g_diff = 255 - abs(output_g - image_g)
            b_diff = 255 - abs(output_b - image_b)
            total_diff = r_diff + g_diff + b_diff
            temp_fitness += total_diff
    return temp_fitness

def roulette_selection(individuals: list[Individual]):
    choice_amount = config["selection_amount"]

def elite_selection(individuals: list[Individual]):

    # we set the fitness of the individuals and sort them desc
    with Pool() as pool:
        fitness_values = pool.map(_calculate_fitness, individuals)
    for i, individual in enumerate(individuals):
        individual.fitness = fitness_values[i]
    # new list, so we can modify it on the crossover
    sorted_individuals = sorted(individuals, reverse=True)

    _length = len(sorted_individuals)

    choice_amount: int = config["selection_amount"]

    # case when K is less than N
    if choice_amount < _length:
        return sorted_individuals[:choice_amount]

    new_list = []
    for idx, individual in enumerate(sorted_individuals):
        amount = ceil((choice_amount - idx) / _length)
        for i in range(amount):
            new_list.append(individual)
    return new_list

def selection(individuals: list[Individual]):
    selection_method: str = config["selection"]
    selection_methods: dict[str, callable] = {
        "elite": elite_selection,
        "roulette": lambda: None,
        "deterministic_tournament": lambda: None,
        "probabilistic_tournament": lambda: None,
        "boltzman": lambda: None,
        "universal": lambda: None,
        "ranking": lambda: None,
    }
    return selection_methods[selection_method](individuals)
