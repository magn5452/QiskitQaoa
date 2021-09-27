import numpy as np
from qiskit import QuantumCircuit
from scipy.optimize import minimize
from VehicleRouting.framework.factory.QaoaFactory import QaoaFactory


class Qaoa:

    def __init__(self, factory: QaoaFactory):
        # Strategies
        self.initial_parameter = factory.create_initial_parameter()
        self.precision = factory.create_precision()
        self.backend = factory.create_backend().get_backend()
        self.initial_strategy = factory.create_initial()
        self.mixer_strategy = factory.create_mixer()
        self.phase_strategy = factory.create_phase()

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
        quantum_circuit.measure_all()

    def get_execute_circuit(self):
        """
        Runs parametrized circuit

        Args:
        """

        def execute_circuit(theta):
            quantum_circuit = self.set_up_qaoa_circuit(theta)
            counts = self.backend.run(quantum_circuit).result().get_counts()
            return self.calculate_expectation(counts)

        return execute_circuit

    def minimize(self):
        optimization_method = 'COBYLA'
        execute_circuit = self.get_execute_circuit()
        result = minimize(execute_circuit, self.initial_parameter, method=optimization_method)
        self.result = result
        return result

    def simulate(self):
        return self.backend.run(self.get_optimal_circuit()).result().get_counts()

    def get_result(self):
        if self.result is not None:
            return self.result
        else:
            return self.minimize()

    def get_optimal_circuit(self):
        return self.set_up_qaoa_circuit(self.get_optimal_parameter())

    def get_optimal_parameter(self):
        return self.get_result().x
