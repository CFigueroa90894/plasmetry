# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings
#   - comment init
#   - public methods
#   - integrate with system control
#   - resolve placeholder probe attribute
#   - when done, delete basic tests
#   - correct key used to access dictionaries

# built-in imports
import sys
import os

from threading import Event
from queue import Queue, Empty

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
WAIT_TIMEOUT = 5

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

        # Save arguments
        self.status_flags = status_flags    # system state indicators
        self.command_flags = command_flags  # action triggers
        self.results_buffer = results_buffer    # returns experiment results to System Control
        self.real_time_param = real_time_param  # paramater container for real-time display
        self.hardware_wrapper_cls = hardware_wrapper_cls    # wrapper class for generating hardware objects
        
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
        self.aggregate_samples:list = None   # stores data samples from probes; returns to control when stoppping


    # ----- Overloaded Thread Methods ----- #
    # TO DO - validate
    def _THREAD_MAIN_(self):
        """<...>"""
        self.aggregate_samples = []
        while self.status_flags.operating or not self.data_buff.empty():
            try:
                samples = self.data_buff.get(timeout=BUFF_TIMEOUT)  # get data samples sent by Probe Object
                params, display_params = self.calculate_params(ProtectedDictionary(samples))    # sequentially apply obtain plasma paramaters
                self.real_time_param.update(display_params)         # update real-time parameter container for display
                self.command_flags.refresh.set()    # indicate new data for display
                self.aggregate_samples.append(params)
            except Empty:   # do nothing while data buffer is empty
                pass
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
        result = self.status_flags.operating.wait(timeout=WAIT_TIMEOUT)
        if result: self.say("Probe Object never exited!")
        super()._setup() # basic print

    # TO DO - validate
    # threading cleanup
    def _cleanup(self):
        """<...>"""
        # CLEAR PROBE STATUS FLAGS
        # <...>
        self.say("waiting for Probe Object to exit...")
        self.probe.join()
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

