from abc import ABC, abstractmethod

from qiskit_optimization import QuadraticProgram


class Qubo(ABC):
    @abstractmethod
    def get_num_variables(self):
        pass

    @abstractmethod
    def get_quadratic_program(self):
        pass

    @abstractmethod
    def calculate_qubo_cost(self):
        pass

    @abstractmethod
    def get_qubo_calculator_strategy(self):
        pass
