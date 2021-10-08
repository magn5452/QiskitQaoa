from abc import ABC, abstractmethod


class CostStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, qubo):
        pass
