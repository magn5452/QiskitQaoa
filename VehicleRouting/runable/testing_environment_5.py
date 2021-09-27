from matplotlib import pyplot as plt
from qiskit.algorithms import NumPyMinimumEigensolver, QAOA
from qiskit.algorithms.optimizers import COBYLA
from qiskit.providers.aer import Aer
from qiskit.visualization import plot_histogram
from qiskit_optimization.algorithms import MinimumEigenOptimizer

from VehicleRouting.framework.qaoa.CircuitPlotter import CircuitPlotter
from VehicleRouting.standard.problems.MaxCutProblem import MaxCutProblem
from VehicleRouting.standard.problems.GraphPlotter import GraphPlotter
from VehicleRouting.standard.Qubo import Qubo
from VehicleRouting.standard.concretization.GraphStrategy import SimpleVertexProblemStrategy
from VehicleRouting.standard.concretization.CircuitPlotter import MPLCircuitPlotStrategy
from VehicleRouting.standard.concretization.QuboCalculatorStrategy import MaxCutQuboCalculatorStrategy

problem_factory = SimpleVertexProblemStrategy()
problem = MaxCutProblem(problem_factory)
plotter = GraphPlotter(problem)
plotter.plot_problem()

maxCutQuboCalculatorStrategy = MaxCutQuboCalculatorStrategy(problem)
qubo = Qubo(maxCutQuboCalculatorStrategy)
print(maxCutQuboCalculatorStrategy.calculate_linear())
print(maxCutQuboCalculatorStrategy.calculate_quadratic())

quadratic_program = qubo.get_quadratic_program()
print(quadratic_program)

exact_minimum_eigen_solver = NumPyMinimumEigensolver()
optimizer = MinimumEigenOptimizer(exact_minimum_eigen_solver)
result = optimizer.solve(quadratic_program)
print(result)
print(result.x)

precision = 4
classical_optimization_method = COBYLA()
# backend = StatevectorSimulator(precision='single')
backend = Aer.get_backend('aer_simulator')
backend.shots = 2 ^ 12

qaoa = QAOA(optimizer=classical_optimization_method, reps=precision, quantum_instance=backend)
optimizer = MinimumEigenOptimizer(qaoa)
result = optimizer.solve(quadratic_program)

print(result)
print(result.min_eigen_solver_result)

optimal_circuit = qaoa.get_optimal_circuit()

circuit_plotter = CircuitPlotter(MPLCircuitPlotStrategy())
circuit_plotter.plot_circuit(optimal_circuit)
optimal_vector = qaoa.get_optimal_vector()

plot_histogram(optimal_vector, color='blue')
plt.show()
