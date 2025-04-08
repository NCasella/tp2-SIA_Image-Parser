from PIL.Image import Image

from src.individual import Individual
from math import ceil
from src.config import config
import random

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
    
    fitness_sum=0
    fitness_per_individual=[]
    for individual in individuals:
        individual_fitness=_calculate_fitness(individual=individual)
        fitness_sum+=individual_fitness
        fitness_per_individual.append(individual_fitness)
    
    if fitness_sum==0:
        return random.choices(individuals, k=choice_amount)
    
    probabilites=[f/fitness_sum for f in fitness_per_individual]
    return random.choices(individuals, weights=probabilites, k=choice_amount)
    

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

def deterministic_tournament_selection(individuals: list[Individual]):
    tournament_size=10 #TODO hacer el M dinamico
    choice_amount = config["selection_amount"]
    fitness_per_individual=[_calculate_fitness(individual=individual) for individual in individuals]
    
    selected_individuals=[]
    while len(selected_individuals)<choice_amount:
        tournament_indices = random.sample(range(len(individuals)), tournament_size)
        tournament_individuals = [individuals[i] for i in tournament_indices]
        tournament_fitnesses = [fitness_per_individual[i] for i in tournament_indices]
        
        best_index = tournament_fitnesses.index(max(tournament_fitnesses))
        selected_individuals.append(tournament_individuals[best_index])

    return selected_individuals
  
def probabilistic_tournament_selection(individuals: list[Individual]):
    choice_amount = config["selection_amount"]
    selected_individuals=[]
    
    while(len(selected_individuals))<choice_amount:
        threshold=random.uniform(0.5, 1)
        individual1,individual2=random.sample(individuals,k=2)
        r=random.uniform(0,1)
        best_fit_individual=individual1 if _calculate_fitness(individual=individual1)>_calculate_fitness(individual=individual2) else individual2
        worst_fit_individual=individual2 if best_fit_individual==individual1 else individual1
        selected_individuals.append(best_fit_individual) if r<threshold else selected_individuals.append(worst_fit_individual)
        
    return selected_individuals

    


def selection(individuals: list[Individual]):
    selection_method: str = config["selection"]
    selection_methods: dict[str, callable] = {
        "elite": elite_selection,
        "roulette": roulette_selection,
        "deterministic_tournament": deterministic_tournament_selection,
        "probabilistic_tournament": probabilistic_tournament_selection,
        "boltzman": lambda: None,
        "universal": lambda: None,
        "ranking": lambda: None,
    }
    return selection_methods[selection_method](individuals)
