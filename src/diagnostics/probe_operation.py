""" G3 - Plasma Devs
Layer 3 - Diagnostics
    Provides the main implementation for the Diagnostics Layer, controlling probes and calculating
    plasma parameters. Accesses the Hardware Interface Layer through a set of hardware objects.

author: figueroa_90894@students.pupr.edu
status: WIP
  - add docstrings
  - comment init
  - integrate with system control
  - resolve placeholder probe attribute
  - when done, delete basic tests
  - correct keys used to access dictionaries

classes:
    ProbeOperation - Control probe objects 

"""
# built-in imports
import sys
import os

from threading import Event
from queue import Queue, Empty

# ----- PATH HAMMER v2.7 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:  # execute snippet if current script was run directly 
    """Resolve absolute imports by recusring into subdirectories and appending them to python path."""
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    assert src_abs.split('\\')[-1*len(root_target):] == root_target   # validate correct top folder
    
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split('\\')[-1] not in exclude] # get subdirs, exclude unwanted
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
    """<...>"""
    def __init__(self,
                 status_flags,
                 command_flags,
                 results_buffer,
                 real_time_param,
                 name="PRB_OP",
                 daemon=True,
                 hardware_wrapper_cls=DAQC2plateWrapper,
                 *args, **kwargs
        ):
        """"<...>"""
        # Invoke BaseThread constructor; AbstractDiagnostics has no constructor.
        super().__init__(*args, daemon=daemon, name=name, **kwargs)

        # --- Save arguments --- #
        self.status_flags = status_flags    # system state indicators
        self.command_flags = command_flags  # action triggers
        self.results_buffer = results_buffer    # returns experiment results to System Control
        self.real_time_param = real_time_param  # paramater container for real-time display
        self.hardware_wrapper_cls = hardware_wrapper_cls    # generates hardware objects
        
        # Instantiate Probe Factory
        probe_factory_args = {
            "status_flags": self.status_flags,
            "command_flags": self.command_flags,
            "hardware_factory": HardwareFactory(self.hardware_wrapper_cls),
            "calculations_factory": CalculationsFactory
        }
        self.probe_factory = ProbeFactory(**probe_factory_args)

        # None values until setup_experiment() instatiates the required probe object.
        self.probe = None       # the probe object with specific data acquisition algorithms
        self.data_buff:Queue = None   # container to recieve data samples from probe object
        self.aggregate_samples:list = None   # stores probe data samples to return to control layer


    # ----- Overloaded Thread Methods ----- #
    # TO DO - validate
    def _THREAD_MAIN_(self):
        """<...>"""
        attribute_errors = 0         # count raised attribute errors
        self.aggregate_samples = []  # store samples and calculated params of a single experiment
        fail = False
        while self.status_flags.operating or not self.data_buff.empty():
            try:
                # get data samples sent by Probe Object through data buffer
                samples:dict = self.data_buff.get(timeout=BUFF_TIMEOUT)
                self.say(err)

                # sequentially apply calculations to obtain plasma paramaters
                samples = ProtectedDictionary(samples)  # apply mutex
                params, display_params = self.calculate_params(samples)  # perform all calculations

                # update real-time parameter container for display
                self.real_time_param.update(display_params)  # read by UI layer
                self.command_flags.refresh.set()        # indicate new data for display
                self.aggregate_samples.append(params)   # append new samples

            except Empty:   # do nothing while data buffer is empty
                pass

            except AttributeError as err:
                self.say(f"{err} in _THREAD_MAIN_")
                attribute_errors += 1
                if attribute_errors >= MAX_ATTR_ERR:
                    self.say("attribute errors exceeded threshold!")
                    fail = True
                    break
                else:
                    self.pause(BUFF_TIMEOUT)
                    continue
        if not fail:
            self.results_buffer.put(self.aggregate_samples)
            self.say("pushed new samples set to control")

    # TO DO -validate
    def calculate_params(self, samples):
        """<...>"""
        self.say("calculating paramaters...")
        self.status_flags.calculating.set()     # prevent shutdown while still calculating
        params = ProtectedDictionary(samples)
        for calculation in range(len(self.probe.equations)-1):  # run perform all calculations except last one
            calculation(params)    # in-place operations
        display_params = self.probe.equation[-1](params)  # last calculation returns parameters specifically to display
        self.status_flags.calculating.clear()
        self.say("calculations complete")
        return params, display_params

    # Invokes _setup(), then _THREAD_MAIN_(), and lastly _cleanup()
    def run(self):
        """<...>"""
        super().run()   # call parents run() method
        self.probe.start()

    # TO DO - validate
    # threading setup
    def _setup(self):
        """<...>"""
        # SET PROBE STATUS FLAGS
        self.say("waiting for Probe Object to start...")
        result = self.status_flags.operating.wait(timeout=JOIN_TIMEOUT)
        if result: self.say("Probe Object never exited!")
        super()._setup() # basic print

    # TO DO - validate
    # threading cleanup
    def _cleanup(self):
        """<...>"""
        # CLEAR PROBE STATUS FLAGS
        # <...>
        self.say("waiting for Probe Object to exit...")
        try:
            self.probe.join()
        except AttributeError as err:
            self.say(f"{err} in _cleanup")
        super()._cleanup()

    # thread-safe printing
    def say(self, msg):
        """<...>"""
        super().say(msg)

    # ----- Overloaded Layer Methods ----- #
    # User confirms config and prepares to begin experiment
    def setup_experiment(self, sys_ref:dict, config_ref:dict, probe_thread_name="PROBE"):
        """<...>"""
        # Initialize Probe Object through Probe Factory
        self.probe = self.probe_factory.make(
            probe_type=config_ref['probe_id'],
            config_ref=config_ref,
            sys_ref=sys_ref,
            probe_name=probe_thread_name
        )
        # acquire probe's data sample buffer
        self.data_buff = self.probe.data_buff

    # TO DO - Entire system is terminating
    def shutdown(self):
        """<...>"""
        pass

    # TO DO - User starts experiment, launch ProbeOperation thread
    def start_diagnostics(self):
        """<...>"""
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

    # v = vars(po)
    # for key in v:
    #     print(f"{key} : {v[key]}")
    printer.start()
    po.start()
    po.join()
    kill.set()
    printer.join()
    print('done')

