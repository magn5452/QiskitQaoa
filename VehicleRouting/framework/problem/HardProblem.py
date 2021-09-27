from abc import ABC, abstractmethod


class HardProblem(ABC):
    @abstractmethod
    def get_penalty_factor(self):
        pass
