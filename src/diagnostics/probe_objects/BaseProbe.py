# author: figueroa_90894@studnt.pupr.edu

from threading import Event     # built-in
from ProbeEnum import PRB       # local

# TO DO - ENFORCE ABSTRACT, and others
class BaseProbe:
    # TO DO
    def __init__(self, 
                 shutdown_flag:Event=None,
                 run_flag:Event=None,
                 config:dict=None
                 ):
        # --- Parametric Attributes --- #
        self.shutdown_flag = shutdown_flag  # Set externally, signals system-wide shutdown
        self.run_flag = run_flag            # Set externally, signals diagnostics must be performed
        self.config = config                # dictionary containing relevant configuration data

        # --- Non-parametric Attributes --- #
        self.probe_type = PRB.ABS   # Denotes the probe's type, in this case abstract

        # !!! HIGH VOLTAGE INDICATOR !!!
        # Set this BEFORE enabling the relay
        # Clear AFTER confirming the relay is disabled
        self.running:Event = Event()      # Set internally, signals that diagnostics are being performed
        
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
    

