import networkx as nx

from VehicleRouting.framework.ProblemFactory import VehicleRoutingProblemStrategy


class Experiment2ProblemFactory(VehicleRoutingProblemStrategy):
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
        return 1000

    def create_number_of_vehicles(self):
        return 2
