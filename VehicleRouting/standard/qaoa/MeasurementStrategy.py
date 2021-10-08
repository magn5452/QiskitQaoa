from VehicleRouting.framework.qaoa.CircuitStrategy import MeasurementStrategy


class TomographyMeasurementStrategy(MeasurementStrategy):
    def __init__(self):
        pass

    def set_up_measurement_circuit(self, quantum_circuit):
        quantum_circuit.measure_all()


class NullMeasurementStrategy(MeasurementStrategy):
    def __init__(self):
        pass

    def set_up_measurement_circuit(self, quantum_circuit):
        pass