import networkx as nx

from VehicleRouting.framework.problem.GraphProblem import GraphProblem


class GraphPlotter():

    def __init__(self, problem: GraphProblem):
        self.problem = problem

    def plot_problem(self):
        graph = self.problem.get_graph()
        nx.draw_shell(graph, with_labels=True, alpha=0.8, node_size=500)
        labels = nx.get_edge_attributes(graph, 'weight')
        pos = nx.spring_layout(graph)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
