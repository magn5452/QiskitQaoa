from abc import ABC, abstractmethod

from qiskit import QuantumCircuit


class InitialStrategy(ABC):
    @abstractmethod
    def set_up_initial_state_circuit(self, quantum_circuit: QuantumCircuit, num_qubits: int):
        pass


class PhaseStrategy(ABC):
    @abstractmethod
    def set_up_phase_circuit(self, theta, index_repetition: int, quantum_circuit, num_qubits: int, precision: int):
        pass


class MixerStrategy(ABC):
    @abstractmethod
    def set_up_mixer_circuit(self, theta, index_repetition: int, quantum_circuit, num_qubits: int, precision: int):
        pass
