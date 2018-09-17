deposit = (268440195, 268440181, 0)

class Chromosome:
    def __init__(self):
        self.path = []
        self.trucks_used = []
        self.routes = []
        self.path_set = None
        self.simple_path = None
        self.fitness = None

    def get_path_set(self):
        if self.path_set == None:
            self.path_set = set(self.get_simple_path())
        return self.path_set

    def get_simple_path(self):
        if (self.simple_path == None):
            self.simple_path = list([edge[0:3] for edge in self.path])
        return self.simple_path

    # fitness is the total amount of distance of the chromosome
    # must calculate each route total distance, and add a number of
    # meters to each truck, meaning begin and return to the base
    def get_fitness(self, helper):
        if helper == None:
            print 'No helper to calculate fitness, can not proceed'
            return None

        if self.fitness != None:
            return self.fitness

        fitness = 0
        for truck in self.trucks_used:
            edges = self.path[truck[1]:truck[2]]
            fitness += helper.calc_distance(edges)            
            # sum the distance between the last node and the deposit
            distance_last_edge_deposit = helper.calc_distance([edges[-1], deposit])
            # remove the distance of the last edge from the distance to deposit
            distance_last_edge_deposit = distance_last_edge_deposit - helper.calc_distance([edges[-1]])
            fitness += distance_last_edge_deposit

            # sum distance between departure site and the first node
            distance_deposit_first_edge = helper.calc_distance([deposit, edges[0]])
            # remove the distance of the first edge from the distance to deposit
            distance_deposit_first_edge = distance_deposit_first_edge - helper.calc_distance([edges[0]])
            fitness += distance_deposit_first_edge

            #print 'distance from deposit=' + str(distance_deposit_first_edge)
            #print 'distance to deposit=' + str(distance_last_edge_deposit)

        self.fitness = fitness
        return self.fitness

    def generate_routes(self):
        # generate a route for each truck used
        for truck in self.trucks_used:
            r = Route(self.path, truck[1], truck[2], truck[0][1])
            self.routes.append(r)

class Route:
    def __init__(self, full_path, init, end, truck_capacity):
        self.full_path = full_path
        self.initial_index = init
        self.final_index = end
        self.truck_capacity = truck_capacity
        self.route_length = 20  # the initial length to go to the base and return
        self.garbage_weigth = None

    def check_route_validity(self):
        if self.truck_capacity > self.get_garbage_weight():
            return 'ok'
        else:
            return 'capacity exceeded'

    def get_route_path(self):
        return self.full_path[self.initial_index:self.final_index]

    def get_route_length(self):
        if self.route_length == None:
            print 'must load the route length and store it in the length variable'
            self.route_length += 0
        return self.route_length

    def get_garbage_weight(self):
        if self.garbage_weigth == None:
            print 'must load the total weight of garbage collected and store it at the garbage_weight variable'
            self.garbage_weigth = 0
        return self.garbage_weigth
