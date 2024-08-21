# author:   cases_123268@students.pupr.edu
# modified: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings
#   - resolve equation imports

# ----- LOCAL IMPORTS ----- #
# PARAMETER EQUATIONS
from slp_plasma_parameters import get_equations as slp_equations
from dlp_plasma_parameters import get_equations as dlp_equations
from tlv_plasma_parameters import get_equations as tlv_equations
from tlc_plasma_parameters import get_equations as tlc_equations
from global_parameters import get_equations as analyzers_equations

# CONCRETE PROBE OBJECTS
from Langmuir_Probe import LangmuirProbe
from Triple_Lang_Voltage import TripleLangVoltage
from Triple_Lang_Current import TripleLangCurrent
from Energy_Analyzer import EnergyAnalyzer

# PROBE IDENTIFIERS
from ProbeEnum import PRB        


class ProbeFactory:
    "<...>"
    def __new__(self, probe_type: PRB):
        match probe_type:
            case PRB.SLP:
                probe = LangmuirProbe(equations=slp_equations)
            case PRB.DLP:
                probe = LangmuirProbe(equations=dlp_equations)
            case PRB.HEA | PRB.IEA:     # how to select particle type for HEA?
                probe = EnergyAnalyzer(equations=analyzers_equations)
            case PRB.TLV:
                probe = TripleLangVoltage(equations=tlv_equations)
            case PRB.TLC:
                probe = TripleLangCurrent(equations=tlc_equations)
            case _: # edge case handling
                raise ValueError(f"Unknown probe type: {self.probe_type}")
        return probe


