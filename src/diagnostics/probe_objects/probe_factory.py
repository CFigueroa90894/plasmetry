# author:   cases_123268@students.pupr.edu
# modified: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings

# ----- BUILT-IN IMPORTS ----- #
import sys
import os
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
from probe_enum import PRB

# CONCRETE PROBE OBJECTS
from Langmuir_Probe import LangmuirProbe
from Triple_Lang_Voltage import TripleLangVoltage
from Triple_Lang_Current import TripleLangCurrent
from Energy_Analyzer import EnergyAnalyzer


class ProbeFactory:
    "<...>"
    
    def __init__(self,
                 status_flags,
                 command_flags,
                 hardware_factory,
                 calculations_factory,
                 ):
        """<...>"""
        # Save argument references
        self.config = None
        self.system = None
        self.probe_name
        self.status_flags = status_flags
        self.command_flags = command_flags
        self.hardware_factory = hardware_factory
        self.calculations_factory = calculations_factory

    def make(self, probe_type: PRB, config_ref:dict, sys_ref:dict, probe_name="PROBE"):
        """<...>"""
        self.config = config_ref
        self.system = sys_ref
        # Package probe config by ID
        match probe_type:
            # Single Langmuir Probe
            case PRB.SLP:
                Probe_Class = LangmuirProbe
                probe_args = self._pack_lp()
            
            # Double Langmuir Probe
            case PRB.DLP:
                Probe_Class = LangmuirProbe
                probe_args = self._pack_lp()
            
            # Hyperbolic Energy Analyzer
            case PRB.HEA:
                Probe_Class = EnergyAnalyzer
                probe_args = self._pack_ea()
            
            # Ion Energy Analyzer
            case PRB.IEA:
                Probe_Class = EnergyAnalyzer
                probe_args = self._pack_ea()
            
            # Triple Langmuir Probe - Voltage Mode
            case PRB.TLV:
                Probe_Class = TripleLangVoltage
                probe_args = self._pack_tlpv()
            
            # Triple Langmuir Probe - Current Mode
            case PRB.TLC:
                Probe_Class = TripleLangCurrent
                probe_args = self._pack_tlpc()
            
            # Unknown Probe
            case _:
                raise ValueError(f"Unknown probe type: {probe_type}")
        
        probe_args["probe_id"] = probe_type
        probe_args["equations"] = self.calculations_factory(probe_type)
        
        # Initialize and return Probe Object using packed arguments.
        return Probe_Class(**probe_args)
    

    # ----- PROBE ARGUMENT PACKACKING ----- #
    
    # GENERAL CONFIG ARTIFACTS
    def __pack_general(self) -> dict:
        """<...>"""
        args = {
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
            "sampling_rate": self.config["sampling_rate"],
            "relay_address": self.system["relay_address"],
            **self.__pack_general()     # inherit general args
        }
        return args
    
    # SWEEPER PROBE CONFIG (abstract)
    def __pack_sweeper(self):
        """<...>"""
        args = {
            "num_samples": self.config["num_samples"],
            "sweeper_address": self.system["sweeper_address"],
            "collector_address": self.system["collector_address"],
            **self.__pack_base_probe()  # inherit base probe args
        }
        return args
    
    # BASE TLP CONFIG (abstract)
    def __pack_base_tlp(self):
        """<...>"""
        args = {
            "upper_probe_address": self.system["upper_probe_address"],
            "upper_amp_address": self.system["upper_amp_address"]
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
            "rejector_address": self.system["rejector_address"],
            "collector_bias_address": self.system["collector_bias_address"],
            **self.__pack_sweeper()     # inherit sweeper args 
        }
        return args

    # TRIPLE LANGMUIR PROBE - CURRENT MODE CONFIG (concrete)
    def _pack_tlpc(self) -> dict:
        """<...>"""
        args = {
            "lower_probe_address": self.system["lower_probe_address"],
            "lower_amp_address": self.system["lower_amp_address"],
            **self.__pack_base_tlp()    # inherit base tlp args
        }
        return args

    # TRIPLE LANGMUIR PROBE - VOLTAGE MODE CONFIG (concrete)
    def _pack_tlpv(self) -> dict:
        """<...>"""
        args = {
            "floating_probe_address": self.system["floating_probe_address"],
            **self.__pack_base_tlp()    # inherit base tlp args
        }
        return args


