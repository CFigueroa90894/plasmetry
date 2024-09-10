"""G3 - Plasma Devs
Layer 4 - Hardware Interface - Channel Objects
    Defines classes for basic hardware channels, including analog and digital I/O channels.

author: figueroa_90894@students.pupt.edu
status: WIP
  - add docstrings
  - modify channel classes to match new, incoming hardware component classes
"""

# built-in imports
import sys
import os

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 1             # how many parent folders to reach /plasmetry/src

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
    """<...>"""
    def __init__(self, address:int, hardware_wrapper:interface):
        """<...>"""
        self.address = address
        self.hardware = hardware_wrapper


# ----- ANALOG CHANNELS ----- #
class AnalogOut(BaseChannel):
    """<...>"""
    def __init__(self, *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

    def write(self, voltage:float) -> None:
        self.hardware.write_analog(self.address, voltage)


class AnalogIn(BaseChannel):
    """<...>"""
    def __init__(self, *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

    def read(self) -> float:
        """<...>"""
        return self.hardware.read_analog(self.address)
    
# ----- DIGITAL CHANNELS ----- #
class DigitalOut(BaseChannel):
    """<...>"""
    def __init__(self, *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

    def write(self, level:bool) -> None:
        self.hardware.write_digital(self.address, level)


class DigitalIn(BaseChannel):
    """<...>"""
    def __init__(self, *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

    def read(self) -> bool:
        """<...>"""
        return self.hardware.read_digital(self.address)