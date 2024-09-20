"""G3 - Plasma Devs
Layer 4 - Hardware Interface - Channel Objects
    Defines classes for basic hardware channels, including analog and digital I/O channels.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    BaseChannel
    AnalogOut
    AnalogIn
    DigitalOut
    DigitalIn
"""

# built-in imports
import sys
import os

# ----- PATH HAMMER v3.0 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:
    """Resolve absolute imports by recursing into subdirs and appending them to python path."""
    # os delimeters
    win_delimeter, rpi_delimeter = "\\", "/"

    # locate project root
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    print(f"Path Hammer: {src_abs}")

    # select path delimeter
    if win_delimeter in src_abs: delimeter = win_delimeter
    elif rpi_delimeter in src_abs: delimeter = rpi_delimeter
    else: raise RuntimeError("Path Hammer could not determine path delimeter!")

    # validate correct top folder
    assert src_abs.split(delimeter)[-1*len(root_target):] == root_target
    
    # get subdirs, exclude unwanted
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split(delimeter)[-1] not in exclude]
    for dir in dirs: sys.path.append(dir)    # add all subdirectories to python path

if __name__ == "__main__":  # execute path hammer if this script is run directly
    path_hammer(2, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
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