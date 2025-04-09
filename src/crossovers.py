import copy

from src.config import config
from src.individual import Individual
from src.chromosome import Chromosome, Genes
import random


def point_crossover(selected_individuals: list[Individual]) -> list[Individual]:
    crossover_chance: float = config["crossover_chance"]
    new_population: list[Individual] = []

    random.shuffle(selected_individuals)
    _length = len(selected_individuals)

    chromosomes_amount = len(selected_individuals[0].chromosomes)

    for i in range(0, _length - 1, 2):
        first = copy.deepcopy(selected_individuals[i])
        second = copy.deepcopy(selected_individuals[i + 1])
        for j in range(chromosomes_amount):
            if random.random() < crossover_chance:
                first_genes = first.chromosomes[j].genes
                second_genes = second.chromosomes[j].genes
                Chromosome.exchange_genes(first_genes, second_genes)

                first.fitness = 0.0
                second.fitness = 0.0
        new_population.extend([first, second])
    if _length % 2 == 1:
        new_population.append(copy.deepcopy(selected_individuals[-1]))
    return new_population
def uniform_crossover(selected_individuals: list[Individual])-> list[Individual]:
    crossover_chance: float = config["crossover_chance"]
    uniform_crossover_chance: float = config["uniform_crossover_chance"]
    new_population: list[Individual] = []

    random.shuffle(selected_individuals)
    _length = len(selected_individuals)

    for i in range(0,_length-1,2):
        parent1=selected_individuals[i]
        parent2=selected_individuals[i+1]
        if random.random()>crossover_chance:
            new_population.append(copy.deepcopy(parent1))
            new_population.append(copy.deepcopy(parent2))
            continue
        child1_chroms=[]
        child2_chroms=[]
        for chrom1,chrom2 in zip(parent1.chromosomes,parent2.chromosomes):
            if random.random()<uniform_crossover_chance:
                rgba1=chrom2.get_rgba()
                vertices1=chrom2.get_vertices()
                rgba2=chrom1.get_rgba()
                vertices2=chrom1.get_vertices()
            else:
                rgba1=chrom1.get_rgba()
                vertices1=chrom1.get_vertices()
                rgba2=chrom2.get_rgba()
                vertices2=chrom2.get_vertices()
            genes1=Genes((rgba1,vertices1))
            genes2=Genes((rgba2,vertices2))
            child1_chroms.append(Chromosome(genes1))
            child2_chroms.append(Chromosome(genes2))
        new_population.append(Individual(child1_chroms))
        new_population.append(Individual(child2_chroms))
    return new_population

def crossover(selected_individuals: list[Individual]) -> list[Individual]:
    crossover_method: str = config["crossover"]
    crossover_methods: dict[str, callable] = {
        "one_point": point_crossover,
        "two_points": lambda: None,
        "uniform": uniform_crossover,
        "annul": lambda: None
    }
    return crossover_methods[crossover_method](selected_individuals)
