"""G3 - Plasma Devs
Layer 4 - Hardware Interface - Component Objects
    Defines classes for probe subcomponents, including basic sensors and amplifiers.

author: figueroa_90894@students.pupt.edu
status: WIP
    - add docstrings
    - finish classes
"""

# built-in imports
import sys
import os

# ----- PATH HAMMER v2.7 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:
    """Resolve absolute imports by recusring into subdirs and appending them to python path."""
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    assert src_abs.split('\\')[-1*len(root_target):] == root_target   # validate correct top folder
    
    # get subdirs, exclude unwanted
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split('\\')[-1] not in exclude]
    for dir in dirs: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: {src_abs}")

if __name__ == "__main__":  # execute path hammer if this script is run directly
    path_hammer(2, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #


# local imports
from channel_objects import AnalogIn, AnalogOut, DigitalOut


# ----- INPUT SUBCOMPONENTS ----- #
class VoltageSensor:
    """Implements a voltage sensor based on a differential amplifier.
    
    Public Methods:
        __init__() - initialize the sensor object
        read(): float - return voltage measured by analog input

    Protected Methods:
        _division_read(): float - returns voltage divided by gain
        _no_division_read(): float - returns the voltage, without dividing by gain
    """

    def __init__(self, gain:float, analog_in: AnalogIn):
        """Constructor for VoltageSensor, saves the given channel and gain.
        
        Arguments:
            gain: float - gain value of associated diff amp; used to divide voltage measures
            analog_in: AnalogIn - input channel from the diff amp
        """

        # Validate analog_in
        if not isinstance(analog_in, AnalogIn):
            err_msg = f"analog_in must be instance of AnalogIn!"
            err_msg += f" Given {type(AnalogIn)}"
            raise TypeError(err_msg)
        else:
            self._input = analog_in

        # Validate gain
        if gain == 0:
            raise ValueError("Gain cannot be zero!")

        # Select appropriate read function
        if gain == 1: # input does not require dividing by gain
            self.read = self._no_division_read
        else:         # inpuy requires division by gain
            self._gain = gain
            self.read = self._division_read

    # Overridden by constructor
    def read(self) -> float:
        """Returns the voltage measured by the associated differential amplifier."""
        raise NotImplementedError("VoltageSensor did not correctly override its read() method!")

    def _division_read(self) -> float:
        """Returns the voltage, corrected for gain."""
        return self._input.read() / self._gain

    def _no_division_read(self) -> float:
        """Returns voltage as is, without correcting for gain."""
        return self._input.read()
    
# ----- OUTPUT SUBCOMPONENTS ----- #
class BaseAmp:
    """Parent class for concrete amplifier classes."""
    def __init__(self, dac_range:dict, amp_range: dict, analog_out: AnalogOut):
        """Constructor for BaseAmp and its subclasses.
        
        Arguments:
            dac_range: dict - min and max of the DAC's output
            amp_range: dict - min and max of the amp's output
            analog_out: AnalogOut - output channel to the amplifier
        """
        pass

class HVAmp(BaseAmp):
    """<...>"""
    pass

class BaseAmp:
    """<...>"""
    pass

class VoltageSweeper(HVAmp):
    """<...>"""
    pass

class BaseAmp:
    """<...>"""
    pass

class RelaySet:
    """<...>"""
    pass