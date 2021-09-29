from VehicleRouting.framework.factory.VehicleRoutingProblemFactory import VehicleRoutingProblemFactory
from VehicleRouting.framework.problem.GraphStrategy import GraphStrategy
from VehicleRouting.standard.concretization.GraphStrategy import Experiment1GraphStrategy, Experiment2GraphStrategy, \
    SimpleExperimentGraphStrategy


class SimpleVehicleRoutingProblemFactory(VehicleRoutingProblemFactory):

    def create_graph_strategy(self) -> GraphStrategy:
        return SimpleExperimentGraphStrategy()

    def create_penalty_factor(self) -> float:
        return 10000

    def create_number_of_vehicles(self) -> int:
        return 2

    def create_depot(self) -> int:
        return 0



class Experiment1VehicleRoutingProblemFactory(VehicleRoutingProblemFactory):

    def create_graph_strategy(self) -> GraphStrategy:
        return Experiment1GraphStrategy()

    def create_penalty_factor(self) -> float:
        return 10000

    def create_number_of_vehicles(self) -> int:
        return 2

    def create_depot(self) -> int:
        return 0


class Experiment2VehicleRoutingProblemFactory(VehicleRoutingProblemFactory):

    def create_graph_strategy(self) -> GraphStrategy:
        return Experiment2GraphStrategy()

    def create_penalty_factor(self) -> float:
        return 10000

    def create_number_of_vehicles(self) -> int:
        return 2

    def create_depot(self) -> int:
        return 0
