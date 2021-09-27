from abc import abstractmethod, ABC

from VehicleRouting.framework.problem.GraphStrategy import GraphStrategy


class MaxCutFactory(ABC):
    @abstractmethod
    def create_graph_strategy(self) -> GraphStrategy:
        pass


