# author: figueroa_90894@studnt.pupr.edu

from threading import Event     # built-in
from ProbeEnum import PRB       # local

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
        
        # TO DO
        self.params:dict = None
        self._relay = None      # <relay object from hardware interface>
        self._filter = None     # <filter object, package TBD>

    # TO DO - ABSTRACT
    def calc_params(self) -> dict:
        raise NotImplementedError
    
    # TO DO - ABSTRACT
    def run(self) -> None:
        raise NotImplementedError



# Basic tests
if __name__ == "__main__":
    print("Hello!")
    probe = BaseProbe()
    print("World!")
    print(PRB.ABS)
    

