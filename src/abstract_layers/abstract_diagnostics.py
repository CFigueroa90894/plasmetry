# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings

# built-in imports
from abc import ABCMeta, abstractmethod


class AbstractDiagnostics(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self,
                 config_ref,            # ProtectedDictionary object containing user-settings
                 sys_ref,               # ProtectedDictionary object containing system-settings
                 status_flags,          # collection of Events to indicate system states
                 command_flags,         # collection of Events to trigger actions
                 hardware_wrapper_cls,  # wrapper class for hardware interface implementation
                 real_time_param,       # ProtectedDicitonary object to store most recent calculated parameters
                 results_buffer,        # Queue to return aggregated results to Control Layer
                 args, **kwargs):
        raise NotImplementedError("This function was not overloaded in the subclass!")
    
    @abstractmethod
    def start_diagnostics(self):
        """<...>"""
        raise NotImplementedError("This function was not overloaded in the subclass!")
    
    @abstractmethod
    def stop_diagnostics(self):
        """<...>"""
        raise NotImplementedError("This function was not overloaded in the subclass!")
    
    @abstractmethod
    def setup_experiment(self):
        """<...>"""
        raise NotImplementedError("This function was not overloaded in the subclass!")
    
    @abstractmethod
    def shutdown(self):
        """<...>"""
        raise NotImplementedError("This function was not overloaded in the subclass!")