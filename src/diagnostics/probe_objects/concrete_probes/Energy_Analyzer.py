# author: figueroa_90894@students.pupr.edu
# status: WIP


# local imports
from abstract_probes.Sweeper_Probe import SweeperProbe


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

