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