# author: figueroa_90894@students.pupr.edu

"""PATH HAMMER

    Code snippet that adds each of Plasmetry's layer folders to the python path.
    Assumes absolute imports will invoke modules under /plasmetry/src/<target>.

    Copy-paste this code to any script that will be invoked directly; then update
    its arguments accordingly, based on where the script resides in plasmetry's
    folder structure.
  
    Unfortunately, this snippet cannot be imported since it itself appends each 
    directory path needed to resolve absolute imports at runtime.
"""

# built-in imports
import sys
import os

# ----- PATH HAMMER v2.3 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 2             # how many parent folders to reach /plasmetry/src

    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..') # absolute path to plasmetry/src
    print(f"Path Hammer: {src_abs}")
    targets = [x[0] for x in os.walk(src_abs) if x[0][-1]!='_']          # all subdirectories, except __pycache__
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #


# ----- LOCAL IMPORT TESTS ----- #
print("\nPath Hammer absolute import tests...")
import placeholder_layers
import placeholder_ctrl
from calculations import placeholder_calc
from probe_objects import placeholder_probe
import placeholder_hardware
import placeholder_ui
import placeholder_utils
print("Path Hammer: absolute import tests successful\n")