from Single_Langmuir_Probe import Single_Lamguir_Probe
# TO DO - ENFORCE ABSTRACT, and others

def get_probe_object(probe_number):
    
    probe_objects = {
    
        1: Single_Lamguir_Probe(),
        
    }
    return probe_objects[probe_number]  
    
