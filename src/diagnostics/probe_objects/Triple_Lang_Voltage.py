# author: figueroa_90894@studnt.pupr.edu
# status: WIP
#   - add docstrings
#   - add hardware interface objects
#   - implement run

from Base_TLP import BaseTLP

class TripleLangVoltage(BaseTLP):
    "<...>"
    def __init__(self, *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

        # TO DO - PROBE INFO
        self.upper_probe = None     # hardware interface

    # TO DO
    def run(self):
        """<...>"""
        raise NotImplementedError