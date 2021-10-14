import numpy as np
from scipy.optimize import minimize

from VehicleRouting.framework.interfaces.QaoaMinimizer import QaoaMinimizer
from VehicleRouting.standard.concretization.Qaoa import Qaoa


class QaoaMinimizerImpl(QaoaMinimizer):

    def __init__(self, qaoa: Qaoa):
        self.qaoa = qaoa
        self.result = None

    def minimize(self, initial_parameters=None):
        if initial_parameters is None:
            initial_parameters = np.ones(2 * self.qaoa.get_precision())

        optimization_method = "Cobyla"
        execute_circuit = self.qaoa.get_execute_circuit()
        options = {'disp':True,'maxiter':100}
        self.result = minimize(execute_circuit, initial_parameters, method=optimization_method, options=options)
        return self.get_result(), self.get_optimal_parameter(), self.get_optimal_circuit()

    def get_result(self):
        return self.result

    def get_optimal_circuit(self):
        return self.qaoa.set_up_qaoa_circuit(self.get_optimal_parameter())

    def get_optimal_parameter(self):
        return self.get_result().x
