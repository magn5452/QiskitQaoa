from VehicleRouting.standard.strategies.CircuitPlotterStrategy import CircuitPlotStrategy


class CircuitPlotter:
    def __init__(self, circuit_plot_strategy: CircuitPlotStrategy):
        self.circuit_plot_strategy = circuit_plot_strategy

    def plot_circuit(self, circuit):
        self.circuit_plot_strategy.plot(circuit)
