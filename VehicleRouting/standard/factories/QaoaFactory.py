import numpy as np

from VehicleRouting.framework.factory.QaoaFactory import QaoaFactory
from VehicleRouting.framework.qaoa.BackendStrategy import BackendStrategy
from VehicleRouting.framework.qaoa.CircuitStrategy import InitialStrategy, PhaseStrategy, MixerStrategy
from VehicleRouting.standard.Qubo import Qubo
from VehicleRouting.standard.problems.MaxCutProblem import MaxCutProblem
from VehicleRouting.standard.problems.VehicleRoutingProblem import VehicleRoutingProblem
from VehicleRouting.standard.qaoa.BackendStrategy import AerBackendStrategy, NoisyBackendStrategy
from VehicleRouting.standard.qaoa.CircuitStrategy import XGateMixerStrategy, HGateInitialStrategy, \
    ZGatePhaseStrategy
from VehicleRouting.standard.concretization.QuboCalculatorStrategy import MaxCutQuboCalculatorStrategy, \
    VertexOrderingQuboCalculatorStrategy, EdgeQuboCalculatorStrategy


class MaxCutQaoaFactory(QaoaFactory):

    def __init__(self, problem: MaxCutProblem):
        self.problem = problem

    def create_qubo(self) -> Qubo:
        calculator_strategy = MaxCutQuboCalculatorStrategy(self.problem)
        return Qubo(calculator_strategy)

    def create_backend(self) -> BackendStrategy:
        return AerBackendStrategy()

    def create_mixer(self) -> MixerStrategy:
        return XGateMixerStrategy()

    def create_phase(self) -> PhaseStrategy:
        couplings = self.problem.get_edges()
        return ZGatePhaseStrategy(couplings)

    def create_initial(self) -> InitialStrategy:
        return HGateInitialStrategy()

    def create_initial_parameter(self):
        return np.ones(2 * self.create_precision())

    def create_precision(self):
        return 1


class NoisyMaxCutQaoaFactory(QaoaFactory):

    def __init__(self, problem: MaxCutProblem):
        self.problem = problem

    def create_qubo(self) -> Qubo:
        calculator_strategy = MaxCutQuboCalculatorStrategy(self.problem)
        return Qubo(calculator_strategy)

    def create_backend(self) -> BackendStrategy:
        return NoisyBackendStrategy()

    def create_mixer(self) -> MixerStrategy:
        return XGateMixerStrategy()

    def create_phase(self) -> PhaseStrategy:
        couplings = self.problem.get_edges()
        return ZGatePhaseStrategy(couplings)

    def create_initial(self) -> InitialStrategy:
        return HGateInitialStrategy()

    def create_initial_parameter(self):
        return np.ones(2 * self.create_precision())

    def create_precision(self):
        return 1


class VertexOrderingVehicleRoutingQaoaFactory(QaoaFactory):

    def __init__(self, problem: VehicleRoutingProblem):
        self.problem = problem

    def create_qubo(self) -> Qubo:
        calculator_strategy = VertexOrderingQuboCalculatorStrategy(self.problem)
        return Qubo(calculator_strategy)

    def create_backend(self) -> BackendStrategy:
        return AerBackendStrategy()

    def create_mixer(self) -> MixerStrategy:
        return XGateMixerStrategy()

    def create_phase(self) -> PhaseStrategy:
        couplings = self.problem.get_edges()
        return ZGatePhaseStrategy(couplings)

    def create_initial(self) -> InitialStrategy:
        return HGateInitialStrategy()

    def create_initial_parameter(self):
        return np.ones(2 * self.create_precision())

    def create_precision(self):
        return 1


class EdgeVehicleRoutingQaoaFactory(QaoaFactory):

    def __init__(self, problem: VehicleRoutingProblem):
        self.problem = problem

    def create_qubo(self) -> Qubo:
        calculator_strategy = EdgeQuboCalculatorStrategy(self.problem)
        return Qubo(calculator_strategy)

    def create_backend(self) -> BackendStrategy:
        return AerBackendStrategy()

    def create_mixer(self) -> MixerStrategy:
        return XGateMixerStrategy()

    def create_phase(self) -> PhaseStrategy:
        couplings = [(1,2),[1,3],[0,1]]
        return ZGatePhaseStrategy(couplings)

    def create_initial(self) -> InitialStrategy:
        return HGateInitialStrategy()

    def create_initial_parameter(self):
        return np.ones(2 * self.create_precision())

    def create_precision(self):
        return 1

