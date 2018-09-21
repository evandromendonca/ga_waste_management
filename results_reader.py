import json
from chromosome import Chromosome
from helper import Helper
import osmnx as ox
import networkx as nx

LISBON_GRAPH = 'lisbon_graph.graphml'
G_lisbon = ox.load_graphml(LISBON_GRAPH)

def show_route(edges):    
    route = []
    route.append(edges[0][0])
    previous_node = edges[0][1]
    for edge in edges[1:]:            
        go_node = edge[0] 
        r = nx.shortest_path(G_lisbon, previous_node, go_node, weight='length')
        if False and len(r) <= 1:
            print 'strange... => previus_node:' + str(previous_node) + ' go_node:' +  str(go_node)
            print r
        route.extend(r)
        previous_node = edge[1]
    
    print 'route with ' + str(len(route)) + ' nodes'
    ox.plot_graph_route(G_lisbon, route, route_linewidth=2)

result = None

with open("best_solutions.json", "r") as f:
    result = json.load(f)

best_fitness = {}
for s in result:
    if best_fitness == {} or s['fitness'] < best_fitness['fitness']:
        best_fitness = s

# Print the best fitness found
print 'final best_population best fitness: ' + str(best_fitness['fitness']) + ' with ' + str(len(
    best_fitness['trucks_used'])) + ' trucks and with paths number: ' + str(len(best_fitness['path'])) + \
    ' - Distance from deposit: ' + str(best_fitness['deposit_distance']) + ' - Difference: ' + \
    str(best_fitness['fitness'] - best_fitness['deposit_distance'])

deposit = filter(lambda x: x[0] == 268440195 and x[1] == 268440181 and x[2] == 0, list(G_lisbon.edges(keys=True, data=True)))[0]

# Plot the route
best = Chromosome()
best.path = best_fitness['path'] 
best.trucks_used = best_fitness['trucks_used']
best.generate_routes()
for route in best.routes:
    route_path = route.get_route_path()
    route_path.insert(0, deposit)
    route_path.append(deposit)
    show_route(route_path)