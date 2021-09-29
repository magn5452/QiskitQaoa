from abc import ABC, abstractmethod


class QaoaMinimizer(ABC):
    @abstractmethod
    def minimize(self, initial_parameter):
        pass
