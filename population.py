import ga


class Population:
    def __init__(self, edges=None, trucks=None, randomize=None):
        self.chromosomes = []

        # generate a random population given the edges and trucks
        if randomize == True and edges != None and trucks != None:
            self.chromosomes = ga.randomize_population(edges, trucks)

    def best_fitness(self):
        if len(self.chromosomes) <= 0:
            print 'No chromosome in this population yet'
            return None

        best_fit_chromosome = self.chromosomes[0]
        for chromosome in self.chromosomes[1:]:
            if chromosome.fitness() > best_fit_chromosome.fitness():
                best_fit_chromosome = chromosome

        print 'best fitness of: ' + str(best_fit_chromosome.fitness())
        return best_fit_chromosome

    def tournament_selection(self):
        print 'choosing an indivial in the population based on a tournament'

    def evolve(self):
        print 'evolving the population'

        # create a new population
        new_population = Population()

        # the best fitting solution go to the next population automatically (ELITISM)
        best_fit = self.best_fitness()
        new_population.chromosomes.append(best_fit)

        # for the number of the population size - 1, do:
        remaining_size = len(self.chromosomes[1:])
        for i in range(1, remaining_size + 1):
            print 'generating child ' + str(i)
            new_population.chromosomes.append(self.chromosomes[i])
            # must select parent 1 using TOURNAMENT SELECTION
            # must select parent 2 using TOURNAMENT SELECTION
            # crossover these chomosomes
            # mutate at a LOW RATE

        return new_population
