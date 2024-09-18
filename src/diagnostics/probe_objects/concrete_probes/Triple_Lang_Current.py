# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings
#   - add hardware interface objects
#   - implement run
"""
Triple Langmuir Probe - Current Mode
            - V1 +                          V1 - 'Raw Voltage 1'         (sampled across shunt_1)
    - |-------S1------- up probe            S1 - 'Shunt 1': up_shunt     (shunt resistor)
  B1  A1                                    A1 - Up Probe Amp            (up_amp)
    + |                                     B1 - 'Bias 1': up_amp_bias   (applied bias)
      |---------------- center probe        
    + |                                     B2 - 'Bias 2': down_amp_bias (applied bias)
  B2  A2                                    A2 - Down Probe Amp          (down_amp)
    - |-------S2------- down probe          S2 - 'Shunt 2': down_shunt   (shunt resistor)
            - V2 +                          V2 - 'Raw Voltage 2'         (sampled across shunt_2)
"""

# built-in imports
import sys
import os

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
from Base_TLP import BaseTLP

class TripleLangCurrent(BaseTLP):
    "<...>"
    def __init__(self,
                 down_amp_bias:float,
                 down_amp,
                 down_collector,
                 down_shunt,
                 *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

        # PROBE CONFIG
        self.down_amp_bias = down_amp_bias
        self.down_shunt = down_shunt
        
        # PROBE SUBCOMPONENTS
        self.down_amp = down_amp              # set applied voltage to lower source
        self.down_collector = down_collector  # obtain voltage to calculate current through probe

