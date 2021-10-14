import numpy as np

from VehicleRouting.framework.factory.QaoaFactory import QaoaFactory
from VehicleRouting.framework.qaoa.BackendStrategy import BackendStrategy
from VehicleRouting.framework.qaoa.CircuitStrategy import InitialStrategy, PhaseStrategy, MixerStrategy, \
    MeasurementStrategy
from VehicleRouting.framework.qaoa.CostStategy import CostStrategy
from VehicleRouting.standard.concretization.QuboImpl import QuboImpl
from VehicleRouting.standard.problems.MaxCutProblem import MaxCutProblem
from VehicleRouting.standard.problems.VehicleRoutingProblem import VehicleRoutingProblem
from VehicleRouting.standard.qaoa.BackendStrategy import AerBackendStrategy, NoisyBackendStrategy, \
    StateVectorBackendStrategy

from VehicleRouting.standard.concretization.QuboCalculatorStrategy import MaxCutQuboCalculatorStrategy, \
    VertexOrderingQuboCalculatorStrategy, EdgeQuboCalculatorStrategy
from VehicleRouting.standard.qaoa.CostStrategy import AverageCostStrategy, CVaRCostStrategy, MinCostStrategy, \
    ProjectionStrategy
from VehicleRouting.standard.qaoa.InitialStrategy import HGateInitialStrategy, OneHotSingleInitialStrategy, \
    CustomInitialStrategy, AdjacentSwapInitialStrategy, Adjacent2SwapInitialStrategy, PartialSwapInitialStrategy
from VehicleRouting.standard.qaoa.MeasurementStrategy import NullMeasurementStrategy, TomographyMeasurementStrategy
from VehicleRouting.standard.qaoa.MixerStrategy import RXGateMixerStrategy, AdjacentSwapMixerStrategy, NullMixerStrategy

from VehicleRouting.standard.qaoa.PhaseStrategy import MaxCutSimpleZGatePhaseStrategy, WeightedZGatePhaseStrategy, \
    NullPhaseStrategy, FromQuboZGatePhaseStrategy


class ExactMaxCutQaoaFactory(QaoaFactory):

    def __init__(self, problem: MaxCutProblem):
        self.problem = problem

    def create_qubo(self) -> QuboImpl:
        calculator_strategy = MaxCutQuboCalculatorStrategy(self.problem)
        return QuboImpl(calculator_strategy)

    def create_backend(self) -> BackendStrategy:
        return StateVectorBackendStrategy()

    def create_mixer(self) -> MixerStrategy:
        return RXGateMixerStrategy()

    def create_phase(self) -> PhaseStrategy:
        qubo = self.create_qubo()
        return FromQuboZGatePhaseStrategy(qubo)

    def create_measurement(self) -> MeasurementStrategy:
        return NullMeasurementStrategy()

    def create_initial(self) -> InitialStrategy:
        return HGateInitialStrategy()

    def create_cost(self) -> CostStrategy:
        return AverageCostStrategy()

    def create_precision(self):
        return 1


class NoisyMaxCutQaoaFactory(QaoaFactory):

    def create_measurement(self) -> MeasurementStrategy:
        return TomographyMeasurementStrategy()

    def __init__(self, problem: MaxCutProblem):
        self.problem = problem

    def create_qubo(self) -> QuboImpl:
        calculator_strategy = MaxCutQuboCalculatorStrategy(self.problem)
        return QuboImpl(calculator_strategy)

    def create_backend(self) -> BackendStrategy:
        return NoisyBackendStrategy()

    def create_mixer(self) -> MixerStrategy:
        return RXGateMixerStrategy()

    def create_phase(self) -> PhaseStrategy:
        qubo = self.create_qubo()
        return FromQuboZGatePhaseStrategy(qubo)

    def create_initial(self) -> InitialStrategy:
        return HGateInitialStrategy()

    def create_cost(self) -> CostStrategy:
        return CVaRCostStrategy(0.6)

    def create_precision(self):
        return 1


class CustomVertexOrderingVehicleRoutingQaoaFactory(QaoaFactory):

    def __init__(self, problem: VehicleRoutingProblem):
        self.problem = problem

    def create_measurement(self) -> MeasurementStrategy:
        return NullMeasurementStrategy()

    def create_qubo(self) -> QuboImpl:
        calculator_strategy = VertexOrderingQuboCalculatorStrategy(self.problem)
        return QuboImpl(calculator_strategy)

    def create_backend(self) -> BackendStrategy:
        return StateVectorBackendStrategy()

    def create_mixer(self) -> MixerStrategy:
        return AdjacentSwapMixerStrategy()

    def create_phase(self) -> PhaseStrategy:
        qubo = self.create_qubo()
        return FromQuboZGatePhaseStrategy(qubo)

    def create_initial(self) -> InitialStrategy:
        return PartialSwapInitialStrategy()

    def create_cost(self) -> CostStrategy:
        return CVaRCostStrategy(0.5)

    def create_precision(self):
        return 1


class SimpleVertexOrderingVehicleRoutingQaoaFactory(QaoaFactory):

    def __init__(self, problem: VehicleRoutingProblem):
        self.problem = problem

    def create_measurement(self) -> MeasurementStrategy:
        return NullMeasurementStrategy()

    def create_qubo(self) -> QuboImpl:
        calculator_strategy = VertexOrderingQuboCalculatorStrategy(self.problem)
        return QuboImpl(calculator_strategy)

    def create_backend(self) -> BackendStrategy:
        return StateVectorBackendStrategy()

    def create_mixer(self) -> MixerStrategy:
        return RXGateMixerStrategy()

    def create_phase(self) -> PhaseStrategy:
        qubo = self.create_qubo()
        return FromQuboZGatePhaseStrategy(qubo)

    def create_initial(self) -> InitialStrategy:
        return HGateInitialStrategy()

    def create_cost(self) -> CostStrategy:
        return CVaRCostStrategy(1)

    def create_precision(self):
        return 1


class InitializerMixerVehicleRoutingQaoaFactory(QaoaFactory):

    def __init__(self, problem: VehicleRoutingProblem):
        self.problem = problem

    def create_measurement(self) -> MeasurementStrategy:
        return NullMeasurementStrategy()

    def create_qubo(self) -> QuboImpl:
        calculator_strategy = VertexOrderingQuboCalculatorStrategy(self.problem)
        return QuboImpl(calculator_strategy)

    def create_backend(self) -> BackendStrategy:
        return StateVectorBackendStrategy()

    def create_mixer(self) -> MixerStrategy:
        return NullMixerStrategy()

    def create_phase(self) -> PhaseStrategy:
        return NullPhaseStrategy()

    def create_initial(self) -> InitialStrategy:
        return PartialSwapInitialStrategy()

    def create_cost(self) -> CostStrategy:
        return CVaRCostStrategy(1)

    def create_precision(self):
        return 1


class EdgeVehicleRoutingQaoaFactory(QaoaFactory):

    def __init__(self, problem: VehicleRoutingProblem):
        self.problem = problem

    def create_measurement(self) -> MeasurementStrategy:
        return NullMeasurementStrategy()

    def create_qubo(self) -> QuboImpl:
        calculator_strategy = EdgeQuboCalculatorStrategy(self.problem)
        return QuboImpl(calculator_strategy)

    def create_backend(self) -> BackendStrategy:
        return StateVectorBackendStrategy()

    def create_mixer(self) -> MixerStrategy:
        return RXGateMixerStrategy()

    def create_phase(self) -> PhaseStrategy:
        qubo = self.create_qubo()
        return FromQuboZGatePhaseStrategy(qubo)

    def create_initial(self) -> InitialStrategy:
        return HGateInitialStrategy()

    def create_cost(self) -> CostStrategy:
        # ProjectionStrategy("100110")
        return CVaRCostStrategy(1)

    def create_precision(self):
        return 1
