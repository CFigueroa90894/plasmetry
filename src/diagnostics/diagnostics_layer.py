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

import inspect
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
from abstract_diagnostics import AbstractDiagnostics


# TO TO
class DiagnosticsLayer(AbstractDiagnostics):
    """<...>"""

    # Default subcomponent module names
    calculations_factory_mod = 'calculations_factory'
    probe_factory_mod = 'probe_factory'
    probe_operation_mod = 'probe_operation'

    # Default lower layer module name
    hardware_layer_mod = 'hardware_layer'


    def __init__(self,
                 status_flags,
                 command_flags,
                 results_buffer:Queue=None,
                 real_time_param:dict=None,
        ):
        """<...>"""
        # default buffer if none was specified
        if results_buffer is None:
            results_buffer = Queue()    # redefine arg variable
        
        # default dict if none was specified
        if real_time_param is None:
            real_time_param = {}        # redefine arg variable

        # ----- Save Arguments ----- #
        self._status = status_flags     # system state indicators
        self._command = command_flags   # action triggers
        self._result_buff = results_buffer         # buffer to pass experiment results up the stack
        self._real_time_param = real_time_param


        # ----- Assemble Diagnostic Layer ----- #
        sub = self._load_all_subcomponents()   # import subcomponents, returned in a dict
        
        # unpack subcomponent classes
        hardware_layer = sub["hardware_layer"]
        calcs_factory = sub["calc_fac"]
        probe_factory = sub["probe_fac"]
        probe_operation = sub["probe_op"]
        
        # instantiate lower layer
        self._hardware = hardware_layer()  # lower layer interface
        self._comp_fac = self._hardware.get_component_factory() # makes hardware components

        # instantiate subcomponents
        self._calc_fac = calcs_factory  # makes probe specific equations
        self._probe_fac = probe_factory(**self.__probe_factory_args()) # makes specific probes
        self._probe_op = probe_operation(**self.__probe_op_args())     # controls probes
        

    # ----- LAYER PUBLIC METHODS ----- #

    # TO DO
    # User confirms config and prepares to begin experiment
    def setup_diagnostics(self, sys_ref:dict, config_ref:dict):
        """Initializes probe object and prepare to launch threads.
        
        Arguments:
            sys_ref: `ProtectedDictionary` containing probe specific system settings
            config_ref: `ProtectedDictionary` containing probe specific user settings
            probe_thread_name: str - name assigned to probe object's thread
                default: "PROBE"
        """
        pass
    
    # TO DO
    def start_diagnostics(self):
        """Launches ProbeOperation's thread.

        Raises a RuntimeError if `setup_diagnostics()` was not invoked first.
        """
        if not self._ready:
            raise RuntimeError("Cannot begin diagnostics before setup_experiment() is called!")
        else:
            self._ready = False  # clear ready value to prevent recurring calls to this method
        self.start()    # launch Probe Operation thread
    
    # TO DO
    def stop_diagnostics(self):
        """<...>"""
        raise NotImplementedError
    
    # TO DO
    def diagnostics_shutdown(self):
        """<...>"""
        raise NotImplementedError
    

    # ----- UTILS ----- #
    def _load_all_subcomponents(self):
        """<...>"""
        # load subcomponent modules
        calculations_factory_mod = self._load_mod(self.calculations_factory_mod)
        probe_factory_mod = self._load_mod(self.probe_factory_mod)
        probe_operation_mod = self._load_mod(self.probe_operation_mod)

        print(type(calculations_factory_mod))

        # load subcomponent classes
        calc_fac_cls = calculations_factory_mod.CalculationsFactory
        probe_fac_cls = probe_factory_mod.ProbeFactory
        probe_op_cls = probe_operation_mod.ProbeOperation

        # load lower layer
        hardware_layer_mod = self._load_mod(self.hardware_layer_mod)
        hardware_layer_cls = hardware_layer_mod.HardwareLayer

        # pack and return subcomponent classes
        classes = {
            "calc_fac": calc_fac_cls,
            "probe_fac": probe_fac_cls,
            "probe_op": probe_op_cls,
            "hardware_layer": hardware_layer_cls
        }
        return classes
    
    def _load_mod(self, mod):
        """<...>"""
        # check the module was specified as a string
        if inspect.ismodule(mod):
            pass
        elif isinstance(mod, str):
            mod = __import__(mod)
        else:
            raise TypeError(f"Class attribute {mod} must be module or string! Given {type(mod)}")
        return mod
    
    # TO DO
    def _info(self):
        """<...>"""
        sub = [
            ("Diagnostics", "Calculations Factory", str(self._calc_fac)),
            ("Diagnostics", "Probe Factory", str(self._probe_fac)),
            ("Diagnostics", "Probe Operation", str(self._probe_op)),
            ("Diagnostics", "Hardware Interface", str(self._hardware))
        ]
        sub.extend(self._hardware._info())
        return sub

    def __probe_factory_args(self):
        """<...>"""
        probe_factory_args = {
            "status_flags": self._status,
            "command_flags": self._command,
            "hardware_factory": self._comp_fac,
            "calculations_factory": self._calc_fac
        }
        return probe_factory_args

    def __probe_op_args(self):
        """<...>"""
        probe_op_args = {
            "status_flags": self._status,
            "command_flags": self._command,
            "results_buffer": self._result_buff,
            "real_time_param": self._real_time_param,
            "probe_factory": self._probe_fac
        }
        return probe_op_args

# # Basic tests
# if __name__ == "__main__":
    
#     # local imports
#     from system_flags import StatusFlags, CommandFlags
#     import hardware_interface.hardware_layer
    
#     # init control objects
#     status = StatusFlags()
#     commands = CommandFlags()

#     # configure hardware layer for test
#     custom_h = hardware_interface.hardware_layer
#     custom_h.HardwareLayer.hardware_wrapper_mod = 'counter_wrapper'

#     # init diagnostics layer
#     diagnostics_args = {
#         "status_flags": status,
#         "command_flags": CommandFlags
#     }
#     a = DiagnosticsLayer
#     a.hardware_layer_mod = custom_h
#     a = a(**diagnostics_args)
#     for sub in a._info():
#         print(sub)