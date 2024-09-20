"""G3 - Plasma Devs
Layer 4 - Hardware Interface - DAQC2plate Wrapper
    Implements the hardware interfacing methods specified by the AbstractWrapper class using the
    piplates.DAQC2plate library. Provides basic analog and digital I/O methods.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    DAQC2plateWrapper - exported as 'wrapper'
"""
# built-in imports
import sys
import os

# third-party imports
import piplates.DAQC2plate as dac

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
    path_hammer(3, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #


# local imports
from abstract_wrapper import AbstractWrapper
from type_enforcer import enforce_type


class DAQC2plateWrapper(AbstractWrapper):
    """Implements the methods specified by AbstractWrapper, providing calls to the DAQC2plate
    library without the caller having to be aware of the used interface.

    Attributes:
        + plate: int - the address of the piplate in the plate stack (see DAQC2plate documentation)

    Methods:
        + __init__() - object constructor
        + write_analog() - sets the output voltage of a DAC channel
        + read_analog() - reads the input voltage of a ADC channel
        + write_digital() - sets the output voltage level of a DOUT channel
        + read_digital() - reads the input voltage level of a DIN channel
    """
    def __init__(self, plate_addr:int=0):
        """Constructor for the wrapper object.
        
        Arguments:
            plate_addr: int - address of the piplate, to distinguish it from others in the stack
                default: 0
        """
        self.plate = plate_addr     # address of the piplate in the stack
    
    # ----- ANALOG I/0 ----- #
    @enforce_type
    def write_analog(self, address:int, value:float|int) -> None:
        """Sets the output voltage of the DAC channel at the given address.
        
        Arguments:
            address: int - the address of the channel being written
            value: float|int - the voltage value to output from the channel (Volts)
        """
        dac.setDAC(self.plate, address, value)
    
    @enforce_type
    def read_analog(self, address:int) -> float:
        """Returns the voltage value measured at the given ADC channel."""
        return dac.getADC(self.plate, address)
    
    # ----- DIGITAL I/O ----- #
    @enforce_type
    def write_digital(self, address:int, level:bool) -> None:
        """Sets the output voltage level of the DOUT channel at the given address.
        
        Arguments:
            address: int - the address of the channel being written
            level: bool - voltage level to output
                True: High
                False: Low
        """
        if level:   # set on True
            dac.setDOUTbit(self.plate, address)
        else:       # clear on False
            pass
            dac.clrDOUTbit(self.plate, address)
    
    @enforce_type
    def read_digital(self, address:int) -> bool:
        """Returns the voltage level measured at the given DIN channel.
        
        Returns:
            True: High
            False: Low
        """
        return dac.getDINbit(self.plate, address)

    
# WRAPPER EXPORT
wrapper = DAQC2plateWrapper

