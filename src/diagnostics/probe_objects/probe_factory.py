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

    # absolute path to plasmetry/src
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..')
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    # get subdirs, exclude __pycache__
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__']
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
        self.status_flags = status_flags
        self.command_flags = command_flags
        self.hardware_factory = hardware_factory
        self.COMP = hardware_factory.ID
        self.calculations_factory = calculations_factory

    def make(self, probe_type: PRB, config_ref:dict, sys_ref:dict, probe_name="PROBE"):
        """<...>"""
        self.config = config_ref
        self.system = sys_ref
        
        # Package probe specific config by ID
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
        
        # pack general config
        probe_args["probe_id"] = probe_type
        probe_args["equations"] = self.calculations_factory(probe_type, self.config)
        probe_args["name"] = probe_name
        #probe_args["text_out"] = config_ref["text_out"]
        
        # Initialize and return Probe Object using packed arguments.
        return Probe_Class(**probe_args)
    

    # ----- PROBE ARGUMENT PACKAGING ----- #
    
    # GENERAL CONFIG ARTIFACTS
    def __pack_general(self) -> dict:
        """<...>"""
        args = {
            "sys_ref": self.system,
            "config_ref": self.config,
            "status_flags": self.status_flags,
            "command_flags": self.command_flags,
            "data_buff": Queue()     # new queue every time a probe is instantiated
        }
        return args

    # BASE PROBE CONFIG (abstract)
    def __pack_base_probe(self):
        """<...>"""

        # make relay subcomponent
        relays = self.__make_relays(
            addresses=self.system["relay_addresses"]
        )
        # pack probe args
        probe_args = {
            "sampling_rate": self.config["sampling_rate"],
            "relay_set": relays,
            "num_samples": self.config["num_samples"],
            **self.__pack_general()     # inherit general args
        }
        return probe_args
    
    # SWEEPER PROBE CONFIG (abstract)
    def __pack_sweeper(self):
        """<...>"""

        base_probe_args = self.__pack_base_probe()
        # shared argument
        dac_range = {
            "min": self.config["dac_min"],
            "max": self.config["dac_max"]
        }
        # make sweeper subcomponent
        sweep_amp_range = {
            "min": self.config["sweep_amp_min"],
            "max": self.config["sweep_amp_max"]
        }
        sweeper = self.__make_sweeper(
            address=self.system["sweeper_address"],
            num_samples=base_probe_args["num_samples"],
            dac_range=dac_range,
            amp_range=sweep_amp_range,
            sweep_min=self.config["sweep_min"],
            sweep_max=self.config["sweep_max"]
        )
        # make collector subcomponent
        collector = self.__make_volt_sens(
            address=self.system["collector_address"],
            gain=self.config["collector_gain"]
        )
        # pack probe args
        args = {
            "sweeper": sweeper,
            "collector": collector,
            "sweeper_shunt": self.config["sweeper_shunt"],
            **base_probe_args  # inherit base probe args
        }
        return args
    
    # BASE TLP CONFIG (abstract)
    def __pack_base_tlp(self):
        """<...>"""
        # make upper probe bias amp
        dac_range = {
            "min": self.config["dac_min"],
            "max": self.config["dac_max"]
        }
        up_amp_range = {
            "min": self.config["up_amp_min"],
            "max": self.config["up_amp_max"]
        }
        up_amp = self.__make_hv_amp(
            address=self.system["up_amp_address"],
            dac_range=dac_range,
            amp_range=up_amp_range
        )
        # make upper probe collector
        up_collector = self.__make_volt_sens(
            address=self.system["up_collector_address"],
            gain=self.config["up_collector_gain"]
        )
        # pack probe args
        args = {
            "up_amp_bias": self.config["up_amp_bias"],
            "up_amp": up_amp,
            "up_collector": up_collector,
            "up_shunt": self.config["up_shunt"]
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
        
        # pack DAC range arguments (shared for all amps)
        dac_range = {
            "min": self.config["dac_min"],
            "max": self.config["dac_max"]
        }
        # make rejector bias amp
        rejector_range = {
            "min": self.config["rejector_min"],
            "max": self.config["rejector_max"]
        }
        rejector_amp = self.__make_hv_amp(
            address=self.system["rejector_address"],
            dac_range=dac_range,
            amp_range=rejector_range
        )
        # make collector bias amp
        collector_bias_range = {
            "min": self.config["collector_bias_min"],
            "max": self.config["collector_bias_max"]
        }
        collector_amp = self.__make_hv_amp(
            address=self.system["collector_bias_address"],
            dac_range=dac_range,
            amp_range=collector_bias_range
        )
        # pack probe args
        args = {
            "rejector_bias": self.config["rejector_bias"],
            "rejector_amp": rejector_amp,
            "collector_bias": self.system["collector_bias"],
            "collector_amp": collector_amp,
            **self.__pack_sweeper()     # inherit sweeper args 
        }
        return args

    # TRIPLE LANGMUIR PROBE - CURRENT MODE CONFIG (concrete)
    def _pack_tlpc(self) -> dict:
        """<...>"""
        # pack DAC range arguments (shared for all amps)
        dac_range = {
            "min": self.config["dac_min"],
            "max": self.config["dac_max"]
        }
        # make down probe bias amp
        down_amp_range = {
            "min": self.config["down_amp_min"],
            "max": self.config["down_amp_max"]
        }
        down_amp = self.__make_hv_amp(
            address=self.system["down_amp_address"],
            dac_range=dac_range,
            amp_range=down_amp_range
        )
        # make down probe collector
        down_collector = self.__make_volt_sens(
            address=self.system["down_collector_address"],
            gain=self.config["down_collector_gain"]
        )
        # pack probe args
        args = {
            "down_amp_bias": self.config["down_amp_bias"],
            "down_amp": down_amp,
            "down_collector": down_collector,
            "down_shunt": self.config["down_shunt"]
            **self.__pack_base_tlp()    # inherit base tlp args
        }
        return args

    # TRIPLE LANGMUIR PROBE - VOLTAGE MODE CONFIG (concrete)
    def _pack_tlpv(self) -> dict:
        """<...>"""
        # make floating probe collector
        float_collector = self.__make_volt_sens(
            address=self.system["float_collector_address"],
            gain=self.config["float_collector_gain"]
        )
        args = {
            "float_collector": float_collector,
            **self.__pack_base_tlp()    # inherit base tlp args
        }
        return args
    
    # ----- SUBCOMPONENT INSTANTIATION ----- #
    
    # Generic component factory call
    def __make_component(self, args):
        return self.hardware_factory.make(**args)

    # VoltageSensor
    def __make_volt_sens(self, address, gain):
        """<...>"""
        args = {
            "type": self.COMP.VSENS,
            "address": address,
            "gain": gain
        }
        return self.__make_component(args)
        
    # HighVoltAmp
    def __make_hv_amp(self, address, dac_range, amp_range):
        """<...>"""
        args = {
            "type": self.COMP.HVAMP,
            "address": address,
            "dac_range": dac_range,
            "amp_range": amp_range
        }
        return self.__make_component(args)

    # VoltageSweeper
    def __make_sweeper(self, address, dac_range, amp_range, num_samples, sweep_min, sweep_max):
        """<...>"""
        args = {
            "type": self.COMP.SWEEP,
            "address": address,
            "dac_range": dac_range,
            "amp_range": amp_range,
            "num_samples": num_samples,
            "sweep_min": sweep_min,
            "sweep_max": sweep_max
        }
        return self.__make_component(args)

    # RelaySet
    def __make_relays(self, addresses):
        """<...>"""
        args = {
            "type": self.COMP.RLSET,
            "address": addresses
        }
        return self.__make_component(args)


