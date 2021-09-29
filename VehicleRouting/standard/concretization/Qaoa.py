import numpy as np
from qiskit import QuantumCircuit, transpile
from scipy.optimize import minimize
from VehicleRouting.framework.factory.QaoaFactory import QaoaFactory


class Qaoa:

    def __init__(self, factory: QaoaFactory):
        # Strategies
        self.precision = factory.create_precision()
        self.backend = factory.create_backend().get_backend()
        self.initial_strategy = factory.create_initial()
        self.mixer_strategy = factory.create_mixer()
        self.phase_strategy = factory.create_phase()
        self.measurement_strategy = factory.create_measurement()

        # Qubo
        self.qubo = factory.create_qubo()
        self.calculator_strategy = self.qubo.get_calculator_strategy()
        self.quadratic_program = self.qubo.get_quadratic_program()
        self.num_qubits = self.quadratic_program.get_num_vars()

        # Result
        self.result = None

    def calculate_expectation(self, counts):
        """
        Computes expectation value based on measurement results

        Args:
            counts: dict
                    key as bitstring, val as count

        Returns:
            avg: float
                 expectation value
        """

        sum_cost = 0
        sum_count = 0
        for bitstring, count in counts.items():
            solution_array = np.fromiter(bitstring, np.int8)  # convert string of number to np.array of integer
            cost = self.qubo.calculate_cost(solution_array)
            sum_cost += cost * count
            sum_count += count

        expectation_value = sum_cost / sum_count
        return expectation_value

    def set_up_qaoa_circuit(self, theta):
        """
        Sets up qaoa circuit

        Args:
            theta: qaoa parameters
        """

        quantum_circuit = QuantumCircuit(self.num_qubits)
        self.set_up_initial_state_circuit(quantum_circuit)
        self.set_up_main_circuit(theta, quantum_circuit)
        self.set_up_measurement_circuit(quantum_circuit)

        return quantum_circuit

    def set_up_initial_state_circuit(self, quantum_circuit):
        """
        Sets up initial qaoa circuit

        Args:
            quantum_circuit: quantum circuit
        """

        self.initial_strategy.set_up_initial_state_circuit(quantum_circuit, self.num_qubits)

    def set_up_main_circuit(self, theta, quantum_circuit):
        """
        Sets up main qaoa circuit

        Args:
            theta: qaoa parameters
            quantum_circuit: quantum circuit
        """

        for index_repetition in range(0, self.precision):
            self.set_up_phase_circuit(theta, index_repetition, quantum_circuit)
            self.set_up_mixer_circuit(theta, index_repetition, quantum_circuit)

    def set_up_phase_circuit(self, theta, index_repetition, quantum_circuit):
        """
        Sets up phase qaoa circuit

        Args:
            theta: qaoa parameters
            index_repetition: index repetition
            quantum_circuit: quantum circuit
        """

        self.phase_strategy.set_up_phase_circuit(theta, index_repetition, quantum_circuit, self.num_qubits,
                                                 self.precision)

    def set_up_mixer_circuit(self, theta, index_repetition, quantum_circuit):
        """
        Sets up mixer qaoa circuit

        Args:
            theta: qaoa parameters
            index_repetition: index repetition
            quantum_circuit: quantum circuit
        """

        self.mixer_strategy.set_up_mixer_circuit(theta, index_repetition, quantum_circuit, self.num_qubits,
                                                 self.precision)

    def set_up_measurement_circuit(self, quantum_circuit):
        """
        Sets up final measurement qaoa circuit

        Args:
            quantum_circuit: quantum circuit
        """
        self.measurement_strategy.set_up_measurement_circuit(quantum_circuit)

    def get_execute_circuit(self):
        """
        Runs parametrized circuit

        Args:
        """

        def execute_circuit(theta):
            quantum_circuit = self.set_up_qaoa_circuit(theta)
            transpiled = transpile(quantum_circuit, backend=self.backend)
            counts = self.backend.run(transpiled).result().get_counts()
            return self.calculate_expectation(counts)

        return execute_circuit

    def simulate(self, theta):
        transpiled = transpile(self.set_up_qaoa_circuit(theta), backend=self.backend)
        result = self.backend.run(transpiled).result()
        counts = result.get_counts()
        expectation = self.calculate_expectation(counts)
        return result, counts, expectation

    def get_precision(self):
        return self.precision

