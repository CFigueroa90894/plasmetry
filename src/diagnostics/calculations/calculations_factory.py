# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings

# built-in imports
import sys
import os
from enum import Enum, unique

# ----- PATH HAMMER v2.3 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 2             # how many parent folders to reach /plasmetry/src

    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..') # absolute path to plasmetry/src
    print(f"Path Hammer: {src_abs}")
    targets = [x[0] for x in os.walk(src_abs) if x[0][-1]!='_']          # all subdirectories, except __pycache__
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #


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
    IDs:EQ = EQ     # package factory's valid IDs as class attribute

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

