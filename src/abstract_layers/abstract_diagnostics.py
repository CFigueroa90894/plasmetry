# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings

# built-in imports
from abc import ABCMeta, abstractmethod


class AbstractDiagnostics(metaclass=ABCMeta):
    """<...>"""
    
    @abstractmethod
    def start_diagnostics(self):
        """<...>"""
        raise NotImplementedError("This function was not overloaded in the subclass!")
    
    @abstractmethod
    def stop_diagnostics(self):
        """<...>"""
        raise NotImplementedError("This function was not overloaded in the subclass!")
    
    @abstractmethod
    def setup_experiment(self):
        """<...>"""
        raise NotImplementedError("This function was not overloaded in the subclass!")
    
    @abstractmethod
    def shutdown(self):
        """<...>"""
        raise NotImplementedError("This function was not overloaded in the subclass!")