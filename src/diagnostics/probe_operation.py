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
                 sys_ref,
                 config_ref,
                 status_flags,
                 command_flags,
                 results_buffer,
                 real_time_param,
                 hardware_wrapper_cls=DAQC2plateWrapper,
                 *args, **kwargs
                 ):
        """"<...>"""
        super().__init__(*args, **kwargs)
        # Save arguments
        self.sys_ref = sys_ref
        self.config_ref = config_ref
        self.status_flags = status_flags
        self.command_flags = command_flags
        self.results_buffer = results_buffer
        self.real_time_param = real_time_param
        self.hardware_wrapper_cls = hardware_wrapper_cls
        
        # Instantiate Probe Factory
        probe_factory_args = {
            "config_ref": self.config_ref,
            "status_flags": self.status_flags,
            "command_flags": self.command_flags,
            "hardware_factory": HardwareFactory(self.hardware_wrapper_cls),
            "calculations_factory": CalculationsFactory
        }
        self.probe_factory = ProbeFactory(**probe_factory_args)

    # ----- Inherited Thread Methods ----- #
    def _THREAD_MAIN_(self):
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

    # ----- Inherited Layer Methods ----- #
    def setup_experiment(self):
        pass

    def shutdown(self):
        pass

    def start_diagnostics(self):
        pass

    def stop_diagnostics(self):
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

