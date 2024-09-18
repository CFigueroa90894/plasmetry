""" G3 - Plasma Devs
Layer 2 - Control - Concrete Implementation
    Provides the main implementation for the Control Layer, assembling its subcomponents and
    exposing the layer's public functionality.

author: figueroa_90894@students.pupr.edu
status: WIP
    - add docstrings
    - remove temporary relative imports
    - redefine and implement abstract methods from interface specification
    - validate with team
"""

# built-in imports
import sys
import os

from typing import Tuple
from threading import Event

# ----- PATH HAMMER v2.7 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:
    """Resolve absolute imports by recusring into subdirs and appending them to the python path."""
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    assert src_abs.split('\\')[-1*len(root_target):] == root_target   # validate correct top folder
    
    # get subdirs, exclude unwanted
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split('\\')[-1] not in exclude]
    for dir in dirs: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: {src_abs}")

if __name__ == "__main__":  # execute path hammer if this script is run directly
    path_hammer(1, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #

# TO DO - Remove temporary relative imports (used to get type hints in IDE)
# local imports
from abstract_layers.abstract_control import AbstractControl
from system_flags import StatusFlags, CommandFlags

# TO DO
class ControlLayer(AbstractControl):
    """<...>"""
    # TO DO - Carlos
    def __init__(self, name:str="CTRL", *args, **kwargs):
        """<...>"""
        super().__init__(*args, name=name, **kwargs)    # call parent constructor
        raise NotImplementedError

    # TO DO - Alberto
    def set_config(self) -> Tuple[bool, str]:
        """<...>"""
        raise NotImplementedError

    # TO DO - Alberto
    def get_config(self) -> any:
        """<...>"""
        raise NotImplementedError

    # TO DO - Alberto
    def save_config_file(self) -> bool:
        """<...>"""
        raise NotImplementedError

    # TO DO - Alberto
    def load_config_file(self) -> None:
        """<...>"""
        raise NotImplementedError

    # TO DO - Carlos
    def get_real_time_container(self) -> Tuple[dict, Event]:
        """<...>"""
        raise NotImplementedError

    # TO DO - Carlos
    def setup_experiment(self) -> None:
        """<...>"""
        raise NotImplementedError

    # TO DO - Carlos
    def start_experiment(self) -> None:
        """<...>"""
        raise NotImplementedError

    # TO DO - Carlos
    def stop_experiment(self) -> None:
        """<...>"""
        raise NotImplementedError

    # TO DO - Carlos
    def layer_shutdown(self) -> None:
        """<...>"""
        raise NotImplementedError

    # TO DO - Carlos
    def get_status_flags(self) -> StatusFlags:
        """<...>"""
        raise NotImplementedError

    # TO DO - Carlos
    def get_command_flags(self) -> CommandFlags:
        """<...>"""
        raise NotImplementedError

