""" G3 - Plasma Devs
Layer 3 - Diagnostics - Concrete Implementation
    Provides the main implementation for the Diagnostics Layer, assembling its subcomponents and
    exposing the layer's public functionality.

author: figueroa_90894@students.pupr.edu
status: WIP
    - add docstrings
    - remove relative import (added so docstrings are displayed)
    - validate with team

"""
# built-in imports
import sys
import os

from queue import Queue

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


# TO DO - remove relative imports
# local imports
from abstract_layers.abstract_diagnostics import AbstractDiagnostics


# TO TO
class DiagnosticsLayer(AbstractDiagnostics):
    """<...>"""

    # Default subcomponent module names
    calculations_factory_modname = 'calculations_factory'
    probe_factory_modname = 'probe_factory'
    probe_operation_modname = 'probe_operation'

    # Default lower layer
    hardware_layer_modname = 'hardware_layer'


    def __init__(self, 
                 status_flags, 
                 command_flags,
                 results_buffer:Queue=None,
                 real_time_param:dict=None,
        ):
        """<...>"""
        # --- Save Arguments --- #
        """
        NOTE: I'm wishing there was a way to instantiate flags with defaults without
        needing to violate the principle of not importing modules from other layers.

        Perhaps its for the best, we might not realize the layer is using different
        flags, making debugging layer integrations harder.
        """
        self.__status = status_flags     # system state indicators
        self.__command = command_flags   # action triggers

        # validate results_buffer
        if results_buffer is not None:
            self.__result_buff = results_buffer
        else:
            self.__result_buff = Queue() # create default Queue

        # validate real_time_param
        if real_time_param is not None:
            self.__real_time_param = real_time_param
        else:
            self.__real_time_param = {}  # create default dictionary

        # ----- LOAD LAYER COMPONENTS ----- #
        # load subcomponent modules
        calculations_factory_mod = __import__(self.calculations_factory_modname)
        probe_factory_mod = __import__(self.probe_factory_modname)
        probe_operation_mod = __import__(self.probe_operation_modname)

        # load subcomponent classes
        calc_fac_cls = calculations_factory_mod.CalculationsFactory
        probe_fac_cls = probe_factory_mod.ProbeFactory
        probe_op_cls = probe_operation_mod.ProbeOperation

        # load lower layer
        hardware_layer_mod = __import__(self.hardware_layer_modname)
        hardware_layer_cls = hardware_layer_mod.HardwareLayer

        # ---- LAYER ASSEMBLY ---- #
        # lower layer
        self.__hardware = hardware_layer_cls()  # lower layer interface
        self.__comp_fac = self.__hardware.get_component_factory() # hardware component factory

        # calculations factory subcomponent
        self.__calc_fac = calc_fac_cls      # calculations factory is not instantiable
        
        # probe factory subcomponent
        self.__probe_fac = probe_fac_cls(
            status_flags=self.__status,
            command_flags=self.__command,
            hardware_factory=self.__comp_fac,
            calculations_factory=self.__calc_fac
        )

        # probe operation subcomponent
        self.__probe_op = probe_op_cls(
            status_flags=self.__status,
            command_flags=self.__command,
            results_buffer=self.__result_buff,
            real_time_param=self.__real_time_param,
            probe_factory=self.__probe_fac
        )

    # TO DO
    def setup_diagnostics(self):
        """<...>"""
        raise NotImplementedError
    
    # TO DO
    def start_diagnostics(self):
        """<...>"""
        raise NotImplementedError
    
    # TO DO
    def stop_diagnostics(self):
        """<...>"""
        raise NotImplementedError
    
    # TO DO
    def diagnostics_shutdown(self):
        """<...>"""
        raise NotImplementedError
