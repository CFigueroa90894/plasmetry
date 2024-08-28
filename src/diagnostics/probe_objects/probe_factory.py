# author:   cases_123268@students.pupr.edu
# modified: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings

# ----- BUILT-IN IMPORTS ----- #
import sys
import os
from enum import Enum, unique
from queue import Queue

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
# CONCRETE PROBE OBJECTS
from Langmuir_Probe import LangmuirProbe
from Triple_Lang_Voltage import TripleLangVoltage
from Triple_Lang_Current import TripleLangCurrent
from Energy_Analyzer import EnergyAnalyzer


# PROBE IDENTIFIERS
@unique # prevent duplicate values
class PRB(Enum):
    """An enumarator class to represent probe types."""
    SLP = 0     # Single Langmuir Probe
    DLP = 1     # Double Langmuir Probe
    HEA = 2     # Hyperbolic Energy Analyzer
    IEA = 3     # Ion Energy Analyzer
    TLC = 4     # Triple Langmuir Probe - Current Mode
    TLV = 5     # Triple Langmuir Probe - Voltage Mode


class ProbeFactory:
    "<...>"
    ID:PRB = PRB   # package factory's valid IDs as class attribute
    
    def __init__(self,
                 config_ref,
                 status_flags,
                 command_flags,
                 hardware_factory,
                 calculations_factory,
                 ):
        """<...>"""
        # Save argument references
        self.config = config_ref
        self.status_flags = status_flags
        self.command_flags = command_flags
        self.hardware_factory = hardware_factory
        self.calculations_factory = calculations_factory

    def make(self, probe_type: PRB):
        """<...>"""
        # Factory aliases
        Equations = self.calculations_factory
        EQ = self.calculations_factory.IDs
        
        # General Probe Arguments - dictionary unpacking depends on named probe parameters
<<<<<<< Updated upstream
        probe_args = {"config_ref": self.config,
=======
<<<<<<< Updated upstream
        probe_args = {"config": self.config,
>>>>>>> Stashed changes
                      "shutdown": self.command_flags.shutdown,
                      "diagnose": self.command_flags.diagnose,
                      "operating": self.status_flags.operating,
                      "data_buff": Queue(),     # new queue every time a probe is instantiated
                      "sampling_rate": self.config.get("sampling_rate"),
                      "hardware_factory": self.hardware_factory
                      }
=======
        probe_args = {
            "config_ref": self.config,
            "shutdown": self.command_flags.shutdown,
            "diagnose": self.command_flags.diagnose,
            "operating": self.status_flags.operating,
            "data_buff": Queue(),     # new queue every time a probe is instantiated
            "hardware_factory_obj": self.hardware_factory
        }
>>>>>>> Stashed changes
        
        # Specific Probe Arguments
        base_probe_args = {
            "sampling_rate": self.config.get("sampling_rate"),
            "relay_address": self.config.get("relay_address")
        }
        sweeper_args = {
            "num_samples": self.config.get("num_samples"),
            "sweeper_address": self.config.get("sweeper_address"),
            "collector_address": self.config.get("collector_address"),
            **base_probe_args   # inherit from base probe
        }
        base_tlp_args = {
            "upper_probe_address": self.config.get("upper_probe_address"),
            "upper_amp_address": self.config.get("upper_amp_address"),
            **base_probe_args   # inherit base probe args
        }
        lp_args = {
            **sweeper_args      # inherit sweeper args
        }
        ea_args = {
            "rejector_address": self.config.get("rejector_address"),
            "collector_bias_address": self.config.get("collector_bias_address"),
            **sweeper_args      # inherit sweeper args 
        }
        tlpc_args = {
            "lower_probe_address": self.config.get("lower_probe_address"),
            "lower_amp_address": self.config.get("lower_amp_address"),
            **base_tlp_args     # inherit base tlp args
        }
        tlpv_args = {
            "floating_probe_address": self.config.get("floating_probe_address"),
            **base_tlp_args     # inherit base tlp args
        }

        # Probe Specific Arguments and Instantiation
        match probe_type:
            # Single Langmuir Probe
            case PRB.SLP:
                Probe_Class = LangmuirProbe
                probe_args["equations"] = Equations(EQ.SLP_EQ)
                end_args = {**probe_args, **lp_args}
            
            # Double Langmuir Probe
            case PRB.DLP:
                Probe_Class = LangmuirProbe
                probe_args["equations"] = Equations(EQ.DLP_EQ)
                end_args = {**probe_args, **lp_args}
            
            # Hyperbolic Energy Analyzer
            case PRB.HEA:
                Probe_Class = EnergyAnalyzer
                probe_args["equations"] = Equations(EQ.HEA_EQ)
                end_args = {**probe_args, **ea_args}
            
            # Ion Energy Analyzer
            case PRB.IEA:
                Probe_Class = EnergyAnalyzer
                probe_args["equations"] = Equations(EQ.IEA_EQ)
                end_args = {**probe_args, **ea_args}
            
            # Triple Langmuir Probe - Voltage Mode
            case PRB.TLV:
                Probe_Class = TripleLangVoltage
                probe_args["equations"] = Equations(EQ.TLV_EQ)
                end_args = {**probe_args, **tlpv_args}
            
            # Triple Langmuir Probe - Current Mode
            case PRB.TLC:
                Probe_Class = TripleLangCurrent
                probe_args["equations"] = Equations(EQ.TLC_EQ)
                end_args = {**probe_args, **tlpc_args}
            
            # Unknown Probe
            case _:
                raise ValueError(f"Unknown probe type: {probe_type}")
        
        # Initialize and return Probe Object using packed arguments.
        return Probe_Class(**end_args)


