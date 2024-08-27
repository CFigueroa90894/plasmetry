# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings
#   - add hardware interface objects
#   - implement run

import sys
import os

# add the src folder to the python path to locate local modules
if __name__ == "__main__":
    target = os.path.dirname(__file__)  # concrete probes
    target = os.path.dirname(target)    # probe objects
    target = os.path.dirname(target)    # diagnostics
    target = os.path.dirname(target)    # src
    sys.path.append(target)             # add src for absolute imports

from diagnostics.probe_objects.abstract_probes.Base_TLP import BaseTLP

class TripleLangVoltage(BaseTLP):
    "<...>"
    def __init__(self,
                 floating_probe_address:int,
                 *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

        # pack subcomponent arguments
        float_args = {"address": floating_probe_address,
                      "type": self.HW.AI}

        # PROBE SUBCOMPONENTS
        self.float_probe = self.hard.make(**float_args)     # get voltage difference from center probe down to floating probe

    # TO DO
    def run(self):
        """<...>"""
        raise NotImplementedError