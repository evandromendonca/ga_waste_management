# encoding: utf-8
# ----------------------------------------------------------------------------------
# A genetic algorithm for the Capacitated Arc Rout Problem (CARP) with multiple capacities
# Case of Campolide
# Using the new Genetic Representation for the Vehicle Route Problem
# count the cars by capacity (n importa a placa do carro, e sim a capacidade DISTINCT)
#
# Osmnx docs: http://osmnx.readthedocs.io/en/stable/osmnx.html
# Xml.etree.ElementTree docs: https://docs.python.org/2/library/xml.etree.elementtree.html#elementtree-xpath
# Shortest path: https://networkx.github.io/documentation/stable/reference/algorithms/shortest_paths.html?highlight=shortest%20path#module-networkx.algorithms.shortest_paths.astar
# Routing: https://medium.com/@bobhaffner/osmnx-intro-and-routing-1fd744ba23d8
# OpenStreetMaps: https://www.openstreetmap.org/relation/5400890#map=12/38.7441/-9.1581
# https://www.uv.es/belengue/carp.html
# Garbage m3 to kg converter: http://osof.org/wp-content/uploads/2016/03/OSOF-Waste-Conversion-Table.pdf
#
# Depósito de embalagens, é uma rua com mão dupla, usar essa edge: (268440195, 268440181, 0)
# ----------------------------------------------------------------------------------

import csv
from datetime import datetime
import xml.etree.ElementTree as ET
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import random
import ga
from population import Population
from helper import Helper
import collections
import sys
import json

if __name__ == "__main__":
    file_name = sys.argv[1]
    print 'file name is: ' + file_name
    
    # # this is only for choosing the best parameters for the GA
    # start_params_from = int(sys.argv[1])
    # end_param = start_params_from + 9
    # print 'start_param_from [0-35] = ' + \
    #     str(start_params_from) + ' end param = ' + str(end_param)

def population_evolution(num_iterations):
    ### The parameters choosen were ###
    # Pop size: 125
    # Tournament size: 13, in fact 10% rounded up
    # Crossover rate: 1
    # Mutation rate: 0,005
    pop = 126 # MUST BE AN EVEN NUMBER
    tour = 13
    cross = 1
    mut = 0.01

    # pop = 130
    # tour = 26
    # cross = 0.9
    # mut = 0.01

    best_solutions = []

    with open(file_name, 'w') as f:
        best_population = None

        for i in range(0, 1):
            # randomize the initial population
            population = Population(helper, G.edges(
                keys=True, data=True), trucks, True, pop, tour, cross, mut)
            print 'initial population best fitness: ' + str(population.get_best_fitness().fitness) + ' with ' + str(len(
                population.get_best_fitness().trucks_used)) + ' trucks and with paths number: ' + str(len(population.get_best_fitness().path))

            line = ''
            last_best_iteration = None
            last_best_fitness = None
            # evolve the population
            for i in range(num_iterations):
                population = population.evolve()
                print 'iteration ' + str(i) + ' best fitness: ' + str(population.get_best_fitness().fitness) + ' with ' + str(len(
                    population.get_best_fitness().trucks_used)) + ' trucks and with paths number: ' + str(len(population.get_best_fitness().path))
                line += str(population.get_best_fitness().fitness) + ';'

                # store the last best fitness and last best iteration
                if last_best_fitness == None or last_best_fitness > population.get_best_fitness().fitness:
                    last_best_fitness = population.get_best_fitness().fitness
                    last_best_iteration = i
                
                # check for stop condition, 8000 iterations without improvement 
                if i - last_best_iteration > 800:
                    break

            f.write(line)
            f.write('\n')

            best_solutions.append(population.get_best_fitness())

            if best_population == None or best_population.get_best_fitness().fitness > population.get_best_fitness().fitness:
                best_population = population

    # save the best solutions to the json file
    with open("best_solutions.json", "w") as jfile:
        json.dump(best_solutions, jfile)

    # Print the best fitness found
    print 'final best_population best fitness: ' + str(best_population.get_best_fitness().fitness) + ' with ' + str(len(
        best_population.get_best_fitness().trucks_used)) + ' trucks and with paths number: ' + str(len(best_population.get_best_fitness().path)) + \
        ' - Distance from deposit: ' + str(best_population.get_best_fitness().deposit_distance) + ' - Difference: ' + \
        str(best_population.get_best_fitness().fitness - best_population.get_best_fitness().deposit_distance)

    # deposit = filter(lambda x: x[0] == 268440195 and x[1] == 268440181 and x[2] == 0, list(G_lisbon.edges(keys=True, data=True)))[0]

    # # Plot the route
    # best = best_population.get_best_fitness()
    # best.generate_routes()
    # for route in best.routes:
    #     route_path = route.get_route_path()
    #     route_path.insert(0, deposit)
    #     route_path.append(deposit)
    #     helper.show_route(route_path)


### THIS CODE IS FOR CHOOSING THE PARAMETERS ###
def test_multiple_ga_parameters():
    # Run the tests 30 times with 10.000 iterations and store in the best_fitness_array
    params_test = []
    with open('./data/params_test/comb_params_tests.csv', 'r') as f:
        lines = f.read().splitlines()
        for l in lines[1:]:
            s = l.split(';')
            params_test.append((s[1], s[2], s[3], s[4]))

    for i in range(start_params_from, end_param):
        file_name = './data/params_test_' + str(i+1) + '.csv'

        # define the parameters, they now go inside the population
        pop = int(params_test[i][0])
        tour = int(params_test[i][1])
        cross = float(params_test[i][2])
        mut = float(params_test[i][3])

        with open(file_name, 'w') as f:
            for _ in range(10):

                # line to save on file
                line = ''

                print '\nstarting new round...'

                # randomize the initial population
                population = Population(helper, G.edges(
                    keys=True, data=True), trucks, True, pop, tour, cross, mut)
                print 'initial population best fitness: ' + str(population.get_best_fitness().fitness) + ' with ' + str(len(
                    population.get_best_fitness().trucks_used)) + ' trucks and with paths number: ' + str(len(population.get_best_fitness().path))

                # evolving
                for i in range(10000):
                    population = population.evolve()
                    # increase the line to save
                    line += str(population.get_best_fitness().fitness) + ';'
                    print 'iteration: ' + str(i)

                # Print the best fitness found
                print 'final population best fitness: ' + str(population.get_best_fitness().fitness) + ' with ' + str(len(
                    population.get_best_fitness().trucks_used)) + ' trucks and with paths number: ' + str(len(population.get_best_fitness().path))

                line += '\n'  # jump line
                f.write(line)  # write on file


# Media de lixo por metro em base nas duas rotas E0504 e E0714 Int = 0.21757637738 kg (vide data_filter.py)
residuo_metro = 0.21757637738

# WHERE AM I ? TE OR HOME
where_am_i = "HOME"

if where_am_i == "HOME":
    CAMPOLIDE_GRAPH = 'campolide_graph.graphml'
    LISBON_GRAPH = 'lisbon_graph.graphml'
    EDGES_FILE = './data/edges.csv'
else:
    CAMPOLIDE_GRAPH = 'TE_campolide_graph.graphml'
    LISBON_GRAPH = 'TE_lisbon_graph.graphml'
    EDGES_FILE = './data/TE_edges.csv'

# available trucks must also be presented
# in the 'trucks_available.csv' file there are 53 trucks with 3 different capacities
# as the different truck capacity matter, in this example is used one truck of each capacity
# 80% of the full capacity of the truck is used to give space to error
# To see how these trucks were generated refer to data_filter.py
# Plate	    Cap	Cap_KG
# 31-61-UI	14	1820
# 02-TZ-69	9	1170
# 87-CE-84	7	910
trucks = [
    ('31-61-UI', 1456),
    ('02-TZ-69', 936),
    ('87-CE-84', 728)
]

try:
    print 'about to open campolide_graph and lisbon_graph from file'
    G = ox.load_graphml(CAMPOLIDE_GRAPH)
    G_lisbon = ox.load_graphml(LISBON_GRAPH)
    print 'opened the campolide_graph and lisbon_graph from file'
except:
    print 'could not open the campolide_graph or lisbon_graph from file, try to download it'
    # Getting city data from Open Street Maps
    G = ox.graph_from_place('Campolide, Lisboa', network_type='drive')
    G_lisbon = ox.graph_from_place(
        'Lisbon, Portugal', network_type='drive', which_result=2)

    print 'got osm data downloaded for Campolide and Lisbon with OSMnx'

    # save street network as GraphML file
    print 'saving the network and graph in the disk'
    G_projected = ox.project_graph(G)
    G_projected_lisbon = ox.project_graph(G_lisbon)
    ox.save_graphml(G_projected, filename=CAMPOLIDE_GRAPH)
    ox.save_graphml(G_projected_lisbon, filename=LISBON_GRAPH)
    print 'done saving in the disk'

print 'We have (' + str(G.number_of_nodes()) + \
    ') nodes and (' + str(G.number_of_edges()) + ') edges'

# Full city data plot
# ox.plot_graph(G)

# Keep the edges that are not residential or secondary from the map
print 'only let residential and secondary nodes at Campolide graph'
edges_to_remove = []
for edge in G.edges:
    if (G.edges[edge]['highway'] != 'residential' and G.edges[edge]['highway'] != 'secondary'):
        edges_to_remove.append(edge)

# Remove the kept edges and nodes without edges after that
for edge in edges_to_remove:
    G.remove_edge(edge[0], edge[1], edge[2])
G.remove_nodes_from(list(nx.isolates(G)))

print 'We have (' + str(G.number_of_nodes()) + ') nodes and (' + \
    str(G.number_of_edges()) + ') edges after removal'

# # plot the graph
# print 'plooting'
# plt.subplot(111)
# nx.draw(G, with_labels=False, font_weight='normal', node_size=10)
# plt.show()

# City data plot with removed highways
# ox.plot_graph(G)

# Must attribute a weight of garbage to each edge
for edge in G.edges:
    G.edges[edge]['weight'] = residuo_metro * G.edges[edge]['length']

# create a helper
helper = Helper(G_lisbon, trucks, list(G.edges(keys=True, data=True)))

# SUM of every edge in Campolide
total_length = 0
total_weight = 0
way_count = 0
cor_seen_edges = []
for edge in G.edges(keys=True, data=True):
    if edge[0:3] in cor_seen_edges:
        continue
    if edge[0:3] in helper.corresponding_edges:
        cor_seen_edges.append(helper.corresponding_edges[edge[0:3]][0:3])
        if helper.corresponding_edges[edge[0:3]][3]['length'] != edge[3]['length']:
            print 'ó ó ó aqui tiu!!!'
    total_length += edge[3]['length']
    total_weight += edge[3]['weight']
    way_count += 1
print 'Total ways of campolide to serve: ' +str(way_count)
print 'total length of Campolide is: ' + str(total_length)
print 'total weight of Campolide is: ' + str(total_weight)


# calculate each campolide edge distance
#distance_map = helper.build_distance_map(G.edges, EDGES_FILE)
distance_map = helper.build_distance_map_from_files(EDGES_FILE)
helper.build_closest_before()

# check for duplicates, just in case
duplicates = [item for item, count in collections.Counter(
    [edge for edge in G.edges]).items() if count > 1]
if len(duplicates) > 0:
    print 'duplicates in chromosome'
    print duplicates

#population_evolution(7000)
population_evolution(4000)

# test_multiple_ga_parameters()