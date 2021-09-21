from matplotlib import pyplot as plt
from qiskit.visualization import plot_histogram

from VehicleRouting.framework.strategy.CircuitPlotter import CircuitPlotter
from VehicleRouting.framework.strategy.Problem import Problem
from VehicleRouting.standard.ProblemPlotter import ProblemPlotter
from VehicleRouting.standard.Program import Program
from VehicleRouting.standard.Qubo import Qubo
from VehicleRouting.standard.factories.ProblemFactories import TwoVertexProblemFactory
from VehicleRouting.standard.factories.QaoaMinimumEigenSolverFactories import StandardQaoaMinimumEigenSolverFactory
from VehicleRouting.standard.strategies.CircuitPlotterStrategy import MPLCircuitPlotStrategy
from VehicleRouting.standard.strategies.MinimumEigenSolverStrategy import QAOAMinimumEigenSolver
from VehicleRouting.standard.strategies.QuboCalculatorStrategy import VertexOrderingQuboCalculatorStrategy

problem_factory = TwoVertexProblemFactory()
problem = Problem(problem_factory)
plotter = ProblemPlotter(problem)
plotter.plot_problem()

quboCalculatorStrategy = VertexOrderingQuboCalculatorStrategy(problem)
qubo = Qubo(quboCalculatorStrategy)

quadratic_program = qubo.get_quadratic_program()
print(quadratic_program)

qaoa_factory = StandardQaoaMinimumEigenSolverFactory()
solver = QAOAMinimumEigenSolver(qaoa_factory)
program = Program(qubo, solver)
program.run()
result = program.get_result()

print(result)
print(result.min_eigen_solver_result)

optimal_circuit = solver.get_optimal_circuit()
optimal_vector = solver.get_optimal_vector()
optimal_cost = solver.get_optimal_cost()

circuit_plotter = CircuitPlotter(MPLCircuitPlotStrategy())
circuit_plotter.plot_circuit(optimal_circuit)

print(optimal_cost)
print(optimal_vector)

plot_histogram(optimal_vector, color='blue')

plt.show()
