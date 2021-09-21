from VehicleRouting.standard.strategies.QuboCalculatorStrategy import QuboCalculatorStrategy


class Qubo:

    def __init__(self, calculator_strategy: QuboCalculatorStrategy):
        self.calculator_strategy = calculator_strategy

    def get_number_of_variables(self):
        quadratic_program = self.calculator_strategy.get_number_of_variables()
        return quadratic_program

    def get_quadratic_program(self):
        quadratic_program = self.calculator_strategy.get_quadratic_program()
        return quadratic_program

    def calculate_cost(self, x):
        quadratic_term = x @ self.calculator_strategy.calculate_quadratic() @ x
        linear_term = self.calculator_strategy.calculate_linear() @ x
        constant_term = self.calculator_strategy.calculate_constant()
        return quadratic_term + linear_term + constant_term
