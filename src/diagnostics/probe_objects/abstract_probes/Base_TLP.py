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
    def __init__(self, *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

        # TO DO - PROBE SUBCOMPONENTS
        self.upper_probe = None     # <analog in> obtain voltage to calculate current through probe
        self.upper_amp = None       # <analog out> set applied voltage
