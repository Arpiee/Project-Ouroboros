from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name, role):
        self.name = name
        self.role = role

    @abstractmethod
    def run(self, input_data):
        pass

