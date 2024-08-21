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

        # TO DO - PROBE INFO
        self.lower_probe = None
        self.center_probe = None 
