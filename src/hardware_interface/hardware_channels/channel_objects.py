"""G3 - Plasma Devs
Layer 4 - Hardware Interface - Channel Objects
    Defines classes for basic hardware channels, including analog and digital I/O channels.

author: figueroa_90894@students.pupt.edu
status: WIP
  - validate with team
"""

# built-in imports
import sys
import os

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 2             # how many parent folders to reach /plasmetry/src

    # absolute path to plasmetry/src
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..')
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    # get subdirs, exclude __pycache__
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__']
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #

# local-imports
from abstract_wrapper import AbstractWrapper as interface


# ----- PARENT CLASS ----- #
class BaseChannel:
    """The parent class for all concrete channel types.
    
    Defines the basic constructor for all channels, taking as arguments the address and 
    hardware_wrapper object that all channels require.

    Attributes:
        # _address: int - address of the channel's associated port
        # _hardware: subclass of AbstractWrapper - provides access to I/O ports

    Methods:
        + __init__() - constructor to initialize objects of this class
    """
    def __init__(self, address:int, hardware_wrapper:interface):
        """The constructor for BaseChannel and all of its subclasses.
        
        Arguments:
            address: int - hardware port address associated with the channel
            hardware_wrapper: subclass of AbstractWrapper - I/O functions specific to the ADC/DAC
        """
        # Validate given argument subclasses the AbstractWrapper class
        if not issubclass(type(hardware_wrapper), interface):
            err_msg = f"hardware_wrapper must subclass AbstractWrapper!"
            err_msg += f" Given {type(hardware_wrapper)}"
            raise TypeError(err_msg)
        
        # Save arguments
        self._address = address
        self._hardware = hardware_wrapper


# ----- ANALOG CHANNELS ----- #
class AnalogOut(BaseChannel):
    """Subclass of BaseChannel, associated with analog output ports.
    
    Attributes
        ^# _address: int
        ^# _hardware

    Methods:
        ^+ __init__() - initialize object, inherited
        + write(float) - sets the out of the associated DAC port
    """
    def __init__(self, *args, **kwargs):
        """Constructor for AnalogOut class, invokes the inherited parent constructor."""
        super().__init__(*args, **kwargs)

    def write(self, voltage:float) -> None:
        """Sets the output of the corresponding DAC port to the given float value."""
        self._hardware.write_analog(self._address, voltage)


class AnalogIn(BaseChannel):
    """Subclass of BaseChannel, associated with analog input ports.
    
    Attributes:
        ^# _address: int
        ^# _hardware
    
    Methods:
        ^+ __init__() - initialize object, inherited
        + read(): float - return measured voltage
    """
    def __init__(self, *args, **kwargs):
        """Constructor for AnalogIn class, invokes inherited parent constructor."""
        super().__init__(*args, **kwargs)

    def read(self) -> float:
        """Returns the voltage value measured at the corresponding ADC port."""
        return self._hardware.read_analog(self._address)


# ----- DIGITAL CHANNELS ----- #
class DigitalOut(BaseChannel):
    """Subclass of BaseChannel, associated with digital output pins.

    Attributes:
        ^# _address: int
        ^# _hardware
    
    Methods:
        ^+ __init__() - initialize object, inherited
        + set() - output HIGH signal
        + clear() - output LOW signal
    """
    def __init__(self, *args, **kwargs):
        """Constructor for DigitalOut class, invokes inherited parent constructor."""
        super().__init__(*args, **kwargs)

    def set(self):
        """Output the HIGH value from the associated digital pin."""
        self._hardware.write_digital(self._address, True)

    def clear(self):
        """Output the LOW value from the associated digital pin."""
        self._hardware.write_digital(self._address, False)


class DigitalIn(BaseChannel):
    """Subclass of BaseChannel, associated with digital input pins.
    
    Attributes:
        ^# _address: int
        ^# _hardware
    
    Methods:
        ^+ __init__() - initialize object, inherited
        + read(): bool - return value from associated pin
    """
    def __init__(self, *args, **kwargs):
        """Constructor for DigitalIn class, invokes inherited parent constructor."""
        super().__init__(*args, **kwargs)

    def read(self) -> bool:
        """Return the measured state the associated pin.
        
            True, for HIGH value
            False, for LOW value
        """
        return self._hardware.read_digital(self._address)