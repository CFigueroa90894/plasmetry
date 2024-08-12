from threading import Event     # built-in
import queue
from BaseProbe import BaseProbe
from slp_plasma_parameters import get_equations
# TO DO - ENFORCE ABSTRACT, and others
class Single_Lamguir_Probe(BaseProbe):
    # TO DO
    def __init__(self):
        super().__init__()
        self.equations = get_equations()
        # TO DO
        self.data_buffer= queue.Queue()
        self.clock_flag = Event()
        #self.probe_type = PRB.SLP
        
        
        

    
    


