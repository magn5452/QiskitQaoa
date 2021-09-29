from VehicleRouting.framework.qaoa.CircuitStrategy import MeasurementStrategy


class AllMeasurementStrategy(MeasurementStrategy):
    def __init__(self):
        pass

    def set_up_measurement_circuit(self, quantum_circuit):
        quantum_circuit.measure_all()


class NoMeasurementStrategy(MeasurementStrategy):
    def __init__(self):
        pass

    def set_up_measurement_circuit(self, quantum_circuit):
        pass