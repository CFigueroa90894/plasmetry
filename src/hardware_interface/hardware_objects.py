# author: figueroa_90894@students.pupt.edu
# status: WIP
#   - add docstrings

# built-in imports
import sys
import os

# ----- PATH HAMMER ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 2             # how many parent folders to reach /plasmetry/src
    
    # Locate absolute path to /plasmetry/src
    parent = os.path.dirname(__file__)  # traverse directory upwards
    for _ in range(num_dir): parent = os.path.dirname(parent)
    print(f"Path Hammer: {parent}")     # expect absolute path to /plasmetry/src

    # Append all target folders to python path
    for dir in os.listdir(parent): sys.path.append(f"{parent}/{dir}")
    print(f"Path Hammer: folders appended")
# ----- END PATH HAMMER ----- #

# local-imports
from hardware_interface.abstract_wrapper import AbstractWrapper as interface


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
        super().__init__(self, *args, **kwargs)

    def write(self, voltage:float) -> None:
        self.hardware.write_analog(self.address, voltage)


class AnalogIn(BaseChannel):
    """<...>"""
    def __init__(self, *args, **kwargs):
        """<...>"""
        super().__init__(self, *args, **kwargs)

    def read(self) -> float:
        """<...>"""
        return self.hardware.read_analog(self.address)
    
# ----- DIGITAL CHANNELS ----- #
class DigitalOut(BaseChannel):
    """<...>"""
    def __init__(self, *args, **kwargs):
        """<...>"""
        super().__init__(self, *args, **kwargs)

    def write(self, level:bool) -> None:
        self.hardware.write_digital(self.address, level)


class DigitalIn(BaseChannel):
    """<...>"""
    def __init__(self, *args, **kwargs):
        """<...>"""
        super().__init__(self, *args, **kwargs)

    def read(self) -> bool:
        """<...>"""
        return self.hardware.read_digital(self.address)