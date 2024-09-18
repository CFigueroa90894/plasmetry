from counter_wrapper import CounterWrapperTest
from concrete_wrappers.daqc2plate_wrapper import DAQC2plateWrapper

class CounterDAQC2DoutWrapper(CounterWrapperTest):
    """<...>"""
    def __init__(self, *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)   # call both parent constructors
        self.dac = DAQC2plateWrapper()      # default wrapper

    
    # ----- ANALOG I/0 ----- #
    def write_analog(self, address:int, value:float) -> None:
        """<...>"""
        super().write_analog(address, value)
    
    def read_analog(self, address:int) -> float:
        """<...>"""
        super().read_analog(address)
    
    # ----- DIGITAL I/O ----- #
    def write_digital(self, address:int, level:bool) -> None:
        """<...>"""
        super().write_digital(address, level)
        self.dac.write_digital(address, level)
    
    def read_digital(self, address:int) -> bool:
        """<...>"""
        super().read_digital(address)

    
# WRAPPER EXPORT
wrapper = CounterDAQC2DoutWrapper