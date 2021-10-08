import unittest
from test import support

import numpy as np

from VehicleRouting.standard.concretization.QuboCalculatorStrategy import MaxCutQuboCalculatorStrategy
from VehicleRouting.standard.concretization.QuboImpl import QuboImpl
from VehicleRouting.standard.factories.MaxCutFactories import TwoConnectedMaxCutFactory
from VehicleRouting.standard.problems.MaxCutProblem import MaxCutProblem


class MyTestCase1(unittest.TestCase):

    def setUp(self):
        rand_num = np.random.randint(10)
        factory = TwoConnectedMaxCutFactory(rand_num)
        problem = MaxCutProblem(factory)
        calculator_strategy = MaxCutQuboCalculatorStrategy(problem)
        self.bit_array = np.random.randint(2, size=rand_num)
        self.qubo = QuboImpl(calculator_strategy)

    def test_ising_qubo_cost_equal(self):
        qubo_cost = self.qubo.calculate_qubo_cost(self.bit_array)
        ising_cost = self.qubo.calculate_ising_cost(self.bit_array)
        assert qubo_cost == ising_cost

