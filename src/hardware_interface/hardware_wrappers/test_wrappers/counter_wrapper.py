# author: figueroa_90894@students.pupr.edu
# status: DONE

# built-in imports
import sys
import os

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 3             # how many parent folders to reach /plasmetry/src

    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..') # absolute path to plasmetry/src
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__'] # get subdirs, exclude __pycache__
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #

# local imports
from abstract_wrapper import AbstractWrapper
from type_enforcer import enforce_type


class CounterWrapperTest(AbstractWrapper):
    """A dummy hardware interface wrapper for testing purposes.
    Prints arguments and tracks calls to read methods.
    """

    def __init__(self, name:str="CountHW", debug:bool=False):
        """Initialize CounterWrapperTest.
        
                name: str - shorthand name for printing  
                debug: bool - set to print debug messages
        """
        # Instance attributes
        self.name = name            # shorthand name
        self.analog_in_count = 0    # number of times read_analog() has been called for this object
        self.analog_out_count = 0   # number of times write_analog() has been called for this object
        self.digital_in_count = 0   # number of times read_digital() has been called for this object
        self.digital_out_count = 0  # number of times write_digital() has been called for this object
        self.debug = debug          # boolean, to decide whether to print debug messages
        
        # Debug prints
        if self.debug:
            self.say(f"init {type(self)}")
            self.print_state()


    # ----- ANALOG I/O ----- #
    @enforce_type
    def write_analog(self, address:int, value:float) -> None:
        """Prints arguments.
        """
        self.analog_out_count += 1    # increment counter
        if self.debug:                # print debug message
            self.say(f"analog out - address: {address}; value: {value}; count: {self.analog_out_count}")

    @enforce_type
    def read_analog(self, address:int) -> float:
        """Print arguments. Return count value as float."""
        self.analog_in_count += 1     # increment counter
        if self.debug:                # print debug message
            self.say(f"analog in - address: {address}; count: {self.analog_in_count}")
        return float(self.analog_in_count)


    # ----- DIGITAL I/O ----- #
    @enforce_type
    def write_digital(self, address: int, level: bool) -> None:
        """Prints arguments.
        """
        self.digital_out_count += 1    # increment counter
        if self.debug:
            self.say(f"digital out - address: {address}; level: {level}; count: {self.digital_out_count}")
    
    @enforce_type
    def read_digital(self, address: int) -> bool:
        """Print arguments. Return count value as int."""
        self.digital_in_count += 1     # increment counter
        if self.debug:                 # print debug message
            self.say(f"digital in - address: {address}; count: {self.digital_in_count}")
        return int(self.digital_in_count)


    # ----- UTILITIES ----- #
    def say(self, msg):
        """Print messages prepended with object's name."""
        print(f"{self.name}: {msg}")

    def print_state(self):
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


# ----- BASIC TESTS ----- #
if __name__ == "__main__":
    print("COUNTER WRAPPER TESTS")
    obj  = CounterWrapperTest(debug=True)   # initialize with debug prints enabled

    # Digital Input
    print("\nDIGITAL INPUT")
    obj.read_digital(0)

    # Analog Input
    print("\nANANLOG INPUT")
    obj.read_analog(1)
    obj.read_analog(1)

    # Digital Output
    print("\nDIGITAL OUTPUT")
    obj.write_digital(2, True)
    obj.write_digital(2, False)
    obj.write_digital(2, True)

    # Analog Output
    print("\nANALOG INPUT")
    obj.write_analog(3, 1.5)
    obj.write_analog(3, 1.0)
    obj.write_analog(3, 0.5)
    obj.write_analog(3, 0.0)

    # Print final state
    print()
    obj.say("final state")
    obj.print_state()