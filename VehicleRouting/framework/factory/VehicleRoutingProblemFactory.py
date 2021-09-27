from abc import abstractmethod, ABC

from VehicleRouting.framework.problem.GraphStrategy import GraphStrategy


class VehicleRoutingProblemFactory(ABC):

    @abstractmethod
    def create_graph_strategy(self) -> GraphStrategy:
        pass

    @abstractmethod
    def create_penalty_factor(self) -> float:
        pass

    @abstractmethod
    def create_number_of_vehicles(self) -> int:
        pass

    @abstractmethod
    def create_depot(self) -> int:
        pass