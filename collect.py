# encoding: utf-8 

import csv
from collection_data import collection_data
from datetime import datetime
import xml.etree.ElementTree as ET
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import random

def read_file():
    collect_data = []

    # read the csv of the collected data and store it in a list of
    # collect_objects, each object is a row in the csv
    with open("dados_residuos.csv") as file:
        reader = csv.reader(file, delimiter=";")
        reader.next()
        for row in reader:
            data = collection_data(row) 
            collect_data.append(data)
    
    # sort the built list
    collect_data = sorted(collect_data,key=lambda o: o.group)

def do():
    tree = ET.parse('map.osm')
    root = tree.getroot()
    
    #all = root.findall(u'./way/tag[@v="Calçada dos Mestres"]/..')
    all = root.findall(u'./way/tag[@v="Rua da Artilharia 1"]/..')

    # for item in all:
    #     print item.get('id')
    #     street = item.find('./tag[@k="name"]')
    #     print street.attrib

    artilharias = root.findall(u'./way/tag[@v="Rua da Artilharia 1"]/..')
    padre = root.findall(u'./way/tag[@v="Rua Padre António Vieira"]/..')
    sampaio = root.findall(u'./way/tag[@v="Rua Sampaio e Pina"]/..')

    for way in artilharias:
        #print way.attrib
        nodes = way.findall(u'./nd[@ref]')
        for node in nodes:
            #print 'artilharia: ' + node.get('ref')
            for pway in padre:
                pnodes = pway.findall(u'./nd[@ref]')
                for pnode in pnodes:
                    #print 'padre: ' + pnode.get('ref') 
                    if node.get('ref') == pnode.get('ref'):
                        print 'MATCH in ' + pnode.get('ref')
                        print way.attrib
                        print pway.attrib


#if __name__ == "__main__":
    # read_file()    
    # do()

#tree = ET.parse('map.osm')
#root = tree.getroot()
#print 'got osm xml data'

# artilharias = root.findall(u'./way/tag[@v="Rua da Artilharia 1"]/..')
# padre = root.findall(u'./way/tag[@v="Rua Padre António Vieira"]/..')
# sampaio = root.findall(u'./way/tag[@v="Rua Sampaio e Pina"]/..')

# DISTANCE
# define a lat-long point, create network around point, define origin/destination nodes
# location_point = (38.7272672, -9.1588165)
# G = ox.graph_from_place('Campolide, Lisboa', network_type='drive')
# origin_node = ox.get_nearest_node(G, location_point)
# destination_node = list(G.nodes())[-1]
# print origin_node


# ----------------------------------------------------------------------------------
# A genetic algorithm for the Capacitated Arc Rout Problem (CARP) with multiple
# capacities
# Case of Campolide
# Using the new Genetic Representation for the Vehicle Route Problem    
# count the cars by capacity (n importa a placa do carro, e sim a capacidade DISTINCT)
# ----------------------------------------------------------------------------------

# Getting city data from Open Street Maps
G = ox.graph_from_place('Campolide, Lisboa', network_type='drive')
print 'got osm data downloaded for campolide with OSMnx'

print 'We have (' + str(G.number_of_nodes()) + ') nodes and (' + str(G.number_of_edges()) + ') edges'

# Full city data plot
# ox.plot_graph(G)

# Keep the edges that are not residential or secondary from the map
print 'only let the residential and secondary nodes pass'
edges_to_remove = []
for edge in G.edges:
    if (G.edges[edge]['highway'] != 'residential' and G.edges[edge]['highway'] != 'secondary'):
        edges_to_remove.append(edge)

# Remove the kept edges
for edge in edges_to_remove:
    G.remove_edge(edge[0], edge[1], edge[2])

# Remove nodes without edges 
G.remove_nodes_from(list(nx.isolates(G)))

print 'We have (' + str(G.number_of_nodes()) + ') nodes and (' + str(G.number_of_edges()) + ') edges'

# City data plot with removed highways 
# ox.plot_graph(G)

# Must attribute a weight of garbage to each edge
for edge in G.edges:
    G.edges[edge]['garbage_weight'] = random.randint(1, 100)

# # plot the graph
# print 'plooting'
# plt.subplot(111)
# nx.draw(G, with_labels=False, font_weight='normal', node_size=10)
# plt.show()

node_1 = 416835588
node_2 = 416835591
route = nx.shortest_path(G, node_1, node_2, weight='length')
length = nx.shortest_path_length(G, node_1, node_2, weight='length')
garbage_collected = nx.shortest_path_length(G, node_1, node_2, weight='garbage_weight')
print 'route: '
print route
print 'length: ' + str(length)
print 'garbage collected: ' + str(garbage_collected)