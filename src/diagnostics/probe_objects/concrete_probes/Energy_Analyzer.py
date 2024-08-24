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
                 *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

        # TO DO
        self.collimator = None  #hardware interface

    def run(self):
        """<...>"""
        raise NotImplementedError

