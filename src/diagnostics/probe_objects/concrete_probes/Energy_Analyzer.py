# author: figueroa_90894@students.pupr.edu
# status: WIP

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
from Sweeper_Probe import SweeperProbe


class EnergyAnalyzer(SweeperProbe):
    """<...>"""
    def __init__(self,
                 rejector_address:int,
                 collector_bias_address:int,
                 *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)


        # pack subcomponent arguments
        rejector_args = {"address": rejector_address,
                         "type": self.HW.AO}
        
        bias_args = {"address": collector_bias_address,
                     "type": self.HW.AO}

        # PROBE SUBCOMPONENTS
        self._rejector_bias = self.hard.make(**rejector_args)   # set voltage to reject particles at outer subcomponent
        self._collector_bias = self.hard.make(**bias_args)      # set voltage to attract particles at innermost subcomponent

    def run(self):
        """<...>"""
        raise NotImplementedError

