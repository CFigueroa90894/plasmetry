# author: figueroa_90894@students.pupr.edu
# status: WIP

import sys
import os

# add the src folder to the python path to locate local modules
if __name__ == "__main__":
    target = os.path.dirname(__file__)  # concrete probes
    target = os.path.dirname(target)    # probe objects
    target = os.path.dirname(target)    # diagnostics
    target = os.path.dirname(target)    # src
    sys.path.append(target)             # add src for absolute imports

# local imports
from diagnostics.probe_objects.abstract_probes.Sweeper_Probe import SweeperProbe


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

