# author: figueroa_90894@students.pupr.edu

# built-in imports
import sys
import os

from unittest import TestCase, main as RUNTESTS, skip

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


# SYSTEM UNDER TEST
from probe_factory import ProbeFactory

# RESOURCES FOR INITIALIZATION
from counter_wrapper import CounterWrapperTest          # dummy hardware wrapper
from system_flags import StatusFlags, CommandFlags      # system control flags
from config_struct import ConfigStruct                  # thread-safe container
from hardware_factory import HardwareFactory            # instantiates hardware interface objects
from calculations_factory import CalculationsFactory    # returns probe specific equations

# PROBE TYPES FOR TESTING
from probe_enum import PRB
from Base_Probe import BaseProbe
from Sweeper_Probe import SweeperProbe
from Langmuir_Probe import LangmuirProbe
from Energy_Analyzer import EnergyAnalyzer
from Base_TLP import BaseTLP
from Triple_Lang_Voltage import TripleLangVoltage
from Triple_Lang_Current import TripleLangCurrent



class ProbeFactory_TestTemplate(TestCase):
    # ----- TESTCASE CONFIG ----- #
    def setUp(self):
        self.status, self.commands = self.make_flags()
        self.config_struct = self.make_probe_config()
        self.probe_factory_args = self.make_probe_factory_args()
        
        self.factory = ProbeFactory(**self.probe_factory_args)
        self.probe = None
        self.state = None
    
    def tearDown(self):
        del self.status
        del self.commands
        del self.config_struct
        del self.probe_factory_args
        del self.factory
        del self.probe
        del self.state

    def make_flags(self):
        status = StatusFlags()
        commands = CommandFlags()
        return status, commands

    def make_probe_config(self):
        probe_config = {
            "sampling_rate": 20,
            "relay_address": 0,
            "upper_probe_address": 1,
            "upper_amp_address": 2,
            "lower_probe_address": 3,
            "lower_amp_address": 4,
            "floating_probe_address": 5,
            "num_samples": 10,
            "sweeper_address": 6,
            "collector_address": 7,
            "rejector_address": 8,
            "collector_bias_address": 9
        }
        return ConfigStruct(probe_config)
    
    def make_probe_factory_args(self):
        factory_args = {
            "config_ref": self.config_struct,
            "status_flags": self.status,
            "command_flags": self.commands,
            "hardware_factory": HardwareFactory(CounterWrapperTest),
            "calculations_factory": CalculationsFactory
        }
        return factory_args

class ProbeFactoryTest(ProbeFactory_TestTemplate):
    # ----- PROBE CREATION ----- #
    def test_make_all(self):
        """Make all probes supported by enum PRB."""
        for ID in PRB:
            with self.subTest(PROBE_ID = ID):
                self.probe = self.factory.make(ID)

    def test_make_invalid(self):
        """Raise an error for unknown probe types."""
        self.assertRaises(ValueError, self.factory.make, None)


class ProbeObj_TestTemplate(ProbeFactory_TestTemplate):
    # ----- TEST UTILS ----- #
    def check_inheritance(self, parents):
        for par in parents:
            with self.subTest(PARENT_CLASS = par):
                self.assertIsInstance(self.probe, par)


if __name__ == "__main__":
    RUNTESTS(verbosity=2)
    sys.exit(0)