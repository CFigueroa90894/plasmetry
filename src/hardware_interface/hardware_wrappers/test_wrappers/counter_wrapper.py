"""G3 - Plasma Devs
Layer 1 - Hardware Interface - Counter Wrapper
    Implements a testing variant of the hardware wrapper interface that does not depend on physical
    hardware components or external packages.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    CounterWrapperTest - exported as 'wrapper'
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
    path_hammer(3, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #

# local imports
from abstract_wrapper import AbstractWrapper
from type_enforcer import enforce_type

from say_writer import SayWriter


class CounterWrapperTest(AbstractWrapper):
    """A dummy hardware wrapper for testing purposes. Prints arguments and tracks calls.
    
    Attributes:
        + name - label used for printing debug messages
        + analog_in_count - number calls to read_analog()
        + analog_out_count - number calls to write_analog()
        + digital_in_count - number calls to read_digital()
        + digital_out_count - number calls to write_analog()
        + max_addr - highest address number allowed by the wrapper
        # _say_obj - text output object
    """
    def __init__(self, name:str="CountHW", output:SayWriter=None):
        """Initialize CounterWrapperTest.
        
        Arguments:
            name: str - label prefixed to text output
                default: "CountHW"
            output: SayWriter - text output object
                default: None - use built-in 'print()' method
        """
        # Validate output writer
        if output is None:
            output = SayWriter()

        # Instance attributes
        self._say_obj = output
        self.name = name            # shorthand name
        self.analog_in_count = 0    # number of times read_analog() has been called
        self.analog_out_count = 0   # number of times write_analog() has been called
        self.digital_in_count = 0   # number of times read_digital() has been called
        self.digital_out_count = 0  # number of times write_digital() has been called
        self.max_addr = 8           # highest allowed address for counter wrapper tests

    # ----- ANALOG I/O ----- #
    @enforce_type
    def write_analog(self, address:int, value:float|int) -> None:
        """Prints arguments and increments counter."""
        self.validate_address(address)
        self.analog_out_count += 1    # increment counter
        self.say(f"Aout addr:{address} val:{value} count:{self.analog_out_count}")

    @enforce_type
    def read_analog(self, address:int) -> float:
        """Print arguments and increments counter. Return count value as float."""
        self.validate_address(address)
        self.analog_in_count += 1     # increment counter
        self.say(f"Ain addr:{address} count:{self.analog_in_count}")
        return float(self.analog_in_count)

    # ----- DIGITAL I/O ----- #
    @enforce_type
    def write_digital(self, address: int, level: bool) -> None:
        """Print arguments and increments counter."""
        self.validate_address(address)
        self.digital_out_count += 1    # increment counter
        self.say(f"Dout addr:{address} val:{level} count:{self.digital_out_count}")
    
    @enforce_type
    def read_digital(self, address: int) -> bool:
        """Print arguments and increments counter. Returns True."""
        self.validate_address(address)
        self.digital_in_count += 1     # increment counter
        self.say(f"Din addr:{address} count:{self.digital_in_count}")
        return True

    # ----- UTILITIES ----- #
    def validate_address(self, address):
        """Raises an error if the given address exceeds the maximum number."""
        if address > self.max_addr:
            raise RuntimeError(f"Address exceeds allowed max of {self.max_addr}. Given {address}")

    def say(self, msg):
        """Print messages prepended with the object's name using the SayWriter."""
        self._say_obj(f"{self.name}: {msg}")

    def print_state(self):
        """Prints the values returned by the state() method."""
        state_msg = self.lpreppend(1, '\t ', self.state())
        self.lprint(state_msg)

    def state(self) -> list:
        """Return state messages as a list."""
        msg = [ f"digital-in  count: {self.digital_in_count}",
                f"analog-in   count: {self.analog_in_count}",
                f"digital-out count: {self.digital_out_count}",
                f"analog-out  count: {self.analog_out_count}"]
        return msg
    
    def lprint(self, arr: list):
        """Print elements in list on separate lines."""
        for line in arr:
            print(line)

    def lpreppend(self, num, sym, arr):
        """Prepend every item in the list with the specified amount of given char."""
        new = []
        for line in arr:
            new.append(f"{num*sym}{line}")
        return new

# WRAPPER EXPORT
wrapper = CounterWrapperTest


# # ----- BASIC TESTS ----- #
# if __name__ == "__main__":
#     print("COUNTER WRAPPER TESTS")
#     obj  = CounterWrapperTest(debug=True)   # initialize with debug prints enabled

#     # Digital Input
#     print("\nDIGITAL INPUT")
#     obj.read_digital(0)

#     # Analog Input
#     print("\nANANLOG INPUT")
#     obj.read_analog(1)
#     obj.read_analog(1)

#     # Digital Output
#     print("\nDIGITAL OUTPUT")
#     obj.write_digital(2, True)
#     obj.write_digital(2, False)
#     obj.write_digital(2, True)

#     # Analog Output
#     print("\nANALOG INPUT")
#     obj.write_analog(3, 1.5)
#     obj.write_analog(3, 1.0)
#     obj.write_analog(3, 0.5)
#     obj.write_analog(3, 0.0)

#     # Print final state
#     print()
#     obj.say("final state")
#     obj.print_state()