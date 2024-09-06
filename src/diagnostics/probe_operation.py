""" G3 - Plasma Devs
Layer 3 - Diagnostics
    Provides the main implementation for the Diagnostics Layer, controlling probes and calculating
    plasma parameters. Accesses the Hardware Interface Layer through a set of hardware objects.

author: figueroa_90894@students.pupr.edu
status: WIP
  - add docstrings: shutdown(), start_diagnostics()
  - validate all methods
  - correct keys used to access dictionaries
  - move tests to a unittest file

classes:
    ProbeOperation - Control probe objects and perform general layer functions. 

"""
# built-in imports
import sys
import os

from threading import Event
from queue import Queue, Empty

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


# ----- local imports ----- #
from protected_dictionary import ProtectedDictionary

# subclassing
from abstract_diagnostics import AbstractDiagnostics
from base_thread import BaseThread

# probe instantiation
from probe_factory import ProbeFactory
from calculations_factory import CalculationsFactory

# hardware interfacing (lower layer)
from hardware_factory import HardwareFactory
from daqc2plate_wrapper import DAQC2plateWrapper


# Constants - local config
BUFF_TIMEOUT = 3    # wait for data samples no more than three seconds
JOIN_TIMEOUT = 5    # wait for Probe Object thread to exit
MAX_ATTR_ERR = 5    # threshold for AttributeErrors before breaking from _THREAD_MAIN_


class ProbeOperation(AbstractDiagnostics, BaseThread):
    """The top boundary of the Diagnostics Layer.
    
    ProbeOperation implements the `AbstractDiagnostics` interface, and inherits utils from
    `BaseThread`. During diagnostics, the ProbeOperation thread collects data samples from
    Probe Objects, calculates plasma parameters, updates parameters to display, and aggregates
    samples as results. When diagnostics halt, results are returned pushed to the results buffer.
    
    Public Attributes:
        status_flags: `StatusFlags` - system state indicators
        command_flags: `CommandFlags` - action triggers
        results_buffer: `Queue` - sends experiment results to Control Layer
        real_time_param: `ProtectedDictionary` - sends to UI parameters to display

    Protected Attributes:
        _probe_factory: instantiates various probe objects
        _probe: `BaseProbe` subclass - instantiated probe object
        _ready: indicate ProbeOperation is awaiting to begin diagnostics
        _fail: bool - indicates error during operations
        _data_buff: `Queue` - recieves data samples Probe Object
        _aggregate_samples: list - collected samples and plasma parameters

    Public Methods:
        run(): invoked by calling thread's start(); overloads BaseThread
        say(): thread-safe printing; inherited from BaseThread
        setup_experiment(): prepares diagnostic layer for operations
        shutdown(): invoked during system-wide shutdown
        start_diagnostics(): begin operatios
        stop_diagnostics(): halt operations and request results

    Protected Methods:
        _calculate_params(): calculate plasma parameters from data samples
            return: Two ProtectedDictionary objects, containing plasma parameters
        _THREAD_MAIN_(): controls probe objects and processes data samples
        _setup(): thread related initialization
        _cleanup(): thread related cleanup
    """
    def __init__(self,
                 status_flags,
                 command_flags,
                 results_buffer:Queue,
                 real_time_param:dict,
                 name:str="PRB_OP",
                 daemon:bool=True,
                 hardware_wrapper_cls=DAQC2plateWrapper,
                 *args, **kwargs
        ):
        """"Use keyword arguments to correctly invoke parent constructors.

        Keyword Arguments:
            status_flags: `StatusFlags` - indicators for subsystem states 
            command_flags: `CommandFlags` - triggers for subsystem behavior
            results_buffer: `Queue` thread-safe queue to pass results to Control Layer
            real_time_param: `ProtectedDictionary` - container to forward paramaters to display
            name: str - thread name for probe operation
                from: BaseThread
                default: "PRB_OP"
            daemon: bool - makes thread daemonic, see `threading` documentation
                from: BaseThread
                default: True
            hardware_wrapper_cls: interface wrapper passed to ProbeFactory
                type: `AbstractWrapper` subclass 
                default: `DAQC2plateWrapper`
        """
        # Invoke BaseThread constructor; AbstractDiagnostics has no constructor.
        super().__init__(*args, daemon=daemon, name=name, **kwargs)

        # --- Save arguments --- #
        self.status_flags = status_flags    # system state indicators
        self.command_flags = command_flags  # action triggers
        self.results_buffer = results_buffer    # returns experiment results to System Control
        self.real_time_param = real_time_param  # paramater container for real-time display
        
        # Instantiate Probe Factory
        probe_factory_args = {
            "status_flags": self.status_flags,
            "command_flags": self.command_flags,
            "hardware_factory": HardwareFactory(hardware_wrapper_cls),
            "calculations_factory": CalculationsFactory
        }
        self._probe_factory = ProbeFactory(**probe_factory_args)

        # None values until setup_experiment() instatiates the required probe object.
        self._probe = None       # the probe object with specific data acquisition algorithms
        self._ready = False      # configuration is set and probe object was created
        self._fail = False       # indicate errors during data acquisition
        self._data_buff:Queue = None   # container to recieve data samples from probe object
        self._aggregate_samples:list = None   # stores probe data samples to return to control layer

    # TO DO - validate
    def _calculate_params(self, samples):
        """Calculates plasma paramaters with the equations packaged in the probe object.
        Returns two ProtectDictionaries, the first with all data samples and plasma parameters,
        the second with plasma parameters that must be displayed by the UI.

        samples: `ProtectedDictionary` containing applied biases and measured voltages.
        """
        # setup
        self.status_flags.calculating.set()     # indicate calculations are being performed
        self.say("calculating paramaters...")
        params = ProtectedDictionary(samples)   # argument for calculations

        # perform all calculations except last one
        for calculation in range(len(self._probe.equations)-1):
            calculation(params)    # in-place operations

        # last calculation returns parameters specifically for display
        display_params = self._probe.equation[-1](params)
        
        # cleanup
        self.status_flags.calculating.clear()   # indicate calculations are completed
        self.say("calculations complete")
        return params, display_params
    
    # ----- Overloaded Thread Methods ----- #
    # thread launch script
    def run(self):
        """Invoked when the start() method is called."""
        self._setup()
        self._THREAD_MAIN_()
        self._cleanup()

    # TO DO - validate
    def _THREAD_MAIN_(self):
        """Main thread script for ProbeOperation.
        Aggregates results, calculates plasma parameters, updates display values, and sends
        result to the Control Layer.
        """
        attribute_errors = 0  # count raised attribute errors
        while self.status_flags.operating or not self._data_buff.empty():
            try:
                # get data samples sent by Probe Object through data buffer
                samples:dict = self._data_buff.get(timeout=BUFF_TIMEOUT)
                self.say(err)

                # sequentially apply calculations to obtain plasma paramaters
                samples = ProtectedDictionary(samples)  # enforce mutex
                params, display_params = self._calculate_params(samples)  # perform all calculations

                # update real-time parameter container for display
                self.real_time_param.update(display_params)  # read by UI layer
                self.command_flags.refresh.set()        # indicate new data for display
                self._aggregate_samples.append(params)   # append new samples
            except Empty:   # do nothing while data buffer is empty
                pass

            # TO DO - DELETE - temporary for basic tests
            except AttributeError as err:
                self.say(f"{err} in _THREAD_MAIN_")
                attribute_errors += 1
                if attribute_errors >= MAX_ATTR_ERR:
                    self.say("attribute errors exceeded threshold!")
                    self._fail = True
                    break
                else:
                    self.pause(BUFF_TIMEOUT)
                    continue

    # TO DO - validate
    # threading setup
    def _setup(self):
        """Initialize values and perform entry actions for threaded operations."""
        self._aggregate_samples = []  # clear list
        self._fail = False            # reset indicator

        # TO DO - SET PROBE STATUS FLAGS

        # launch probe object thread and wait for it to start
        self._probe.start()  # launch thread
        self.say("waiting for Probe Object to start...")
        result = self.status_flags.operating.wait(timeout=JOIN_TIMEOUT) # wait for thread
        if not result: self.say("Probe Object thread never started!")   # error message

        super()._setup() # basic print from parent

    # TO DO - validate
    # threading cleanup
    def _cleanup(self):
        """Clear values and perform exit actions after threaded operations."""
        # Send aggregated results to Control Layer
        if not self._fail:
            self.results_buffer.put(self._aggregate_samples)
            self.say("pushed new samples set to control")

        # Wait until probe object thread stops
        self.say("waiting for Probe Object to exit...")
        try:
            self._probe.join()   # wait until thread exits
            self._probe = None   # clear probe object
        except AttributeError as err:
            self.say(f"{err} in _cleanup")
        
        # TO DO - CLEAR PROBE STATUS FLAGS

        super()._cleanup()

    # thread-safe printing
    def say(self, msg:str):
        """Prints to directly to console (unsafe), or to PrinterThread (thread-safe) depending on
        configuration.
        """
        super().say(msg)

    # ----- Overloaded Layer Methods ----- #
    # User confirms config and prepares to begin experiment
    def setup_experiment(self, sys_ref:dict, config_ref:dict, probe_thread_name="PROBE"):
        """Initializes probe object and prepare to launch threads.
        
        Arguments:
            sys_ref: `ProtectedDictionary` containing system settings
            config_ref: `ProtectedDictionary` containing user settings
            probe_thread_name: str - name assigned to probe object's thread
                default: "PROBE"
        """
        # Initialize Probe Object through Probe Factory
        self._probe = self._probe_factory.make(
            probe_type=config_ref['probe_id'],
            config_ref=config_ref,
            sys_ref=sys_ref,
            probe_name=probe_thread_name
        )
        # acquire probe's data sample buffer
        self._data_buff = self._probe.data_buff
        self._ready = True

    # TO DO - Entire system is terminating
    def shutdown(self):
        """<...>"""
        pass

    # TO DO - User starts experiment, launch ProbeOperation thread
    def start_diagnostics(self):
        """Launches ProbeOperation's thread.
        Raises a RuntimeError if `setup_experiment()` was not invoked first."""
        if not self._ready:
            raise RuntimeError("Cannot begin diagnostics before setup_experiment() is called!")
        else:
            self._ready = False  # clear ready value to prevent recurring calls to this method
        self.start()    # launch Probe Operation thread

    # TO DO - User stops experiment, called by _cleanup()
    # Return aggregated results
    def stop_diagnostics(self):
        """<...>"""
        pass

if __name__ == "__main__":
    from counter_wrapper import CounterWrapperTest
    from printer_thread import PrinterThread
    from system_flags import StatusFlags, CommandFlags
    from threading import Event
    from queue import Queue
    
    kill = Event()
    printing_buff = Queue()
    results_buff = Queue()
    status = StatusFlags()
    commands = CommandFlags()
    rt_container = ProtectedDictionary()

    printer = PrinterThread(
        name="PRINTR",
        kill=kill,
        console_buff=printing_buff,
    )
    po = ProbeOperation(
        start_delay=3,
        console_buff=printing_buff,
        status_flags=status,
        command_flags=commands,
        hardware_wrapper_cls=CounterWrapperTest,
        real_time_param=rt_container,
        results_buffer=results_buff,
        name='PRB_OP'
    )
    from unittest.mock import MagicMock
    po._probe = MagicMock()
    # a = ProbeOperation(status_flags=0, real_time_param=0)
    # v = vars(po)
    # for key in v:
    #     print(f"{key} : {v[key]}")
    printer.start()
    po.start()
    po.join()
    kill.set()
    printer.join()
    print('done')

