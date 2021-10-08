from abc import ABC, abstractmethod

from VehicleRouting.framework.qaoa.BackendStrategy import BackendStrategy
from VehicleRouting.framework.qaoa.CircuitStrategy import InitialStrategy, MixerStrategy, PhaseStrategy, \
    MeasurementStrategy
from VehicleRouting.framework.qaoa.CostStategy import CostStrategy
from VehicleRouting.standard.concretization.QuboImpl import QuboImpl


class QaoaFactory(ABC):
    @abstractmethod
    def create_qubo(self) -> QuboImpl:
        pass

    @abstractmethod
    def create_backend(self) -> BackendStrategy:
        pass

    @abstractmethod
    def create_mixer(self) -> MixerStrategy:
        pass

    @abstractmethod
    def create_phase(self) -> PhaseStrategy:
        pass

    @abstractmethod
    def create_initial(self) -> InitialStrategy:
        pass

    @abstractmethod
    def create_measurement(self) -> MeasurementStrategy:
        pass

    @abstractmethod
    def create_precision(self) -> int:
        pass

    @abstractmethod
    def create_cost(self) -> CostStrategy:
        pass
