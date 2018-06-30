# encoding: utf-8 

import csv
from collection_data import collection_data
from datetime import datetime
import xml.etree.ElementTree as ET
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

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

tree = ET.parse('map.osm')
root = tree.getroot()
print 'got osm xml data'

# artilharias = root.findall(u'./way/tag[@v="Rua da Artilharia 1"]/..')
# padre = root.findall(u'./way/tag[@v="Rua Padre António Vieira"]/..')
# sampaio = root.findall(u'./way/tag[@v="Rua Sampaio e Pina"]/..')

campolideOSM = ox.graph_from_place('Campolide, Lisboa', network_type='drive')
print 'got osm data downloaded for campolide with OSMnx'

nodes = list(campolideOSM.nodes)
edges = [ edge[0:2] for edge in list(campolideOSM.edges)] # as edges são two ways qnd se precisa
print "nodes(",len(nodes),") and edges(",len(edges),") removed from the osm data"

kept_nodes = []

print 'only let the residential and secondary nodes pass'
for node in nodes:
    keep_node = False
    
    # search in the osm file for ways with that node
    osm_file_nodes = root.findall(u'./way/nd[@ref="'+str(node)+'"]/..')

    # iterate over the found ways, if at least a way is residential or secondary, keep the node
    for found_ways in osm_file_nodes:
        # search the tag highway of the found ways, and get the value of it
        tag = found_ways.find(u'./tag[@k="highway"]')        

        # if the tag was not found, cant assume its not residential or secondary, so add and continue
        if tag is None:
            #print 'kept'
            keep_node = True
            break

        #print tag.attrib
        tag_val = tag.get('v')                
        # if the value is residential or secondary, we want to keep track of this node
        if tag_val == 'residential' or tag_val == 'secondary':
            #print 'kept'
            keep_node = True
            break

    if keep_node:        
        kept_nodes.append(node)            

for i in kept_nodes:
    print i
# i dont wanna see 82779428 here


graph = nx.DiGraph()
graph.add_nodes_from(kept_nodes)
graph.add_edges_from(edges)
print "graph built"

print 'plooting'
plt.subplot(111)
nx.draw(graph, with_labels=False, font_weight='normal', node_size=10)
plt.show()

# G.
# ox.plot_graph(G)

# DISTANCE
# define a lat-long point, create network around point, define origin/destination nodes
# location_point = (38.7272672, -9.1588165)
# G = ox.graph_from_place('Campolide, Lisboa', network_type='drive')
# origin_node = ox.get_nearest_node(G, location_point)
# destination_node = list(G.nodes())[-1]
# print origin_node
