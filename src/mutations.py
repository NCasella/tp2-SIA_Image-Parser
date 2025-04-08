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
    pass

def _mutate_gene_at(genes: Genes, index: int):
    mutation_strategy: str = config["mutation_strategy"]
    if mutation_strategy == "new":
        _new(genes, index)
    elif mutation_strategy == "delta":
        _delta(genes, index)
    else:
        random.choice([_new, _delta])(genes, index)

def _gen_mutate(chromosome: Chromosome):
    mutation_chance: float = config["mutation_chance"]
    chance = random.random()
    if chance < mutation_chance:
        genes = chromosome.genes
        genes_amount = len(genes)
        random_gene_index = random.randint(0, genes_amount - 1)
        _mutate_gene_at(genes, random_gene_index)

def gen_mutation(individuals: list[Individual]):
    for individual in individuals:
        for chromosome in individual.chromosomes:
            _gen_mutate(chromosome)

def mutate(individuals: list[Individual]):
    mutation_method = config["mutation"]
    mutation_methods: dict[str, callable] = {
        "gen": gen_mutation,
        "multi_gen": lambda: None,
        "uniform": lambda: None,
        "non_uniform": lambda: None
    }
    mutation_methods[mutation_method](individuals)