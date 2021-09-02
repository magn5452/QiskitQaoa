import networkx as nx
import numpy as np


class VehicleRoutingProblem:

    def __init__(self, graph, number_of_vehicles, penalty_factor):
        self.number_of_vertices = graph.order()
        self.number_of_edges = graph.number_of_edges()
        self.number_of_vehicles = number_of_vehicles
        self.graph = graph
        self.penalty_factor = penalty_factor
        self.weights = np.real([*nx.get_edge_attributes(self.graph, 'weight').values()])

    def get_weights(self):
        return self.weights

    def get_penalty_factor(self):
        return self.penalty_factor

    def get_graph(self):
        return self.graph

    def get_number_of_vehicles(self):
        return self.number_of_vehicles

    def get_number_of_vertices(self):
        return self.number_of_vertices

    def get_number_of_edges(self):
        return self.number_of_edges

    def get_edges(self):
        return self.graph.edges
