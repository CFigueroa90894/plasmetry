# author: figueroa_90894@studnt.pupr.edu
# status: WIP
#   - add docstrings
#   - add hardware interface objects

from Base_Probe import BaseProbe

class BaseTLP(BaseProbe):
    "<...>"
    def __init__(self, *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

        # TO DO - PROBE SUBCOMPONENTS
        self.upper_probe = None     # <analog in> obtain voltage to calculate current through probe
        self.upper_amp = None       # <analog out> set applied voltage
