# encoding: utf-8

import csv
from itertools import groupby
from collection_data import collection_data

# O arquivo de coleta tem dados de 01/11/2017 até 30/04/2018
# A intenção é filtrar os dados da coleta de embalagens ou papel em campolide
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



all_collection_data = read_collection_data()
campolide_routes = read_campolide_routes_file()

campolide_collection_data_embalagens = []
campolide_collection_data_papel = []

for data in all_collection_data:
    if data.route in campolide_routes and data.group == 'Embalagens' and \
        (data.route_type == 'Remoção-Selectiva-PaP-Troço' or data.route_type == 'Remoção-Selectiva-PaP-Entidade'):
        campolide_collection_data_embalagens.append(data)

for data in all_collection_data:
    if data.route in campolide_routes and data.group == 'Papel' and \
        (data.route_type == 'Remoção-Selectiva-PaP-Troço' or data.route_type == 'Remoção-Selectiva-PaP-Entidade'):
        campolide_collection_data_papel.append(data)

print 'total de dados da recolha de embalagens em campolide:' + str(len(campolide_collection_data_embalagens))
print 'min date embalagens' + str(min(data.date for data in campolide_collection_data_embalagens))
print 'max date embalagens' + str(max(data.date for data in campolide_collection_data_embalagens))

print 'total de dados da recolha de papel em campolide:' + str(len(campolide_collection_data_papel))
print 'min date papel: ' + str(min(data.date for data in campolide_collection_data_papel))
print 'max date papel: ' + str(max(data.date for data in campolide_collection_data_papel))

sorted_campolide_embalagens_data = sorted(campolide_collection_data_embalagens, key=lambda x: x.week)

for k, v in groupby(sorted_campolide_embalagens_data, key=lambda x: x.week):
    print "Group embalagens: " + str(k) + " weight: " + str(sum(int(data.weight) for data in v))

for k, v in groupby(campolide_collection_data_papel, key=lambda x: x.week):
    print "Group papel: " + str(k) + " weight: " + str(sum(int(data.weight) for data in v))    