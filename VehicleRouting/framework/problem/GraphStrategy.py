from abc import abstractmethod, ABC


class GraphStrategy(ABC):
    @abstractmethod
    def get_graph(self):
        pass





