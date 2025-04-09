from src.individual import Individual
from src.config import config
import random

def _young_next_generation(current_population: list[Individual], children: list[Individual]) -> list[Individual]:
    pass

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
        "young": lambda: None,
    }
    return criteria_methods[next_generation_criteria](current_population, children)
