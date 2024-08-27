# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings

# built-in imports
from abc import ABC, abstractmethod


class AbstractWrapper(ABC):
    """<...>"""
    
    # ----- ANALOG I/0 ----- #
    @abstractmethod
    def write_analog(cls, address:int, value:float) -> None:
        """<...>"""
        raise NotImplementedError
    
    @abstractmethod
    def read_analog(cls, address:int) -> float:
        """<...>"""
        raise NotImplementedError
    
    # ----- DIGITAL I/O ----- #
    @abstractmethod
    def write_digital(cls, address:int, level:bool) -> None:
        """<...>"""
        raise NotImplementedError
    
    @abstractmethod
    def read_digital(cls, address:int) -> bool:
        """<...>"""
        raise NotImplementedError