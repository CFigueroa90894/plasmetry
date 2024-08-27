# author: figueroa_90894@students.pupr.edu
# status: WIP

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
from probe_objects.abstract_probes.Sweeper_Probe import SweeperProbe


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

