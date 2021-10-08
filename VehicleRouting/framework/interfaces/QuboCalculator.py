from abc import ABC, abstractmethod

from qiskit_optimization import QuadraticProgram


class QuboCalculatorStrategy(ABC):
    @abstractmethod
    def calculate_quadratic(self):
        pass

    @abstractmethod
    def calculate_linear(self):
        pass

    @abstractmethod
    def calculate_constant(self):
        pass

    @abstractmethod
    def encoding(self, quadratic_program: QuadraticProgram):
        pass

    @abstractmethod
    def get_num_variables(self):
        pass