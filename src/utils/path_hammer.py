""" G3 - Plasma Devs
Utilities - Path Hammer
    Provides a parametrized method that recursively searches for subdirectories in a given path,
    and appends them to the python path, allowing absolute imports of local modules regardless of
    where they reside in the project folder structure. 

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


author: figueroa_90894@students.pupr.edu
status: DONE

Method Arguments:
    num_dir: int - number of directories, from the current file, to the project's root folder
    root_target: list[str] - the expected root folder and its parents; validates if it was found
    exclude: list[str] - subdirectories that should not be appended to the python path
    suffix: str - appended to folder path, allows targetting the root outside of its subfolders
        default: empty string
"""

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
    path_hammer(1, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #


# ----- LOCAL IMPORT TESTS ----- #
if __name__ == "__main__":
    print("\nPath Hammer absolute import tests...")
    import abstract_control
    import abstract_diagnostics
    import abstract_hardware
    from system_flags import StatusFlags, CommandFlags
    # import calculations_factory  # commented while awaiting equations
    import probe_operation
    import channel_factory
    import component_factory
    import placeholder_ui
    from type_enforcer import enforce_type
    print("Path Hammer: absolute import tests successful\n")

