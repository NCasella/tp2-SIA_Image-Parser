from PIL.Image import Image
from PIL.ImageChops import difference
from PIL.ImageStat import Stat
from PIL.ImageOps import invert

from src.individual import Individual
from math import ceil
from src.config import config
import random

from multiprocessing import Pool, cpu_count

def _optimized_calculate_fitness(individual: Individual):
    """
    Calculate fitness of individual in an optimized way, avoiding recalculating fitness values.
    Requires special handling on the crossover and mutation methods.
    :param individual: the individual whose fitness should be calculated
    :return: the fitness of the individual
    """
    if individual.fitness != 0.0:
        return individual.fitness
    return _calculate_fitness(individual)

def _calculate_fitness(individual: Individual):
    image: Image = config["image"]
    #temp_fitness = 0
    width, height = image.size
    output_img = individual.get_current_image(width, height)

    stat = Stat(invert(difference(image, output_img).convert("RGB")))
    return sum(stat.sum)

    #for i in range(width):
    #    for j in range(height):
    #        pixel_out = output_img.getpixel((i, j))
    #        pixel_ref = image.getpixel((i, j))
    #        temp_fitness += sum(255 - abs(out - ref) for out, ref in zip(pixel_ref[:4], pixel_out[:4]))
    #return temp_fitness

def roulette_selection(individuals: list[Individual],choice_amount: int):
    fitness_sum=0
    fitness_per_individual=[]
    for individual in individuals:
        individual_fitness=_calculate_fitness(individual=individual)
        fitness_sum+=individual_fitness
        fitness_per_individual.append(individual_fitness)
    
    accumulated_fitness_per_individual=[0]
    last_accumulated_fitness=0
    for fitness in fitness_per_individual:
        relative_fitness=fitness/fitness_sum
        last_accumulated_fitness+=relative_fitness
        accumulated_fitness_per_individual.append(last_accumulated_fitness)
    
    selected_individuals=[]
    while len(selected_individuals)<choice_amount:
        r=random.uniform(0,1)
        for i in range(len(accumulated_fitness_per_individual)-1):
            if accumulated_fitness_per_individual[i]<r and r<=accumulated_fitness_per_individual[i+1]:
                selected_individuals.append(individuals[i])
                break
    return selected_individuals

def universal_selection(individuals: list[Individual],choice_amount: int):
    fitness_sum=0
    fitness_per_individual=[]
    for individual in individuals:
        individual_fitness=_calculate_fitness(individual=individual)
        fitness_sum+=individual_fitness
        fitness_per_individual.append(individual_fitness)
    
    accumulated_fitness_per_individual=[0]
    last_accumulated_fitness=0
    for fitness in fitness_per_individual:
        relative_fitness=fitness/fitness_sum
        last_accumulated_fitness+=relative_fitness
        accumulated_fitness_per_individual.append(last_accumulated_fitness)
    
    selected_individuals=[]
    for i in range(choice_amount):
        r=random.uniform(0,1)
        ri=(r+i)/choice_amount
        for p in range(len(accumulated_fitness_per_individual)-1):
            if accumulated_fitness_per_individual[p]<ri and ri<=accumulated_fitness_per_individual[p+1]:
                selected_individuals.append(individuals[p])
                break
    return selected_individuals
    

def elite_selection(individuals: list[Individual],choice_amount: int):

    # we set the fitness of the individuals and sort them desc
    with Pool(processes=max(3 * cpu_count() // 4, 1)) as pool:
        fitness_values = pool.map(_optimized_calculate_fitness, individuals)
    for i, individual in enumerate(individuals):
        individual.fitness = fitness_values[i]
    # new list, so we can modify it on the crossover
    sorted_individuals = sorted(individuals, key=lambda ind: ind.fitness, reverse=True)

    _length = len(sorted_individuals)

    # case when K is less than N
    if choice_amount < _length:
        return sorted_individuals[:choice_amount]

    new_list = []
    for idx, individual in enumerate(sorted_individuals):
        amount = ceil((choice_amount - idx) / _length)
        for i in range(amount):
            new_list.append(individual)
    return new_list

def deterministic_tournament_selection(individuals: list[Individual],choice_amount: int):
    tournament_size=10 #TODO hacer el M dinamico
    fitness_per_individual=[_calculate_fitness(individual=individual) for individual in individuals]
    
    selected_individuals=[]
    while len(selected_individuals)<choice_amount:
        tournament_indices = random.sample(range(len(individuals)), tournament_size)
        tournament_individuals = [individuals[i] for i in tournament_indices]
        tournament_fitnesses = [fitness_per_individual[i] for i in tournament_indices]
        
        best_index = tournament_fitnesses.index(max(tournament_fitnesses))
        selected_individuals.append(tournament_individuals[best_index])

    return selected_individuals
  
def probabilistic_tournament_selection(individuals: list[Individual],choice_amount: int):
    selected_individuals=[]
    
    while(len(selected_individuals))<choice_amount:
        threshold=random.uniform(0.5, 1)
        individual1,individual2=random.sample(individuals,k=2)
        r=random.uniform(0,1)
        best_fit_individual=individual1 if _calculate_fitness(individual=individual1)>_calculate_fitness(individual=individual2) else individual2
        worst_fit_individual=individual2 if best_fit_individual==individual1 else individual1
        selected_individuals.append(best_fit_individual) if r<threshold else selected_individuals.append(worst_fit_individual)
        
    return selected_individuals

    


def selection(individuals: list[Individual]) -> list[Individual]:
    selection_method: str = config["selection"]
    choice_amount = config["selection_amount"]
    selection_methods: dict[str, callable] = {
        "elite": elite_selection,
        "roulette": roulette_selection,
        "deterministic_tournament": deterministic_tournament_selection,
        "probabilistic_tournament": probabilistic_tournament_selection,
        "boltzman": lambda: None,
        "universal": universal_selection,
        "ranking": lambda: None,
    }
    return selection_methods[selection_method](individuals, choice_amount)
