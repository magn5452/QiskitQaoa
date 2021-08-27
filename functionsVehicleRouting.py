from qiskit import Aer
from qiskit import QuantumCircuit
from CostVehicleRoutingCalculator import CostVehicleRoutingCalculator


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
        cost_calculator = CostVehicleRoutingCalculator(bitstring, graph, 1, 200)
        obj = cost_calculator.vehicle_routing_cost()
        sum_obj += obj * count
        sum_count += count

    return sum_obj / sum_count


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
    nqubits = number_of_nodes * (number_of_nodes - 1)
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


