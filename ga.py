import random
from chromosome import Chromosome


def crossover(parent_1, parent_2):
    print 'crossover must take place here'


def mutation(chromosome):
    print 'mutation must take place here'


def randomize_population(edges, trucks):
    chromosomes = []

    # generate random routes combinations
    for _ in range(2):
        # create a chromosome
        cr = Chromosome()

        # copy and shuffle all the edges
        cr.path = list(edges)  # copy the list
        random.shuffle(cr.path)

        # to keep the trucks that were already chosen by the algorithm
        already_chosen_trucks = []

        total_edges = len(cr.path)
        served_edges = 0
        # do this while there are unvisited edges
        while served_edges < total_edges:

            # give the opportunity for the unchosed truck
            # with this I want ot maximaze the utilization of all trucks
            # if every truck had the chance, let it be FFA
            if len(already_chosen_trucks) == len(trucks):
                to_chose_trucks = trucks
            else:
                to_chose_trucks = [
                    truck for truck in trucks if truck not in already_chosen_trucks]

            # select a random truck
            t = random.choice(to_chose_trucks)
            t_start = served_edges  # inclusive  [t_start, t_end)
            t_end = served_edges  # exclusive
            t_fill = 0
            t_capacity = t[1]

            # just update the already chosen trucks if it matters
            if len(already_chosen_trucks) < len(trucks):
                already_chosen_trucks.append(t)

            # start filling the truck with the sequence of edges
            for edge in cr.path[served_edges:]:
                if t_fill + edges[edge]['garbage_weight'] <= t_capacity:
                    t_fill += edges[edge]['garbage_weight']
                    t_end += 1
                    served_edges += 1
                else:
                    # the truck is full loaded, stop the loop and chose other truck to complete the job
                    break

            # here we must check if the truck will join the list of route trucks
            # if the truck drived at least one edge, add it to the list
            if t_end - t_start > 0:
                cr.trucks_used.append((t, t_start, t_end, t_fill))

        chromosomes.append(cr)

    return chromosomes
