import random
from chromosome import Chromosome


def crossover(parent_1, parent_2):
    print 'crossover must take place here'
    
    # select a truck from the parent 2
    truck_route =  random.choice(parent_2.trucks_used)
    truck_ini = truck_route[1]
    truck_end = truck_route[2]

    # select a subroute from the chosen truck_route
    subroute_ini = random.randint(truck_ini, truck_end - 1)
    subroute_end = random.randint(subroute_ini, truck_end - 1)

    subroute = parent_2.path[subroute_ini, subroute_end]
    closest_before_subroute = 0 #get_closest_betore_edge(subroute[0])

    # now create a child inserting the subroute created in the parent_1
    child = Chromosome()

    create_new_route = False
    last_end = 0
    for truck_used in parent_1.trucks_used:
        # get the edges_t of the route from trouck_used
        truck_edges = parent_1.path[truck_used[1]: truck_used[2]] 
        removed_edges = 0
        added_edges = 0

        for edge in truck_edges:
            if edge not in subroute:
                child.path.append(edge)

                if edge == closest_before_subroute: 
                    # MUST CHECK THE CAPACITY HERE?
                    child.path.append(subroute)
                    added_edges += len(subroute)
            else:
                removed_edges += 1

        new_start = last_end
        new_end = truck_used[2] - removed_edges + added_edges
        last_end = new_end

        if new_end - new_start > 0: # MUST CHECK THE CAPACITY HERE?
            child.trucks_used.append((truck_used, new_start, new_end))
        
        # remove the edges in edges_t that match with the edges of the subroute
        # if the 
    

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
