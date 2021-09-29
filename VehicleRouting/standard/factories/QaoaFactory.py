import numpy as np

from VehicleRouting.framework.factory.QaoaFactory import QaoaFactory
from VehicleRouting.framework.qaoa.BackendStrategy import BackendStrategy
from VehicleRouting.framework.qaoa.CircuitStrategy import InitialStrategy, PhaseStrategy, MixerStrategy, \
    MeasurementStrategy
from VehicleRouting.framework.interfaces.QaoaMinimizer import QaoaMinimizer
from VehicleRouting.standard.Qubo import Qubo
from VehicleRouting.standard.problems.MaxCutProblem import MaxCutProblem
from VehicleRouting.standard.problems.VehicleRoutingProblem import VehicleRoutingProblem
from VehicleRouting.standard.qaoa.BackendStrategy import AerBackendStrategy, NoisyBackendStrategy, \
    StateVectorBackendStrategy
from VehicleRouting.standard.qaoa.CircuitStrategy import RXGateMixerStrategy, HGateInitialStrategy, \
    WeightedZGatePhaseStrategy, ZGatePhaseStrategy, NoMeasurementStrategy, AllMeasurementStrategy, CustomMixerStrategy, \
    OneHotSingleInitialStrategy
from VehicleRouting.standard.concretization.QuboCalculatorStrategy import MaxCutQuboCalculatorStrategy, \
    VertexOrderingQuboCalculatorStrategy, EdgeQuboCalculatorStrategy

class ExactMaxCutQaoaFactory(QaoaFactory):

    def __init__(self, problem: MaxCutProblem):
        self.problem = problem

    def create_qubo(self) -> Qubo:
        calculator_strategy = MaxCutQuboCalculatorStrategy(self.problem)
        return Qubo(calculator_strategy)

    def create_backend(self) -> BackendStrategy:
        return StateVectorBackendStrategy()

    def create_mixer(self) -> MixerStrategy:
        return RXGateMixerStrategy()

    def create_phase(self) -> PhaseStrategy:
        couplings = self.problem.get_edges()
        return ZGatePhaseStrategy(couplings)

    def create_measurement(self) -> MeasurementStrategy:
        return NoMeasurementStrategy()

    def create_initial(self) -> InitialStrategy:
        return HGateInitialStrategy()

    def create_precision(self):
        return 1


class NoisyMaxCutQaoaFactory(QaoaFactory):

    def create_measurement(self) -> MeasurementStrategy:
        return AllMeasurementStrategy()

    def __init__(self, problem: MaxCutProblem):
        self.problem = problem

    def create_qubo(self) -> Qubo:
        calculator_strategy = MaxCutQuboCalculatorStrategy(self.problem)
        return Qubo(calculator_strategy)

    def create_backend(self) -> BackendStrategy:
        return NoisyBackendStrategy()
    
    def create_mixer(self) -> MixerStrategy:
        return RXGateMixerStrategy()

    def create_phase(self) -> PhaseStrategy:
        couplings = self.problem.get_edges()
        return ZGatePhaseStrategy(couplings)

    def create_initial(self) -> InitialStrategy:
        return HGateInitialStrategy()

    def create_precision(self):
        return 1


class VertexOrderingVehicleRoutingQaoaFactory(QaoaFactory):

    def __init__(self, problem: VehicleRoutingProblem):
        self.problem = problem

    def create_measurement(self) -> MeasurementStrategy:
        return NoMeasurementStrategy()

    def create_qubo(self) -> Qubo:
        calculator_strategy = VertexOrderingQuboCalculatorStrategy(self.problem)
        return Qubo(calculator_strategy)

    def create_backend(self) -> BackendStrategy:
        return StateVectorBackendStrategy()

    def create_mixer(self) -> MixerStrategy:
        return CustomMixerStrategy(self.problem)

    def create_phase(self) -> PhaseStrategy:
        couplings = self.get_weighted_couplings()
        return WeightedZGatePhaseStrategy(couplings)

    def create_initial(self) -> InitialStrategy:
        return OneHotSingleInitialStrategy(self.problem.get_number_of_vertices())

    def create_precision(self):
        return 1

    def get_weighted_couplings(self):
        n = self.problem.get_number_of_vertices()
        couplings = []
        edges = self.problem.get_edges()
        weight_max = np.max(self.problem.get_weight_vector())
        for i in range(n):
            for (u, v) in edges:
                if u != v and u < v:
                    couplings.append((self.mapping(u, i), self.mapping(v, np.mod(i + 1, n)), self.problem.get_weight(u, v)/weight_max))
        return couplings

    def mapping(self, u, i):
        return self.problem.get_number_of_vertices() * u + i


class EdgeVehicleRoutingQaoaFactory(QaoaFactory):

    def create_measurement(self) -> MeasurementStrategy:
        return AllMeasurementStrategy()

    def __init__(self, problem: VehicleRoutingProblem):
        self.problem = problem

    def create_qubo(self) -> Qubo:
        calculator_strategy = EdgeQuboCalculatorStrategy(self.problem)
        return Qubo(calculator_strategy)

    def create_backend(self) -> BackendStrategy:
        return AerBackendStrategy()

    def create_mixer(self) -> MixerStrategy:
        return RXGateMixerStrategy()

    def create_phase(self) -> PhaseStrategy:
        couplings = self.problem.get_edges()
        return ZGatePhaseStrategy(couplings)

    def create_initial(self) -> InitialStrategy:
        return HGateInitialStrategy()

    def create_precision(self):
        return 1
