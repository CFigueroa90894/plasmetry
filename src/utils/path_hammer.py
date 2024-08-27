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

# ----- PATH HAMMER ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly
    name = "Path Hammer"
    print(f"{name}: resolving imports...")
    
    # HAMMER ARGUMENTS
    num_dir = 1     # how many parent folders to reach /plasmetry/src
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