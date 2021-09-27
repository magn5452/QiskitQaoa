from matplotlib import pyplot as plt
from qiskit.visualization import plot_histogram

from VehicleRouting.framework.qaoa.CircuitPlotter import CircuitPlotter
from VehicleRouting.standard.factories.MaxCutFactories import TwoConnectedMaxCutFactory, \
    FiveVertexMaxCutFactory
from VehicleRouting.standard.factories.QaoaFactory import MaxCutQaoaFactory, NoisyMaxCutQaoaFactory, \
    VertexOrderingVehicleRoutingQaoaFactory, EdgeVehicleRoutingQaoaFactory
from VehicleRouting.standard.factories.VehicleRoutingProblemFactories import Experiment1VehicleRoutingProblemFactory
from VehicleRouting.standard.problems.GraphPlotter import GraphPlotter
from VehicleRouting.standard.problems.MaxCutProblem import MaxCutProblem
from VehicleRouting.standard.concretization.CircuitPlotter import MPLCircuitPlotter
from VehicleRouting.standard.concretization.Qaoa import Qaoa
from VehicleRouting.standard.problems.VehicleRoutingProblem import VehicleRoutingProblem

factory = Experiment1VehicleRoutingProblemFactory()
problem = VehicleRoutingProblem(factory)
plotter = GraphPlotter(problem)
plotter.plot_problem()

qaoa_factory = EdgeVehicleRoutingQaoaFactory(problem)
qaoa = Qaoa(qaoa_factory)

result = qaoa.minimize()
circuit = qaoa.get_optimal_circuit()

circuit_plotter = MPLCircuitPlotter()
circuit_plotter.plot(circuit)

counts = qaoa.simulate()
plot_histogram(counts)

plt.show()
