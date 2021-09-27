from abc import ABC, abstractmethod


class CircuitPlotter(ABC):
    @abstractmethod
    def plot(self, circuit):
        pass
