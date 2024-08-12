from Single_Langmuir_Probe import Single_Langmuir_Probe

def get_probe_object(probe_number):
    
    probe_objects = {
    
        1: Single_Langmuir_Probe(),
        
    }
    return probe_objects[probe_number]  
    
