from matplotlib import pyplot as plt
from qiskit import QuantumCircuit
from qiskit.algorithms import QAOA
from qiskit.algorithms.optimizers import COBYLA
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram
from qiskit_optimization.algorithms import MinimumEigenOptimizer

from VehicleRouting.framework.strategy.CircuitPlotter import CircuitPlotter
from VehicleRouting.framework.strategy.Problem import Problem
from VehicleRouting.standard.ProblemPlotter import ProblemPlotter
from VehicleRouting.standard.Qubo import Qubo
from VehicleRouting.standard.factories.ProblemFactories import TwoVertexProblemFactory
from VehicleRouting.standard.strategies.CircuitPlotterStrategy import MPLCircuitPlotStrategy
from VehicleRouting.standard.strategies.QuboCalculatorStrategy import EdgeQuboCalculatorStrategy
from qiskit.circuit import Parameter

problem_factory = TwoVertexProblemFactory()
problem = Problem(problem_factory)
plotter = ProblemPlotter(problem)
plotter.plot_problem()

quboCalculatorStrategy = EdgeQuboCalculatorStrategy(problem)
qubo = Qubo(quboCalculatorStrategy)
quadratic_program = qubo.get_quadratic_program()
print(quadratic_program)
precision = 2
classical_optimization_method = COBYLA()
# backend = StatevectorSimulator(precision='single')
backend = QasmSimulator()


qc=QuantumCircuit(qubo.get_number_of_variables())
print(qc)

qc.barrier()
beta = Parameter("$\\beta$")
for i in range(qubo.get_number_of_variables()):
    qc.rx(2*beta,i)
qc.barrier()


mixer  = qc
qaoa = QAOA(optimizer=classical_optimization_method, reps=precision, quantum_instance=backend, mixer=mixer)
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
