# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings
#   - comment init
#   - public methods
#   - integrate with system control
#   - resolve placeholder probe attribute
#   - when done, delete basic tests

# built-in imports
import sys
import os

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 1             # how many parent folders to reach /plasmetry/src

    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..') # absolute path to plasmetry/src
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__'] # get subdirs, exclude __pycache__
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #


# local imports
from probe_factory import ProbeFactory
from hardware_factory import HardwareFactory
from calculations_factory import CalculationsFactory
from daqc2plate_wrapper import DAQC2plateWrapper


class ProbeOperation:
    """<...>"""
    def __init__(self,
                 config_ref,
                 status_flags,
                 command_flags,
                 hardware_wrapper_cls=DAQC2plateWrapper
                 ):
        """"<...>"""
        # Save arguments
        self.commands = command_flags
        self.status = status_flags
        self.config = config_ref
        
        # Instantiate Probe Factory
        probe_factory_args = {
            "config_ref": config_ref,
            "status_flags": status_flags,
            "command_flags": command_flags,
            "hardware_factory": HardwareFactory(hardware_wrapper_cls),
            "calculations_factory": CalculationsFactory
        }
        self.probe_factory = ProbeFactory(**probe_factory_args)

    # TEMPORARY
    def __create_probe_test(self, probe_type):
        return self.probe_factory.make(probe_type)



# PROBE OPERATION TESTS
if __name__ == "__main__":
    print("\n# ----- PROBE OPERATION TESTS ----- #\n")
    
    # local imports
    from counter_wrapper import CounterWrapperTest          # dummy hardware wrapper
    from system_flags import StatusFlags, CommandFlags      # system control flags
    from config_struct import ConfigStruct
    from probe_enum import PRB
    
    # init system flags
    status = StatusFlags()
    commands = CommandFlags()

    
    # init probe configs
    base_probe_config = {
        "sampling_rate": 20,
        "relay_address": 0,
    }
    
    base_tlp_config = {
        "upper_probe_address": 1,
        "upper_amp_address": 2
    }
    
    tlpc_config = {
        "lower_probe_address": 3,
        "lower_amp_address": 4
    }
    
    tlpv_config = {
        "floating_probe_address": 5
    }
    
    sweeper_config = {
        "num_samples": 10,
        "sweeper_address": 6,
        "collector_address": 7
    }
    
    ea_config = {
        "rejector_address": 8,
        "collector_bias_address": 9
    }

    lang_config = {}

    # pack probe config values
    config_values = {
        **base_probe_config,
        **base_tlp_config,
        **tlpc_config,
        **tlpv_config,
        **sweeper_config,
        **ea_config,
        **lang_config
    }
    # init config struct (config_ref)
    config_struct = ConfigStruct(config_values)

    # init probe operation
    probe_operation_args = {
        "config_ref": config_struct,
        "status_flags": status,
        "command_flags": commands,
        "hardware_wrapper_cls": CounterWrapperTest
    }
    print("init probe operation")
    po = ProbeOperation(**probe_operation_args)
    
    # PROBE TESTS
    print("MAKE PROBES")
    slp = po._ProbeOperation__create_probe_test(PRB.SLP)
    dlp = po._ProbeOperation__create_probe_test(PRB.DLP)
    hea = po._ProbeOperation__create_probe_test(PRB.HEA)
    iea = po._ProbeOperation__create_probe_test(PRB.IEA)
    tlc = po._ProbeOperation__create_probe_test(PRB.TLC)
    tlv = po._ProbeOperation__create_probe_test(PRB.TLV)
    



    print()

