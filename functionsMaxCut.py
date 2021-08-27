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
    sum_obj = 0
    sum_count = 0
    for bitstring, count in counts.items():
        cost = maxcut_cost(bitstring, graph)
        sum_obj += cost * count
        sum_count += count
    expectation_value = sum_obj / sum_count
    return expectation_value


# We will also bring the different circuit components that
# build the qaoa circuit under a single function
def create_qaoa_circuit(graph, theta) -> object:
    """
    Creates a parametrized qaoa circuit

    Args:
        graph: networkx graph
        theta: list
               unitary parameters

    Returns:
        qc: qiskit circuit
    """
    number_of_nodes = len(graph.nodes())
    nqubits = number_of_nodes
    p = len(theta) // 2  # number of alternating unitaries
    qc = QuantumCircuit(nqubits)

    beta = theta[:p]
    gamma = theta[p:]

    # initial_state
    for i in range(0, nqubits):
        qc.h(i)

    qc.barrier()

    for irep in range(0, p):

        # problem unitary
        for pair in list(graph.edges()):
            qc.rzz(2 * gamma[irep], pair[0], pair[1])
        qc.barrier()

        # mixer unitary
        for i in range(0, nqubits):
            qc.rx(2 * beta[irep], i)

    qc.measure_all()

    return qc


# Finally we write a function that executes the circuit on the chosen backend
def get_execute_circuit(graph, shots=512):
    """
    Runs parametrized circuit

    Args:
        graph: networkx graph
        p: int,
           Number of repetitions of unitaries
    """

    backend = Aer.get_backend('qasm_simulator')
    backend.shots = shots

    def execute_circuit(theta):
        qc = create_qaoa_circuit(graph, theta)
        counts = backend.run(qc, seed_simulator=10,
                             nshots=2 ^ 12).result().get_counts()

        return compute_expectation(counts, graph)

    return execute_circuit
