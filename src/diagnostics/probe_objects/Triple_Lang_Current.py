# author: figueroa_90894@studnt.pupr.edu
# status: WIP
#   - add docstrings
#   - add hardware interface objects


from Base_TLP import BaseTLP

class TripleLangCurrent(BaseTLP):
    "<...>"
    def __init__(self, *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

        # TO DO - PROBE SUBCOMPONENTS
        self.lower_probe = None     # <analog in> obtain voltage to calculate current through probe
        self.lower_amp = None       # <analog in> set applied voltage

    # TO DO
    def run(self):
        "<...>"
        raise NotImplementedError