from qiskit import QuantumCircuit
from qiskit import Aer
import networkx as nx
import numpy as np


def maxcut_cost(bitstring, graph):
    """
    Given a bitstring as a solution, this function returns minus
    the weighted number of edges shared between the two partitions
    of the graph.

    Args:
        bitstring: str
           solution bitstring

        graph: networkx graph

    Returns:
        cost: float
             Objective
    """
    cost = 0
    for i, j in graph.edges():
        if bitstring[i] != bitstring[j]:
            edge_weight = graph.edges[i, j]['weight']
            cost -= edge_weight
    return cost


def compute_expectation(counts, graph):
    """
    Computes expectation value based on measurement results

    Args:
        counts: dict
                key as bitstring, val as count

        graph: networkx graph

    Returns:
        avg: float
             expectation value
    """
    sum_cost = 0
    sum_count = 0
    for bitstring, count in counts.items():
        cost = maxcut_cost(bitstring, graph)
        sum_cost += cost * count
        sum_count += count
    expectation_value = sum_cost / sum_count
    return expectation_value


def create_qaoa_circuit(graph, theta):
    """
    Creates qaoa circuit

    Args:
        graph: networkx graph
        theta: qaoa parameters
    """

    number_of_nodes = len(graph.nodes())
    number_of_qubits = number_of_nodes
    precision = len(theta) // 2  # number of alternating unitaries p
    quantum_circuit = QuantumCircuit(number_of_qubits)

    beta = theta[:precision]
    gamma = theta[precision:]

    # initial_state
    for index_qubit in range(0, number_of_qubits):
        quantum_circuit.h(index_qubit)

    quantum_circuit.barrier()

    for index_repetition in range(0, precision):

        # problem unitary
        for pair in list(graph.edges()):
            quantum_circuit.rzz(2 * gamma[index_repetition], pair[0], pair[1])

        quantum_circuit.barrier()

        # mixer unitary
        for index_qubit in range(0, number_of_qubits):
            quantum_circuit.rx(2 * beta[index_repetition], index_qubit)

    # measure
    quantum_circuit.measure_all()

    return quantum_circuit


# Finally we write a function that executes the circuit on the chosen backend
def get_execute_circuit(graph, shots=512):
    """
    Runs parametrized circuit

    Args:
        graph: networkx graph
    """

    backend = Aer.get_backend('qasm_simulator')
    backend.shots = shots

    def execute_circuit(theta):
        qc = create_qaoa_circuit(graph, theta)
        counts = backend.run(qc, seed_simulator=10,
                             nshots=2 ^ 12).result().get_counts()

        return compute_expectation(counts, graph)

    return execute_circuit
