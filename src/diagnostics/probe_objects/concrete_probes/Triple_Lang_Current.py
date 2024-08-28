# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings
#   - add hardware interface objects
#   - implement run

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
from Base_TLP import BaseTLP

class TripleLangCurrent(BaseTLP):
    "<...>"
    def __init__(self,
                 lower_probe_address:int,
                 lower_amp_address:int,
                 *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

        # pack subcomponent arguments
        probe_args = {"address": lower_probe_address,
                      "type": self.HW.AI}
        
        amp_args = {"address": lower_amp_address,
                    "type": self.HW.AO}
        
        # PROBE SUBCOMPONENTS
        self._low_probe = self.hard.make(**probe_args)  # obtain voltage to calculate current through probe
        self._low_amp = self.hard.make(**amp_args)      # set applied voltage to lower source

