from counter_wrapper import CounterWrapperTest
from concrete_wrappers.daqc2plate_wrapper import DAQC2plateWrapper

from type_enforcer import enforce_type

class TestDAQC2Wrapper(CounterWrapperTest):
    """<...>"""
    def __init__(self, *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)   # call both parent constructors
        self.dac = DAQC2plateWrapper()      # default hardware wrapper
    
    # ----- ANALOG I/0 ----- #
    @enforce_type
    def write_analog(self, address:int, value:float|int) -> None:
        """<...>"""
        self.analog_out_count += 1
        self.say(f"Aout addr:{address} val:{value} count:{self.analog_out_count}")
        self.dac.write_analog(address, value)
    
    @enforce_type
    def read_analog(self, address:int) -> float:
        """<...>"""
        self.analog_in_count += 1
        val = self.dac.read_analog(address)
        self.say(f"Ain addr:{address} val:{val} count:{self.analog_in_count}")
        return val
    
    # ----- DIGITAL I/O ----- #
    @enforce_type
    def write_digital(self, address:int, level:bool) -> None:
        """<...>"""
        self.digital_out_count += 1
        self.say(f"Dout addr:{address} val:{level} count:{self.digital_out_count}")
        self.dac.write_digital(address, level)
    
    @enforce_type
    def read_digital(self, address:int) -> bool:
        """<...>"""
        val = self.dac.read_digital(address)
        self.say(f"Din addr:{address} val:{val} count:{self.digital_in_count}")
        return val

    
# WRAPPER EXPORT
wrapper = TestDAQC2Wrapper