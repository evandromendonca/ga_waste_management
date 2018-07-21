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
    collect_data = sorted(collect_data, key=lambda o: o.group)


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


# if __name__ == "__main__":
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







# # plot the graph
# print 'plooting'
# plt.subplot(111)
# nx.draw(G, with_labels=False, font_weight='normal', node_size=10)
# plt.show()

# node_1 = 416835588
# node_2 = 416835591
# route = nx.shortest_path(G, node_1, node_2, weight='length')
# length = nx.shortest_path_length(G, node_1, node_2, weight='length')
# garbage_collected = nx.shortest_path_length(
#     G, node_1, node_2, weight='garbage_weight')
# print 'route: '
# print route
# print 'length: ' + str(length)
# print 'garbage collected: ' + str(garbage_collected)
