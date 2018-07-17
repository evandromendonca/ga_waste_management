import random
import ga


class Population:
    def __init__(self, helper, edges=None, trucks=None, randomize=None):
        self.chromosomes = []
        self.helper = helper
        self.best_fitness = None

        # generate a random population given the edges and trucks
        if randomize == True and edges != None and trucks != None:
            self.chromosomes = ga.randomize_population(edges, trucks)

    def get_best_fitness(self):
        if self.best_fitness == None:
            self.best_fitness = ga.get_best_fitness(self.chromosomes, self.helper)
        return self.best_fitness

    def evolve(self):
        print 'evolving the population'

        # create a new population
        new_population = Population(self.helper)

        # the best fitting solution go to the next population automatically (ELITISM)
        best_fit = ga.get_best_fitness(self.chromosomes, self.helper)
        new_population.chromosomes.append(best_fit)

        # for the number of the population do:
        for _ in range(1, len(self.chromosomes)):
            #print 'generating child ' + str(i)
            # must select parent 1 using TOURNAMENT SELECTION
            parent_1 = ga.tournament_selection(self.chromosomes, self.helper)
            # must select parent 2 using TOURNAMENT SELECTION
            parent_2 = ga.tournament_selection(self.chromosomes, self.helper)
            # crossover these chomosomes
            child = ga.crossover(parent_1, parent_2, self.helper)
            # mutate at a LOW RATE
            # ga.mutation(child)

            new_population.chromosomes.append(child)

        return new_population
