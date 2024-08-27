# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add subcomponents once hardware interface is implemented
#   - implement sweep method

import sys
import os

# add the src folder to the python path to locate local modules
if __name__ == "__main__":
    target = os.path.dirname(__file__)  # abstract probes
    target = os.path.dirname(target)    # probe objects
    target = os.path.dirname(target)    # diagnostics
    target = os.path.dirname(target)    # src
    sys.path.append(target)             # add src for absolute imports

# local imports
from diagnostics.probe_objects.abstract_probes.Base_Probe import BaseProbe        # parent class

# TO DO
class SweeperProbe(BaseProbe):
    """<...>"""
    def __init__(self,
                 num_samples:int,
                 sweeper_address:int,
                 collector_address:int,
                 *args, **kwargs
                 ):
        super().__init__(*args, **kwargs)   # initialize attributes inherited from parent
        
        # PROBE INFO
        self.num_samples = num_samples      # number of samples to obtain per sweep

        # pack subcomponent arguments
        sweeper_args = {"address": sweeper_address,
                        "type": self.HW.AO}
        
        collector_args = {"address": collector_address,
                          "type": self.HW.AI}

        # PROBE SUBCOMPONENTS
        self._sweeper = self.hard.make(**sweeper_args)      # Hardware interface obj - TBD
        self._collector = self.hard.make(**collector_args)  # Hardware interface obj - TBD

    # TO DO
    def sweep(self) -> dict:
        """Performs a single voltage sweep on the sweeper object.
        Returns a dictionary consisting of applied biases and raw sampled voltages."""
        raise NotImplementedError




