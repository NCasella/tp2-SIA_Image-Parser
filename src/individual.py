from src.chromosome import Chromosome

class Individual:
    @staticmethod
    def generate_random_individual(chromosome_amount:int, max_coordinate:int):
        chromosomes=[]
        for _ in range(chromosome_amount):
            chromosomes.append(Chromosome.generate_random_chromosome(max_coordinate=max_coordinate))
        return Individual(chromosomes=chromosomes)
        

    def __init__(s,chromosomes:list[Chromosome]):
        s.chromosomes=chromosomes
    
