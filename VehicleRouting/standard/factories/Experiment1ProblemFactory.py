import networkx as nx

from VehicleRouting.framework.ProblemFactory import VehicleRoutingProblemStrategy


class Experiment1ProblemFactory(VehicleRoutingProblemStrategy):
    def create_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from([0, 1, 2, 3])
        graph.add_weighted_edges_from(
            [[0, 1, 36.840], [0, 2, 5.061], [0, 3, 30.632], [1, 0, 36.840], [1, 2, 24.55], [1, 3, 63.22], [2, 0, 5.061],
             [2, 1, 24.55], [2, 3, 15.497], [3, 0, 30.632], [3, 1, 63.22], [3, 2, 15.497]])

        return graph

    def create_penalty_factor(self):
        return 1000

    def create_number_of_vehicles(self):
        return 2

