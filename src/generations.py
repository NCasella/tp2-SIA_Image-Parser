from src.individual import Individual
from src.config import config
import random

def _young_next_generation(current_population: list[Individual], children: list[Individual]) -> list[Individual]:
    K:int=config["selection_amount"]
    N:int =config["population"]
    if K>N:
        return random.choices(children,K=N)
    selected_current_population=random.choices(current_population,k=N-K)
    selected_new_generation=random.choices(children,k=N)
    return selected_current_population+selected_new_generation

def _traditional_next_generation(current_population: list[Individual], children: list[Individual]) -> list[Individual]:
    generation_gap: float = config["generation_gap"]
    _length = len(current_population)
    old_amount = int((1 - generation_gap) * _length)
    new_amount = _length - old_amount
    random.shuffle(current_population)
    remaining_gen = current_population[:old_amount]
    population = current_population[old_amount:]
    joined_population = population + children
    return remaining_gen + random.choices(joined_population, k=new_amount)

def next_generation(current_population: list[Individual], children: list[Individual]) -> list[Individual]:
    next_generation_criteria: str = config["criteria"]
    criteria_methods: dict[str, callable] = {
        "traditional": _traditional_next_generation,
        "young": _young_next_generation,
    }
    return criteria_methods[next_generation_criteria](current_population, children)
