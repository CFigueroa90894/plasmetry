# author: figueroa_90894@studnets.pupr.edu
# status: WIP
#   - add docstrings
#   - add hardware interface objects

# built-in imports
import sys
import os

# ----- PATH HAMMER v3.0 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:
    """Resolve absolute imports by recursing into subdirs and appending them to python path."""
    # os delimeters
    win_delimeter, rpi_delimeter = "\\", "/"

    # locate project root
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    print(f"Path Hammer: {src_abs}")

    # select path delimeter
    if win_delimeter in src_abs: delimeter = win_delimeter
    elif rpi_delimeter in src_abs: delimeter = rpi_delimeter
    else: raise RuntimeError("Path Hammer could not determine path delimeter!")

    # validate correct top folder
    assert src_abs.split(delimeter)[-1*len(root_target):] == root_target
    
    # get subdirs, exclude unwanted
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split(delimeter)[-1] not in exclude]
    for dir in dirs: sys.path.append(dir)    # add all subdirectories to python path

if __name__ == "__main__":  # execute path hammer if this script is run directly
    path_hammer(3, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #

# local imports
from Base_Probe import BaseProbe

class BaseTLP(BaseProbe):
    "<...>"
    def __init__(self,
                 up_amp_bias: float,
                 up_amp,
                 up_collector,
                 up_shunt:float,
                 *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

        # PROBE CONFIG
        self.up_amp_bias = up_amp_bias  # fixed voltage bias applied to the upper probe
        self.up_shunt = up_shunt

        # PROBE SUBCOMPONENTS
        self.up_amp = up_amp               # Set voltage source output
        self.up_collector = up_collector   # Obtain voltage samples to calculate probe current.

    def run(self):
        """<...>"""
        super().run() 