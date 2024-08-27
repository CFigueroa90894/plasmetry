# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings
#   - add hardware interface objects
#   - implement run

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
from probe_objects.abstract_probes.Base_TLP import BaseTLP

class TripleLangCurrent(BaseTLP):
    "<...>"
    def __init__(self,
                 lower_probe_addres:int,
                 lower_amp_address:int,
                 *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

        # pack subcomponent arguments
        probe_args = {"address": lower_probe_addres,
                      "type": self.HW.AI}
        
        amp_args = {"address": lower_amp_address,
                    "type": self.HW.AO}
        
        # PROBE SUBCOMPONENTS
        self._low_probe = self.hard.make(**probe_args)  # obtain voltage to calculate current through probe
        self._low_amp = self.hard.make(**amp_args)      # set applied voltage to lower source

    # TO DO
    def run(self):
        "<...>"
        raise NotImplementedError