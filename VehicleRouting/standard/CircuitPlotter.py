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


class CircuitPlotter:
    def __init__(self, circuit_plot_strategy: CircuitPlotStrategy):
        self.circuit_plot_strategy = circuit_plot_strategy

    def plot_circuit(self, circuit):
        self.circuit_plot_strategy.plot(circuit)
