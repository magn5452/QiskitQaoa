from abc import abstractmethod, ABC

from VehicleRouting.framework.problem.GraphStrategy import GraphStrategy


class MaxCutProblemFactory(ABC):
    @abstractmethod
    def create_graph_strategy(self) -> GraphStrategy:
        pass


