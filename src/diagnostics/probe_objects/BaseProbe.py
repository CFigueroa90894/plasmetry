# author: figueroa_90894@studnt.pupr.edu
# status: WIP

# built-in imports
from threading import Event
from queue import Queue

# local imports
from ProbeEnum import PRB

# TO DO - ENFORCE ABSTRACT, and others
class BaseProbe:
    # TO DO
    def __init__(self, 
                 shutdown:Event,
                 diagnose:Event,
                 emergency:Event,
                 operating:Event,
                 equations:list,
                 config:dict,
                 data_buff:Queue
                 ):
        
        # SIGNAL FLAGS - Set externally, indicates an action this object must perform.
        self.shutdown = shutdown        # graceful system-wide shutdown, begin exit script
        self.diagnose = diagnose        # diagnostics must be performed
        self.emergency = emergency      # emergency system-wide shutdown, terminate immediately
        
        # STATUS FLAGS - Set internally, notifies other subcomponents of this objects state.
        # !!! HIGH VOLTAGE INDICATOR !!!
        # Set this BEFORE enabling the relay
        # Clear AFTER confirming the relay is disabled
        self.operating = operating      # indicate that diagnostics are being performed
        
        # PROBE INFO
        self.probe_type = PRB.ABS   # specifies the probe's type, in this case abstract
        self.config = config        # dictionary containing relevant configuration data
        self.equations = equations  # list of callables to calculate plasma parameters
        self.data_buff = data_buff  # thread-safe queue, pass data samples to probe operation
        
        # TO DO - Redundant? Is this needed if run() creates a new one every time it pushes to data_buff?
        self.params:dict = None     # used to store data samples and calculated parameters

        # TO DO - PROBE SUBCOMPONENTS
        self._relay = None      # <relay object from hardware interface>
        self._filter = None     # <filter object, package TBD>
    
    # TO DO - ABSTRACT
    def run(self) -> None:
        raise NotImplementedError



# Basic tests
if __name__ == "__main__":
    print("Hello!")
    probe = BaseProbe()
    print("World!")
    print(PRB.ABS)
    

