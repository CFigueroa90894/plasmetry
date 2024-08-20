# author: figueroa_90894@studnt.pupr.edu
# status: WIP
#   - add subcomponents once hardware interface is implemented
#   - implement sweep method

# local imports
from Base_Probe import BaseProbe        # parent class

# TO DO
class SweeperProbe(BaseProbe):
    """<...>"""
    def __init__(self,
                 num_samples:int,
                 *args, **kwargs
                 ):
        super().__init__(*args, **kwargs)   # initialize attributes inherited from parent
        
        # PROBE INFO
        self.num_samples = num_samples      # number of samples to obtain per sweep

        # TO DO - PROBE SUBCOMPONENTS
        self._sweeper = None        # Hardware interface obj - TBD
        self._collector = None      # Hardware interface obj - TBD

    # TO DO
    def sweep(self) -> dict:
        """Performs a single voltage sweep on the sweeper object.
        Returns a dictionary consisting of applied biases and raw sampled voltages."""
        raise NotImplementedError




