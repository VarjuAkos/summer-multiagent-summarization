from abc import ABC, abstractmethod

class Graph(ABC):
    @abstractmethod
    def create_graph(self):
        pass
    
    @abstractmethod
    def run_graph(self, project_folder):
        pass