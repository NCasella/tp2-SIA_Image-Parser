from numpy import random, uint8

from typing import TypeAlias

RGBA: TypeAlias = tuple[int,int,int,int]
XY: TypeAlias = tuple[float,float]
TriangleVertices: TypeAlias = tuple[XY, XY, XY]

class Chromosome:

    @staticmethod
    def generate_random_chromosome(max_coordinate:int):
        rgba = random.randint(low=0, high=255, size=4, dtype=uint8)
        rgba = RGBA(rgba)
        vertices_arr = random.uniform(low=0,high=max_coordinate, size=(3,2))
        triangle_vertices = tuple([tuple(row) for row in vertices_arr])
        return Chromosome(rgba, triangle_vertices)

    def __init__(self, rgba: RGBA, vertices: TriangleVertices):
        self.rgba=rgba
        self.vertices=vertices
    
    


