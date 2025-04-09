from numpy import random

from typing import TypeAlias
from src.config import config
from numpy import uint8

RGBA: TypeAlias = list[int]
XY: TypeAlias = tuple[float,float]
TriangleVertices: TypeAlias = list[XY]
Genes: TypeAlias = list[RGBA, TriangleVertices]

class Chromosome:

    @staticmethod
    def generate_random_chromosome():
        genes = Chromosome.generate_random_genes()
        return Chromosome(genes)

    @staticmethod
    def generate_random_genes():
        rgba_gene = Chromosome.generate_random_gene(0)
        vertices_gene = Chromosome.generate_random_gene(1)
        return [rgba_gene, vertices_gene]

    @staticmethod
    def generate_random_gene(index: int):
        if index == 0:
            alpha = random.randint(low=100, high=128, dtype=uint8)
            rgb = random.randint(low=0, high=255, size=3, dtype=uint8)
            return RGBA((rgb[0],rgb[1],rgb[2],alpha))
        elif index == 1:
            max_coordinate: float = config["max_coordinate"]
            vertices_arr = random.uniform(low=-max_coordinate, high=max_coordinate, size=(3, 2))
            return [tuple(row) for row in vertices_arr]


    @staticmethod
    def exchange_genes(first_genes: Genes, second_genes: Genes):
        genes_per_chromosome = len(first_genes)

        # we'll choose a set of genes, and we choose one "sub-gene" to exchange
        if genes_per_chromosome <= 2:
            exchange_point = 1
        else:
            exchange_point = random.randint(1, genes_per_chromosome - 1)
        for i in range(exchange_point):
            sub_genes_length = len(first_genes[i])
            sub_genes_index = random.randint(0, sub_genes_length - 1)
            first_genes[i][sub_genes_index], second_genes[i][sub_genes_index] = second_genes[i][sub_genes_index], first_genes[i][sub_genes_index]

    def get_rgba(self) -> RGBA:
        return self.genes[0]

    def get_vertices(self) -> TriangleVertices:
        return self.genes[1]

    def __str__(self):
        return f"genes: {self.genes}"

    def __repr__(self):
        return str(self)

    def __init__(self, genes: Genes):
        self.genes = genes
