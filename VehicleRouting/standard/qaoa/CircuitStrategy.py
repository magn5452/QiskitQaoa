import numpy as np
from qiskit import QuantumCircuit

from VehicleRouting.framework.qaoa.CircuitStrategy import MixerStrategy, InitialStrategy, PhaseStrategy


class HGateInitialStrategy(InitialStrategy):

    def __init__(self):
        pass

    def set_up_initial_state_circuit(self, quantum_circuit: QuantumCircuit, num_qubits):
        quantum_circuit.barrier()
        for index_qubit in range(0, num_qubits):
            quantum_circuit.h(index_qubit)


class XGateMixerStrategy(MixerStrategy):

    def __init__(self):
        pass

    def set_up_mixer_circuit(self, theta, index_repetition, quantum_circuit, number_of_qubits, precision):
        quantum_circuit.barrier()
        beta = theta[:precision]
        for index_qubit in range(0, number_of_qubits):
            quantum_circuit.rx(2 * beta[index_repetition], index_qubit)


class ZGatePhaseStrategy(PhaseStrategy):

    def __init__(self, couplings):
        self.couplings = couplings

    def set_up_phase_circuit(self, theta, index_repetition, quantum_circuit, number_of_qubits, precision):
        quantum_circuit.barrier()
        gamma = theta[precision:]
        for (i, j) in self.couplings:
            quantum_circuit.rzz(2 * gamma[index_repetition], i, j)
