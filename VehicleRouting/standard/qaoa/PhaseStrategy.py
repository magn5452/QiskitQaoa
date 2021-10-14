import numpy as np

from VehicleRouting.framework.qaoa.CircuitStrategy import PhaseStrategy
from VehicleRouting.standard.concretization.QuboImpl import QuboImpl


class NullPhaseStrategy(PhaseStrategy):

    def __init__(self):
        pass

    def set_up_phase_circuit(self, gamma, quantum_circuit):
        pass


class MaxCutSimpleZGatePhaseStrategy(PhaseStrategy):

    def __init__(self, couplings):
        self.couplings = couplings

    def set_up_phase_circuit(self, gamma, quantum_circuit):
        quantum_circuit.barrier()
        for (i, j) in self.couplings:
            quantum_circuit.rzz(2 * gamma, i, j)


class FromQuboZGatePhaseStrategy(PhaseStrategy):

    def __init__(self, qubo: QuboImpl):
        self.qubo = qubo

    def set_up_phase_circuit(self, gamma, quantum_circuit):
        quantum_circuit.barrier()
        constant, linear, quadratic = self.get_normalized_quadratic_and_linear()
        for i in range(self.qubo.get_num_variables()):
            for j in range(i+1):
                if i == j:
                    weight = linear[i]
                    if weight != 0:
                        quantum_circuit.rz(2 * weight * gamma, i)
                else:
                    weight = quadratic[i][j] + quadratic[i][j]
                    if weight != 0:
                        quantum_circuit.rzz(2 * weight * gamma, i, j)

    def get_normalized_quadratic_and_linear(self):

        # Get Ising terms to be used
        constant, linear, quadratic = self.qubo.get_ising_terms()
        # Find maximum
        max_constant = np.amax(constant)
        max_linear = np.amax(linear)
        max_quadratic = np.amax(quadratic)
        max_all = np.amax([max_constant, max_linear, max_quadratic])

        # Normalized
        normalized_constant = constant/max_all
        normalized_linear = linear/max_all
        normalized_quadratic = quadratic/max_all

        return normalized_constant, normalized_linear, normalized_quadratic


class WeightedZGatePhaseStrategy(PhaseStrategy):

    def __init__(self, couplings):
        self.couplings = couplings

    def set_up_phase_circuit(self, gamma, quantum_circuit):
        quantum_circuit.barrier()
        for (i, j, weight) in self.couplings:
            quantum_circuit.rzz(2 * weight * gamma, i, j)
