# encoding: utf-8

import os
import csv
from itertools import groupby
from difflib import SequenceMatcher
from collection_data import collection_data
from route_detail import route_detail


# O arquivo de coleta tem dados de 01/11/2017 até 30/04/2018
# A intenção é filtrar os dados da coleta de embalagens em campolide
# onde a remoção ocorra porta a porta

def read_collection_data():
    collect_data = []

    # read the csv of the collected data and store it in a list of
    # collect_objects, each object is a row in the csv
    with open("./data/dados_residuos.csv") as file:
        reader = csv.reader(file, delimiter=";")
        reader.next()
        for row in reader:
            data = collection_data(row)
            collect_data.append(data)

    # sort the built list
    collect_data = sorted(collect_data, key=lambda o: o.group)

    return collect_data

def read_campolide_routes_file():
    campolide_routes = []

    with open("./data/campolide_routes.csv") as file:
        reader = csv.reader(file, delimiter=";")        
        for row in reader:
            campolide_routes.append(row[0])

    return campolide_routes

def read_routes_details():
    route_details = []

    path = os.path.abspath("./data/circuitos_details.csv")
    with open(path) as file:
        reader = csv.reader(file, delimiter=";")
        reader.next()
        for row in reader:
            data = route_detail(row)
            route_details.append(data)

    return route_details


all_collection_data = read_collection_data() # list of objects of the collection data from Camara de Lisboa
campolide_routes = read_campolide_routes_file() # list with the route codes for campolide
routes_details = read_routes_details() # list of objects with route details for campolide

trucks_campolide = {}
campolide_collection_data_embalagens = []
for data in all_collection_data:
    if data.route in campolide_routes and data.group == 'Embalagens' and \
        (data.route_type == 'Remoção-Selectiva-PaP-Troço'):
        if data.truck_plate not in trucks_campolide:
            trucks_campolide[data.truck_plate] = (data.truck_plate, data.truck_capacity, data.truck_type)
        campolide_collection_data_embalagens.append(data)

rota_E0714_Int = filter(lambda x: x.route == 'E0714 Int', campolide_collection_data_embalagens)
rota_E0504 = filter(lambda x: x.route == 'E0504', campolide_collection_data_embalagens)

total_weight_rota_E0714_Int = 0
total_weight_rota_E0504 = 0
number_of_weeks = 0

rota_E0714_Int = sorted(rota_E0714_Int, key=lambda x: x.week)
for k, v in groupby(rota_E0714_Int, key=lambda x: x.week):
    # print "Group embalagens: " + str(k) + " weight: " + str(sum(int(data.weight) for data in v))
    total_weight_rota_E0714_Int += sum(int(data.weight) for data in v)
    number_of_weeks += 1
print 'ROUTE E0714 Int -> Weeks: ' + str(number_of_weeks) + ' total weight: ' + str(total_weight_rota_E0714_Int)
media_rota_E0714_Int = total_weight_rota_E0714_Int / number_of_weeks
print 'ROUTE E0714 Int -> Media: ' + str(media_rota_E0714_Int)

number_of_weeks = 0
rota_E0504 = sorted(rota_E0504, key=lambda x: x.week)
for k, v in groupby(rota_E0504, key=lambda x: x.week):
    # print "Group embalagens: " + str(k) + " weight: " + str(sum(int(data.weight) for data in v))
    total_weight_rota_E0504 += sum(int(data.weight) for data in v)
    number_of_weeks += 1
print 'ROUTE E0504 -> Weeks: ' + str(number_of_weeks) + ' total weight: ' + str(total_weight_rota_E0504)
media_rota_E0504 = total_weight_rota_E0504 / number_of_weeks
print 'ROUTE E0504 -> Media: ' + str(media_rota_E0504)

num_ruas_em_campolide_E0714_Int = 15
num_ruas_em_campolide_E0504 = 2

num_ruas_em_total_E0714_Int = sum(1 for r in map(lambda x: x.route, filter(lambda x: x.route == 'E0714 Int', routes_details)))
print 'ROUTE E0714 Int -> Total ruas: ' + str(num_ruas_em_total_E0714_Int) + ' Em campolide: ' + str(num_ruas_em_campolide_E0714_Int)
percentual_ruas_rota_E0714_Int_campolide = num_ruas_em_campolide_E0714_Int / float(num_ruas_em_total_E0714_Int)
print 'ROUTE E0714 Int -> Percentual da rota em Campolide: ' + str(percentual_ruas_rota_E0714_Int_campolide)

num_ruas_em_total_E0504 = sum(1 for r in map(lambda x: x.route, filter(lambda x: x.route == 'E0504', routes_details)))
print 'ROUTE E0504 -> Total ruas: ' + str(num_ruas_em_total_E0504) + ' Em campolide: ' + str(num_ruas_em_campolide_E0504)
percentual_ruas_rota_E0504_campolide = num_ruas_em_campolide_E0504 / float(num_ruas_em_total_E0504)
print 'ROUTE E0504 -> Percentual da rota em Campolide: ' + str(percentual_ruas_rota_E0504_campolide)

print 'ROUTE E0504 -> total coletado na parte de campolide: ' + str(media_rota_E0504 * percentual_ruas_rota_E0504_campolide)
print 'Route E0714 Int -> total coletado na parte de campolide: ' + str(media_rota_E0714_Int * percentual_ruas_rota_E0714_Int_campolide)


# para todos os dados de coleta disponibilizados pela Camara de Lisboa, vou usar apenas os que a rota passa por Campolide e que sejam
# coleta porta a porta seletiva

# para cada uma das rotas que incluem campolide e sejam coleta porta a porta seletiva, armazeno os detalhes
campolide_routes_details = {}
for route_detail in routes_details:
    if route_detail.collection_type_abrev != 'P-a-P Sel':
        continue
    if route_detail.route in campolide_routes:
        if route_detail.route in campolide_routes_details:
            campolide_routes_details[route_detail.route].append((route_detail.freg_id, route_detail.address))
        else:
            campolide_routes_details[route_detail.route] = []
            campolide_routes_details[route_detail.route].append((route_detail.freg_id, route_detail.address))

# para cada uma das rotas na lista montada acima, que inclui campolide, monto uma nova lista com os detalhes apenas dos
# endereços dentro de campolide
# campolide freg id = 111
only_campolide_routes = {}
for route_detail in campolide_routes_details:
    only_campolide_routes[route_detail] = []
    for address in campolide_routes_details[route_detail]:
        if address[0] == "111":
            only_campolide_routes[route_detail].append(address)



# todas rotas dos dados de coleta que sao de embalagens e nao sao vazias
collection_data_routes = list(map(lambda x: x.route, 
    filter(lambda x: x.group == 'Embalagens' and x.route != '', all_collection_data)))

# guardar apenas as rotas que estao contidas nos dados coletados pela camara, e que sejam de Embalagens
campolide_embalagem_routes = {}
for route in only_campolide_routes:
    if len(only_campolide_routes[route]) <= 0:
        continue
    if route in collection_data_routes:        
        campolide_embalagem_routes[route] = []
        campolide_embalagem_routes[route].extend(only_campolide_routes[route])

# get the edges from the campolide OSMnx graph
import osmnx as ox
import networkx as nx
CAMPOLIDE_GRAPH = 'campolide_graph.graphml'
G = ox.load_graphml(CAMPOLIDE_GRAPH)
edges_to_remove = []
for edge in G.edges:
    if (G.edges[edge]['highway'] != 'residential' and G.edges[edge]['highway'] != 'secondary'):
        edges_to_remove.append(edge)
# Remove the kept edges
for edge in edges_to_remove:
    G.remove_edge(edge[0], edge[1], edge[2])
# Remove nodes without edges
G.remove_nodes_from(list(nx.isolates(G)))
edges_list = list(G.edges(keys=True, data=True))

# match elements
# from: https://docs.python.org/2/library/difflib.html#sequencematcher-objects
# ratio() returns a float in [0, 1], measuring the similarity of the sequences. 
# As a rule of thumb, a ratio() value over 0.6 means the sequences are close matches
junk_func = lambda x: x in " \t"
for route in campolide_embalagem_routes:
    for address in campolide_embalagem_routes[route]:
        splitted_address = address[1].split('(')[0].decode('utf-8')
        print splitted_address
        matches = filter(lambda way: SequenceMatcher(junk_func, way[3]['name'], splitted_address).ratio() > 0.6 if 'name' in way[3] else False, edges_list)
        print matches


# pego cada informacao da coleta data pela Camara, pego apenas as que estao dentro da freguesia de campolide, que sejam 
# sobre embalagens, e que a coleta seja feita porta a porta
campolide_collection_data_embalagens = []
for data in all_collection_data:
    if data.route in campolide_routes and data.group == 'Embalagens' and \
        (data.route_type == 'Remoção-Selectiva-PaP-Troço'):
        campolide_collection_data_embalagens.append(data)

campolide_collection_data_papel = []
for data in all_collection_data:
    if data.route in campolide_routes and data.group == 'Papel' and \
        (data.route_type == 'Remoção-Selectiva-PaP-Troço'):
        campolide_collection_data_papel.append(data)

print 'total de dados da recolha de embalagens em campolide:' + str(len(campolide_collection_data_embalagens))
print 'min date embalagens' + str(min(data.date for data in campolide_collection_data_embalagens))
print 'max date embalagens' + str(max(data.date for data in campolide_collection_data_embalagens))

print 'total de dados da recolha de papel em campolide:' + str(len(campolide_collection_data_papel))
print 'min date papel: ' + str(min(data.date for data in campolide_collection_data_papel))
print 'max date papel: ' + str(max(data.date for data in campolide_collection_data_papel))

total_weight_embalagens = 0
sorted_campolide_embalagens_data = sorted(campolide_collection_data_embalagens, key=lambda x: x.week)
for k, v in groupby(sorted_campolide_embalagens_data, key=lambda x: x.week):
    # print "Group embalagens: " + str(k) + " weight: " + str(sum(int(data.weight) for data in v))
    total_weight_embalagens += sum(int(data.weight) for data in v)
print total_weight_embalagens

total_weight_papel = 0
sorted_campolide_papel_data = sorted(campolide_collection_data_papel, key=lambda x: x.week)
for k, v in groupby(sorted_campolide_papel_data, key=lambda x: x.week):
    # print "Group papel: " + str(k) + " weight: " + str(sum(int(data.weight) for data in v))
    total_weight_papel += sum(int(data.weight) for data in v)
print total_weight_papel