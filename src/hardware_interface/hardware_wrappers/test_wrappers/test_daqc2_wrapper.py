"""G3 - Plasma Devs
Layer 4 - Hardware Interface - Test DAQC2 Wrapper
    Implements a testing variant of the hardware wrapper interface that incorporates CounterWrapper
    and DAQC2plateWrapper methods into a single call. Allows debug printing while also operating
    the physical DAQC2plate channels.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    TestDAQC2Wrapper - exported as 'wrapper'
"""

from counter_wrapper import CounterWrapperTest
from concrete_wrappers.daqc2plate_wrapper import DAQC2plateWrapper

from type_enforcer import enforce_type

class TestDAQC2Wrapper(CounterWrapperTest):
    """Combines the functionality of the CounterWrapperTest class and the DAQC2plateWrapper class
    to provide practical hardware interfacing while outputting debug messages.
    
    This hardware wrapper inherits from the CounterWrapperTest class to instantiate the debug
    attributes, as well as inherit its text output method. It instantiates a DAQC2plateWrapper
    object as one of its attributes, and invokes its corresponding method in all its calls. The
    returned values are the ones obtained from DAQC2plateWrapper object.

    Attributes:
        + dac: DAQC2plateWrapper - operates the piplates physical channels
        ^+ name - label used for printing debug messages
        ^+ analog_in_count - number calls to read_analog()
        ^+ analog_out_count - number calls to write_analog()
        ^+ digital_in_count - number calls to read_digital()
        ^+ digital_out_count - number calls to write_analog()
        ^+ max_addr - highest address number allowed by the wrapper
        ^# _say_obj - text output object
    
    Methods:
        + __init__() - object constructor
        + write_analog() - sets the output voltage of a DAC channel
        + read_analog() - reads the input voltage of a ADC channel
        + write_digital() - sets the output voltage level of a DOUT channel
        + read_digital() - reads the input voltage level of a DIN channel
    """
    def __init__(self, name:str="DAQC2", *args, **kwargs):
        """Constructor for wrapper object."""
        super().__init__(*args, name=name, **kwargs)   # call both parent constructors
        self.dac = DAQC2plateWrapper()      # default hardware wrapper
    
    # ----- ANALOG I/0 ----- #
    @enforce_type
    def write_analog(self, address:int, value:float|int) -> None:
        """Sets the output voltage of the DAC channel at the given address.
        
        Arguments:
            address: int - the address of the channel being written
            value: float|int - the voltage value to output from the channel (Volts)
        """
        self.analog_out_count += 1
        self.say(f"Aout addr:{address} val:{value} count:{self.analog_out_count}")
        self.dac.write_analog(address, value)
    
    @enforce_type
    def read_analog(self, address:int) -> float:
        """Returns the voltage value measured at the given ADC channel."""
        self.analog_in_count += 1
        val = self.dac.read_analog(address)
        self.say(f"Ain addr:{address} val:{val} count:{self.analog_in_count}")
        return val
    
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
        self.digital_out_count += 1
        self.say(f"Dout addr:{address} val:{level} count:{self.digital_out_count}")
        self.dac.write_digital(address, level)
    
    @enforce_type
    def read_digital(self, address:int) -> bool:
        """Returns the voltage level measured at the given DIN channel.
        
        Returns:
            True: High
            False: Low
        """
        val = self.dac.read_digital(address)
        self.say(f"Din addr:{address} val:{val} count:{self.digital_in_count}")
        return val

    
# WRAPPER EXPORT
wrapper = TestDAQC2Wrapper

