# encoding: utf-8

import random
from chromosome import Chromosome
import collections

POPULATION_SIZE = 100
CROSSOVER_RATE = 0.8
MUTATION_SWAP_RATE = 0.01
MUTATION_INVERSION_RATE = 0.01
TOURNAMENT_SIZE = 10

def mutate(chromosomes):
    for chromosome in chromosomes:            
        num = random.random()
        if num < MUTATION_SWAP_RATE:
            mutation_swap(chromosome)

        num = random.random()
        if num < MUTATION_INVERSION_RATE:
            mutation_inverse(chromosome)

def mutation_swap(chromosome):
    # this can fail, so try the mutation 10 times only
    for _ in range(10):
        truck_1 = random.choice(chromosome.trucks_used)
        index_1 = random.randint(truck_1[1], truck_1[2] - 1)
        edge_1 = chromosome.path[index_1]
        truck_1_capacity = truck_1[0][1]
        truck_1_fill = truck_1[3]
        edge_1_weight = edge_1[3]['weight']

        truck_2 = random.choice(chromosome.trucks_used)
        index_2 = random.randint(truck_2[1], truck_2[2] - 1)
        edge_2 = chromosome.path[index_2]
        truck_2_capacity = truck_2[0][1]
        truck_2_fill = truck_2[3]
        edge_2_weight = edge_2[3]['weight']
        
        if truck_1_fill - edge_1_weight + edge_2_weight <= truck_1_capacity and truck_2_fill - edge_2_weight + edge_1_weight <= truck_2_capacity:
            chromosome.path[index_1] = edge_2
            chromosome.path[index_2] = edge_1
            break


def mutation_inverse(chromosome):
    # select a truck from the chromosome
    truck_route = random.choice(chromosome.trucks_used)
    truck_ini = truck_route[1]
    truck_end = truck_route[2]

    # select a subroute from the chosen truck_route
    subroute_ini = random.randint(truck_ini, truck_end - 1)
    subroute_end = random.randint(subroute_ini, truck_end - 1)
    subroute_end += 1

    subroute = chromosome.path[subroute_ini:subroute_end]    

    i = subroute_ini
    for edge in reversed(subroute):
        chromosome.path[i] = edge
        i += 1

# this is to check the performance using line_profiler @ https://github.com/rkern/line_profiler
#@profile 
def crossover(parent_1, parent_2, helper):
    num = random.random()
    if num > CROSSOVER_RATE:
        # since this crossover generates only one child, and the genetic material
        # is not shared between the two parents, I'm choosing to pass the one that
        # is being used to insert the genetic material from the other, so more of him would
        # be passed anyway
        return parent_1 
    
    # select a truck from the parent 2
    truck_route = random.choice(parent_2.trucks_used)
    truck_ini = truck_route[1]
    truck_end = truck_route[2]

    # select a subroute from the chosen truck_route
    subroute_ini = random.randint(truck_ini, truck_end - 1)
    subroute_end = random.randint(subroute_ini, truck_end - 1)
    subroute_end += 1

    subroute = parent_2.path[subroute_ini:subroute_end]
    subroute_set = set(edge[0:3] for edge in subroute)
    
    # Must get the subroute weight
    subroute_weight = 0  
    for edge in subroute:
        subroute_weight += edge[3]['weight']

    # # teste
    # if len(subroute) <= 0:
    #     print 'A subrota para crossover não tem nenhum elemento'

    #closest_before_subroute_old = helper.closest_edge_before_old(subroute, parent_1.path)    
    closest_before_subroute = helper.closest_edge_before(subroute, parent_1.path)

    # print 'closest_before_old = ' + str(closest_before_subroute_old)
    # print 'closest_before = ' + str(closest_before_subroute)
    # if closest_before_subroute not in (edge[0:3] for edge in parent_1.path):
    #     print 'DEU MERDA AQUI Ó'

    # A CLOSEST EDGE BEFORE PRECISA ESTAR NO PARENT 1 PATH, ENTAO SE VIER UMA EDGE QUE NAO ESTEJA,
    # COM CERTEZA EXISTE UMA CORRESPONDENTE QUE ESTÁ. BASTA BUSCAR ESSA CORRESPONDENTE
    # in_path = filter(lambda x: x[0:3] == closest_before_subroute, parent_1.path)
    # if (len(in_path) > 1):
    #     print 'merda aqui'
    # if (len(in_path) == 0):
    #     closest_before_subroute = helper.corresponding_edges[closest_before_subroute][0:3]

    # now create a child inserting the subroute created in the parent_1
    child = Chromosome()

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
            edge_abv = edge[0:3]

            # NO CROSSOVER PRECISO VERIFICAR SE AS EDGES, OU SUAS CORRESPONDENTES, NAO ESTAO NA SUBROUTE
            if edge_abv in subroute_set or \
                (edge_abv in helper.corresponding_edges and \
                helper.corresponding_edges[edge_abv][0:3] in subroute_set):
                continue
                
            # # teste
            # if edge in child.path:
            #     print 'repetido'

            # check the capacity here
            if truck_capacity >= truck_used_capacity + edge[3]['weight']:
                new_end += 1
                truck_used_capacity += edge[3]['weight']
                child.path.append(edge)
            else:
                to_new_truck.append(edge)

            if edge_abv == closest_before_subroute:
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

    # serve the edges that were not served yet due to smth
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
                if t_fill + edge[3]['weight'] <= t_capacity:
                    t_fill += edge[3]['weight']
                    t_end += 1
                    child.path.append(edge)
                    served_edges += 1
                else:
                    # the truck is full loaded, stop the loop and chose other truck to complete the job
                    break

            # here we must check if the truck will join the list of route trucks
            # if the truck drove at least one edge, add it to the list
            if t_end - t_start > 0:
                child.trucks_used.append((truck, t_start, t_end, t_fill))

    # # teste
    # duplicates = [item for item, count in collections.Counter([edge[0:3] for edge in child.path]).items() if count > 1]
    # if len(duplicates) > 0:
    #     print 'duplicates found:'
    #     print duplicates

    # # teste
    # if (len(child.path) != len(parent_1.path) or len(child.path) != len(parent_2.path)):
    #     print 'Tamanho filho é diferente do que algum dos pais'

    return child    


def tournament_selection(chromosomes, helper):
    if len(chromosomes) <= 0:
        print 'No chromosome in this population yet'
        return None

    # choosing an indivial in the population based on a tournament
    selected_chromosomes = random.sample(chromosomes, TOURNAMENT_SIZE)

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


def randomize_population(edges, trucks, corresponding_edges):
    chromosomes = []

    # generate random routes combinations
    for _ in range(POPULATION_SIZE):
        # create a chromosome
        cr = Chromosome()

        # copy and shuffle all the edges
        cr.path = list(edges)  # copy the list
        random.shuffle(cr.path)

        # remove the corresponding edges that appear last
        remaning_edges = list(cr.path)
        removed_edges = []
        for edge in remaning_edges:
            if (edge[0:3] in removed_edges):
                continue
            if (edge[0:3] in corresponding_edges):
                edge_to_remove = corresponding_edges[edge[0:3]]
                removed_edges.append(edge_to_remove[0:3])
                cr.path.remove(edge_to_remove)

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
                if t_fill + edge[3]['weight'] <= t_capacity:
                    t_fill += edge[3]['weight']
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
