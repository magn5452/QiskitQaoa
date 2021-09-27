from abc import abstractmethod, ABC

from VehicleRouting.framework.factory.MaxCutFactory import MaxCutFactory
from VehicleRouting.framework.problem.GraphStrategy import GraphStrategy
from VehicleRouting.standard.concretization.GraphStrategy import TwoConnectedGraphStrategy, CompleteGraphStrategy, \
    Experiment1GraphStrategy, FiveVertexGraphStrategy


class TwoConnectedMaxCutFactory(MaxCutFactory):

    def __init__(self, num_vertex=4):
        self.num_vertex = num_vertex

    def create_graph_strategy(self):
        return TwoConnectedGraphStrategy(self.num_vertex)


class FiveVertexMaxCutFactory(MaxCutFactory):

    def __init__(self, num_vertex=4):
        self.num_vertex = num_vertex

    def create_graph_strategy(self):
        return FiveVertexGraphStrategy()


class CompleteMaxCutFactory(MaxCutFactory):

    def __init__(self, num_vertex=4):
        self.num_vertex = num_vertex

    def create_graph_strategy(self):
        return CompleteGraphStrategy(self.num_vertex)
