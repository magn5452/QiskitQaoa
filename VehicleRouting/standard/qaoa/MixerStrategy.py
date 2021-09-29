import math

import numpy as np
from qiskit.extensions import HamiltonianGate
from qiskit_nature.operators.second_quantization import SpinOp

from VehicleRouting.framework.qaoa.CircuitStrategy import MixerStrategy, PhaseStrategy
from VehicleRouting.standard.problems.VehicleRoutingProblem import VehicleRoutingProblem


class RXGateMixerStrategy(MixerStrategy):

    def __init__(self):
        pass

    def set_up_mixer_circuit(self, beta, quantum_circuit):
        quantum_circuit.barrier()
        for index_qubit in range(0, quantum_circuit.num_qubits):
            quantum_circuit.rx(2 * beta, index_qubit)


class CustomMixerStrategy(MixerStrategy):

    def __init__(self):
        pass

    def set_up_mixer_circuit(self, beta, quantum_circuit):
        quantum_circuit.barrier()
        hamiltonian = SpinOp([("++--", 1), ("--++", 1)])
        unitary_gate = HamiltonianGate(hamiltonian.to_matrix(), beta, label="U")
        num_vertices = int(np.round(np.sqrt(quantum_circuit.num_qubits)))

        for city_u in range(num_vertices):
            for city_v in range(num_vertices):
                for position_i in range(num_vertices):
                    for position_j in range(num_vertices):
                        if city_u < city_v and position_i < position_j:
                            quantum_circuit.append(unitary_gate, [self.map(city_u, position_i, num_vertices),
                                                                  self.map(city_v, position_i + position_j, num_vertices),
                                                                  self.map(city_u, position_i + position_j, num_vertices),
                                                                  self.map(city_v, position_i, num_vertices)])

    def map(self, city: int, position: int, num_vertices: int):
        mapping = num_vertices * np.mod(city, num_vertices) + np.mod(position, num_vertices)
        return mapping


