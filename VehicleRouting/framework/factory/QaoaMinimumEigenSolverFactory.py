from abc import abstractmethod, ABC

class QAOAMinimumEigenSolverFactory(ABC):
    @abstractmethod
    def create_qaoa(self):
        pass
