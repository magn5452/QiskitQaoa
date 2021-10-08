import numpy as np
from qiskit_optimization import QuadraticProgram

from VehicleRouting.framework.problem.GraphProblem import GraphProblem
from VehicleRouting.framework.interfaces.QuboCalculator import QuboCalculatorStrategy
from VehicleRouting.standard.problems.MaxCutProblem import MaxCutProblem
from VehicleRouting.standard.problems.VehicleRoutingProblem import VehicleRoutingProblem


class VertexOrderingQuboCalculatorStrategy(QuboCalculatorStrategy):

    def __init__(self, problem: VehicleRoutingProblem):
        self.problem = problem

    def get_num_variables(self):
        return (self.problem.get_number_of_vertices()) ** 2

    def encoding(self, quadratic_program: QuadraticProgram):
        for vertex in self.problem.get_vertices():
            for index in range(self.problem.get_number_of_vertices()):
                quadratic_program.binary_var("x_" + str(vertex) + "," + str(index))

    def calculate_constant(self):
        return 2 * self.problem.get_penalty_factor() * self.problem.get_number_of_vertices()

    def calculate_linear(self):
        np.zeros(self.get_num_variables())
        return - 4 * self.problem.get_penalty_factor() * (np.ones(self.get_num_variables()))

    def calculate_quadratic(self):
        Q = self.get_weight_matrix()
        z_I_matrix = self.calculate_z_I_matrix()
        z_P_matrix = self.calculate_z_P_matrix()
        Q += self.problem.get_penalty_factor() * (
                z_I_matrix.dot(np.transpose(z_I_matrix)) + z_P_matrix.dot(np.transpose(z_P_matrix)))
        return Q

    def get_ordering(self, result):
        ordering = np.zeros(self.problem.get_number_of_vertices())
        for i in range(self.problem.get_number_of_vertices()):
            for p in range(self.problem.get_number_of_vertices()):
                if result[i * self.problem.number_of_vertices + p] == 1:
                    ordering[p] = i

        depot_index = np.where(ordering == self.problem.depot)[0]
        return np.roll(ordering, -depot_index)

    def get_weight_matrix(self):
        weight_matrix = np.zeros((self.get_num_variables(), self.get_num_variables()))

        number_vertices = self.problem.get_number_of_vertices()

        for i in range(number_vertices):
            for pi in range(number_vertices):
                for j in range(number_vertices):
                    for pj in range(number_vertices):
                        if pj == np.mod(pi + 1, number_vertices) and i != j:
                            weight_matrix[i * number_vertices + pi][j * number_vertices + pj] = self.problem.get_weight(
                                i, j)
                        else:
                            weight_matrix[i * number_vertices + pi][j * number_vertices + pj] = 0

        return weight_matrix

    def calculate_z_I(self, index):
        z_I = np.zeros(self.get_num_variables())
        for i in range(self.problem.get_number_of_vertices()):
            for p in range(self.problem.get_number_of_vertices()):
                if i == index:
                    z_I[i * self.problem.get_number_of_vertices() + p] = 1
        return z_I

    def calculate_z_I_matrix(self):
        z_I_matrix = np.zeros((self.get_num_variables(), self.problem.get_number_of_vertices()))
        for i in range(0, self.problem.get_number_of_vertices()):
            z_I_matrix[:, i] = self.calculate_z_I(i)
        return z_I_matrix

    def calculate_z_P(self, index):
        z_I = np.zeros(self.get_num_variables())
        for i in range(self.problem.get_number_of_vertices()):
            for p in range(self.problem.get_number_of_vertices()):
                if p == index:
                    z_I[i * self.problem.get_number_of_vertices() + p] = 1
        return z_I

    def calculate_z_P_matrix(self):
        z_P_matrix = np.zeros((self.get_num_variables(), self.problem.get_number_of_vertices()))
        for p in range(0, self.problem.get_number_of_vertices()):
            z_P_matrix[:, p] = self.calculate_z_P(p)
        return z_P_matrix


class EdgeQuboCalculatorStrategy(QuboCalculatorStrategy):

    def __init__(self, problem: VehicleRoutingProblem):
        self.problem = problem

    def get_num_variables(self):
        return self.problem.get_number_of_edges()

    def encoding(self, quadratic_program: QuadraticProgram):
        for (source, target) in self.problem.get_edges():
            quadratic_program.binary_var("x_" + str(source) + str(target))

    def calculate_constant(self):
        return 2 * self.problem.get_penalty_factor() * (
                (self.problem.get_number_of_vertices() - 1) + self.problem.get_number_of_vehicles() ** 2)

    def calculate_linear(self):
        g_A = self.problem.get_weight_vector()
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
        z_S = np.zeros(self.get_num_variables())
        for index, (source, target) in enumerate(self.problem.get_edges()):
            source_is_i = source == i
            if source_is_i:
                z_S[index] = 1
        return z_S

    def calculate_z_S_matrix(self):
        z_S_matrix = np.zeros((self.get_num_variables(), self.problem.get_number_of_vertices()))
        for i in range(0, self.problem.get_number_of_vertices()):
            z_S_matrix[:, i] = self.calculate_z_S(i)
        return z_S_matrix

    def calculate_z_T(self, i):
        z_T = np.zeros(self.get_num_variables())
        for index, (source, target) in enumerate(self.problem.get_edges()):
            target_is_i = target == i
            if target_is_i:
                z_T[index] = 1
        return z_T

    def calculate_z_T_matrix(self):
        z_T_matrix = np.zeros((self.get_num_variables(), self.problem.get_number_of_vertices()))
        for i in range(0, self.problem.get_number_of_vertices()):
            z_T_matrix[:, i] = self.calculate_z_T(i)
        return z_T_matrix

    def calculate_z_T_matrix(self):
        z_T_matrix = np.zeros((self.problem.get_number_of_edges(), self.problem.get_number_of_vertices()))
        for i in range(0, self.problem.get_number_of_vertices()):
            z_T_matrix[:, i] = self.calculate_z_T(i)
        return z_T_matrix


class StubQuboCalculatorStrategy(QuboCalculatorStrategy):

    def __init__(self, problem: GraphProblem):
        self.problem = problem

    def get_num_variables(self):
        return self.problem.get_number_of_vertices()

    def encoding(self, quadratic_program: QuadraticProgram):
        for vertex in self.problem.get_vertices():
            quadratic_program.binary_var("x_" + str(vertex))

    def calculate_constant(self):
        return 1

    def calculate_linear(self):
        return np.ones(self.get_num_variables())

    def calculate_quadratic(self):
        return np.ones(self.get_num_variables(), self.get_num_variables())


class MaxCutQuboCalculatorStrategy(QuboCalculatorStrategy):
    """
    A MaxCut qubo calculator strategy bas on the following web page. I have used the first equation on the site.

    https://qiskit.org/documentation/optimization/tutorials/06_examples_max_cut_and_tsp.html
    """

    def __init__(self, problem: MaxCutProblem):
        self.problem = problem

    def get_edges(self):
        return self.problem.get_edges()

    def get_num_variables(self):
        return self.problem.get_number_of_vertices()

    def encoding(self, quadratic_program: QuadraticProgram):
        for vertex in self.problem.get_vertices():
            quadratic_program.binary_var("x_" + str(vertex))

    def calculate_constant(self):
        return 0

    def calculate_linear(self):
        linear = np.zeros(self.get_num_variables())
        for i in range(self.get_num_variables()):
            #linear += self.problem.get_weight(i, i) Add weight of nodes
            for j in range(self.get_num_variables()):
                if i != j:
                    linear[i] += self.problem.get_weight(i, j)
        return -linear

    def calculate_quadratic(self):
        quadratic = np.zeros((self.get_num_variables(), self.get_num_variables()))
        for i in range(self.get_num_variables()):
            for j in range(self.get_num_variables()):
                if i != j:
                    quadratic[i, j] = self.problem.get_weight(i, j)
        return quadratic
