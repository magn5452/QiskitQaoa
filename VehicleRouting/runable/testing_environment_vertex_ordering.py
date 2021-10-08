import numpy as np
from matplotlib import pyplot as plt
from qiskit.visualization import plot_histogram

from VehicleRouting.standard.concretization.QaoaMinimizer import QaoaMinimizerImpl
from VehicleRouting.standard.factories.QaoaFactory import VertexOrderingVehicleRoutingQaoaFactory, \
    InitializerTestMixerVehicleRoutingQaoaFactory, EdgeVehicleRoutingQaoaFactory
from VehicleRouting.standard.factories.VehicleRoutingProblemFactories import Experiment1VehicleRoutingProblemFactory, \
    TwoVertexVehicleRoutingProblemFactory, ThreeVertexVehicleRoutingProblemFactory
from VehicleRouting.standard.plotter.GraphPlotter import GraphPlotter
from VehicleRouting.standard.concretization.CircuitPlotter import MPLCircuitPlotter
from VehicleRouting.standard.concretization.Qaoa import Qaoa
from VehicleRouting.standard.plotter.SurfacePlotter import SurfacePlotter
from VehicleRouting.standard.problems.VehicleRoutingProblem import VehicleRoutingProblem

#Problem
factory = ThreeVertexVehicleRoutingProblemFactory()
problem = VehicleRoutingProblem(factory)
plotter = GraphPlotter(problem)
plotter.plot_problem()

# Qaoa
qaoa_factory = EdgeVehicleRoutingQaoaFactory(problem)
qaoa = Qaoa(qaoa_factory)

# Minimizer
qaoaMinimizer = QaoaMinimizerImpl(qaoa)
result, optimal_parameters, optimal_circuit = qaoaMinimizer.minimize()

circuit_plotter = MPLCircuitPlotter()
circuit_plotter.plot(optimal_circuit)

#Simulate
result, counts, expectation = qaoa.simulate(optimal_parameters)
print(result)
print(counts)
plot_histogram(counts)

#Find Surface Plot
plotter = SurfacePlotter()
plotter.plot(qaoa.get_execute_circuit())
plt.show()
