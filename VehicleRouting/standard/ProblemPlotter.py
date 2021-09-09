import networkx as nx
from matplotlib import pyplot as plt

from VehicleRouting.standard import Problem


class ProblemPlotter():

    def __init__(self, problem: Problem):
        self.problem = problem

    def plot_problem(self):
        graph = self.problem.get_graph()
        nx.draw_shell(graph, with_labels=True, alpha=0.8, node_size=500)
        labels = nx.get_edge_attributes(graph, 'weight')
        pos = nx.spring_layout(graph)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
