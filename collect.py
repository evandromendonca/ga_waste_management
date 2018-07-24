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
#
# Depósito de embalagens, é uma rua com mão dupla, ver qual é mais perto e atribuir ao fim da rota
# (268440195, 268440181, 0)
# (268440181, 268440195, 0)
# ----------------------------------------------------------------------------------

import csv
from collection_data import collection_data
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

# WHERE AM I ? TE OR HOME
where_am_i = "HOME"

if where_am_i == "HOME":
    CAMPOLIDE_GRAPH = 'campolide_graph.graphml'
    LISBON_GRAPH = 'lisbon_graph.graphml'
    EDGES_FILE = 'edges.csv'
else:
    CAMPOLIDE_GRAPH = 'TE_campolide_graph.graphml'
    LISBON_GRAPH = 'TE_lisbon_graph.graphml'
    EDGES_FILE = 'TE_edges.csv'

# available trucks must also be presented
trucks = [
    ('95-60-LG', 900),
    ('05-IG-14', 1400),
    ('53-MP-23', 500),
    ('54-SV-71', 600),
    ('79-20-XT', 400)
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

# Remove the kept edges
for edge in edges_to_remove:
    G.remove_edge(edge[0], edge[1], edge[2])

# Remove nodes without edges
G.remove_nodes_from(list(nx.isolates(G)))

print 'We have (' + str(G.number_of_nodes()) + \
    ') nodes and (' + str(G.number_of_edges()) + ') edges'

# City data plot with removed highways
# ox.plot_graph(G)

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

# Must attribute a weight of garbage to each edge
for edge in G.edges:
    G.edges[edge]['weight'] = random.randint(1, 100)
    #G_lisbon.edges[edge]['weight'] = random.randint(1, 100)

# SUM of every edge in Campolide
total_length = 0
for edge in G.edges(keys=True, data=True):
    total_length += edge[3]['length']
print 'total length of Campolide is: ' + str(total_length)

# create a helper
helper = Helper(G_lisbon, trucks)

# calculate each campolide edge distance
#distance_map = helper.build_distance_map(G.edges, EDGES_FILE)
distance_map = helper.build_distance_map_from_files(EDGES_FILE)

duplicates = [item for item, count in collections.Counter(
    [edge for edge in G.edges]).items() if count > 1]
if len(duplicates) > 0:
    print 'duplicates in chromosome'
    print duplicates

# randomize the initial population
population = Population(helper, G.edges(keys=True, data=True), trucks, True)
print 'initial population best fitness: ' + str(population.get_best_fitness().fitness) + ' with ' + str(len(
    population.get_best_fitness().trucks_used)) + ' trucks and with paths number: ' + str(len(population.get_best_fitness().path))

# evolving
for i in range(1000):
    population = population.evolve()
    print 'iteration ' + str(i) + ' best fitness: ' + str(population.get_best_fitness().fitness) + ' with ' + str(len(
        population.get_best_fitness().trucks_used)) + ' trucks and with paths number: ' + str(len(population.get_best_fitness().path))

print 'final population best fitness: ' + str(population.get_best_fitness().fitness) + ' with ' + str(len(
    population.get_best_fitness().trucks_used)) + ' trucks and with paths number: ' + str(len(population.get_best_fitness().path))