import math

import numpy as np
from qiskit.extensions import HamiltonianGate
from qiskit_nature.operators.second_quantization import SpinOp

from VehicleRouting.framework.qaoa.CircuitStrategy import MixerStrategy, PhaseStrategy
from VehicleRouting.standard.problems.VehicleRoutingProblem import VehicleRoutingProblem


class NullMixerStrategy(MixerStrategy):

    def __init__(self):
        pass

    def set_up_mixer_circuit(self, beta, quantum_circuit):
        pass


class RXGateMixerStrategy(MixerStrategy):

    def __init__(self):
        pass

    def set_up_mixer_circuit(self, beta, quantum_circuit):
        quantum_circuit.barrier()
        for index_qubit in range(0, quantum_circuit.num_qubits):
            quantum_circuit.rx(2 * beta, index_qubit)


class PartialSwapMixerStrategy(MixerStrategy):

    def __init__(self):
        pass

    def set_up_mixer_circuit(self, beta, quantum_circuit):
        quantum_circuit.barrier()
        hamiltonian = SpinOp([("++--", 1), ("--++", 1)])
        unitary_gate = HamiltonianGate(hamiltonian.to_matrix(), beta, label="(" + str(round(beta, 1)) + ")")
        num_vertices = int(np.round(np.sqrt(quantum_circuit.num_qubits)))

        for city_u in range(num_vertices):
            for city_v in range(num_vertices):
                for position_i in range(num_vertices):
                    for position_j in range(num_vertices):
                        if city_u != city_v and position_i != position_j:
                            quantum_circuit.append(unitary_gate, [self.map(city_u, position_i, num_vertices),
                                                                  self.map(city_v, position_j,
                                                                           num_vertices),
                                                                  self.map(city_u, position_j,
                                                                           num_vertices),
                                                                  self.map(city_v, position_i, num_vertices)])

    def map(self, city: int, position: int, num_vertices: int):
        mapping = num_vertices * np.mod(city, num_vertices) + np.mod(position, num_vertices)
        return mapping


class AdjacentSwapMixerStrategy(MixerStrategy):

    def __init__(self):
        pass

    def set_up_mixer_circuit(self, beta, quantum_circuit):
        quantum_circuit.barrier()
        num_vertices = int(np.round(np.sqrt(quantum_circuit.num_qubits)))
        hamiltonian = self.make_adjacent_swap_mixer_hamiltonian(num_vertices)
        unitary_gate = HamiltonianGate(hamiltonian.to_matrix(), beta, label="(" + str(round(beta, 1)) + ")")
        quantum_circuit.append(unitary_gate, range(quantum_circuit.num_qubits))

    def make_adjacent_swap_mixer_hamiltonian(self, num_vertices) -> SpinOp:
        opr_list = []
        for city_u in range(num_vertices):
            for city_v in range(num_vertices):
                for position_i in range(num_vertices):
                    for position_j in range(num_vertices):
                        if city_u < city_v and position_i < position_j:
                            string, string_hermitian = self.make_string_partial_mixer(city_u, city_v, position_i, position_j, num_vertices)
                            opr_list.append((string, 1))
                            opr_list.append((string_hermitian, 1))

        return SpinOp(opr_list)

    def make_string_partial_mixer(self, city_u, city_v, position_i, position_j, num_vertices):

        string_list = []
        string_hermitian_list = []
        for i in range(num_vertices ** 2):
            string_list.append("I")
            string_hermitian_list.append("I")

        string_list[self.map(city_u, position_i, num_vertices)] = "+"
        string_list[self.map(city_v, position_j, num_vertices)] = "+"
        string_list[self.map(city_u, position_j, num_vertices)] = "-"
        string_list[self.map(city_v, position_i, num_vertices)] = "-"

        string_hermitian_list[self.map(city_u, position_i, num_vertices)] = "-"
        string_hermitian_list[self.map(city_v, position_j, num_vertices)] = "-"
        string_hermitian_list[self.map(city_u, position_j, num_vertices)] = "+"
        string_hermitian_list[self.map(city_v, position_i, num_vertices)] = "+"

        new_string = "".join(string_list)
        new_string_hermitian = "".join(string_hermitian_list)
        return new_string, new_string_hermitian

    def map(self, city: int, position: int, num_vertices: int):
        mapping = num_vertices * np.mod(city, num_vertices) + np.mod(position, num_vertices)
        return mapping
