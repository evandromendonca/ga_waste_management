import ga
from chromosome import Chromosome

class Population:
    def __init__(self, helper, edges=None, trucks=None, randomize=None, pop=None, tour=None, cross=None, mut=None):
        self.chromosomes = []
        self.helper = helper
        self.best_fitness = None
        
        self.POPULATION_SIZE = pop
        self.TOURNAMENT_SIZE = tour
        self.CROSSOVER_RATE = cross
        self.MUTATION_SWAP_RATE = mut
        self.MUTATION_INVERSION_RATE = mut
        
        # generate a random population given the edges and trucks
        if randomize == True and edges != None and trucks != None:
            self.chromosomes = ga.randomize_population(edges, trucks, self.helper.corresponding_edges, self.POPULATION_SIZE)

    def get_best_fitness(self):
        if self.best_fitness == None:
            self.best_fitness = ga.get_best_fitness(self.chromosomes, self.helper)
        return self.best_fitness

    #@profile 
    def evolve(self):
        # create a new population
        new_population = Population(self.helper, pop=self.POPULATION_SIZE, tour=self.TOURNAMENT_SIZE, cross=self.CROSSOVER_RATE, mut=self.MUTATION_INVERSION_RATE)

        # the best fitting solution go to the next population automatically (ELITISM)
        best_fit = ga.get_best_fitness(self.chromosomes, self.helper)                
        
        elit_chromosome = Chromosome()
        elit_chromosome.path = list(best_fit.path)
        elit_chromosome.trucks_used = list(best_fit.trucks_used)

        new_population.chromosomes.append(elit_chromosome)

        elit_unchanged = Chromosome()
        elit_unchanged.path = list(best_fit.path)
        elit_unchanged.trucks_used = list(best_fit.trucks_used)

        # crossover
        for _ in range((self.POPULATION_SIZE - 2)/2):
            #print 'generating child ' + str(i)
            # must select parent 1 using TOURNAMENT SELECTION
            parent_1 = ga.tournament_selection(self.chromosomes, self.helper, self.TOURNAMENT_SIZE)
            # must select parent 2 using TOURNAMENT SELECTION
            parent_2 = ga.tournament_selection(self.chromosomes, self.helper, self.TOURNAMENT_SIZE)
            
            # crossover these chomosomes
            child = ga.crossover(parent_1, parent_2, self.helper, self.CROSSOVER_RATE)            
            child.fitness = None  # reset the fitness (it was calculated in the tournament and yet can mutate)
            child.deposit_distance = None

            new_population.chromosomes.append(child)

            child2 = ga.crossover(parent_2, parent_1, self.helper, self.CROSSOVER_RATE)
            child2.fitness = None  # reset the fitness (it was calculated in the tournament and yet can mutate)
            child2.deposit_distance = None

            new_population.chromosomes.append(child2)
        
        # mutate
        ga.mutate(new_population.chromosomes, self.helper, self.MUTATION_INVERSION_RATE)

        # insert one unchanged elit (to keep the best if its the case)
        new_population.chromosomes.append(elit_unchanged)

        if len(new_population.chromosomes) != self.POPULATION_SIZE:
            print 'POPULATION WITH DFF SIZE'

        return new_population
