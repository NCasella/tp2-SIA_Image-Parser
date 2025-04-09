from src.chromosome import Chromosome
from PIL import Image, ImageDraw

class Individual:
    @staticmethod
    def generate_random_individual(chromosome_amount:int):
        chromosomes=[]
        for _ in range(chromosome_amount):
            chromosomes.append(Chromosome.generate_random_chromosome())
        return Individual(chromosomes=chromosomes)

    def __lt__(self, other):
        return self.fitness < other.fitness

    def get_current_image(self, image_width: int, image_height: int) -> Image:
        output = Image.new("RGBA", (image_width, image_height))

        for chromosome in self.chromosomes:
            overlay = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.polygon(chromosome.get_vertices(), fill=tuple(chromosome.get_rgba()))
            output = Image.alpha_composite(output, overlay)
            overlay.close()

        return output

    def __str__(self):
        return f"""
            chromosomes: {self.chromosomes},
            fitness: {self.fitness}
        """

    def __repr__(self):
        return str(self)

    def __init__(self, chromosomes:list[Chromosome]):
        self.chromosomes=chromosomes
        self.fitness = 0.0