import networkx as nx
import numpy as np

from VehicleRouting.framework.problem.GraphStrategy import GraphStrategy


class SimpleExperimentGraphStrategy(GraphStrategy):
    def get_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from([0, 1, 2])
        graph.add_weighted_edges_from(
            [[0, 1, 36.840], [0, 2, 5.061], [1, 0, 36.840], [1, 2, 24.55], [2, 0, 5.061],
             [2, 1, 24.55]])

        return graph


class Experiment1GraphStrategy(GraphStrategy):
    def get_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from([0, 1, 2, 3])
        graph.add_weighted_edges_from(
            [[0, 1, 36.840], [0, 2, 5.061], [0, 3, 30.632], [1, 0, 36.840], [1, 2, 24.55], [1, 3, 63.22], [2, 0, 5.061],
             [2, 1, 24.55], [2, 3, 15.497], [3, 0, 4 * 30.632], [3, 1, 63.22], [3, 2, 15.497]])

        return graph


class Experiment2GraphStrategy(GraphStrategy):
    def get_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from([0, 1, 2, 3, 4])
        graph.add_weighted_edges_from(
            [[0, 1, 6.794], [0, 2, 61.653], [0, 3, 24.556], [0, 4, 47.767], [1, 0, 6.794], [1, 2, 87.312],
             [1, 3, 47.262],
             [1, 4, 39.477], [2, 0, 61.653], [2, 1, 87.312], [2, 3, 9.711], [2, 4, 42.887], [3, 0, 24.557],
             [3, 1, 47.262],
             [3, 2, 9.711], [3, 4, 40.98], [4, 0, 47.767], [4, 1, 39.477], [4, 2, 42.887], [4, 3, 40.98]])
        return graph


class OneVertexGraphStrategy(GraphStrategy):
    def get_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from([0])
        return graph


class TwoVertexGraphStrategy(GraphStrategy):
    def get_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from([0, 1])
        graph.add_weighted_edges_from([[0, 1, 1], [1, 0, 1]])

        return graph


class ThreeVertexGraphStrategy(GraphStrategy):

    def get_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from([0, 1, 2])
        graph.add_weighted_edges_from(
            [[0, 1, 36.840], [0, 2, 5.061], [1, 0, 36.840], [1, 2, 24.55], [2, 0, 5.061],
             [2, 1, 24.55]])

        return graph


class CompleteGraphStrategy(GraphStrategy):

    def __init__(self, n=4):
        self.n = n

    def get_graph(self):
        graph = nx.Graph()
        for i in range(self.n):
            graph.add_node(i)

        for i in graph.nodes:
            for j in graph.nodes:
                if i != j:
                    graph.add_edge(i, j)

        return graph


class TwoConnectedGraphStrategy(GraphStrategy):

    def __init__(self, n=4):
        self.n = n

    def get_graph(self):
        graph = nx.Graph()
        for i in range(self.n):
            graph.add_node(i)

        for i in graph.nodes:
            graph.add_edge(i, np.mod(i + 1, self.n))

        return graph


class FiveVertexGraphStrategy(GraphStrategy):

    def __init__(self, n=4):
        self.n = n

    def get_graph(self):
        graph = nx.Graph()
        graph.add_nodes_from([0, 1, 2, 3, 4])
        graph.add_weighted_edges_from(
            [[0, 1, 1], [1, 2, 1], [2, 3, 1], [3, 4, 1], [4, 0, 1], [0, 2, 1]])

        return graph
