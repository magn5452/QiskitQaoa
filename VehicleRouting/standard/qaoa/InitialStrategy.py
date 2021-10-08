import numpy as np
from qiskit import QuantumCircuit

from VehicleRouting.framework.qaoa.CircuitStrategy import InitialStrategy
from VehicleRouting.standard.qaoa.MixerStrategy import PartialSwapMixerStrategy, AdjacentSwapMixerStrategy


class NullInitialStrategy(InitialStrategy):

    def __init__(self):
        pass

    def set_up_initial_state_circuit(self, quantum_circuit: QuantumCircuit):
        pass


class HGateInitialStrategy(InitialStrategy):

    def __init__(self):
        pass

    def set_up_initial_state_circuit(self, quantum_circuit: QuantumCircuit):
        quantum_circuit.barrier()
        for index_qubit in range(0, quantum_circuit.num_qubits):
            quantum_circuit.h(index_qubit)


class OneHotSingleInitialStrategy(InitialStrategy):

    def __init__(self):
        pass

    def set_up_initial_state_circuit(self, quantum_circuit: QuantumCircuit):
        quantum_circuit.barrier()
        num_vertices = int(np.round(np.sqrt(quantum_circuit.num_qubits)))
        for index_qubit in range(0, quantum_circuit.num_qubits):
            if np.mod(index_qubit, num_vertices + 1) == 0:
                quantum_circuit.x(index_qubit)


class CustomInitialStrategy(InitialStrategy):

    def __init__(self):
        pass

    def set_up_initial_state_circuit(self, quantum_circuit: QuantumCircuit):
        initializer = OneHotSingleInitialStrategy()
        initializer.set_up_initial_state_circuit(quantum_circuit)
        mixer = AdjacentSwapMixerStrategy()
        mixer.set_up_mixer_circuit(np.pi / 4, quantum_circuit)

