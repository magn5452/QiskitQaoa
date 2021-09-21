import networkx as nx

from VehicleRouting.framework.factory.ProblemFactory import VehicleRoutingProblemFactory


class Experiment1ProblemFactory(VehicleRoutingProblemFactory):
    def create_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from([0, 1, 2, 3])
        graph.add_weighted_edges_from(
            [[0, 1, 36.840], [0, 2, 5.061], [0, 3, 30.632], [1, 0, 36.840], [1, 2, 24.55], [1, 3, 63.22], [2, 0, 5.061],
             [2, 1, 24.55], [2, 3, 15.497], [3, 0, 30.632], [3, 1, 63.22], [3, 2, 15.497]])

        return graph

    def create_penalty_factor(self):
        return 100000

    def create_number_of_vehicles(self):
        return 2


class Experiment2ProblemFactory(VehicleRoutingProblemFactory):
    def create_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from([0, 1, 2, 3, 4])
        graph.add_weighted_edges_from(
            [[0, 1, 6.794], [0, 2, 61.653], [0, 3, 24.556], [0, 4, 47.767], [1, 0, 6.794], [1, 2, 87.312],
             [1, 3, 47.262],
             [1, 4, 39.477], [2, 0, 61.653], [2, 1, 87.312], [2, 3, 9.711], [2, 4, 42.887], [3, 0, 24.557],
             [3, 1, 47.262],
             [3, 2, 9.711], [3, 4, 40.98], [4, 0, 47.767], [4, 1, 39.477], [4, 2, 42.887], [4, 3, 40.98]])
        return graph

    def create_penalty_factor(self):
        return 100000

    def create_number_of_vehicles(self):
        return 2


class OneVertexProblemFactory(VehicleRoutingProblemFactory):
    def create_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from([0])
        return graph

    def create_penalty_factor(self):
        return 100000

    def create_number_of_vehicles(self):
        return 1


class TwoVertexProblemFactory(VehicleRoutingProblemFactory):
    def create_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from([0, 1])
        graph.add_weighted_edges_from([[0, 1, 1], [1, 0, 1]])

        return graph

    def create_penalty_factor(self):
        return 100000

    def create_number_of_vehicles(self):
        return 1


class ThreeVertexProblemFactory(VehicleRoutingProblemFactory):
    def create_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from([0, 1, 2])
        graph.add_weighted_edges_from(
            [[0, 1, 36.840], [0, 2, 5.061], [1, 0, 36.840], [1, 2, 24.55], [2, 0, 5.061],
             [2, 1, 24.55]])

        return graph

    def create_penalty_factor(self):
        return 100000

    def create_number_of_vehicles(self):
        return 1
