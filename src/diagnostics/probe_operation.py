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
# subclassing
from abstract_diagnostics import AbstractDiagnostics
from base_thread import BaseThread

# probe instantiation
from probe_factory import ProbeFactory
from calculations_factory import CalculationsFactory

# hardware interfacing (lower layer)
from hardware_factory import HardwareFactory
from daqc2plate_wrapper import DAQC2plateWrapper


class ProbeOperation(AbstractDiagnostics, BaseThread):
    """<...>"""
    def __init__(self,
                 status_flags,
                 command_flags,
                 results_buffer,
                 real_time_param,
                 hardware_wrapper_cls=DAQC2plateWrapper,
                 *args, **kwargs
                 ):
        """"<...>"""
        # Invoke BaseThread constructor; AbstractDiagnostics has no constructor.
        super().__init__(*args, **kwargs)

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
        self.data_buff = None   # container to recieve data samples from probe object


    # ----- Overloaded Thread Methods ----- #
    def _THREAD_MAIN_(self):
        """<...>"""
        self.say('1')
        self.pause(1)
        self.say('2')
        self.pause(1)
        self.say('3')
        self.pause(1)

    def run(self):
        super().run()

    def _setup(self):
        super()._setup()

    def _cleanup(self):
        super()._cleanup()

    def say(self, msg):
        super().say(msg)

    # ----- Overloaded Layer Methods ----- #
    # TO DO
    def setup_experiment(self, sys_ref:dict, config_ref:dict):
        """<...>"""
        self.probe = self.probe_factory.make(
            probe_type=config_ref['probe_id'],
            config_ref=config_ref,
            sys_ref=sys_ref
        )
        self.data_buff = self.probe.data_buff

    # TO DO
    def shutdown(self):
        """<...>"""
        pass

    # TO DO
    def start_diagnostics(self):
        """<...>"""
        pass

    # TO DO
    def stop_diagnostics(self):
        """<...>"""
        pass

if __name__ == "__main__":
    from counter_wrapper import CounterWrapperTest
    from printer_thread import PrinterThread
    from threading import Event
    from queue import Queue
    
    kill = Event()
    buff = Queue()

    printer = PrinterThread(
        name="PRINTR",
        kill=kill,
        console_buff=buff,
    )
    po = ProbeOperation(
        start_delay=3,
        console_buff=buff,
        config_ref='config_ref',
        sys_ref='sys_ref',
        status_flags='status_flags',
        command_flags='command_flags',
        hardware_wrapper_cls=CounterWrapperTest,
        real_time_param='real_time_param',
        results_buffer='results_buffer',
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

