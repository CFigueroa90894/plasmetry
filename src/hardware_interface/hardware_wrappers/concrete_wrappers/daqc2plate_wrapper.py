# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings

# built-in imports
import sys
import os

# third-party imports
import piplates.DAQC2plate as dac

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 3             # how many parent folders to reach /plasmetry/src

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


# local imports
from abstract_wrapper import AbstractWrapper
from type_enforcer import enforce_type


class DAQC2plateWrapper(AbstractWrapper):
    """<...>"""
    def __init__(self, plate_addr:int=0):
        """<...>"""
        self.plate = plate_addr     # address of the piplate in the stack
    
    # ----- ANALOG I/0 ----- #
    @enforce_type
    def write_analog(self, address:int, value:float) -> None:
        """<...>"""
        dac.setDAC(self.plate, address, value)
    
    @enforce_type
    def read_analog(self, address:int) -> float:
        """<...>"""
        return dac.getADC(self.plate, address)
    
    # ----- DIGITAL I/O ----- #
    @enforce_type
    def write_digital(self, address:int, level:bool) -> None:
        """<...>"""
        if level:   # set on True
            dac.setDOUTbit(self.plate, address)
        else:       # clear on False
            pass
            dac.clrDOUTbit(self.plate, address)
    
    @enforce_type
    def read_digital(self, address:int) -> bool:
        """<...>"""
        return dac.getDINbit(self.plate, address)

    
# WRAPPER EXPORT
wrapper = DAQC2plateWrapper

