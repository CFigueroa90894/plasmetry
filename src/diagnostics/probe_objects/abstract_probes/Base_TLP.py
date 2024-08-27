# author: figueroa_90894@studnets.pupr.edu
# status: WIP
#   - add docstrings
#   - add hardware interface objects

# built-in imports
import sys
import os

# ----- PATH HAMMER ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 3             # how many parent folders to reach /plasmetry/src
    
    # Locate absolute path to /plasmetry/src
    parent = os.path.dirname(__file__)  # traverse directory upwards
    for _ in range(num_dir): parent = os.path.dirname(parent)
    print(f"Path Hammer: {parent}")     # expect absolute path to /plasmetry/src

    # Append all target folders to python path
    for dir in os.listdir(parent): sys.path.append(f"{parent}/{dir}")
    print(f"Path Hammer: folders appended")
# ----- END PATH HAMMER ----- #

# local imports
from probe_objects.abstract_probes.Base_Probe import BaseProbe

class BaseTLP(BaseProbe):
    "<...>"
    def __init__(self,
                 upper_probe_address:int,
                 upper_amp_address:int,
                 *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

        # pack subcomponent's arguments
        probe_args = {"address": upper_probe_address,
                      "type": self.HW.AI}
        
        amp_args = {"address": upper_amp_address,
                    "type": self.HW.AO}

        # PROBE SUBCOMPONENTS
        self._up_probe = self.hard.make(**probe_args)   # Obtain voltage samples to calculate probe current.
        self._up_amp = self.hard.make(**amp_args)       # Set voltage source output
