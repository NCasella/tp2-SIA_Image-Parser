from src.individual import Individual
from src.output_generator import generate_output
import numpy as np

def calculate_fitness(image, individuals: list[Individual]):
    width, height = image.size
    print(width, height)
    fitness = {}
    for individual in individuals:
        temp_fitness = 0
        output_img = generate_output(individual=individual, image_width=width, image_height=height)
        pixel_matrix = np.array(output_img)
        for i in range(height -1):
          for j in range(width - 1):
            print(i,j)
            output_r, output_g, output_b = output_img.getpixel((j, i))
            image_r, image_g, image_b = image.getpixel((j, i))
            r_diff = 255 - abs(output_r - image_r)
            g_diff = 255 - abs(output_g - image_g)
            b_diff = 255 - abs(output_b - image_b)
            total_diff = r_diff  + g_diff + b_diff
            temp_fitness += total_diff
        fitness[individual] = temp_fitness
        print(temp_fitness)
    return fitness

def roulette_selection(individuals: list[Individual]):
    aux = 1

def elite_selection(individuals: list[Individual], choice_amount: int):
    aux = 1

