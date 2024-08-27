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
    num_dir = 1             # how many parent folders to reach /plasmetry/src
    
    # Locate absolute path to /plasmetry/src
    parent = os.path.dirname(__file__)  # traverse directory upwards
    for _ in range(num_dir): parent = os.path.dirname(parent)
    print(f"Path Hammer: {parent}")     # expect absolute path to /plasmetry/src

    # Append all target folders to python path
    for dir in os.listdir(parent): sys.path.append(f"{parent}/{dir}")
    print(f"Path Hammer: folders appended")
# ----- END PATH HAMMER ----- #


# ----- LOCAL IMPORT TESTS ----- #
print("\nPath Hammer absolute import tests...")
import placeholder_layers
import placeholder_ctrl
# calc still needs concrete equations has
# from calculations import placeholder_calc
from probe_objects.probe_factory import ProbeFactory
import placeholder_hardware
import placeholder_ui
import placeholder_utils
print("Path Hammer: absolute import tests successful\n")