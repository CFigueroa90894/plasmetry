# author:   cases_123268@students.pupr.edu
# modified: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings
#   - resolve equation imports

import sys
import os
from enum import Enum, unique

# ----- LOCAL IMPORTS ----- #
# add the src folder to the python path to locate local modules
if __name__ == "__main__":
    target = os.path.dirname(__file__)  # probe_objects
    target = os.path.dirname(target)    # diagnostics
    target = os.path.dirname(target)    # src
    sys.path.append(target)             # add src for absolute imports

# PARAMETER EQUATIONS
from slp_plasma_parameters import get_equations as slp_equations
from dlp_plasma_parameters import get_equations as dlp_equations
from tlv_plasma_parameters import get_equations as tlv_equations
from tlc_plasma_parameters import get_equations as tlc_equations
from global_parameters import get_equations as analyzers_equations

# CONCRETE PROBE OBJECTS
from diagnostics.probe_objects.concrete_probes.Langmuir_Probe import LangmuirProbe
from diagnostics.probe_objects.concrete_probes.Triple_Lang_Voltage import TripleLangVoltage
from diagnostics.probe_objects.concrete_probes.Triple_Lang_Current import TripleLangCurrent
from diagnostics.probe_objects.concrete_probes.Energy_Analyzer import EnergyAnalyzer


# PROBE IDENTIFIERS
@unique # prevent duplicate values
class PRB(Enum):
    """An enumarator class to represent probe types."""
    ABS = 0     # abstract probe type
    SLP = 1     # Single Langmuir Probe
    DLP = 2     # Double Langmuir Probe
    HEA = 3     # Hyperbolic Energy Analyzer
    IEA = 4     # Ion Energy Analyzer
    TLC = 5     # Triple Langmuir Probe - Current Mode
    TLV = 6     # Triple Langmuir Probe - Voltage Mode    


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


