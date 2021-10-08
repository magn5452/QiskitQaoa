from abc import abstractmethod, ABC

from VehicleRouting.framework.qaoa.CircuitPlotter import CircuitPlotter


class MPLCircuitPlotter(CircuitPlotter):
    def __init__(self):
        pass

    def plot(self, circuit):
        circuit.draw(output="mpl")

