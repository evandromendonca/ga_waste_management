import osmnx as ox
import networkx as nx


class Helper:
    def __init__(self, graph, trucks, edges_to_correspond):
        self.G = graph
        self.distance_map = None
        self.all_trucks = trucks

        self.corresponding_edges = {}

        # edges list removing two-ways
        el = list(edges_to_correspond) # lista de todas as edges
        #all_edges = list(filter(lambda way: way[3]['oneway'] == True, el)) # edges que tem apenas um lado
        two_way_edges = list(filter(lambda way: way[3]['oneway'] == False, el)) # edges que tem dois lados
        #match_two_way_edges = [] # edges de dois lados com sua match

        for edge in two_way_edges: # para cada edge de dois lados     
            # acha a edge que sao exatamente o oposto da edge estudada    
            opposites = list(filter(lambda way: way[0] == edge[1] and way[1] == edge[0] and way[3]['length'] == edge[3]['length'], two_way_edges))
            if (len(opposites) != 1): # se achou mais de um oposto, algum erro tem
                print 'some error with this edge ' + str(edge[0:3])
            #if (opposites[0] in all_edges or edge in all_edges): # se a edge ja esta na lista de todas as edges, nao verifica
            #    continue
            if (edge[0:3] in self.corresponding_edges):
                continue

            self.corresponding_edges[edge[0:3]] = opposites[0][0:3]
            self.corresponding_edges[opposites[0][0:3]] = edge[0:3]
            #self.corresponding_edges.append((edge[0:3], opposites[0][0:3]))
            # aqui podemos inserir tanto a edge como o oposto encontrado
            #all_edges.append(opposites[0])
            #all_edges.append(edge)


    def parse_tuple(self, string):
        try:
            s = eval(str(string))
            if type(s) == tuple:
                return s
            return
        except:
            return

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

        return distance_map

    def build_distance_map_2(self, edges):
        print 'calculating distance map'
        distance_map = {}

        for edge_from in edges:
            distance_map[edge_from['osmid']] = {}

            for edge_to in edges:
                if edge_from['osmid'] in distance_map and edge_from['osmid'] in distance_map[edge_from['osmid']]:
                    distance_edge_from = distance_map[edge_from['osmid']
                                                      ][edge_from['osmid']]
                else:
                    distance_edge_from = nx.shortest_path_length(
                        self.G, edge_from[0], edge_from[1], weight='length')
                    distance_map[edge_from['osmid']
                                 ][edge_from['osmid']] = distance_edge_from

                if edge_to in distance_map and edge_to in distance_map[edge_to]:
                    distance_edge_to = distance_map[edge_to][edge_to]
                else:
                    distance_edge_to = nx.shortest_path_length(
                        self.G, edge_to[0], edge_to[1], weight='length')
                    if edge_to in distance_map:
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
                    edge = split [0]
                    distance = split[1]
                    self.distance_map[self.parse_tuple(splitted_edges[0])][self.parse_tuple(edge)] = float(distance)

        # with open(edges_file, 'r') as edges_f:
        #     #with open(distances_file, 'r') as distance_f:
        #     edges_lines = edges_f.read().splitlines()
        #     #distances_lines = distance_f.read().splitlines()
        #     for i in range(1, len(edges_lines)):
        #         edge_line = edges_lines[i]
        #         #distance_line = distances_lines[i - 1]

        #         splitted_edges = edge_line.split(';')
        #         #splitted_distances = distance_line.split(';')

        #         self.distance_map[self.parse_tuple(splitted_edges[0])] = {}

        #         for j in range(1, len(splitted_edges)):
        #             self.distance_map[self.parse_tuple(splitted_edges[0])][self.parse_tuple(
        #                 splitted_edges[j])] = float(splitted_distances[j - 1])

                # for line_edges in edges_f:
                #     line_distance = distance_f.readline()
                #     splited_distance = line_distance.split(';')
                #     splited_edges = line_edges.split(';')
                #     self.distance_map[splited_edges[0]] = {}
                #     for i in range(1, len(splited_edges)):
                #         self.distance_map[splited_edges[0]][splited_edges[i]] = splited_distance[i - 1]

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

        # # if one wants to see the route
        # route = nx.shortest_path(self.G, node_1, node_2, weight='length')
        # print 'route: '
        # print route
        #ox.plot_graph_route(self.G, route)
        #route = nx.shortest_path(self.G, 381116687, 247123638, weight='length')

        return distance

    def closest_edge_before(self, edges):
        closest_edge = None
        closest_distance = None
        edges_list = [edge[0:3] for edge in edges]
        for previous_edge in self.distance_map:
            if previous_edge in edges_list:
                continue
            if edges_list[0] in self.distance_map[previous_edge]:
                if closest_distance == None or closest_distance > self.distance_map[previous_edge][edges_list[0]]:
                    closest_distance = self.distance_map[previous_edge][edges_list[0]]
                    closest_edge = previous_edge

        return closest_edge
