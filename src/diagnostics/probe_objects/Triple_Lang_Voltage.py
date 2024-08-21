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

        # TO DO - PROBE SUBCOMPONENTS
        self.float_probe = None     # <analog in> get voltage difference from center probe down to floating probe

    # TO DO
    def run(self):
        """<...>"""
        raise NotImplementedError