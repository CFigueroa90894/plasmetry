from counter_wrapper import CounterWrapperTest
from concrete_wrappers.daqc2plate_wrapper import DAQC2plateWrapper

class CounterDAQC2DoutWrapper(DAQC2plateWrapper, CounterWrapperTest):
    """<...>"""
    def __init__(self, *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)   # call both parent constructors

    
    # ----- ANALOG I/0 ----- #
    def write_analog(self, address:int, value:float) -> None:
        """<...>"""
        CounterDAQC2DoutWrapper.write_analog(address, value)
    
    def read_analog(self, address:int) -> float:
        """<...>"""
        CounterDAQC2DoutWrapper.read_analog(address)
    
    # ----- DIGITAL I/O ----- #
    def write_digital(self, address:int, level:bool) -> None:
        """<...>"""
        CounterDAQC2DoutWrapper.write_digital(address, level)
        DAQC2plateWrapper.write_digital(address, level)
    
    def read_digital(self, address:int) -> bool:
        """<...>"""
        CounterDAQC2DoutWrapper.read_digital(address)

    
# WRAPPER EXPORT
wrapper = DAQC2plateWrapper