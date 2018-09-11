# encoding: utf-8

import osmnx as ox
import networkx as nx

class Helper:
    def __init__(self, graph, trucks, edges_to_correspond):
        self.G = graph
        self.distance_map = None
        self.all_trucks = trucks
        self.corresponding_edges = {} 
        self.closest_before = {}       

        # edges list removing two-ways
        el = list(edges_to_correspond) # lista de todas as edges
        #all_edges = list(filter(lambda way: way[3]['oneway'] == True, el)) # edges que tem apenas um lado
        two_way_edges = list(filter(lambda way: way[3]['oneway'] == False, el)) # edges que tem dois lados
        #match_two_way_edges = [] # edges de dois lados com sua match

        for edge in two_way_edges: # para cada edge de dois lados     
            # acha a edge que sao exatamente o oposto da edge estudada    
            opposites = list(filter(lambda way: way[0] == edge[1] and way[1] == edge[0] and way[3]['length'] == edge[3]['length'], two_way_edges))
            
            if (len(opposites) != 1): # se achou mais de um ou nenhum oposto, algum erro tem
                print 'some error with this edge ' + str(edge[0:3])
            
            if (edge[0:3] in self.corresponding_edges):
                continue

            # insere na lista de correspondencia ambas as edges com suas opostas
            self.corresponding_edges[edge[0:3]] = opposites[0]
            self.corresponding_edges[opposites[0][0:3]] = edge

    def parse_tuple(self, string):
        try:
            s = eval(str(string))
            if type(s) == tuple:
                return s
            return
        except:
            return

    def build_closest_before(self):
        print 'calculating the closest before each edge'

        for edge_to in self.distance_map:
            self.closest_before[edge_to] = []
            # get all edges that have some distance to edge
            for edge_from in self.distance_map:
                if edge_from == edge_to:
                    continue
                if edge_to in self.distance_map[edge_from]:
                    dist = round(self.distance_map[edge_from][edge_to] - self.distance_map[edge_from][edge_from] - self.distance_map[edge_to][edge_to], 8)
                    if (dist < 0):
                        print 'algum error calculando o closest edge before all'
                    self.closest_before[edge_to].append((edge_from, dist)) # edge and distance in a tuple
            
            self.closest_before[edge_to] = sorted(self.closest_before[edge_to], key=lambda x: x[1])

    def build_distance_map(self, edges, edges_file):
        print 'calculating distance map'
        distance_map = {}

        total_edges = len(edges)
        counter = 0
        for edge_from in edges:
            counter += 1
            print 'working on ' + str(counter) + ' edge of the total ' + str(total_edges) + ' edges'
            
            if edge_from not in distance_map:
                distance_map[edge_from] = {}

            for edge_to in edges:
                # edge_from to edge_from
                distance_edge_from = self.G.edges[edge_from]['length']
                if edge_from not in distance_map[edge_from]:
                    distance_map[edge_from][edge_from] = distance_edge_from

                # edge_to to edge_to
                if edge_from != edge_to:
                    distance_edge_to = self.G.edges[edge_to]['length']
                    if edge_to in distance_map:          
                        if edge_to not in distance_map[edge_to]:
                            distance_map[edge_to][edge_to] = distance_edge_to
                    else:
                        distance_map[edge_to] = {edge_to: distance_edge_to}

                # must check here, because it can be added in the previous ifs
                if edge_to not in distance_map[edge_from]:
                    try:
                        last_node_edge_from = edge_from[1]
                        first_node_edge_to = edge_to[0]
                        distance_between_edges = nx.shortest_path_length(
                            self.G, last_node_edge_from, first_node_edge_to, weight='length')
                        distance_map[edge_from][edge_to] = distance_edge_from + \
                            distance_between_edges + distance_edge_to
                    except:
                        print 'ERROR: fiding route between ' + \
                            str(last_node_edge_from) + \
                            ' and ' + str(first_node_edge_to)

        with open(edges_file, 'w') as edges_f:
            edges_f.write('Source;Destinations')
            edges_f.write('\n')
            for edge in distance_map:
                edges_f.write(str(edge))
                for inner_edge in distance_map[edge]:
                    edges_f.write(';')
                    edges_f.write(str(inner_edge))
                    edges_f.write("|")
                    edges_f.write(str(distance_map[edge][inner_edge]))
                edges_f.write('\n')

        # # CALC THE DISTANCE FROM EVERY EDGE OF CAMPOLIDE TO THE DEPOSIT:
        # #   (268440195, 268440181, 0)
        # distances = '(268440195, 268440181, 0)'
        # depot_distance = G_lisbon.edges[(268440195, 268440181, 0)]['length']
        # for edge in G.edges(keys=True, data=True):
        #     distance_edge_to = edge[3]['length']
        #     last_node_edge_from = 268440181
        #     first_node_edge_to = edge[0]
        #     distance_between_edges = nx.shortest_path_length(G_lisbon, last_node_edge_from, first_node_edge_to, weight='length')
        #     total_distance = depot_distance + distance_between_edges + distance_edge_to
        #     distances += ';' + str(tuple(edge[0:3])) + '|' + str(total_distance)

        return distance_map

    def build_distance_map_from_files(self, edges_file):
        self.distance_map = {}

        with open(edges_file, 'r') as edges_f:
            edges_lines = edges_f.read().splitlines()

            for edge_line in edges_lines[1:]:
                splitted_edges = edge_line.split(';')

                self.distance_map[self.parse_tuple(splitted_edges[0])] = {}
                
                for inner_edge in splitted_edges[1:]:
                    split = inner_edge.split("|")
                    edge = split[0]
                    distance = split[1]
                    self.distance_map[self.parse_tuple(splitted_edges[0])][self.parse_tuple(edge)] = float(distance)

    # calculate distance in an ordered list of edges
    def calc_distance(self, edges):
        num_edges = len(edges)

        if num_edges < 1:
            print 'No edges to calculate distance'
            return None

        distance = 0
        if num_edges == 1:
            distance += self.distance_map[edges[0][0:3]][edges[0][0:3]]
            return distance

        #print 'distance between '+ str(edges[0][0:2]) +' and '+ str(edges[1][0:2]) + ' = ' + str(self.distance_map[edges[0][0:2]][edges[1][0:2]])
        distance += self.distance_map[edges[0][0:3]][edges[1][0:3]]

        for i in range(2, len(edges[2:])):
            #print 'distance between '+ str(edges[i - 1][0:2])+ ' and '+ str(edges[i][0:2]) + ' = ' + str(self.distance_map[edges[i - 1][0:2]][edges[i][0:2]])
            distance += self.distance_map[edges[i - 1][0:3]][edges[i][0:3]]
            #print 'distance between '+ str(edges[i - 1]) +' and '+ str(edges[i - 1]) + ' = ' + str(self.distance_map[str(edges[i - 1])][str(edges[i - 1])])
            distance -= self.distance_map[edges[i - 1][0:3]][edges[i - 1][0:3]]

        # # If one wants to see the route
        # route = nx.shortest_path(self.G, node_1, node_2, weight='length')
        # print 'route: '
        # print route
        #ox.plot_graph_route(self.G, route)
        #route = nx.shortest_path(self.G, 381116687, 247123638, weight='length')

        return distance

    # subroute: the selected subroute
    # total_edges: every edge of the parent that the subroute will be inserted, one of the edges must
    # be the closest before
    #@profile
    def closest_edge_before_old(self, subroute, total_edges):
        closest_edge = None
        closest_distance = None
        subroute_set = set([edge[0:3] for edge in subroute])        
        first_edge = subroute[0][0:3]
        for previous_edge in total_edges:
            previous_edge_abv = previous_edge[0:3]
            # check if the edge is in the edge list, so it can be the closest before it
            if previous_edge_abv in subroute_set:
                continue
            # check if the corresponding edge is in the list, because corresponding edges are served only once per path
            if previous_edge_abv in self.corresponding_edges and \
                self.corresponding_edges[previous_edge_abv][0:3] in subroute_set:
                continue
            if first_edge in self.distance_map[previous_edge_abv]:
                if closest_distance == None or closest_distance > self.distance_map[previous_edge_abv][first_edge]:
                    closest_distance = self.distance_map[previous_edge_abv][first_edge]
                    closest_edge = previous_edge_abv

        return closest_edge

    #@profile
    def closest_edge_before(self, subroute, total_edges):        
        first_edge = subroute[0][0:3]
        subroute_set = set([edge[0:3] for edge in subroute])
        total_edges_set = set([edge[0:3] for edge in total_edges])
        closest = None
        # essa lista está ordenada da menor distancia para a maior, portanto a primeira edge que não estiver na subroute,
        # nem a edge oposta a ela estiver na subroute, será a CLOSEST EDGE
        # isso deve reduzir muito a complexidade
        for edge_dist in self.closest_before[first_edge]: 
            edge = edge_dist[0]                        
            if edge in subroute_set:
                continue
            # check if the corresponding edge is in the list, because corresponding edges are served only once per path
            if edge in self.corresponding_edges and \
                self.corresponding_edges[edge][0:3] in subroute_set:
                continue
            # if the edge in inside the path, return, the corresponding edge can have a greater distance because of the direction            
            if edge in total_edges_set:
                closest = edge
                break

        return closest
