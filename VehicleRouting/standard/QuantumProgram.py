from qiskit import Aer
from qiskit.algorithms import QAOA, NumPyMinimumEigensolver
from qiskit.algorithms.optimizers import COBYLA
from qiskit_optimization.algorithms import MinimumEigenOptimizer

from VehicleRouting.standard.CircuitPlotter import MPLCircuitPlotStrategy, CircuitPlotter
from VehicleRouting.standard.Problem import Problem
from VehicleRouting.standard.ProblemPlotter import ProblemPlotter
from VehicleRouting.standard.QUBO import QUBO
from VehicleRouting.standard.factories.Experiment1ProblemFactory import Experiment1ProblemFactory


class QuantumProgram:
    def __init__(self, problem):
        self.problem = problem

    def run(self):
        qubo = QUBO(self.problem)
        quadratic_program = qubo.get_quadratic_program()

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

        result = qaoa_result.min_eigen_solver_result
        optimal_circuit = qaoa.get_optimal_circuit()
        circuit_plot_strategy = MPLCircuitPlotStrategy()
        circuit_plotter = CircuitPlotter(circuit_plot_strategy)
        circuit_plotter.plot_circuit(optimal_circuit)
        print(result)
