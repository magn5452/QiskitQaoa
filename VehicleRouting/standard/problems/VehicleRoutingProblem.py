import networkx as nx
import numpy as np

from VehicleRouting.framework.factory.VehicleRoutingProblemFactory import VehicleRoutingProblemFactory
from VehicleRouting.framework.problem.GraphProblem import GraphProblem
from VehicleRouting.framework.problem.HardProblem import HardProblem
from VehicleRouting.framework.problem import GraphStrategy


class VehicleRoutingProblem(GraphProblem, HardProblem):

    def __init__(self, factory: VehicleRoutingProblemFactory):
        self.graph_strategy = factory.create_graph_strategy()
        self.graph = self.graph_strategy.get_graph()
        self.number_of_vertices = self.graph.order()
        self.number_of_edges = self.graph.number_of_edges()

        self.number_of_vehicles = factory.create_number_of_vehicles()
        self.penalty_factor = factory.create_penalty_factor()
        self.depot = factory.create_depot()

    def get_weight_vector(self):
        if nx.is_weighted(self.graph):
            return np.real([*nx.get_edge_attributes(self.graph, 'weight').values()])
        else:
            return np.ones(self.number_of_edges)

    def get_weight(self, i, j):
        if self.graph.has_edge(i, j):
            if nx.is_weighted(self.graph, (i, j)):
                return self.graph[i][j]["weight"]
            else:
                return 1
        else:
            return np.inf

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

    def get_depot(self):
        return self.depot
