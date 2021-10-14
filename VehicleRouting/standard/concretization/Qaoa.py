import time

import numpy as np
from qiskit import QuantumCircuit, transpile
from scipy.optimize import minimize
from VehicleRouting.framework.factory.QaoaFactory import QaoaFactory


class Qaoa:

    def __init__(self, factory: QaoaFactory):
        # Strategies
        self.precision = factory.create_precision()
        self.backend_strategy = factory.create_backend().get_backend()
        self.initial_strategy = factory.create_initial()
        self.mixer_strategy = factory.create_mixer()
        self.phase_strategy = factory.create_phase()
        self.measurement_strategy = factory.create_measurement()
        self.cost_strategy = factory.create_cost();

        # Qubo
        self.qubo = factory.create_qubo()
        self.num_qubits = self.qubo.get_num_variables()

    def calculate_cost(self, counts):
        return self.cost_strategy.calculate_cost(counts, self.qubo)

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

    def set_up_initial_state_circuit(self, quantum_circuit: QuantumCircuit):
        """
        Sets up initial qaoa circuit

        Args:
            quantum_circuit: quantum circuit
        """

        self.initial_strategy.set_up_initial_state_circuit(quantum_circuit)

    def set_up_main_circuit(self, theta, quantum_circuit: QuantumCircuit):
        """
        Sets up main qaoa circuit

        Args:
            theta: qaoa parameters
            quantum_circuit: quantum circuit
        """
        gamma_list = theta[self.precision:]
        beta_list = theta[:self.precision]

        for index_repetition in range(0, self.precision):
            gamma = gamma_list[index_repetition]
            beta = beta_list[index_repetition]
            self.set_up_phase_circuit(gamma, quantum_circuit)
            self.set_up_mixer_circuit(beta, quantum_circuit)

    def set_up_phase_circuit(self, gamma, quantum_circuit: QuantumCircuit):
        """
        Sets up phase qaoa circuit

        Args:
            gamma: phase qaoa parameters
            quantum_circuit: quantum circuit
        """

        self.phase_strategy.set_up_phase_circuit(gamma, quantum_circuit)

    def set_up_mixer_circuit(self, beta, quantum_circuit: QuantumCircuit):
        """
        Sets up mixer qaoa circuit

        Args:
            beta: mixer qaoa parameters
            quantum_circuit: quantum circuit
        """

        self.mixer_strategy.set_up_mixer_circuit(beta, quantum_circuit)

    def set_up_measurement_circuit(self, quantum_circuit: QuantumCircuit):
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
            transpiled = transpile(quantum_circuit, backend=self.backend_strategy, optimization_level = 3)
            counts = self.backend_strategy.run(transpiled).result().get_counts()
            return self.calculate_cost(counts)

        return execute_circuit

    def simulate(self, theta):
        start_time = time.time()
        transpiled = transpile(self.set_up_qaoa_circuit(theta), backend=self.backend_strategy)
        print("--- %s seconds ---" % (time.time() - start_time))
        result = self.backend_strategy.run(transpiled).result()
        counts = result.get_counts()
        expectation = self.calculate_cost(counts)
        return result, counts, expectation

    def get_precision(self):
        return self.precision
