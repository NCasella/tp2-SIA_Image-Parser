from PIL import Image, ImageDraw
from src.individual import Individual
from src.chromosome import Chromosome

def generate_output(individual, image_width, image_height):
    output = Image.new("RGBA", (image_width, image_height))
    draw = ImageDraw.Draw(output)

    for chromosome in individual.chromosomes:
        overlay = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.polygon(chromosome.vertices, fill=chromosome.rgba)
        output = Image.alpha_composite(output, overlay)
        overlay.close()

    rgb_output = output.convert("RGB")
    return rgb_output


individual = Individual.generate_random_individual(150, 900)

generate_output(individual, 900, 900)