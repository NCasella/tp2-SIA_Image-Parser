from numpy import random, uint8

from typing import TypeAlias
from src.config import config

RGBA: TypeAlias = tuple[int,int,int,int]
XY: TypeAlias = tuple[float,float]
TriangleVertices: TypeAlias = tuple[XY, XY, XY]
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
            rgba = random.randint(low=0, high=255, size=4, dtype=uint8)
            return RGBA(rgba)
        elif index == 1:
            max_coordinate: float = config["max_coordinate"]
            vertices_arr = random.uniform(low=0, high=max_coordinate, size=(3, 2))
            return [tuple(row) for row in vertices_arr]

    def get_rgba(self) -> RGBA:
        return self.genes[0]

    def get_vertices(self) -> TriangleVertices:
        return self.genes[1]

    def __init__(self, genes: Genes):
        self.genes = genes
