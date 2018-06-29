# encoding: utf-8 

import csv
from collection_data import collection_data
from datetime import datetime
import xml.etree.ElementTree as ET

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


if __name__ == "__main__":
    read_file()    
    do()

# tree = ET.parse('map.osm')
# root = tree.getroot()

# artilharias = root.findall(u'./way/tag[@v="Rua da Artilharia 1"]/..')
# padre = root.findall(u'./way/tag[@v="Rua Padre António Vieira"]/..')
# sampaio = root.findall(u'./way/tag[@v="Rua Sampaio e Pina"]/..')