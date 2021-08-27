import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pylatexenc

from functionsMaxCut import get_execute_circuit
from functionsMaxCut import create_qaoa_circuit
from qiskit import Aer
from qiskit.visualization import plot_histogram
from scipy.optimize import minimize

# Setting Up Graph
graph = nx.Graph()
graph.add_nodes_from([0, 1, 2, 3])
graph.add_weighted_edges_from([(0, 1, 2), (1, 2, 1), (2, 3, 1), (3, 0, 1)])

nx.draw_shell(graph, with_labels=True, alpha=0.8, node_size=500)
labels = nx.get_edge_attributes(graph, 'weight')
pos = nx.spring_layout(graph)
nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

# Returns a function to be optimized
p = 1 # number of unitaries
expectation = get_execute_circuit(graph)

# Optimize
initial_parameter = np.ones(2 * p)
optimization_method = 'Cobyla'
optimization_object = minimize(expectation, initial_parameter, method=optimization_method)
print(optimization_object)

# Get a simulator
backend = Aer.get_backend('aer_simulator')
backend.shots = 2 ^ 12

# Create Circuit with Optimized Parameters
optimized_parameters = optimization_object.x
qc_res = create_qaoa_circuit(graph, optimized_parameters)
qc_res.draw(output="mpl")

# Run simulation with optimised parameters
counts = backend.run(qc_res, seed_simulator=10).result().get_counts()
print(counts)

# Plot Histogram
plot_histogram(counts)

plt.show()
