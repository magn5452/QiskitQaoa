from abc import ABC

import numpy as np
from qiskit_optimization import QuadraticProgram

from VehicleRouting.framework.interfaces.QuboCalculator import QuboCalculatorStrategy


class QuboIsingConverter():

    def __init__(self, qubo_calculator_strategy: QuboCalculatorStrategy):
        self.qubo_calculator_strategy = qubo_calculator_strategy
        self.qubo_constant = self.qubo_calculator_strategy.calculate_constant()
        self.qubo_linear = self.qubo_calculator_strategy.calculate_linear()
        self.qubo_quadratic = self.qubo_calculator_strategy.calculate_quadratic()

    def calculate_quadratic(self):
        """
        Gets the Ising quadratic from the Qubo model

        """
        return self.qubo_quadratic/4

    def qubo_array_to_ising_array(self, qubo_array):
        return (qubo_array+1)/2

    def calculate_linear(self):
        """
        Gets the Ising linear term from the Qubo model

        """
        return self.qubo_linear/2+(self.qubo_quadratic.sum(axis=0)+self.qubo_quadratic.sum(axis=1))/4

    def calculate_constant(self):
        return self.qubo_constant+np.sum(self.qubo_linear)/2+np.sum(self.qubo_quadratic)/4

    def get_num_variables(self):
        return self.qubo_calculator_strategy.get_num_variables()
