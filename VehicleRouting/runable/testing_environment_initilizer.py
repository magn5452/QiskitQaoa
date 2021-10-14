import time
import numpy as np
from matplotlib import pyplot as plt
from qiskit.visualization import plot_histogram

from VehicleRouting.standard.concretization.QaoaMinimizer import QaoaMinimizerImpl
from VehicleRouting.standard.factories.QaoaFactory import EdgeVehicleRoutingQaoaFactory, \
    InitializerMixerVehicleRoutingQaoaFactory
from VehicleRouting.standard.factories.VehicleRoutingProblemFactories import Experiment1VehicleRoutingProblemFactory, \
    TwoVertexVehicleRoutingProblemFactory, AsymmetricThreeVertexVehicleRoutingProblemFactory, \
    TwoConnectedVehicleRoutingProblemFactory
from VehicleRouting.standard.plotter.BarPlotter import BarPlotter
from VehicleRouting.standard.plotter.GraphPlotter import GraphPlotter
from VehicleRouting.standard.concretization.CircuitPlotter import MPLCircuitPlotter
from VehicleRouting.standard.concretization.Qaoa import Qaoa
from VehicleRouting.standard.plotter.SurfacePlotter import SurfacePlotter
from VehicleRouting.standard.problems.VehicleRoutingProblem import VehicleRoutingProblem

#Problem
problem_factory = TwoConnectedVehicleRoutingProblemFactory(3)
problem = VehicleRoutingProblem(problem_factory)
plotter = GraphPlotter(problem)
plotter.plot_problem()

# Qaoa
qaoa_factory = InitializerMixerVehicleRoutingQaoaFactory(problem)
qaoa = Qaoa(qaoa_factory)

precision = qaoa.get_precision()
theta = np.ones(2*precision)
circuit = qaoa.set_up_qaoa_circuit(theta)
circuit_plotter = MPLCircuitPlotter()
circuit_plotter.plot(circuit)

#Simulate

result, counts, expectation = qaoa.simulate(theta)

# Bar Plot
barPlotter = BarPlotter()
barPlotter.plot(counts)

plt.show()
