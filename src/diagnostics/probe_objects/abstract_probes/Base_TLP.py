# author: figueroa_90894@studnets.pupr.edu
# status: WIP
#   - add docstrings
#   - add hardware interface objects

import sys
import os

# add the src folder to the python path to locate local modules
if __name__ == "__main__":
    target = os.path.dirname(__file__)  # abstract probes
    target = os.path.dirname(target)    # probe objects
    target = os.path.dirname(target)    # diagnostics
    target = os.path.dirname(target)    # src
    sys.path.append(target)             # add src for absolute imports

from diagnostics.probe_objects.abstract_probes.Base_Probe import BaseProbe

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
