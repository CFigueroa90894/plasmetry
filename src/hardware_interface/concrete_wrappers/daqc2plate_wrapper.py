# author: figueroa_90894@students.pupr
# status: WIP
#   - import DAQC2plate library
#   - override abstract parent's methods
#   - add docstrings

# built-in imports
import sys
import os

# external imports
"""from <...> import <...>"""

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 2             # how many parent folders to reach /plasmetry/src

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


class DAQC2plateWrapper(AbstractWrapper):
    """<...>"""
    def __init__(self):
        """<...>"""
        raise NotImplementedError
    
    # ----- ANALOG I/0 ----- #
    @enforce_type
    def write_analog(self, address:int, value:float) -> None:
        """<...>"""
        raise NotImplementedError
    
    @enforce_type
    def read_analog(self, address:int) -> float:
        """<...>"""
        raise NotImplementedError
    
    # ----- DIGITAL I/O ----- #
    @enforce_type
    def write_digital(self, address:int, level:bool) -> None:
        """<...>"""
        raise NotImplementedError
    
    @enforce_type
    def read_digital(self, address:int) -> bool:
        """<...>"""
        raise NotImplementedError