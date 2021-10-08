from VehicleRouting.framework.qaoa.CircuitStrategy import PhaseStrategy


class NullPhaseStrategy(PhaseStrategy):

    def __init__(self):
        pass

    def set_up_phase_circuit(self, gamma, quantum_circuit):
        pass


class ZGatePhaseStrategy(PhaseStrategy):

    def __init__(self, couplings):
        self.couplings = couplings

    def set_up_phase_circuit(self, gamma, quantum_circuit):
        quantum_circuit.barrier()
        for (i, j) in self.couplings:
            quantum_circuit.rzz(2 * gamma, i, j)


class WeightedZGatePhaseStrategy(PhaseStrategy):

    def __init__(self, couplings):
        self.couplings = couplings

    def set_up_phase_circuit(self, gamma, quantum_circuit):
        quantum_circuit.barrier()
        for (i, j, weight) in self.couplings:
            quantum_circuit.rzz(2 * weight * gamma, i, j)

class FromQuadraticPhaseStrategy(PhaseStrategy):

    def __init__(self, couplings):
        self.couplings = couplings

    def set_up_phase_circuit(self, gamma, quantum_circuit):
        quantum_circuit.barrier()
        for (i, j) in self.couplings:
            quantum_circuit.rzz(2 * gamma, i, j)