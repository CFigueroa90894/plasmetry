# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings

# built-in imports
from enum import Enum, unique

# ----- LOCAL IMPORTS ----- #
# PARAMETER EQUATIONS
from slp_plasma_parameters import get_equations as slp_equations
from dlp_plasma_parameters import get_equations as dlp_equations
from tlv_plasma_parameters import get_equations as tlv_equations
from tlc_plasma_parameters import get_equations as tlc_equations
from global_parameters import get_equations as analyzers_equations


# PARAMETER EQUATION IDENTIFIERS
@unique # prevent duplicate values
class EQ(Enum):
    """<...>"""
    SLP_EQ = 0  # SLP parameter equations
    DLP_EQ = 1  # DLP parameter equation
    TLV_EQ = 2  # TLP-V parameter equations
    TLC_EQ = 3  # TLP-C parameter equations
    HEA_EQ = 4  # HEA parameter equations
    IEA_EQ = 5  # IEA parameter equations


class CalculationsFactory:
    """<...>"""
    def __new__(cls, equation_type: EQ):
        """<...>"""
        match equation_type:
            case EQ.SLP_EQ:
                return slp_equations()
            case EQ.DLP_EQ:
                return dlp_equations()
            case EQ.TLV_EQ:
                return tlv_equations()
            case EQ.TLC_EQ:
                return tlc_equations()
            case EQ.HEA_EQ | EQ.IEA_EQ:
                return analyzers_equations()
            case _: # edge case handling
                raise ValueError(f"Unknown equation type: {equation_type}")

