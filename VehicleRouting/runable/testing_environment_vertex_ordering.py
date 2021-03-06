import numpy as np
from matplotlib import pyplot as plt
from qiskit.visualization import plot_histogram

from VehicleRouting.standard.concretization.QaoaMinimizer import QaoaMinimizerImpl
from VehicleRouting.standard.factories.QaoaFactory import CustomVertexOrderingVehicleRoutingQaoaFactory, EdgeVehicleRoutingQaoaFactory, \
    SimpleVertexOrderingVehicleRoutingQaoaFactory
from VehicleRouting.standard.factories.VehicleRoutingProblemFactories import Experiment1VehicleRoutingProblemFactory, \
    TwoVertexVehicleRoutingProblemFactory, AsymmetricThreeVertexVehicleRoutingProblemFactory
from VehicleRouting.standard.plotter.BarPlotter import BarPlotter
from VehicleRouting.standard.plotter.GraphPlotter import GraphPlotter
from VehicleRouting.standard.concretization.CircuitPlotter import MPLCircuitPlotter
from VehicleRouting.standard.concretization.Qaoa import Qaoa
from VehicleRouting.standard.plotter.SurfacePlotter import SurfacePlotter
from VehicleRouting.standard.problems.VehicleRoutingProblem import VehicleRoutingProblem

#Problem
problem_factory = AsymmetricThreeVertexVehicleRoutingProblemFactory()

problem = VehicleRoutingProblem(problem_factory)

plotter = GraphPlotter(problem)
plotter.plot_problem()

# Qaoa
qaoa_factory = CustomVertexOrderingVehicleRoutingQaoaFactory(problem)
qubo = qaoa_factory.create_qubo()
constant, linear, quadratic = qubo.get_qubo_terms()
print(constant,linear, quadratic)
qaoa = Qaoa(qaoa_factory)

# Minimizer
qaoaMinimizer = QaoaMinimizerImpl(qaoa)
result, optimal_parameters, optimal_circuit = qaoaMinimizer.minimize()
print(optimal_parameters)
circuit_plotter = MPLCircuitPlotter()
circuit_plotter.plot(optimal_circuit)

#Simulate
result, counts, expectation = qaoa.simulate(optimal_parameters)

# Bar Plot
barPlotter = BarPlotter()
barPlotter.plot(counts)


#Find Surface Plot
plotter = SurfacePlotter()
plotter.plot(qaoa.get_execute_circuit())
plt.show()
