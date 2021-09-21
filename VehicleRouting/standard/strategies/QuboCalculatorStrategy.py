from abc import abstractmethod, ABC

import numpy as np
from qiskit_optimization import QuadraticProgram

from VehicleRouting.framework.strategy.Problem import Problem


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
    def get_quadratic_program(self):
        pass

    @abstractmethod
    def get_number_of_variables(self):
        pass


class VertexOrderingQuboCalculatorStrategy(QuboCalculatorStrategy):

    def __init__(self, problem: Problem):
        self.problem = problem

    def get_number_of_variables(self):
        return self.problem.get_number_of_vertices()**2

    def get_quadratic_program(self):
        quadratic_program = QuadraticProgram('Vehicle Routing Problem')

        for vertex in self.problem.get_vertices():
            for index in range(self.problem.get_number_of_vertices()):
                quadratic_program.binary_var("x_" + str(vertex) + str(index))

        constant = self.calculate_constant()
        linear = self.calculate_linear()
        quadratic = self.calculate_quadratic()

        quadratic_program.minimize(constant=constant, linear=linear, quadratic=quadratic)

        return quadratic_program

    def calculate_constant(self):
        return 0

    def calculate_linear(self):
        return np.zeros(self.get_number_of_variables())

    def calculate_quadratic(self):
        return np.ones((self.get_number_of_variables(),self.get_number_of_variables()))


class EdgeQuboCalculatorStrategy(QuboCalculatorStrategy):

    def __init__(self, problem: Problem):
        self.problem = problem

    def get_number_of_variables(self):
        return self.problem.get_number_of_edges()

    def get_quadratic_program(self):
        quadratic_program = QuadraticProgram('Vehicle Routing Problem')

        for (source, target) in self.problem.get_edges():
            quadratic_program.binary_var("x_" + str(source) + str(target))

        constant = self.calculate_constant()
        linear = self.calculate_linear()
        quadratic = self.calculate_quadratic()

        quadratic_program.minimize(constant=constant, linear=linear, quadratic=quadratic)

        return quadratic_program

    def calculate_constant(self):
        return 2 * self.problem.get_penalty_factor() * (
                (self.problem.get_number_of_vertices() - 1) + self.problem.get_number_of_vehicles() ** 2)

    def calculate_linear(self):
        g_A = self.problem.get_weights()
        g_B = -2 * self.problem.get_penalty_factor() * (self.problem.get_number_of_vehicles() - 1) * (
                self.calculate_z_S(0) + self.calculate_z_T(0))
        g_C = -4 * self.problem.get_penalty_factor() * (np.ones(self.problem.get_number_of_edges()))
        return g_A + g_B + g_C

    def calculate_quadratic(self):
        z_T_matrix = self.calculate_z_T_matrix()
        z_S_matrix = self.calculate_z_S_matrix()
        Q = self.problem.get_penalty_factor() * (
                z_T_matrix.dot(np.transpose(z_T_matrix)) + z_S_matrix.dot(np.transpose(z_S_matrix)))
        return Q

    def calculate_z_S(self, i):
        z_S = np.zeros(self.problem.get_number_of_edges())
        for index, (source, target) in enumerate(self.problem.get_edges()):
            source_is_i = source == i
            if source_is_i:
                z_S[index] = 1
        return z_S

    def calculate_z_S_matrix(self):
        z_S_matrix = np.zeros((self.problem.get_number_of_edges(), self.problem.get_number_of_vertices()))
        for i in range(0, self.problem.get_number_of_vertices()):
            z_S_matrix[:, i] = self.calculate_z_S(i)
        return z_S_matrix

    def calculate_z_T(self, i):
        z_T = np.zeros(self.problem.get_number_of_edges())
        for index, (source, target) in enumerate(self.problem.get_edges()):
            target_is_i = target == i
            if target_is_i:
                z_T[index] = 1
        return z_T

    def calculate_z_T_matrix(self):
        z_T_matrix = np.zeros((self.problem.get_number_of_edges(), self.problem.get_number_of_vertices()))
        for i in range(0, self.problem.get_number_of_vertices()):
            z_T_matrix[:, i] = self.calculate_z_T(i)
        return z_T_matrix

    def calculate_z_T_matrix(self):
        z_T_matrix = np.zeros((self.problem.get_number_of_edges(), self.problem.get_number_of_vertices()))
        for i in range(0, self.problem.get_number_of_vertices()):
            z_T_matrix[:, i] = self.calculate_z_T(i)
        return z_T_matrix
