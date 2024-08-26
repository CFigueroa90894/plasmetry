# author: figueroa_90894@students.pupt.edu
# status: WIP
#   - add docstrings


# local-imports
from abstract_wrapper import AbstractWrapper as interface


# ----- PARENT CLASS ----- #
class BaseChannel:
    """<...>"""
    def __init__(self, address:int, hardware_obj:interface):
        """<...>"""
        self.address = address
        self.hardware = hardware_obj


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