from abc import abstractmethod, ABC


class CircuitPlotStrategy(ABC):
    @abstractmethod
    def plot(self, circuit):
        pass


class MPLCircuitPlotStrategy(CircuitPlotStrategy):
    def __init__(self):
        pass

    def plot(self, circuit):
        circuit.draw(output="mpl")


class PrintCircuitPlotStrategy(CircuitPlotStrategy):
    def __init__(self):
        pass

    def plot(self, circuit):
        print(circuit)