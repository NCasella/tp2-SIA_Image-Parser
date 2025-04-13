import random

from src.config import config
from src.chromosome import Chromosome, Genes
from src.individual import Individual

# this is one of the mutations over genes
def _new(genes: Genes, index: int):
    new_gene = Chromosome.generate_random_gene(index)
    genes[index] = new_gene

# this is the other one
def _delta(genes: Genes, index: int):
    if index == 0:
        delta = random.randint(-64, 64)
        idx = random.randint(0, 3)
        if delta < 0:
            genes[index][idx] = max(genes[index][idx] + delta, 0)
        else:
            genes[index][idx] = min(genes[index][idx] + delta, 255)
    elif index == 1:
        max_coordinate = config["max_coordinate"]
        delta = random.randint(-int(max_coordinate * 0.3), int(max_coordinate * 0.3))
        idx = random.randint(0, 2)
        axis = random.randint(0, 1)
        if axis == 0:
            genes[index][idx] = (genes[index][idx][axis] + delta, genes[index][idx][1])
        else:
            genes[index][idx] = (genes[index][idx][0], genes[index][idx][axis] + delta)


def _mutate_gene_at(genes: Genes, index: int):
    mutation_strategy: str = config["mutation_strategy"]
    if mutation_strategy == "new":
        _new(genes, index)
    elif mutation_strategy == "delta":
        _delta(genes, index)
    else:
        random.choice([_new, _delta])(genes, index)

def _gen_mutate(chromosome: Chromosome, individual: Individual):
    genes = chromosome.genes
    genes_amount = len(genes)
    random_gene_index = random.randint(0, genes_amount - 1)
    _mutate_gene_at(genes, random_gene_index)
    individual.fitness = 0.0

def gen_mutation(individuals: list[Individual]):
    mutation_chance: float = config["mutation_chance"]
    for individual in individuals:
        if random.random() < mutation_chance:
            random_chromosome = random.choice(individual.chromosomes)
            _gen_mutate(random_chromosome, individual)

def uniform_mutation(individuals: list[Individual]):
    mutation_chance: float = config["mutation_chance"]
    for individual in individuals:
        for chromosome in individual.chromosomes:
            for i in range(len(chromosome.genes)):
                if random.random()<mutation_chance:
                    _mutate_gene_at(chromosome.genes,i)
                    individual.fitness=0.0
            
def mutate(individuals: list[Individual]):
    mutation_method = config["mutation"]
    mutation_methods: dict[str, callable] = {
        "gen": gen_mutation,
        "multi_gen": lambda: None,
        "uniform": uniform_mutation,
        "non_uniform": lambda: None
    }
    mutation_methods[mutation_method](individuals)