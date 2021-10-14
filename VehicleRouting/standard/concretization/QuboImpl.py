from qiskit_optimization import QuadraticProgram

from VehicleRouting.framework.interfaces.Qubo import Qubo
from VehicleRouting.standard.concretization.QuboCalculatorStrategy import QuboCalculatorStrategy
from VehicleRouting.standard.concretization.QuboIsingConverter import QuboIsingConverter


class QuboImpl(Qubo):

    def __init__(self, qubo_calculator_strategy: QuboCalculatorStrategy):
        self.qubo_calculator_strategy = qubo_calculator_strategy
        self.qubo_ising_converter = QuboIsingConverter(self.qubo_calculator_strategy)

    def get_num_variables(self):
        quadratic_program = self.qubo_calculator_strategy.get_num_variables()
        return quadratic_program

    def get_quadratic_program(self):
        quadratic_program = QuadraticProgram('Quadratic Program')
        self.qubo_calculator_strategy.encoding(quadratic_program)
        constant, linear, quadratic = self.get_qubo_terms()
        quadratic_program.minimize(constant=constant, linear=linear, quadratic=quadratic)
        return quadratic_program

    def get_qubo_terms(self):
        constant = self.qubo_calculator_strategy.calculate_constant()
        linear = self.qubo_calculator_strategy.calculate_linear()
        quadratic = self.qubo_calculator_strategy.calculate_quadratic()
        return constant, linear, quadratic

    def get_ising_terms(self):
        constant = self.qubo_ising_converter.calculate_constant()
        linear = self.qubo_ising_converter.calculate_linear()
        quadratic = self.qubo_ising_converter.calculate_quadratic()
        return constant, linear, quadratic

    def calculate_ising_cost(self, bitstring):
        bitstring = 2 * bitstring - 1
        constant, linear, quadratic = self.get_ising_terms()
        quadratic_cost = bitstring @ quadratic @ bitstring
        linear_cost = linear @ bitstring
        constant_cost = constant
        cost = quadratic_cost + linear_cost + constant_cost
        #print("Ising: ",constant_cost, linear_cost, quadratic_cost,cost)
        return cost

    def calculate_qubo_cost(self, bitstring):
        constant, linear, quadratic = self.get_qubo_terms()
        quadratic_cost = bitstring @ quadratic @ bitstring
        linear_cost = linear @ bitstring
        constant_cost = constant
        cost = quadratic_cost + linear_cost + constant_cost
        #print("Qubo: ",constant_cost, linear_cost, quadratic_cost,cost)
        return cost

    def get_qubo_calculator_strategy(self):
        return self.qubo_calculator_strategy
