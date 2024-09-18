""" G3 - Plasma Devs
Layer 3 - Diagnostics - Concrete Implementation
    Provides the main implementation for the Diagnostics Layer, assembling its subcomponents and
    exposing the layer's public functionality.

author: figueroa_90894@students.pupr.edu
status: WIP
    - add docstrings
    - uncomment hardware shutdown when implemented (in diagnostics_shutdown)
    - validate with team
"""
# built-in imports
import sys
import os
import inspect

from queue import Queue, Full
from threading import Event

# ----- PATH HAMMER v2.7 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:
    """Resolve absolute imports by recusring into subdirs and appending them to the python path."""
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    assert src_abs.split('\\')[-1*len(root_target):] == root_target   # validate correct top folder
    
    # get subdirs, exclude unwanted
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split('\\')[-1] not in exclude]
    for dir in dirs: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: {src_abs}")

if __name__ == "__main__":  # execute path hammer if this script is run directly
    path_hammer(1, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #


# TO DO - remove relative imports
# local imports
from abstract_diagnostics import AbstractDiagnostics


# TO TO
class DiagnosticsLayer(AbstractDiagnostics):
    """<...>"""

    # Default subcomponent module names
    calculations_factory_mod = 'calculations_factory'
    probe_factory_mod = 'probe_factory'
    probe_operation_mod = 'probe_operation'

    # Default lower layer module name
    hardware_layer_mod = 'hardware_layer'


    def __init__(self,
                 status_flags,
                 command_flags,
                 results_buffer:Queue=None,
                 real_time_param:dict=None,
                 name:str="DIAGN",
                 perform_calculations:bool=True,
                 debug:bool=True,
                 *args, **kwargs
        ):
        """<...>"""
        super().__init__(*args, name=name, **kwargs)   # call parent constructor

        # default buffer if none was specified
        if results_buffer is None:
            results_buffer = Queue()    # redefine arg variable
        
        # default dict if none was specified
        if real_time_param is None:
            real_time_param = {}        # redefine arg variable


        # ----- Save Arguments ----- #
        self._status = status_flags     # system state indicators
        self._command = command_flags   # action triggers
        self._result_buff = results_buffer         # buffer to pass experiment results up the stack
        self._real_time_param = real_time_param
        self.calculate = perform_calculations
        self.debug = debug

        # ----- Assemble Diagnostic Layer ----- #
        sub = self._load_all_subcomponents()   # import subcomponents, returned in a dict
        
        # instantiate lower layer
        self._hardware = sub["hardware_layer"](text_out=self._say_obj)  # lower layer interface
        self._comp_fac = self._hardware.get_component_factory() # makes hardware components

        # prepare factories
        self._calc_fac = sub["calc_fac"]  # makes probe equation sets, callable, not instantiable
        self._probe_fac = sub["probe_fac"](**self.__probe_factory_args()) # makes specific probes
        
        # prepare probe op for later instantiation
        self._probe_op_cls = sub["probe_op"]  # reference to class, NOT the object
        self._probe_op = None # probe operation is instantiated during setup

        # local state indicators
        self._ready = Event()
        self._terminated = Event()
        self._performing_diagnostics = Event()
        self._ready.clear()
        self._terminated.clear()
        self._performing_diagnostics.clear()

        self.say(f"DEBUG - {self.debug}")
        self.say("diagnostics layer initialized...")
        

    # ----- LAYER PUBLIC METHODS ----- #

    # TO DO
    # User confirms config and prepares to begin experiment
    def setup_diagnostics(self, sys_ref:dict, config_ref:dict):
        """Called by upper layers to prepare the diagnostic layer for plasma diagnostic operations.
        
        Instantiates and primes all required plasma diagnostic objects, then awaits until this
        interface's `start_diagnostics()` method is called to proceed.

        Arguments:
            sys_ref: `ProtectedDictionary` containing probe specific system settings
            config_ref: `ProtectedDictionary` containing probe specific user settings

        Exceptions:
            RuntimeError: `setup_diagnostics()` was called while:
                - plasma diagnostics are being performed, or
                - system shutdown is underway, or
                - probe operation did not arm correctly
        """
        # validate system is not operating before proceeding
        if self._are_we_diagnosing():
            raise RuntimeError("Cannot call 'setup_diagnostics' while diagnostics are underway!")
        
        # validate system is not undergoing shutdown before proceeding
        elif self._command.shutdown.is_set():
            raise RuntimeError("Cannot call 'setup_diagnostics' while system shutdown is underway!")

        # checks successful, start plasma diagnostics
        else:
            self.say("preparing for diagnostics...")

            # prepare the probe operation thread
            args = self.__probe_op_args()                # prepared from instance attributes
            
            # instantiate ProbeOperation
            self._probe_op = self._probe_op_cls(
                perform_calculation=self.calculate,
                debug=self.debug, 
                **args)
            self._probe_op.arm(sys_ref, config_ref)      # prepare thread for diagnostics

            # confirm subcomponents are ready for diagnostics
            if self._probe_op._ready.is_set():
                self._ready.set()
                self.say("READY")
            else:
                raise RuntimeError("Could not arm Probe Operation!")
    
    # TO DO
    def start_diagnostics(self):
        """Called by upper layers to trigger plasma diagnostics operations in this layer.

        Exceptions:
            RutimeError: `start_diagnostics()` was called:
                - without first calling `setup_diagnostics()`, or
                - while system shutdown was underway, or
                - if probe operation is not ready to diagnose, or
                - diagnostics are already underway
        """

        # validate system is not undergoing shutdown
        if self._command.shutdown.is_set():
            raise RuntimeError("Cannot call 'start_diagnostics' while shutdown is underway!")
    
        # validate layer is ready to perform plasma diagnostics
        # would be true if system shutdown is underway, therefore must evaluate after
        elif not self._ready.is_set():
            raise RuntimeError("Cannot begin diagnostics before setup_diagnostics is called!")

        # validate diagnostics are not already underway
        elif self._are_we_diagnosing():
            raise RuntimeError("Called 'start_diagnostics' while diagnostics already underway!")
        
        # validate ProbeOperation is ready to perform plasma diagnostics
        elif not self._probe_op._ready.is_set():
            raise RuntimeError("Probe Operation is not ready for diagnostics!")
        
        # all checks successful, start diagnostics
        else:
            self.say("starting diagnostics...")
            self._command.diagnose.set()    # notify data acquisition threads may proceed
            self._probe_op.start()          # launch Probe Operation thread
            self._ready.clear()             # cannot be ready for diagnostics while already underway
            self._performing_diagnostics.set()  # set local state
    
    # TO DO
    def stop_diagnostics(self):
        """Called by upper layers to halt plasma diagnostics operations in this layer.
        
        This layer will attempt to complete all pending operations, including data sampling, 
        parameter calculations, and aggregating results, and passing them to the upper layer before
        it returns to its idle state.
        
        Exceptions:
            RuntimeError: `stop_diagnostics()` was called while:
                - system was not performing plasma diagnostics
        """
        # check if diagnostics are not being performed
        if not self._are_we_diagnosing():
            raise RuntimeError("Called 'stop_diagnostics' while none are being performed!")

        # checks passed, attempting to stop diagnostic threads
        else:
            self.say("stopping diagnostics...")
            if not self._probe_op.is_alive():
                self.say("ProbeOperation was already terminated!")
            self._command.diagnose.clear()  # indicate diagnostics should stop
            self.say("waiting for ProbeOperation to exit...")
            self._probe_op.join()           # wait until probe op thread exits...
            self.say("ProbeOperation exited")
            self._performing_diagnostics.clear()  # reset local state indicator

    # TO DO
    def diagnostics_shutdown(self):
        """Called by upper layers to initiates this layer's shutdown process.
        
        This Diagnostic Layer will attempt to complete all pending operations before finally
        terminating all its subcomponents.

        * NOTE: this call blocks until the diagnostic layer has terminated to prevent corruption.
        """
        self.say("initiating local layer shutdown...")
        
        # stop diagnostics
        if self._are_we_diagnosing():
            self.stop_diagnostics()
        else:
            self.say("diagnostics are already halted.")
        
        # destroy subcomponents
        self.say("deleting subcomponents...")
        del self._probe_op
        del self._probe_op_cls
        del self._probe_fac
        del self._calc_fac
        
        # TO DO - implement in hardware layer
        # destroy lower layer references
        # self.say("terminating hardware layer...")
        # self._hardware.layer_shutdown()
        # self._hardware._terminated.wait()
        # del self._hardware

        self.say("layer shutdown complete.")
        self._terminated.set()

    # ----- Layer Specific Utils ----- #
    def _are_we_diagnosing(self) -> bool:
        """<...>"""
        # aggregate diagnostic indicators
        state = self._command.diagnose.is_set() 
        state = state or self._status.operating.is_set() 
        state = state or self._performing_diagnostics.is_set()  
        return state
    
    def _load_all_subcomponents(self):
        """<...>"""
        # load subcomponent modules
        calculations_factory_mod = self._load_mod(self.calculations_factory_mod)
        probe_factory_mod = self._load_mod(self.probe_factory_mod)
        probe_operation_mod = self._load_mod(self.probe_operation_mod)

        # load subcomponent classes
        calc_fac_cls = calculations_factory_mod.CalculationsFactory
        probe_fac_cls = probe_factory_mod.ProbeFactory
        probe_op_cls = probe_operation_mod.ProbeOperation

        # load lower layer
        hardware_layer_mod = self._load_mod(self.hardware_layer_mod)
        hardware_layer_cls = hardware_layer_mod.HardwareLayer

        # pack and return subcomponent classes
        classes = {
            "calc_fac": calc_fac_cls,
            "probe_fac": probe_fac_cls,
            "probe_op": probe_op_cls,
            "hardware_layer": hardware_layer_cls
        }
        return classes
    
    def _load_mod(self, mod):
        """<...>"""
        # check the module was specified as a string
        if inspect.ismodule(mod):
            pass
        elif isinstance(mod, str):
            mod = __import__(mod)
        else:
            raise TypeError(f"Class attribute {mod} must be module or string! Given {type(mod)}")
        return mod
    
    # TO DO
    def _info(self):
        """<...>"""
        sub = [
            ("Diagnostics", "Calculations Factory", str(self._calc_fac)),
            ("Diagnostics", "Probe Factory", str(self._probe_fac)),
            ("Diagnostics", "Probe Operation", str(self._probe_op_cls)),
            ("Diagnostics", "Hardware Interface", str(self._hardware))
        ]
        sub.extend(self._hardware._info())
        return sub

    def __probe_factory_args(self):
        """<...>"""
        probe_factory_args = {
            "status_flags": self._status,
            "command_flags": self._command,
            "hardware_factory": self._comp_fac,
            "calculations_factory": self._calc_fac
        }
        return probe_factory_args

    def __probe_op_args(self):
        """<...>"""
        probe_op_args = {
            "status_flags": self._status,
            "command_flags": self._command,
            "results_buffer": self._result_buff,
            "real_time_param": self._real_time_param,
            "probe_factory": self._probe_fac,
            "text_out": self._say_obj
        }
        return probe_op_args


# Basic tests
if __name__ == "__main__":
    
    # built-in imports
    import time
    import datetime

    # local imports
    from system_flags import StatusFlags, CommandFlags
    import hardware_layer
    from probe_enum import PRB
    from printer_thread import PrinterThread
    
    # init control objects
    status = StatusFlags()
    commands = CommandFlags()
    kill = Event()

    # init printer thread
    fname = str(datetime.datetime.now()).replace(':', '_')
    f = open(f"test_logs/TEST_{fname}.txt", 'a')
    out = [None, f]
    printer = PrinterThread(kill=kill, text_out=out)
    writer = printer.get_writer()


    writer(f"# {fname}")

    # start printer
    printer.start()

    # configure custom layers for test
    hardware = hardware_layer
    hardware.HardwareLayer.hardware_wrapper_mod = 'counter_wrapper'
    diagnostics = DiagnosticsLayer
    diagnostics.hardware_layer_mod = hardware

    # init diagnostics layer
    diagnostics_args = {
        "status_flags": status,
        "command_flags": commands,
        "text_out": writer,
        "perform_calculations": False,
        "debug": True
    }
    diagnostics = diagnostics(**diagnostics_args)
    for sub in diagnostics._info():
        diagnostics.say(sub)
    
    # probe user config
    slp_config_ref = {
        "probe_id": PRB.SLP,
        "text_out": diagnostics._say_obj,

        # base probe
        "sampling_rate": 5,
        "dac_min": 0,
        "dac_max": 4,

        # sweeper probe
        "num_samples": 10,
        "sweep_min": -300,
        "sweep_max": 300,
        "sweep_amp_min": -300,
        "sweep_amp_max": 300,
        "sweeper_shunt": 10,
        "collector_gain": 1
    }

    # probe system config
    slp_sys_ref = {
        # base probe
        "relay_addresses": [0, 1, 2, 3],

        # sweeper probe
        "sweeper_address": 4,
        "collector_address":5
    }

    # test setup_diagnostics
    diagnostics.setup_diagnostics(sys_ref=slp_sys_ref, config_ref=slp_config_ref)

    # print probe
    probe = diagnostics._probe_op._probe
    diagnostics.say(f"probe {probe}")

    # print equations in probe
    eq_msg = "equations:"
    for eq in probe.equations:
        eq_msg += f"\n\t{eq}"
    diagnostics.say(eq_msg)

    # test start_diagnostics
    diagnostics.start_diagnostics()

    # test stop_diagnsotics
    time.sleep(10)
    diagnostics.stop_diagnostics()

    # stop printer
    printer.kill.set()
    printer.join()


