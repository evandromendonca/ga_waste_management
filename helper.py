import osmnx as ox
import networkx as nx

class Helper:
    def __init__(self, graph):
        self.G = graph
        self.distance_map = None

    def parse_tuple(self, string):
        try:
            s = eval(str(string))
            if type(s) == tuple:
                return s
            return
        except:
            return

    def build_distance_map(self, edges):
        print 'calculating distance map'
        distance_map = {}

        for edge_from in edges:
            distance_map[edge_from] = {}

            for edge_to in edges:         
                if edge_from in distance_map and edge_from in distance_map[edge_from]:
                    distance_edge_from = distance_map[edge_from][edge_from]
                else:
                    distance_edge_from = nx.shortest_path_length(self.G, edge_from[0], edge_from[1], weight='length')
                    distance_map[edge_from][edge_from] = distance_edge_from                                

                if edge_to in distance_map and edge_to in distance_map[edge_to]:
                    distance_edge_to = distance_map[edge_to][edge_to]
                else:
                    distance_edge_to = nx.shortest_path_length(self.G, edge_to[0], edge_to[1], weight='length')
                    if edge_to in distance_map:
                        distance_map[edge_to][edge_to] = distance_edge_to
                    else:
                        distance_map[edge_to] = { edge_to: distance_edge_to}

                # must check here, because it can be added in the previous ifs
                if edge_to not in distance_map[edge_from]:                                
                    try:
                        last_node_edge_from = edge_from[1]
                        first_node_edge_to = edge_to[0]                    
                        distance_between_edges = nx.shortest_path_length(self.G, last_node_edge_from, first_node_edge_to, weight='length')
                        distance_map[edge_from][edge_to] = distance_edge_from + distance_between_edges + distance_edge_to
                    except:
                        print 'ERROR: fiding route between ' + str(last_node_edge_from) + ' and ' + str(first_node_edge_to)
        
        return distance_map

    def build_distance_map_from_files(self, edges_file, distances_file):
        self.distance_map = {}

        with open(edges_file, 'r') as edges_f:
            with open(distances_file, 'r') as distance_f:
                edges_lines = edges_f.read().splitlines()
                distances_lines = distance_f.read().splitlines()
                for i in range(1, len(edges_lines)):
                    edge_line = edges_lines[i]                                        
                    distance_line = distances_lines[i - 1]

                    splitted_edges = edge_line.split(';')
                    splitted_distances = distance_line.split(';')

                    self.distance_map[self.parse_tuple(splitted_edges[0])] = {}

                    for j in range(1, len(splitted_edges)):
                        self.distance_map[self.parse_tuple(splitted_edges[0])][self.parse_tuple(splitted_edges[j])] = float(splitted_distances[j - 1])

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
            distance += self.distance_map[edges[0][0:2]][edges[0][0:2]]
            return distance

        #print 'distance between '+ str(edges[0][0:2]) +' and '+ str(edges[1][0:2]) + ' = ' + str(self.distance_map[edges[0][0:2]][edges[1][0:2]])
        distance += self.distance_map[edges[0][0:2]][edges[1][0:2]]

        for i in range(2, len(edges[2:])):
            #print 'distance between '+ str(edges[i - 1][0:2])+ ' and '+ str(edges[i][0:2]) + ' = ' + str(self.distance_map[edges[i - 1][0:2]][edges[i][0:2]])
            distance += self.distance_map[edges[i - 1][0:2]][edges[i][0:2]]
            #print 'distance between '+ str(edges[i - 1]) +' and '+ str(edges[i - 1]) + ' = ' + str(self.distance_map[str(edges[i - 1])][str(edges[i - 1])])
            distance -= self.distance_map[edges[i - 1][0:2]][edges[i - 1][0:2]]
            
        # # if one wants to see the route
        # route = nx.shortest_path(self.G, node_1, node_2, weight='length')
        # print 'route: '
        # print route
        #ox.plot_graph_route(self.G, route)
        #route = nx.shortest_path(self.G, 381116687, 247123638, weight='length')
        
        return distance