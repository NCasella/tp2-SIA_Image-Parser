from PIL.Image import Image
from skimage.metrics import structural_similarity as ssim
import numpy as np

from src.individual import Individual
from math import ceil, exp
from src.config import config
import random
from skimage.color import rgb2lab, deltaE_ciede2000 as deltaE
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
    image_arr: np.ndarray = config["image_array"]
    width, height = image.size
    output_img = individual.get_current_image(width, height)
    output_arr = np.array(output_img, dtype=np.float32)
    fitness=ssim(image_arr, output_arr,data_range=255,channel_axis=-1,multiscale=True) + 2*compute_deltaE(image_arr,output_arr)
    individual.fitness=fitness
    return fitness

def compute_deltaE(image1_array,image2_array):
    rgb1 = image1_array[...,:3] / 255.0
    rgb2 = image2_array[...,:3] / 255.0
    lab1 = rgb2lab(rgb1)
    lab2 = rgb2lab(rgb2)
    delta_e = deltaE(lab1, lab2)
    mean_delta_e = np.mean(delta_e)

    # Normalize: higher ΔE = worse match → map to fitness-like score
    similarity = np.exp(-mean_delta_e/10.0)
    return similarity

def _get_fitness_values(individuals: list[Individual]):
    with Pool(processes=(3 * cpu_count() // 4)) as pool:
       fitness_values = pool.map(_optimized_calculate_fitness, individuals)
    for i, individual in enumerate(individuals):
        individual.fitness = fitness_values[i]
    return fitness_values

def _roulette_selection(individuals: list[Individual], choice_amount: int, fitness_per_individual: list[float], fitness_sum: float):
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

def roulette_selection(individuals: list[Individual],choice_amount: int):
    fitness_per_individual=_get_fitness_values(individuals)
    fitness_sum = sum(fitness_per_individual)
    return _roulette_selection(individuals=individuals, choice_amount=choice_amount, fitness_per_individual=fitness_per_individual, fitness_sum=fitness_sum)

def universal_selection(individuals: list[Individual],choice_amount: int):
    fitness_per_individual=_get_fitness_values(individuals)
    fitness_sum=sum(fitness_per_individual)
    
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
            if accumulated_fitness_per_individual[p] < ri <= accumulated_fitness_per_individual[p + 1]:
                selected_individuals.append(individuals[p])
                break
    return selected_individuals
    

def elite_selection(individuals: list[Individual],choice_amount: int):
    # we set the fitness of the individuals and sort them desc
    _get_fitness_values(individuals)
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
    tournament_size=10 
    fitness_per_individual=_get_fitness_values(individuals)
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
    
    while(len(selected_individuals)) < choice_amount:
        threshold = random.uniform(0.5, 1)
        individual1,individual2 = random.sample(individuals,k=2)
        r = random.uniform(0,1)
        best_fit_individual = individual1 if _calculate_fitness(individual=individual1)>_calculate_fitness(individual=individual2) else individual2
        worst_fit_individual = individual2 if best_fit_individual == individual1 else individual1
        selected_individuals.append(best_fit_individual) if r < threshold else selected_individuals.append(worst_fit_individual)
        
    return selected_individuals

def boltzmann_selection(individuals: list[Individual],choice_amount: int):
    initial_temperature: float = config["initial_temperature"]
    min_temperature: float = config["min_temperature"]
    decreasing_constant = 1/10
    temperature = min_temperature + (initial_temperature - min_temperature) * exp(-decreasing_constant * config["generation"])
    fitness_per_individual = _get_fitness_values(individuals)

    exp_fitness_per_individual = [exp(fitness/temperature) for fitness in fitness_per_individual]
    exp_sum = sum(exp_fitness_per_individual)
    exp_fitness_avg = exp_sum / len(exp_fitness_per_individual)
    exp_fitness_per_individual[:] = [fit / exp_fitness_avg for fit in exp_fitness_per_individual]
    exp_fitness_sum = exp_sum / exp_fitness_avg

    return _roulette_selection(individuals=individuals, choice_amount=choice_amount, fitness_per_individual=exp_fitness_per_individual, fitness_sum=exp_fitness_sum)

def ranking_selection(individuals: list[Individual],choice_amount: int):
    N = len(individuals)

    fitness_per_individual = _get_fitness_values(individuals)
    for idx, individual in enumerate(individuals):
        individual.fitness = fitness_per_individual[idx]

    sorted_individuals = sorted(individuals, key=lambda x: x.fitness, reverse=True)

    ranked_fitness_sum = 0
    ranked_fitness = []
    for individual in individuals:
        rank = sorted_individuals.index(individual) + 1
        ranked_fitness.append((N-rank)/N)
        ranked_fitness_sum += (N-rank)/N

    return _roulette_selection(individuals=individuals, choice_amount=choice_amount, fitness_per_individual=ranked_fitness, fitness_sum=ranked_fitness_sum)

def selection(individuals: list[Individual]) -> list[Individual]:
    selection_method: str = config["selection"]
    choice_amount = config["selection_amount"]
    selection_methods: dict[str, callable] = {
        "elite": elite_selection,
        "roulette": roulette_selection,
        "deterministic_tournament": deterministic_tournament_selection,
        "probabilistic_tournament": probabilistic_tournament_selection,
        "boltzmann": boltzmann_selection,
        "universal": universal_selection,
        "ranking": ranking_selection,
    }
    return selection_methods[selection_method](individuals, choice_amount)
