import random

# http://osof.org/wp-content/uploads/2016/03/OSOF-Waste-Conversion-Table.pdf
plastic_kg_per_cubic_meter = 130

class chromosome:
    def __init__(self):
        self.path = []
        self.trucks_used = []
        self.routes = []

    def generate_routes(self):
        # generate a route for each truck used
        for truck in self.trucks_used:
            r = route(self.path, truck[1], truck[2], truck[0][1])
            self.routes.append(r)

class route:
    def __init__(self, full_path, init, end, truck_capacity):
        self.full_path = full_path
        self.initial_index = init
        self.final_index = end        
        self.truck_capacity = truck_capacity
        self.route_length = 20 # the initial length to go to the base and return
        self.garbage_weigth = None

    def check_route_validity(self):
        if self.truck_capacity > self.get_garbage_weight():
            return 'ok'
        else:
            return 'capacity exceeded'

    def get_route_path(self):
        return self.full_path[self.initial_index, self.final_index]

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

