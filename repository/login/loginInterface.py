from abc import ABC, abstractmethod

class LoginInterface(ABC):
    @abstractmethod
    def autenticar(self, email, senha):
        pass
