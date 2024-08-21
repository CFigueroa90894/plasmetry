# author: figueroa_90894@studnt.pupr.edu
# status: WIP
#   - add docstrings
#   - implement run()

#local imports
from Sweeper_Probe import SweeperProbe
from ProbeEnum import PRB

class LangmuirProbe(SweeperProbe):
    """<...>"""
    def __init__(self, 
                 probe_type:PRB,
                 *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)   # initialize attributes inherited from parent

        # PROBE INFO
        self.probe_type = probe_type

    # TO DO
    def run(self):
        """<...>"""
        raise NotImplementedError