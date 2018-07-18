import random
from chromosome import Chromosome
import collections

def crossover(parent_1, parent_2, helper):
    # select a truck from the parent 2
    truck_route = random.choice(parent_2.trucks_used)
    truck_ini = truck_route[1]
    truck_end = truck_route[2]

    # select a subroute from the chosen truck_route
    subroute_ini = random.randint(truck_ini, truck_end - 1)
    subroute_end = random.randint(subroute_ini, truck_end - 1)
    subroute_end += 1

    if subroute_end - subroute_ini <= 0:
        print 'deu merda'

    subroute = parent_2.path[subroute_ini:subroute_end]
    subroute_weight = 0  # MUST GET THE SUBROUTE WEIGHT
    for edge in subroute:
        subroute_weight += edge[2]['weight']

    if len(subroute) <= 0:
        print 'deu merda'

    closest_before_subroute = helper.closest_edge_before(subroute)

    c = False
    for edge in parent_1.path:
        if edge[0:2] == closest_before_subroute:
            c = True
    if c == False:
        print 'deu merda'

    # now create a child inserting the subroute created in the parent_1
    child = Chromosome()

    e_count = 0

    to_new_truck = []
    last_end = 0
    for truck_used in parent_1.trucks_used:
        # get the edges_t of the route from trouck_used
        truck_edges = parent_1.path[truck_used[1]:truck_used[2]]

        truck_capacity = truck_used[0][1]
        truck_used_capacity = 0
        new_start = last_end
        new_end = last_end

        for edge in truck_edges:            
            e_count += 1
            if edge not in subroute:
                if edge in child.path:
                    print 'repetido'

                # check the capacity here
                if truck_capacity >= truck_used_capacity + edge[2]['weight']:
                    new_end += 1
                    truck_used_capacity += edge[2]['weight']
                    child.path.append(edge)
                else:
                    to_new_truck.append(edge)

                if edge[0:2] == closest_before_subroute:
                    # check the capacity here
                    if truck_capacity >= truck_used_capacity + subroute_weight:
                        new_end += len(subroute)
                        truck_used_capacity += subroute_weight
                        child.path.extend(subroute)
                    else:
                        to_new_truck.extend(subroute)

        if new_end - new_start > 0: 
            child.trucks_used.append(
                (truck_used[0], new_start, new_end, truck_used_capacity))

        last_end = new_end

    if e_count != len(parent_1.path):
        print 'deu merda'

    if len(child.path) + len(to_new_truck) != len(parent_1.path):
        print 'deu merda'

    if len(to_new_truck) > 0:
        served_edges = 0
        while served_edges < len(to_new_truck):
            # select a truck
            truck = random.choice(helper.all_trucks)
            t_fill = 0
            t_capacity = truck[1]
            t_start = len(child.path)
            t_end = t_start
            # start filling the truck with the sequence of edges
            for edge in to_new_truck[served_edges:]:            
                if t_fill + edge[2]['weight'] <= t_capacity:
                    t_fill += edge[2]['weight']
                    t_end += 1
                    child.path.append(edge)
                    served_edges += 1
                else:
                    # the truck is full loaded, stop the loop and chose other truck to complete the job
                    break

            # here we must check if the truck will join the list of route trucks
            # if the truck drived at least one edge, add it to the list
            if t_end - t_start > 0:
                child.trucks_used.append((truck, t_start, t_end, t_fill))

    print 'child path length === ' + str(len(child.path))
    print [item for item, count in collections.Counter([edge[0:2] for edge in child.path]).items() if count > 1]
    return child


# def mutation(chromosome):
#     print 'mutation must take place here'


def tournament_selection(chromosomes, helper):
    if len(chromosomes) <= 0:
        print 'No chromosome in this population yet'
        return None

    # choosing an indivial in the population based on a tournament
    selected_chromosomes = random.sample(chromosomes, 5)

    if len(selected_chromosomes) <= 0:
        print 'No chromosome selected for the sample at the tournament'
        return None

    best_fit_chromosome = selected_chromosomes[0]
    for chromosome in selected_chromosomes[1:]:
        if chromosome.get_fitness(helper) < best_fit_chromosome.get_fitness(helper):
            best_fit_chromosome = chromosome

    # print 'best fitness of tournament: ' + \
    #   str(best_fit_chromosome.get_fitness(helper))
    return best_fit_chromosome


def get_best_fitness(chromosomes, helper):
    if len(chromosomes) <= 0:
        print 'No chromosome in this population yet'
        return None

    best_fit_chromosome = chromosomes[0]
    for chromosome in chromosomes[1:]:
        if chromosome.get_fitness(helper) < best_fit_chromosome.get_fitness(helper):
            best_fit_chromosome = chromosome

    #print 'best fitness of: ' + str(best_fit_chromosome.get_fitness(helper))
    return best_fit_chromosome


def randomize_population(edges, trucks):
    chromosomes = []

    # generate random routes combinations
    for _ in range(10):
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
                if t_fill + edge[2]['weight'] <= t_capacity:
                    t_fill += edge[2]['weight']
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
