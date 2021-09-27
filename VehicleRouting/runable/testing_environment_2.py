from qiskit.algorithms import NumPyMinimumEigensolver
from qiskit_optimization.algorithms import MinimumEigenOptimizer

from VehicleRouting.standard.problems.VehicleRoutingProblem import VehicleRoutingProblem
from VehicleRouting.standard.Qubo import Qubo
from VehicleRouting.standard.concretization.GraphStrategy import TwoVertexProblemStrategy
from VehicleRouting.standard.concretization.QuboCalculatorStrategy import EdgeQuboCalculatorStrategy

problem_factory = TwoVertexProblemStrategy()
problem = VehicleRoutingProblem(problem_factory)
quboCalculatorStrategy = EdgeQuboCalculatorStrategy(problem)
qubo = Qubo(quboCalculatorStrategy)

quadratic_program =qubo.get_quadratic_program()
print(quadratic_program)
exact_minimum_eigen_solver = NumPyMinimumEigensolver()
optimizer = MinimumEigenOptimizer(exact_minimum_eigen_solver)
result = optimizer.solve(quadratic_program)
print(result)
print(result.raw_results)
print(result.min_eigen_solver_result)


