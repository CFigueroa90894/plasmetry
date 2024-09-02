# author: figueroa_90894@students.pupr.edu

"""PATH HAMMER

    Code snippet that adds each of Plasmetry's layer folders to the python path.
    Assumes absolute imports will invoke modules under /plasmetry/src/<target>.

    Copy-paste this code to any script that will be invoked directly; then update
    its arguments accordingly, based on where the script resides in plasmetry's
    folder structure.
  
    Unfortunately, this snippet cannot be imported since it itself appends each 
    directory path needed to resolve absolute imports at runtime.

    To debug the path hammer, execute the relevant script directly, and ensure the
    printed path corresponds to plasmetry/src. The path hammer with automatically
    raise an assertion error if it does not find plasmetry/src. Increase or decrease
    the path hammer's arguments as necessary.
"""

# built-in imports
import sys
import os

# ----- PATH HAMMER v2.7 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:  # execute snippet if current script was run directly 
    """Resolve absolute imports by recusring into subdirectories and appending them to python path."""
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    assert src_abs.split('\\')[-1*len(root_target):] == root_target   # validate correct top folder
    
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split('\\')[-1] not in exclude] # get subdirs, exclude unwanted
    for dir in dirs: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: {src_abs}")

if __name__ == "__main__":  # execute path hammer if this script is run directly
    path_hammer(2, ['plasmetry', 'src'], ['__pycache__'], suffix='/src')  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #


# ----- LOCAL IMPORT TESTS ----- #
print("\nPath Hammer absolute import tests...")
import placeholder_layers
from system_flags import StatusFlags, CommandFlags
# calc still needs concrete equations has
# from calculations import placeholder_calc
from probe_factory import ProbeFactory
from hardware_factory import HardwareFactory
import placeholder_ui
from type_enforcer import enforce_type
print("Path Hammer: absolute import tests successful\n")
