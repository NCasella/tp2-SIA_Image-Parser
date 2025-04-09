import copy

from src.config import config
from src.individual import Individual
import random


def point_crossover(selected_individuals: list[Individual]) -> list[Individual]:
    crossover_chance: float = config["crossover_chance"]
    new_population: list[Individual] = []

    random.shuffle(selected_individuals)
    _length = len(selected_individuals)

    chromosomes_amount = len(selected_individuals[0].chromosomes)
    genes_per_chromosome = len(selected_individuals[0].chromosomes[0].genes)

    for i in range(0, _length - 1, 2):
        first = copy.deepcopy(selected_individuals[i])
        second = copy.deepcopy(selected_individuals[i + 1])
        for j in range(chromosomes_amount):
            if random.random() < crossover_chance:
                exchange_point = random.randint(1, genes_per_chromosome - 1)
                first_genes = first.chromosomes[j].genes
                second_genes = second.chromosomes[j].genes

                first_genes[:exchange_point], second_genes[:exchange_point] = (
                    second_genes[:exchange_point],
                    first_genes[:exchange_point],
                )

                first.fitness = 0.0
                second.fitness = 0.0
        new_population.extend([first, second])
    if _length % 2 == 1:
        new_population.append(copy.deepcopy(selected_individuals[-1]))
    return new_population

def crossover(selected_individuals: list[Individual]) -> list[Individual]:
    crossover_method: str = config["crossover"]
    crossover_methods: dict[str, callable] = {
        "one_point": point_crossover,
        "two_points": lambda: None,
        "uniform": lambda: None,
        "annul": lambda: None
    }
    return crossover_methods[crossover_method](selected_individuals)
