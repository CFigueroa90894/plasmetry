# author: figueroa_90894@students.pupr.edu
# status: DONE

# built-in imports
from threading import Event             # thread-safe signaling mechanisms
from queue import Queue                 # thread-safe data buffer
from abc import ABC, abstractmethod     # enforce abstraction


class BaseProbe(ABC):
    """The top-level, abstract class for all probe implementations.
    Includes initialization for flags, data buffer, equations, config, and data buffer.
    Defines abstract methods run(), and _graceful_exit()."""
    def __init__(self, 
                 config_ref:dict,
                 shutdown:Event,
                 diagnose:Event,
                 operating:Event,
                 equations:list,
                 data_buff:Queue,
                 sampling_rate:int,
                 relay_address:int,
                 hardware_factory_obj,
                 ):
        
        # SIGNAL FLAGS - Set externally, indicates an action this object must perform.
        self.shutdown = shutdown        # graceful system-wide shutdown, begin exit script
        self.diagnose = diagnose        # diagnostics must be performed
        
        # STATUS FLAGS - Set internally, notifies other subcomponents of this objects state.
        # !!! HIGH VOLTAGE INDICATOR !!!
        # Set this BEFORE enabling the relay
        # Clear AFTER confirming the relay is disabled
        self.operating = operating      # indicate that diagnostics are being performed
        
        # PROBE INFO
        self.config_ref = config_ref        # dictionary containing relevant configuration data
        self.equations = equations  # list of callables to calculate plasma parameters
        self.data_buff = data_buff  # thread-safe queue, pass data samples to probe operation
        self.sampling_rate = sampling_rate      # samples to obtain per second, Hertz (Hz)

        # HARDWARE FACTORY SETUP
        self.hard = hardware_factory_obj
        self.HW = hardware_factory_obj.IDs 
        
        # pack arguments
        relay_args = {"address": relay_address,
                      "type": self.HW.DO}
        
        # PROBE SUBCOMPONENTS
        self._relay = self.hard.make(**relay_args)      # turn the probe circuits on or off
    
    @abstractmethod
    def run(self) -> None:
        """Executes the data acquisition process. Children must override it."""
        raise NotImplementedError
    
    @abstractmethod
    def _graceful_exit(self):
        """Complete all pending actions, then exit gracefully."""
        raise NotImplementedError

