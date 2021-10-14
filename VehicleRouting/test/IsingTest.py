import unittest
from test import support

import numpy as np

from VehicleRouting.standard.concretization.QuboCalculatorStrategy import MaxCutQuboCalculatorStrategy, \
    EdgeQuboCalculatorStrategy, VertexOrderingQuboCalculatorStrategy
from VehicleRouting.standard.concretization.QuboImpl import QuboImpl
from VehicleRouting.standard.factories.MaxCutFactories import TwoConnectedMaxCutFactory
from VehicleRouting.standard.factories.VehicleRoutingProblemFactories import Experiment1VehicleRoutingProblemFactory
from VehicleRouting.standard.problems.MaxCutProblem import MaxCutProblem
from VehicleRouting.standard.problems.VehicleRoutingProblem import VehicleRoutingProblem


class MyTestCase1(unittest.TestCase):

    def setUp(self):
        self.allowed_error = 0.0001

    def test_ising_qubo_cost_equal_max_cut(self):
        self.rand_num = np.random.randint(10)
        self.bit_array = np.random.randint(2, size=self.rand_num)
        factory = TwoConnectedMaxCutFactory(self.rand_num)
        problem = MaxCutProblem(factory)
        calculator_strategy = MaxCutQuboCalculatorStrategy(problem)
        qubo = QuboImpl(calculator_strategy)
        qubo_cost = qubo.calculate_qubo_cost(self.bit_array)
        ising_cost = qubo.calculate_ising_cost(self.bit_array)
        assert abs(qubo_cost - ising_cost) <= self.allowed_error

    def test_ising_qubo_cost_equal_edge(self):
        self.bit_array = np.random.randint(2, size=12)
        factory = Experiment1VehicleRoutingProblemFactory()
        problem = VehicleRoutingProblem(factory)
        calculator_strategy = EdgeQuboCalculatorStrategy(problem)
        qubo = QuboImpl(calculator_strategy)
        qubo_cost = qubo.calculate_qubo_cost(self.bit_array)
        ising_cost = qubo.calculate_ising_cost(self.bit_array)
        assert abs(qubo_cost - ising_cost) <= self.allowed_error

    def test_ising_qubo_cost_equal_vertex(self):
        self.bit_array = np.random.randint(2, size=16)
        factory = Experiment1VehicleRoutingProblemFactory()
        problem = VehicleRoutingProblem(factory)
        calculator_strategy = VertexOrderingQuboCalculatorStrategy(problem)
        qubo = QuboImpl(calculator_strategy)
        qubo_cost = qubo.calculate_qubo_cost(self.bit_array)
        ising_cost = qubo.calculate_ising_cost(self.bit_array)
        assert abs(qubo_cost - ising_cost) <= self.allowed_error
