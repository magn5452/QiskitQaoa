import numpy as np
from qiskit import QuantumCircuit
from qiskit.extensions import HamiltonianGate
from qiskit_nature.operators.second_quantization import SpinOp
from VehicleRouting.framework.qaoa.CircuitStrategy import MixerStrategy, InitialStrategy, PhaseStrategy, \
    MeasurementStrategy
from VehicleRouting.standard.problems.VehicleRoutingProblem import VehicleRoutingProblem


class HGateInitialStrategy(InitialStrategy):

    def __init__(self):
        pass

    def set_up_initial_state_circuit(self, quantum_circuit: QuantumCircuit, num_qubits):
        quantum_circuit.barrier()
        for index_qubit in range(0, num_qubits):
            quantum_circuit.h(index_qubit)


class OneHotSingleInitialStrategy(InitialStrategy):

    def __init__(self, n):
        self.n = n

    def set_up_initial_state_circuit(self, quantum_circuit: QuantumCircuit, num_qubits):
        quantum_circuit.barrier()
        for index_qubit in range(0, num_qubits):

            if np.mod(index_qubit, self.n + 1) == 0:
                quantum_circuit.x(index_qubit)



class RXGateMixerStrategy(MixerStrategy):

    def __init__(self):
        pass

    def set_up_mixer_circuit(self, theta, index_repetition, quantum_circuit, number_of_qubits, precision):
        quantum_circuit.barrier()
        beta = theta[:precision]
        for index_qubit in range(0, number_of_qubits):
            quantum_circuit.rx(2 * beta[index_repetition], index_qubit)


class CustomMixerStrategy(MixerStrategy):

    def __init__(self, problem: VehicleRoutingProblem):
        self.problem = problem

    def set_up_mixer_circuit(self, theta, index_repetition, quantum_circuit, num_qubits, precision):
        quantum_circuit.barrier()
        beta = theta[:precision]
        hamiltonian = SpinOp([("++--", 1), ("--++", 1)])
        unitary_gate = HamiltonianGate(hamiltonian.to_matrix(), beta[index_repetition], label="UGate")

        for u in self.problem.get_vertices():
            for v in self.problem.get_vertices():
                for i in range(self.problem.get_number_of_vertices()):
                    if u < v:
                        quantum_circuit.append(unitary_gate,
                                               [self.map(u, i), self.map(v, i + 1),
                                                self.map(u, i + 1), self.map(v, i)])

    def map(self, u, i):
        return self.problem.get_number_of_vertices() * np.mod(u,self.problem.get_number_of_vertices()) + np.mod(i, self.problem.get_number_of_vertices())


class ZGatePhaseStrategy(PhaseStrategy):

    def __init__(self, couplings):
        self.couplings = couplings

    def set_up_phase_circuit(self, theta, index_repetition, quantum_circuit, number_of_qubits, precision):
        quantum_circuit.barrier()
        gamma = theta[precision:]
        for (i, j) in self.couplings:
            quantum_circuit.rzz(2 * gamma[index_repetition], i, j)


class WeightedZGatePhaseStrategy(PhaseStrategy):

    def __init__(self, couplings):
        self.couplings = couplings

    def set_up_phase_circuit(self, theta, index_repetition, quantum_circuit, number_of_qubits, precision):
        quantum_circuit.barrier()
        gamma = theta[precision:]
        for (i, j, weight) in self.couplings:
            quantum_circuit.rzz(2 * weight * gamma[index_repetition], i, j)


class AllMeasurementStrategy(MeasurementStrategy):
    def __init__(self):
        pass

    def set_up_measurement_circuit(self, quantum_circuit):
        quantum_circuit.measure_all()


class NoMeasurementStrategy(MeasurementStrategy):
    def __init__(self):
        pass

    def set_up_measurement_circuit(self, quantum_circuit):
        pass
