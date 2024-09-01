# author: figueroa_90894@students.pupr.edu

# built-in imports
import sys
import os

from unittest import TestCase, skip, expectedFailure, main as RUNTESTS
from unittest.mock import Mock, MagicMock, create_autospec

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
from probe_operation import ProbeOperation

# RESOURCES FOR INITIALIZATIONA
from counter_wrapper import CounterWrapperTest          # dummy hardware wrapper
from system_flags import StatusFlags, CommandFlags      # system control flags
from config_struct import ConfigStruct
from probe_enum import PRB

# PROBE TYPES FOR TESTING
from Langmuir_Probe import LangmuirProbe
from Energy_Analyzer import EnergyAnalyzer
from Triple_Lang_Voltage import TripleLangVoltage
from Triple_Lang_Current import TripleLangCurrent


test_ready = 'WIP'

class ProbeOperationTest(TestCase):
    # ----- TESTCASE CONFIG ----- #
    def setUp(self):
        self.status, self.commands = self.make_flags()
        self.config_struct = self.make_probe_config()
        self.probe_operation_args = self.make_probe_operation_args()
        
        self.operation = ProbeOperation(**self.probe_operation_args)
        self.probe = None
    
    def tearDown(self):
        del self.status
        del self.commands
        del self.config_struct
        del self.probe_operation_args
        del self.operation
        del self.probe

    # ----- PROBE TESTS ----- #
    def test_make_SLP(self):
        self.probe = self.operation.probe_factory.make(PRB.SLP)
        self.assertIsInstance(self.probe, LangmuirProbe)
    
    def test_make_DLP(self):
        self.probe = self.operation.probe_factory.make(PRB.DLP)
        self.assertIsInstance(self.probe, LangmuirProbe)

    def test_make_TLV(self):
        self.probe = self.operation.probe_factory.make(PRB.TLV)
        self.assertIsInstance(self.probe, TripleLangVoltage)

    def test_make_TLC(self):
        self.probe = self.operation.probe_factory.make(PRB.TLC)
        self.assertIsInstance(self.probe, TripleLangCurrent)

    def test_make_HEA(self):
        self.probe = self.operation.probe_factory.make(PRB.HEA)
        self.assertIsInstance(self.probe, EnergyAnalyzer)

    def test_make_IEA(self):
        self.probe = self.operation.probe_factory.make(PRB.IEA)
        self.assertIsInstance(self.probe, EnergyAnalyzer)

    # def temp(self):
    #     # SLP HARDWARE TESTS
    #     print("SLP RELAY TESTS")
    #     name = "\tslp relay: "
    #     print(name, slp._relay.write(True))
    #     print(name, slp._relay.write(False))
    #     print(name, slp._relay.write(True))
    #     print("SLP SWEEPER TESTS")
    #     name = "\tslp sweeper: "
    #     print(name, slp._sweeper.write(10.0))
    #     print(name, slp._sweeper.write(0.0))
    #     print("SLP COLLECTOR TESTS")
    #     name = "\tslp collector: "
    #     print(name, slp._collector.read())
    #     print(name, slp._collector.read())
    
    # ----- TEST UTILS ----- #
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
    
    def make_probe_operation_args(self):
        probe_operation_args = {
            "config_ref": self.config_struct,
            "status_flags": self.status,
            "command_flags": self.commands,
            "hardware_wrapper_cls": CounterWrapperTest
        }
        return probe_operation_args
    

if __name__ == "__main__":
    RUNTESTS()

