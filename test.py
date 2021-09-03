import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from CostVehicleRoutingCalculator import CostVehicleRoutingCalculator

# Setting Up Graph
from VehicleRoutingProblem import VehicleRoutingProblem
from VehicleRoutingQUBO import VehicleRoutingQUBO

graph = nx.DiGraph()
graph.add_node(0)
graph.add_node(1)
graph.add_node(2)
graph.add_node(3)
graph.add_weighted_edges_from([[0, 1, 1], [0, 2, 1], [0, 3, 1], [1, 0, 1], [1, 2, 1], [1, 3, 1], [2, 0, 1], [2, 1, 1], [2, 3, 1], [3, 0, 1], [3, 1, 1], [3, 2, 1]])
nx.draw_shell(graph, with_labels=True, alpha=0.8, node_size=500)
labels = nx.get_edge_attributes(graph, 'weight')
pos = nx.spring_layout(graph)
nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

vehicle_routing_problem = VehicleRoutingProblem(graph, 1, 100)
vehicle_routing_QUBO = VehicleRoutingQUBO(vehicle_routing_problem)
print(vehicle_routing_QUBO.calculate_cost([1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0]))

plt.show()
