from qiskit_optimization import QuadraticProgram

from VehicleRouting.framework.interfaces.Qubo import Qubo
from VehicleRouting.standard.concretization.QuboCalculatorStrategy import QuboCalculatorStrategy


class QuboImpl(Qubo):

    def __init__(self, calculator_strategy: QuboCalculatorStrategy):
        self.calculator_strategy = calculator_strategy

    def get_number_of_variables(self):
        quadratic_program = self.calculator_strategy.get_number_of_variables()
        return quadratic_program

    def get_quadratic_program(self):
        quadratic_program = QuadraticProgram('Vehicle Routing Problem')
        self.calculator_strategy.encoding(quadratic_program)
        constant = self.calculator_strategy.calculate_constant()
        linear = self.calculator_strategy.calculate_linear()
        quadratic = self.calculator_strategy.calculate_quadratic()
        quadratic_program.minimize(constant=constant, linear=linear, quadratic=quadratic)
        return quadratic_program

    def calculate_cost(self, x):
        quadratic_term = x @ self.calculator_strategy.calculate_quadratic() @ x
        linear_term = self.calculator_strategy.calculate_linear() @ x
        constant_term = self.calculator_strategy.calculate_constant()
        return quadratic_term + linear_term + constant_term

    def get_qubo_calculator_strategy(self):
        return self.calculator_strategy
