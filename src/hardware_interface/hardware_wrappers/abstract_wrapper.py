"""G3 - Plasma Devs
Layer 1 - Hardware Interface - Abstract Wrapper
    Specifies the interface for hardware wrappers in order to provide consistent analog and
    digital I/O methods to hardware object representations.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    AbstractWrapper
"""

# built-in imports
from abc import ABCMeta, abstractmethod


class AbstractWrapper(metaclass=ABCMeta):
    """An abstract class specifying the required methods that hardware wrappers must implement.
    
    Methods:
        + __init__() - hardware wrapper constructor
        + write_analog() - sets an analog voltage output
        + read_analog() - reads an analog voltage input
        + write_digital() - sets a digital voltage output
        + read_digital() - reads a digital voltage input
    """
    @abstractmethod
    def __init__(self):
        """Initialize a hardware wrapper object."""
        raise NotImplementedError
    
    # ----- ANALOG I/0 ----- #
    @abstractmethod
    def write_analog(self, address:int, value:float) -> None:
        """Output an analog voltage value at the specified address."""
        raise NotImplementedError
    
    @abstractmethod
    def read_analog(self, address:int) -> float:
        """Return an analog voltage input value from the specified address."""
        raise NotImplementedError
    
    # ----- DIGITAL I/O ----- #
    @abstractmethod
    def write_digital(self, address:int, level:bool) -> None:
        """Output a digital voltage level at the specified address."""
        raise NotImplementedError
    
    @abstractmethod
    def read_digital(self, address:int) -> bool:
        """Return a digital voltage input level from the specified address."""
        raise NotImplementedError