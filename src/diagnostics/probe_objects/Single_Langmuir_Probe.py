from threading import Event     # built-in
import queue
from slp_plasma_parameters import get_equations
import Langmuir_Probe
class Single_Langmuir_Probe(Langmuir_Probe):
    
    def __init__(self):
        
        super().__init__()
        
        self.equations = get_equations()
        
        self.data_buffer= queue.Queue()
        
        self.clock_flag = Event()
        #self.probe_type = PRB.SLP
        
        
        
        

    
    


