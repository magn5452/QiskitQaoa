from abc import abstractmethod, ABC


class VehicleRoutingProblemStrategy(ABC):
    @abstractmethod
    def create_graph(self):
        pass

    @abstractmethod
    def create_penalty_factor(self):
        pass

    @abstractmethod
    def create_number_of_vehicles(self):
        pass



