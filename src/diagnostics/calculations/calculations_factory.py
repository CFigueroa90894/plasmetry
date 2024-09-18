# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings

# built-in imports
import sys
import os
from enum import Enum, unique

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 2             # how many parent folders to reach /plasmetry/src

    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..') # absolute path to plasmetry/src
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__'] # get subdirs, exclude __pycache__
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #


# ----- LOCAL IMPORTS ----- #
from probe_enum import PRB

# PARAMETER EQUATIONS
from slp_plasma_parameters import get_equations as slp_equations
from dlp_plasma_parameters import get_equations as dlp_equations
from tlv_plasma_parameters import get_equations as tlv_equations
from tlc_plasma_parameters import get_equations as tlc_equations
from global_parameters import get_equations as analyzers_equations


class CalculationsFactory:
    """<...>"""

    # TO DO
    particle_mass = {
        "argon": 1,
        "electron": 2,
    }
    def __new__(cls, equation_type: PRB, config_ref):
        """<...>"""
        match equation_type:
            # Single Langmuir Probe
            case PRB.SLP:
                config_ref["Particle mass"] = cls.particle_mass["electron"]
                return slp_equations()
            
            # Double Langmuir Probe
            case PRB.DLP:
                config_ref["Particle mass"] = cls.particle_mass[config_ref["selected_gas"]]
                return dlp_equations()
            
            # Triple Langmuir Probe - Voltage Mode
            case PRB.TLV:
                config_ref["Particle mass"] = cls.particle_mass[config_ref["selected_gas"]]
                return tlv_equations()
            
            # Triple Langmuir Probe - Current Mode
            case PRB.TLC:
                config_ref["Particle mass"] = cls.particle_mass[config_ref["selected_gas"]]
                return tlc_equations()
            
            # Hyperbolic and Ion Energy Analyzers
            case PRB.HEA | PRB.IEA:
                # Electron collection mode
                if config_ref["collector_bias"] > 0:
                    config_ref["Particle mass"] = cls.particle_mass["electron"]
                # Ion collection mode
                elif config_ref["collector_bias"] < 0:
                    config_ref["Particle mass"] = cls.particle_mass[config_ref["selected_gas"]]
                # Error handling
                else:
                    raise ValueError("HEA/IEA collector bias cannot be 0!")
                return analyzers_equations()
            
            # Error case handling
            case _:
                raise ValueError(f"Unknown equation type: {equation_type}")

