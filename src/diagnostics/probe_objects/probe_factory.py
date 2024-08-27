# author:   cases_123268@students.pupr.edu
# modified: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings

# ----- BUILT-IN IMPORTS ----- #
import sys
import os
from enum import Enum, unique
from queue import Queue

# ----- PATH HAMMER ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 2             # how many parent folders to reach /plasmetry/src
    
    # Locate absolute path to /plasmetry/src
    parent = os.path.dirname(__file__)  # traverse directory upwards
    for _ in range(num_dir): parent = os.path.dirname(parent)
    print(f"Path Hammer: {parent}")     # expect absolute path to /plasmetry/src

    # Append all target folders to python path
    for dir in os.listdir(parent): sys.path.append(f"{parent}/{dir}")
    print(f"Path Hammer: folders appended")
# ----- END PATH HAMMER ----- #


# ----- LOCAL IMPORTS ----- #
# CONCRETE PROBE OBJECTS
from probe_objects.concrete_probes.Langmuir_Probe import LangmuirProbe
from probe_objects.concrete_probes.Triple_Lang_Voltage import TripleLangVoltage
from probe_objects.concrete_probes.Triple_Lang_Current import TripleLangCurrent
from probe_objects.concrete_probes.Energy_Analyzer import EnergyAnalyzer


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
    Ids:PRB = PRB   # package factory's valid IDs as class attribute
    
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
        probe_args = {"config": self.config,
                      "shutdown": self.command_flags.shutdown,
                      "diagnose": self.command_flags.diagnose,
                      "emergency": self.command_flags.emergency,
                      "operating": self.status_flags.operating,
                      "data_buff": Queue(),     # new queue every time a probe is instantiated
                      "sampling_rate": self.config.get("sampling_rate"),
                      "hardware_factory": self.hardware_factory
                      }
        
        # Probe Specific Arguments and Instantiation
        match probe_type:
            # Single Langmuir Probe
            case PRB.SLP:
                Probe_Class = LangmuirProbe
                probe_args["equations"] = Equations(EQ.SLP_EQ)
                probe_args["num_samples"] = self.config.get("num_samples") # samples per sweep
            
            # Double Langmuir Probe
            case PRB.DLP:
                Probe_Class = LangmuirProbe
                probe_args["equations"] = Equations(EQ.DLP_EQ)
                probe_args["num_samples"] = self.config.get("num_samples") # samples per sweep
            
            # Hyperbolic Energy Analyzer
            case PRB.HEA:
                Probe_Class = EnergyAnalyzer
                probe_args["equations"] = Equations(EQ.HEA_EQ)
                probe_args["num_samples"] = self.config.get("num_samples") # samples per sweep
            
            # Ion Energy Analyzer
            case PRB.IEA:
                Probe_Class = EnergyAnalyzer
                probe_args["equations"] = Equations(EQ.IEA_EQ)
                probe_args["num_samples"] = self.config.get("num_samples") # samples per sweep
            
            # Triple Langmuir Probe - Voltage Mode
            case PRB.TLV:
                Probe_Class = TripleLangVoltage
                probe_args["equations"] = Equations(EQ.TLV_EQ)
            
            # Triple Langmuir Probe - Current Mode
            case PRB.TLC:
                Probe_Class = TripleLangCurrent
                probe_args["equations"] = Equations(EQ.TLC_EQ)
            
            # Unknown Probe
            case _:
                raise ValueError(f"Unknown probe type: {probe_type}")
        
        # Initialize and return Probe Object using packed arguments.
        return Probe_Class(**probe_args)


