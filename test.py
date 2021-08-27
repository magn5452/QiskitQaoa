import matplotlib.pyplot as plt
import networkx as nx

from CostVehicleRoutingCalculator import CostVehicleRoutingCalculator

# Setting Up Graph
graph = nx.Graph()
graph.add_nodes_from([0, 1, 2, 3])
graph.add_weighted_edges_from([(0, 1, 36.84), (0, 2, 5.06), (0, 3, 30.63), (2, 3, 15.50)])

nx.draw_shell(graph, with_labels=True, alpha=0.8, node_size=500)
labels = nx.get_edge_attributes(graph, 'weight')
pos = nx.spring_layout(graph)
nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

costCalculator = CostVehicleRoutingCalculator('101100100001', graph, 2, 100)
print(costCalculator.get_adjacency_matrix())
print(costCalculator.vehicle_routing_cost())

plt.show()
