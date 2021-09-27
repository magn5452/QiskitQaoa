from abc import ABC, abstractmethod


class BackendStrategy(ABC):
    @abstractmethod
    def get_backend(self):
        pass
