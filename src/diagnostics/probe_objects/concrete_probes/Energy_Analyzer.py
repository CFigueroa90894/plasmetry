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
                 rejector_bias:float,
                 collector_bias:float,
                 rejector_amp,
                 collector_amp,
                 *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

        # PROBE CONFIG
        self.rejector_bias = rejector_bias      # fixed voltage bias applied to particle rejector
        self.collector_bias = collector_bias    # fixed voltage bias applied to particle collector

        # PROBE SUBCOMPONENTS
        self.rejector_amp = rejector_amp    # set voltage to reject particles at outer subcomponent
        self.collector_amp = collector_amp  # set voltage to attract particles at innermost subcomponent

