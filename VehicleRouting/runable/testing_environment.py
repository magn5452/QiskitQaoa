from matplotlib import pyplot as plt
from qiskit.algorithms import NumPyMinimumEigensolver, QAOA
from qiskit.algorithms.optimizers import COBYLA
from qiskit.providers.aer import Aer
from qiskit_optimization.algorithms import MinimumEigenOptimizer

from VehicleRouting.standard.Problem import Problem
from VehicleRouting.standard.ProblemPlotter import ProblemPlotter
from VehicleRouting.standard.QUBO import QUBO
from VehicleRouting.standard.factories.Experiment1ProblemFactory import Experiment1ProblemFactory

problem_factory = Experiment1ProblemFactory()
problem = Problem(problem_factory)
plotter = ProblemPlotter(problem)
plotter.plot_problem()

qubo = QUBO(problem)
quadratic_program = qubo.get_quadratic_program()
#print(quadratic_program.export_as_lp_string())

exact_minimum_eigen_solver = NumPyMinimumEigensolver()
optimizer = MinimumEigenOptimizer(exact_minimum_eigen_solver)

exact_result = optimizer.solve(quadratic_program)
print(exact_result)

precision = 2
optimization_method = COBYLA()
simulator = Aer.get_backend('qasm_simulator')
qaoa = QAOA(optimizer=optimization_method, reps=precision, quantum_instance=simulator)

optimizer = MinimumEigenOptimizer(qaoa)
qaoa_result = optimizer.solve(quadratic_program)
print(qaoa_result)

result = qaoa_result.min_eigen_solver_result
optimal_parameters = result.optimal_point

print(result)
print(result.eigenstate)
print(result.eigenvalue)
print(result.optimizer_time)
plt.show()
