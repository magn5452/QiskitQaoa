import networkx as nx
import numpy as np

from VehicleRouting.framework.factory import ProblemFactory


class Problem:

    def __init__(self, factory: ProblemFactory):
        self.graph = factory.create_graph()
        self.number_of_vertices = self.graph.order()
        self.number_of_edges = self.graph.number_of_edges()
        self.number_of_vehicles = factory.create_number_of_vehicles()
        self.penalty_factor = factory.create_penalty_factor()
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

    def get_vertices(self):
        return self.graph.nodes
