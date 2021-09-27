
import networkx as nx
import numpy as np

from VehicleRouting.framework.problem.GraphProblem import GraphProblem
from VehicleRouting.framework.factory.MaxCutFactory import MaxCutFactory


class MaxCutProblem(GraphProblem):

    def __init__(self, factory: MaxCutFactory):
        self.graph_strategy = factory.create_graph_strategy()
        self.graph = self.graph_strategy.get_graph()
        self.number_of_vertices = self.graph.order()
        self.number_of_edges = self.graph.number_of_edges()

    def get_weights(self):
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
            return 0

    def get_graph(self):
        return self.graph

    def get_number_of_vertices(self):
        return self.number_of_vertices

    def get_number_of_edges(self):
        return self.number_of_edges

    def get_edges(self):
        return self.graph.couplings

    def get_vertices(self):
        return self.graph.nodes
