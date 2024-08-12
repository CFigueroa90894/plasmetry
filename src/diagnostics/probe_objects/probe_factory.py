
from slp_plasma_parameters import get_equations as slp_equations
from dlp_plasma_parameters import get_equations as dlp_equations
from tlv_plasma_parameters import get_equations as tlv_equations
from global_parameters import get_equations as analyzers_equations

from LangmuirProbe import LangmuirProbe
from BaseTLP import BaseTLP
from EnergyAnalyzers import EnergyAnalyzers

from ProbeEnum import PRB        

class ProbeFactory:
    def __init__(self, probe_type: PRB):
        match probe_type:
            case PRB.SLP:
                self.probe= LangmuirProbe(slp_equations)
            case PRB.DLP:
                self.probe= LangmuirProbe(dlp_equations)
            case PRB.HEA | PRB.IEA: 
                self.probe= EnergyAnalyzers(analyzers_equations)
            case PRB.TLV:
                self.probe= BaseTLP(tlv_equations)
            case _:
                raise ValueError(f"Unknown probe type: {self.probe_type}")
        


