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

        # Factory alias
        Equations = self.calculations_factory
        EQ = self.calculations_factory.ID

        # Package probe config by ID
        match probe_type:
            # Single Langmuir Probe
            case PRB.SLP:
                Probe_Class = LangmuirProbe
                probe_args = self._pack_lp()
                probe_args["equations"] = Equations(EQ.SLP_EQ)
            
            # Double Langmuir Probe
            case PRB.DLP:
                Probe_Class = LangmuirProbe
                probe_args = self._pack_lp()
                probe_args["equations"] = Equations(EQ.DLP_EQ)
            
            # Hyperbolic Energy Analyzer
            case PRB.HEA:
                Probe_Class = EnergyAnalyzer
                probe_args = self._pack_ea()
                probe_args["equations"] = Equations(EQ.HEA_EQ)
            
            # Ion Energy Analyzer
            case PRB.IEA:
                Probe_Class = EnergyAnalyzer
                probe_args = self._pack_ea()
                probe_args["equations"] = Equations(EQ.IEA_EQ)
            
            # Triple Langmuir Probe - Voltage Mode
            case PRB.TLV:
                Probe_Class = TripleLangVoltage
                probe_args = self._pack_tlpv()
                probe_args["equations"] = Equations(EQ.TLV_EQ)
            
            # Triple Langmuir Probe - Current Mode
            case PRB.TLC:
                Probe_Class = TripleLangCurrent
                probe_args = self._pack_tlpc()
                probe_args["equations"] = Equations(EQ.TLC_EQ)
            
            # Unknown Probe
            case _:
                raise ValueError(f"Unknown probe type: {probe_type}")
        
        probe_args["probe_id"] = probe_type
        
        # Initialize and return Probe Object using packed arguments.
        return Probe_Class(**probe_args)
    

    # ----- PROBE ARGUMENT PACKACKING ----- #
    
    # GENERAL CONFIG ARTIFACTS
    def __pack_general(self) -> dict:
        """<...>"""
        args = {
            "config_ref": self.config,
            "shutdown": self.command_flags.shutdown,
            "diagnose": self.command_flags.diagnose,
            "operating": self.status_flags.operating,
            "data_buff": Queue(),     # new queue every time a probe is instantiated
            "hardware_factory_obj": self.hardware_factory
        }
        return args

    # BASE PROBE CONFIG (abstract)
    def __pack_base_probe(self):
        """<...>"""
        args = {
            "sampling_rate": self.config.get("sampling_rate"),
            "relay_address": self.config.get("relay_address"),
            **self.__pack_general()     # inherit general args
        }
        return args
    
    # SWEEPER PROBE CONFIG (abstract)
    def __pack_sweeper(self):
        """<...>"""
        args = {
            "num_samples": self.config.get("num_samples"),
            "sweeper_address": self.config.get("sweeper_address"),
            "collector_address": self.config.get("collector_address"),
            **self.__pack_base_probe()  # inherit base probe args
        }
        return args
    
    # BASE TLP CONFIG (abstract)
    def __pack_base_tlp(self):
        """<...>"""
        args = {
            "upper_probe_address": self.config.get("upper_probe_address"),
            "upper_amp_address": self.config.get("upper_amp_address"),
            **self.__pack_base_probe()  # inherit base probe args
        }
        return args

    # LANGMUIR PROBE CONFIG (concrete)
    def _pack_lp(self) -> dict:
        """<...>"""
        args = {
            **self.__pack_sweeper()     # inherit sweeper args
        }
        return args
    
    # ENERGY ANALYZER CONFIG (concrete)
    def _pack_ea(self) -> dict:
        """<...>"""
        args = {
            "rejector_address": self.config.get("rejector_address"),
            "collector_bias_address": self.config.get("collector_bias_address"),
            **self.__pack_sweeper()     # inherit sweeper args 
        }
        return args

    # TRIPLE LANGMUIR PROBE - CURRENT MODE CONFIG (concrete)
    def _pack_tlpc(self) -> dict:
        """<...>"""
        args = {
            "lower_probe_address": self.config.get("lower_probe_address"),
            "lower_amp_address": self.config.get("lower_amp_address"),
            **self.__pack_base_tlp()    # inherit base tlp args
        }
        return args

    # TRIPLE LANGMUIR PROBE - VOLTAGE MODE CONFIG (concrete)
    def _pack_tlpv(self) -> dict:
        """<...>"""
        args = {
            "floating_probe_address": self.config.get("floating_probe_address"),
            **self.__pack_base_tlp()    # inherit base tlp args
        }
        return args


