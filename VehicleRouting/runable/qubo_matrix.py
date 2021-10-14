import numpy as np
from matplotlib import pyplot as plt
from qiskit.visualization import plot_histogram
import json

from VehicleRouting.standard.concretization.QaoaMinimizer import QaoaMinimizerImpl
from VehicleRouting.standard.factories.QaoaFactory import CustomVertexOrderingVehicleRoutingQaoaFactory, \
    EdgeVehicleRoutingQaoaFactory, \
    SimpleVertexOrderingVehicleRoutingQaoaFactory
from VehicleRouting.standard.factories.VehicleRoutingProblemFactories import Experiment1VehicleRoutingProblemFactory, \
    TwoVertexVehicleRoutingProblemFactory, AsymmetricThreeVertexVehicleRoutingProblemFactory, \
    Experiment2VehicleRoutingProblemFactory
from VehicleRouting.standard.plotter.BarPlotter import BarPlotter
from VehicleRouting.standard.plotter.GraphPlotter import GraphPlotter
from VehicleRouting.standard.concretization.CircuitPlotter import MPLCircuitPlotter
from VehicleRouting.standard.concretization.Qaoa import Qaoa
from VehicleRouting.standard.plotter.SurfacePlotter import SurfacePlotter
from VehicleRouting.standard.problems.VehicleRoutingProblem import VehicleRoutingProblem

# Problem
problem_factory = Experiment2VehicleRoutingProblemFactory()
problem = VehicleRoutingProblem(problem_factory)
plotter = GraphPlotter(problem)
plotter.plot_problem()

# Qaoa
qaoa_factory = CustomVertexOrderingVehicleRoutingQaoaFactory(problem)
qubo = qaoa_factory.create_qubo()
constant, linear, quadratic = qubo.get_qubo_terms()

dictionary_data = {"constant": getattr(constant, "tolist", lambda: constant)(),
              "linear": getattr(linear, "tolist", lambda: linear)(),
              "quadratic": getattr(quadratic, "tolist", lambda: quadratic)()}


file = open("../files/qubo_terms_5_vertex_ordering.json", "w")
json.dump(dictionary_data, file)
file.close()

file = open("../files/qubo_terms_5_vertex_ordering.json", "r")
output = file.read()
print(output)


