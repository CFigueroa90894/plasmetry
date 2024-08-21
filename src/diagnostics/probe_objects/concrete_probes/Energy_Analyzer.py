# author: figueroa_90894@students.pupr.edu
# status: WIP


# local imports
from abstract_probes.Sweeper_Probe import SweeperProbe
from ProbeEnum import PRB


class EnergyAnalyzer(SweeperProbe):
    """<...>"""
    def __init__(self,
                 probe_type:PRB,
                 *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

        # PROBE INFO
        self.probe_type = probe_type

        # TO DO
        self.collimator = None  #hardware interface

    def run(self):
        """<...>"""
        raise NotImplementedError

