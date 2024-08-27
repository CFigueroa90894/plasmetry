# author: figueroa_90894@studnets.pupr.edu
# status: WIP
#   - add docstrings
#   - add hardware interface objects

# built-in imports
import sys
import os

# ----- PATH HAMMER ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly
    name = "Path Hammer"
    print(f"{name}: resolving imports...")
    
    # HAMMER ARGUMENTS
    num_dir = 3     # how many parent folders to reach /plasmetry/src
    targets = [     # folders to be added to the python path
        '\\abstract_layers',
        '\\control',
        '\\diagnostics',
        '\\hardware_interface',
        '\\user_interface',
        '\\utils']
    
    # Locate absolute path to /plasmetry/src
    print(f"{name}: locating plasmetry source path...")
    parent = os.path.dirname(__file__)      # get current file's parent directory
    for _ in range(num_dir):                # traverse directory upwards
        parent = os.path.dirname(parent)    # get next parent
    print(f"{name}: {parent}")  # expect absolute path to /plasmetry/src

    # Append all target folders to python path
    print(f"{name}: appending target paths...")
    for subdir in targets:
        target = parent + subdir
        sys.path.append(target)
    print(f"{name}: complete")

# local imports
from probe_objects.abstract_probes.Base_Probe import BaseProbe

class BaseTLP(BaseProbe):
    "<...>"
    def __init__(self,
                 upper_probe_address:int,
                 upper_amp_address:int,
                 *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

        # pack subcomponent's arguments
        probe_args = {"address": upper_probe_address,
                      "type": self.HW.AI}
        
        amp_args = {"address": upper_amp_address,
                    "type": self.HW.AO}

        # PROBE SUBCOMPONENTS
        self._up_probe = self.hard.make(**probe_args)   # Obtain voltage samples to calculate probe current.
        self._up_amp = self.hard.make(**amp_args)       # Set voltage source output
