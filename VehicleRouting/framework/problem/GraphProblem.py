from abc import ABC, abstractmethod


class GraphProblem(ABC):
    @abstractmethod
    def get_graph(self):
        pass

    @abstractmethod
    def get_number_of_vertices(self):
        pass

    @abstractmethod
    def get_number_of_edges(self):
        pass

    @abstractmethod
    def get_edges(self):
        pass

    @abstractmethod
    def get_weights(self):
        pass

    @abstractmethod
    def get_weight(self, i, j):
        pass
