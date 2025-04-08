from src.config import config
from src.individual import Individual
import random

def point_crossover(selected_individuals: list[Individual]) -> list[Individual]:
    survivor = None
    _length = len(selected_individuals)
    if _length % 2 == 1:
        survivor = selected_individuals[-1]

    crossover_chance: float = config["crossover_chance"]

    # all individuals have the same amount of chromosomes
    first_individual = selected_individuals[0]
    chromosomes_amount = len(first_individual.chromosomes)
    # all chromosomes have the same amount of genes (in this case)
    genes_per_chromosome = len(first_individual.chromosomes[0].genes)
    for i in range(0, _length, 2):
        first, second = selected_individuals[i], selected_individuals[i + 1]
        for j in range(chromosomes_amount):
            chance = random.random()
            if chance < crossover_chance:
                exchange_amount = random.randint(0, genes_per_chromosome) - 1
                # this seems weird but what it does is basically exchange the genes sublist until the exchange_amount
                first.chromosomes[j].genes[:exchange_amount], second.chromosomes[j].genes[:exchange_amount] = second.chromosomes[j].genes[:exchange_amount], first.chromosomes[j].genes[:exchange_amount]
    if survivor:
        selected_individuals.append(survivor)
    return selected_individuals

def crossover(selected_individuals: list[Individual]) -> list[Individual]:
    crossover_method: str = config["crossover"]
    crossover_methods: dict[str, callable] = {
        "one_point": point_crossover,
        "two_points": lambda: None,
        "uniform": lambda: None,
        "annul": lambda: None
    }
    return crossover_methods[crossover_method](selected_individuals)
