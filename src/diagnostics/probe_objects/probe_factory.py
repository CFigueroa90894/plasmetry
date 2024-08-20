
from slp_plasma_parameters import get_equations as slp_equations
from dlp_plasma_parameters import get_equations as dlp_equations
from tlv_plasma_parameters import get_equations as tlv_equations
from tlc_plasma_parameters import get_equations as tlc_equations
from global_parameters import get_equations as analyzers_equations

from LangmuirProbe import LangmuirProbe
from BaseTLP import BaseTLP
from EnergyAnalyzers import EnergyAnalyzers

from ProbeEnum import PRB        

class ProbeFactory:
    def __new__(self, probe_type: PRB):
        match probe_type:
            case PRB.SLP:
                probe= LangmuirProbe(slp_equations)
            case PRB.DLP:
                probe= LangmuirProbe(dlp_equations)
            case PRB.HEA | PRB.IEA: 
                probe= EnergyAnalyzers(analyzers_equations)
            case PRB.TLV:
                probe= BaseTLP(tlv_equations)
            case PRB.TLC:
                probe= BaseTLP(tlc_equations)
            case _:
                raise ValueError(f"Unknown probe type: {self.probe_type}")
        return probe


