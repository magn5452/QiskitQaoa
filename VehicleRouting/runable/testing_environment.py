from matplotlib import pyplot as plt
from qiskit.visualization import plot_histogram

from VehicleRouting.standard.concretization.CircuitPlotter import MPLCircuitPlotter
from VehicleRouting.standard.concretization.MinimumEigenSolverStrategy import QAOAMinimumEigenSolver
from VehicleRouting.standard.factories.MaxCutFactories import TwoConnectedMaxCutFactory
from VehicleRouting.standard.factories.VehicleRoutingProblemFactories import AsymmetricThreeVertexVehicleRoutingProblemFactory
from VehicleRouting.standard.problems.VehicleRoutingProblem import VehicleRoutingProblem
from VehicleRouting.standard.plotter.GraphPlotter import GraphPlotter
from VehicleRouting.standard.Program import Program
from VehicleRouting.standard.concretization.QuboImpl import QuboImpl
from VehicleRouting.standard.factories.QaoaMinimumEigenSolverFactories import StandardQaoaMinimumEigenSolverFactory
from VehicleRouting.standard.concretization.QuboCalculatorStrategy import VertexOrderingQuboCalculatorStrategy, \
    EdgeQuboCalculatorStrategy

problem_factory = AsymmetricThreeVertexVehicleRoutingProblemFactory()
problem = VehicleRoutingProblem(problem_factory)
plotter = GraphPlotter(problem)
plotter.plot_problem()

quboCalculatorStrategy = EdgeQuboCalculatorStrategy(problem)
qubo = QuboImpl(quboCalculatorStrategy)
quadratic_program = qubo.get_quadratic_program()

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

circuit_plotter = MPLCircuitPlotter()
circuit_plotter.plot(optimal_circuit)

print(optimal_cost)
print(optimal_vector)

plot_histogram(optimal_vector, color='blue')

plt.show()
