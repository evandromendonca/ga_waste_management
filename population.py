import random
import ga

class Population:
    def __init__(self, helper, edges=None, trucks=None, randomize=None):
        self.chromosomes = []
        self.helper = helper

        # generate a random population given the edges and trucks
        if randomize == True and edges != None and trucks != None:
            self.chromosomes = ga.randomize_population(edges, trucks)

    def best_fitness(self):
        ga.get_best_fitness(self.chromosomes, self.helper)
    #     if len(self.chromosomes) <= 0:
    #         print 'No chromosome in this population yet'
    #         return None

    #     best_fit_chromosome = self.chromosomes[0]
    #     for chromosome in self.chromosomes[1:]:
    #         if chromosome.get_fitness(self.helper) < best_fit_chromosome.get_fitness(self.helper):
    #             best_fit_chromosome = chromosome

    #     print 'best fitness of: ' + str(best_fit_chromosome.get_fitness(self.helper))
    #     return best_fit_chromosome

    # def tournament_selection(self):
    #     if len(self.chromosomes) <= 0:
    #         print 'No chromosome in this population yet'
    #         return None

    #     print 'choosing an indivial in the population based on a tournament'
    #     selected_chromosomes = random.sample(self.chromosomes, 5)

    #     if len(selected_chromosomes) <= 0:
    #         print 'No chromosome selected for the sample at the tournament'
    #         return None
        
    #     best_fit_chromosome = selected_chromosomes[0]
    #     for chromosome in selected_chromosomes[1:]:
    #         if chromosome.get_fitness(self.helper) < best_fit_chromosome.get_fitness(self.helper):
    #             best_fit_chromosome = chromosome

    #     print 'best fitness of tournament: ' + str(best_fit_chromosome.get_fitness(self.helper))
    #     return best_fit_chromosome

    def evolve(self):
        print 'evolving the population'

        # create a new population
        new_population = Population(self.helper)

        # the best fitting solution go to the next population automatically (ELITISM)
        best_fit =  ga.get_best_fitness(self.chromosomes, self.helper)
        new_population.chromosomes.append(best_fit)

        # for the number of the population do:
        for i in range(1, len(self.chromosomes)):
            print 'generating child ' + str(i)
            # must select parent 1 using TOURNAMENT SELECTION
            parent_1 = ga.tournament_selection(self.chromosomes, self.helper)
            # must select parent 2 using TOURNAMENT SELECTION
            parent_2 = ga.tournament_selection(self.chromosomes, self.helper)            
            # crossover these chomosomes
            child = ga.crossover(parent_1, parent_2)
            # mutate at a LOW RATE
            ga.mutation(child)

            new_population.chromosomes.append(child)

        return new_population
