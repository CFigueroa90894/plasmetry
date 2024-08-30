# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings
#   - comment init
#   - public methods
#   - integrate with system control
#   - resolve placeholder probe attribute
#   - when done, delete basic tests

# built-in imports
import sys
import os

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 1             # how many parent folders to reach /plasmetry/src

    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..') # absolute path to plasmetry/src
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__'] # get subdirs, exclude __pycache__
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #


# local imports
from probe_factory import ProbeFactory
from hardware_factory import HardwareFactory
from calculations_factory import CalculationsFactory
from daqc2plate_wrapper import DAQC2plateWrapper


class ProbeOperation:
    """<...>"""
    def __init__(self,
                 config_ref,
                 status_flags,
                 command_flags,
                 hardware_wrapper_cls=DAQC2plateWrapper
                 ):
        """"<...>"""
        # Save arguments
        self.commands = command_flags
        self.status = status_flags
        self.config = config_ref
        
        # Instantiate Probe Factory
        probe_factory_args = {
            "config_ref": config_ref,
            "status_flags": status_flags,
            "command_flags": command_flags,
            "hardware_factory": HardwareFactory(hardware_wrapper_cls),
            "calculations_factory": CalculationsFactory
        }
        self.probe_factory = ProbeFactory(**probe_factory_args)


