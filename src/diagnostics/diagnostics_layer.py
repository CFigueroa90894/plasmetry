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
from abstract_diagnostics import AbstractDiagnostics


# TO TO
class DiagnosticsLayer(AbstractDiagnostics):
    """<...>"""

    # Default subcomponent module names
    calculations_factory_modname = 'calculations_factory'
    probe_factory_modname = 'probe_factory'
    probe_operation_modname = 'probe_operation'

    # Default lower layer module name
    hardware_layer_modname = 'hardware_layer'


    def __init__(self, 
                 status_flags, 
                 command_flags,
                 results_buffer:Queue=None,
                 real_time_param:dict=None,
        ):
        """<...>"""
        # ----- Save Arguments ----- #
        self.__status = status_flags     # system state indicators
        self.__command = command_flags   # action triggers

        # validate results_buffer
        if results_buffer is not None:
            self.__result_buff = results_buffer
        else:
            # create default Queue
            self.__result_buff = Queue() 

        # validate real_time_param
        if real_time_param is not None:
            self.__real_time_param = real_time_param
        else:
            # create default dictionary
            self.__real_time_param = {}


        # ----- Assemble Diagnostic Layer ----- #
        sub = self.__load_subcomponents_cls()   # import subcomponents, returned in a dict
        
        # unpack subcomponent classes
        hardware_layer = sub["hardware_layer"]
        calcs_factory = sub["calc_fac"]
        probe_factory = sub["probe_fac"]
        probe_operation = sub["probe_op"]
        
        # instantiate lower layer
        self.__hardware = hardware_layer()  # lower layer interface
        self.__comp_fac = self.__hardware.get_component_factory() # makes hardware components

        # instantiate subcomponents
        self.__calc_fac = calcs_factory  # makes probe specific equations
        self.__probe_fac = probe_factory(**self.__probe_factory_args()) # makes specific probes
        self.__probe_op = probe_operation(**self.__probe_op_args())     # controls probes
        

    # ----- LAYER PUBLIC METHODS ----- #
    # User confirms config and prepares to begin experiment
    def setup_diagnostics(self, sys_ref:dict, config_ref:dict, probe_thread_name="PROBE"):
        """Initializes probe object and prepare to launch threads.
        
        Arguments:
            sys_ref: `ProtectedDictionary` containing system settings
            config_ref: `ProtectedDictionary` containing user settings
            probe_thread_name: str - name assigned to probe object's thread
                default: "PROBE"
        """
        # Initialize Probe Object through Probe Factory
        self._probe = self._probe_factory.make(
            probe_type=config_ref['probe_id'],
            config_ref=config_ref,
            sys_ref=sys_ref,
            probe_name=probe_thread_name
        )
        # acquire probe's data sample buffer
        self._data_buff = self._probe.data_buff
        self._ready = True
    
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
    

    # ----- PRIVATE UTILS ----- #
    def __load_subcomponents_cls(self):
        """<...>"""
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

        # pack and return subcomponent classes
        classes = {
            "calc_fac": calc_fac_cls,
            "probe_fac": probe_fac_cls,
            "probe_op": probe_op_cls,
            "hardware_layer": hardware_layer_cls
        }
        return classes
    
    def __probe_factory_args(self):
        """<...>"""
        probe_factory_args = {
            "status_flags": self.__status,
            "command_flags": self.__command,
            "hardware_factory": self.__comp_fac,
            "calculations_factory": self.__calc_fac
        }
        return probe_factory_args

    def __probe_op_args(self):
        """<...>"""
        probe_op_args = {
            "status_flags": self.__status,
            "command_flags": self.__command,
            "results_buffer": self.__result_buff,
            "real_time_param": self.__real_time_param,
            "probe_factory": self.__probe_fac
        }
        return probe_op_args