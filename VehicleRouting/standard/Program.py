from VehicleRouting.standard.concretization.QuboImpl import QuboImpl
from VehicleRouting.framework.interfaces.MinimumEigenSolver import MinimumEigenSolver


class Program:
    def __init__(self, qubo: QuboImpl, minimum_eigen_solver: MinimumEigenSolver):
        self.qubo = qubo
        self.minimum_eigen_solver = minimum_eigen_solver
        self.result = None

    def run(self):
        quadratic_program = self.qubo.get_quadratic_program()
        print(quadratic_program)
        self.result = self.minimum_eigen_solver.solve(quadratic_program)

    def get_qubo(self):
        return self.qubo

    def get_minimum_eigensolver(self):
        return self.minimum_eigen_solver

    def get_result(self):
        return self.result;


