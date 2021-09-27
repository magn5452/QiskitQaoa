from abc import abstractmethod, ABC

from VehicleRouting.framework.qaoa.CircuitPlotter import CircuitPlotter


class MPLCircuitPlotter(CircuitPlotter):
    def plot(self, circuit):
        pass

    def __init__(self):
        pass

    def plot(self, circuit):
        circuit.draw(output="mpl")


class PrintCircuitPlotter(CircuitPlotter):
    def __init__(self):
        pass

    def plot(self, circuit):
        print(circuit)
