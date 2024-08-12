from threading import Event     # built-in
import queue
from slp_plasma_parameters import get_equations
import Langmuir_Probe
# TO DO - ENFORCE ABSTRACT, and others
class Single_Lamguir_Probe(Langmuir_Probe):
    # TO DO
    def __init__(self):
        super().__init__()
        self.equations = get_equations()
        # TO DO
        self.data_buffer= queue.Queue()
        self.clock_flag = Event()
        #self.probe_type = PRB.SLP
        
        
        
        

    
    


