""" G3 - Plasma Devs
Layer 3 - Diagnostics
    Provides the main implementation for the Diagnostics Layer's thread, controlling probes and 
    calculating plasma parameters. Creates Probe Objects that access the Hardware Interface Layer
    through a set of hardware objects.

author: figueroa_90894@students.pupr.edu
status: WIP
  - add docstrings
  - move layer logic to DiagnosticsLayer
  - validate all methods
  - correct keys used to access dictionaries
  - move tests to a unittest file

classes:
    ProbeOperation - Control probe objects and perform general data acquisition control functions. 

"""
# built-in imports
import sys
import os

from threading import Event, Barrier
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


# local imports
from base_thread import BaseThread
from protected_dictionary import ProtectedDictionary
from clock_thread import ClockThread


# Constants - local config
BUFF_TIMEOUT = 3    # wait for data samples no more than three seconds
JOIN_TIMEOUT = 5    # wait for Probe Object thread to exit
MAX_ATTR_ERR = 5    # threshold for AttributeErrors before breaking from _THREAD_MAIN_
BARR_PARTIES = 2    # number of threads that trigger clock barrier, including clock thread
DEBUG = True        # defines clock and probe threads' print behavior

class ProbeOperation(BaseThread):
    """The main thread of the Diagnsotics Layer.
    
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

    Protected Methods:
        _calculate_params(): calculate plasma parameters from data samples
            return: Two ProtectedDictionary objects, containing plasma parameters
        _THREAD_MAIN_(): controls probe objects and processes data samples
        _thread_setup_(): thread related initialization
        _thread_cleanup_(): thread related cleanup
    """
    def __init__(self,
                 status_flags,
                 command_flags,
                 results_buffer:Queue,
                 real_time_param:dict,
                 probe_factory,
                 name:str="PRB_OP",
                 daemon:bool=True,
                 *args, **kwargs
        ):
        """"Use keyword arguments to correctly invoke parent constructors.

        Keyword Arguments:
            status_flags: `StatusFlags` - indicators for subsystem states 
            command_flags: `CommandFlags` - triggers for subsystem behavior
            results_buffer: `Queue` thread-safe queue to pass results to Control Layer
            real_time_param: `ProtectedDictionary` - container to forward paramaters to display
            probe_factory: `ProbeFactory` - makes specific types of probes
            name: str - thread name for probe operation
                from: BaseThread
                default: "PRB_OP"
            daemon: bool - makes thread daemonic, see `threading` documentation
                from: BaseThread
                default: True
        """
        # Invoke BaseThread constructor; AbstractDiagnostics has no constructor.
        super().__init__(*args, daemon=daemon, name=name, **kwargs)

        # --- Save arguments --- #
        self.status_flags = status_flags    # system state indicators
        self.command_flags = command_flags  # action triggers
        self.results_buffer = results_buffer    # returns experiment results to System Control
        self.real_time_param = real_time_param  # paramater container for real-time display
        self.probe_factory = probe_factory      # generates probe objects from config values

        # None values until setup_experiment() instatiates the required probe object.
        self._probe = None       # the probe object with specific data acquisition algorithms
        self._ready = False      # configuration is set and probe object was created
        self._fail = False       # indicate errors during data acquisition
        self._data_buff:Queue = None   # container to recieve data samples from probe object
        self._aggregate_samples:list = None   # stores probe data samples to return to control layer

    # ----- PROBE CONTROL METHODS ----- #
    # TO DO
    def arm(self, sys_ref, config_ref, print_buff:Queue=None):
        """Prepares probe operation for impending plasma diagnostic operations. Instantiates probe,
        clock thread, and other control artifacts.
        """
        self.say("arming...")

        # extract config
        probe_id = config_ref["probe_id"]
        sampling_rate = config_ref["sampling_rate"]

        # initialize synchronization objects
        probe_clock_barrier = Barrier(BARR_PARTIES)     # block thread's until all are ready
        sample_trigger = Event()    # set by clock when a new data point should be acquired
        kill = Event()              # set to stop clock thread
        
        # reset flags
        sample_trigger.clear()
        kill.clear()

        # initialize clock thread
        self._clock = ClockThread(
            tick_rate=sampling_rate,
            trigger=sample_trigger,
            kill=kill,
            debug=DEBUG
        )
        # initialize Probe Object thread through Probe Factory
        self._probe = self._probe_factory.make(
            probe_type=probe_id,
            config_ref=config_ref,
            sys_ref=sys_ref,
            probe_name=probe_id
        )

        # configure thread print mode
        self._clock.console_buff = print_buff
        self._probe.console_buff = print_buff

        # set start barrier to delay probe and clock from starting until both are ready
        self._clock.start_barrier = probe_clock_barrier
        self._probe.start_barrier = probe_clock_barrier

        # pass sample trigger to probe
        self._probe.sample_trig = sample_trigger

        # acquire probe's data sample buffer
        self._data_buff = self._probe.data_buff

        # mark probe operation is ready for plasma diagnostics
        self._ready = True


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
        for eq_index in range(len(self._probe.equations)-1):
            self._probe.equations[eq_index](params)    # in-place operations

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
        self._thread_setup_()
        self._THREAD_MAIN_()
        self._thread_cleanup_()

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
    def _thread_setup_(self):
        """Initialize values and perform entry actions for threaded operations."""
        self._aggregate_samples = []  # clear list
        self._fail = False            # reset indicator

        # TO DO - SET PROBE STATUS FLAGS

        # launch probe and clock threads
        self._probe.start()
        self._clock.start()

        # wait until probe probe thread starts
        self.say("waiting for Probe Object to start...")
        result = self.status_flags.operating.wait(timeout=JOIN_TIMEOUT) # wait for thread

        # print error message if probe could not start
        if not result: self.say("Probe Object thread never started!")

        super()._thread_setup_() # basic print from parent

    # TO DO - validate
    # threading cleanup
    def _thread_cleanup_(self):
        """Clear values and perform exit actions after threaded operations."""
        # Send aggregated results to Control Layer
        if not self._fail:
            self.results_buffer.put(self._aggregate_samples)
            self.say("pushed new sample set to control layer")
        else:
            self.say("Failure in diagnostics! Did not send samples to control layer.")

        # Wait until probe object thread stops
        self.say("waiting for Probe Object to exit...")
        try:
            self._probe.join()   # wait until thread exits
            self._probe = None   # clear probe object
        except AttributeError as err:
            self.say(f"{err} in _thread_cleanup_")

        # Stop clock thread and wait until it exits
        self._clock.kill.set()  # attempt to stop clock
        self.say("waiting for Clock Thread to exit...")
        self._clock.join()      # wait until clock exits
        self._clock = None
        
        # TO DO - CLEAR PROBE STATUS FLAGS

        # reset probe operation's ready flag
        self._ready = False
        super()._thread_cleanup_()

    # thread-safe printing
    def say(self, msg:str):
        """Prints to directly to console (unsafe), or to PrinterThread (thread-safe) depending on
        configuration.
        """
        super().say(msg)


# if __name__ == "__main__":
#     from counter_wrapper import CounterWrapperTest
#     from printer_thread import PrinterThread
#     from system_flags import StatusFlags, CommandFlags
#     from threading import Event
#     from queue import Queue
    
#     kill = Event()
#     printing_buff = Queue()
#     results_buff = Queue()
#     status = StatusFlags()
#     commands = CommandFlags()
#     rt_container = ProtectedDictionary()

#     printer = PrinterThread(
#         name="PRINTR",
#         kill=kill,
#         console_buff=printing_buff,
#     )
#     po = ProbeOperation(
#         start_delay=3,
#         console_buff=printing_buff,
#         status_flags=status,
#         command_flags=commands,
#         hardware_wrapper_cls=CounterWrapperTest,
#         real_time_param=rt_container,
#         results_buffer=results_buff,
#         name='PRB_OP'
#     )
#     from unittest.mock import MagicMock
#     po._probe = MagicMock()
#     # a = ProbeOperation(status_flags=0, real_time_param=0)
#     # v = vars(po)
#     # for key in v:
#     #     print(f"{key} : {v[key]}")
#     printer.start()
#     po.start()
#     po.join()
#     kill.set()
#     printer.join()
#     print('done')

