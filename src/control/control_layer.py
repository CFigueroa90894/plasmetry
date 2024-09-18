""" G3 - Plasma Devs
Layer 2 - Control - Concrete Implementation
    Provides the main implementation for the Control Layer, assembling its subcomponents and
    exposing the layer's public functionality.

author: figueroa_90894@students.pupr.edu
status: WIP
    - add docstrings
    - remove temporary relative imports
    - redefine and implement abstract methods from interface specification
    - verify names of subcomponent files and their classes
    - add specific args to components instantiation
    - validate with team
"""

# built-in imports
import sys
import os

import datetime

from threading import Event
from queue import Queue

from typing import Tuple

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

# TO DO - Remove temporary relative imports (used to get type hints in IDE)
# local imports
from abstract_layers.abstract_control import AbstractControl
from system_flags import StatusFlags, CommandFlags
from protected_dictionary import ProtectedDictionary

from utils.threads.printer_thread import PrinterThread


# TO DO
class ControlLayer(AbstractControl):
    """<...>"""

    # Default subcomponent module names
    file_upload_mod = 'file_upload'
    config_manager_mod = 'config_manager'

    # Default lower layer module name
    diagnostics_layer_mod = 'diagnostics_layer'


    # TO DO - Carlos
    def __init__(self,
                 name:str="CTRL",
                 debug:bool=True,
                 buffer_text:bool=False, *args, **kwargs):
        """<...>"""
        # validate if a PrinterThread is needed
        if buffer_text:
            self._printer = self.__make_printer()  # create and launch printer thread
            writer = self._printer.get_writer()    # get text output object
        else:
            self._printer = None  # do not create printer thread
            writer = None         # use default text output

        # call parent constructor
        super().__init__(*args, name=name, text_out=writer, **kwargs)

        # save arguments
        self.debug = debug                  # defines printing behavior, default False

        # create control objects
        self._status = StatusFlags()        # state indicators
        self._commands = CommandFlags()     # action triggers
        self._results = Queue()             # thread-safe queue to recieve experiment results
        self._real_time_param = ProtectedDictionary()  # thread-safe container for plasma parameters

        # ----- Assemble Control Layer ----- #
        sub = self._load_all_subcomponents()    # import subcompoenents, returns in a dict

        # instantiate lower layer
        self._diagnostics = sub["diagnostics_layer"](**self.__diagnostics_args())

        # instantiate subcomponents
        self._file_upload = sub["file_upload"](**self.__file_upload_args())
        self._config_manager = sub["config_manager"](**self.__config_manager_args())

        self.say(f"DEBUG - {self.debug}")
        self.say("control layer initialized...")

        
    # ----- LAYER PUBLIC METHODS ----- #
    # TO DO - Alberto
    def set_config(self) -> Tuple[bool, str]:
        """<...>"""
        raise NotImplementedError

    # TO DO - Alberto
    def get_config(self) -> any:
        """<...>"""
        raise NotImplementedError

    # TO DO - Alberto
    def save_config_file(self) -> bool:
        """<...>"""
        raise NotImplementedError

    # TO DO - Alberto
    def load_config_file(self) -> None:
        """<...>"""
        raise NotImplementedError

    def get_real_time_container(self) -> Tuple[dict, Event]:
        """<...>"""
        return self._real_time_param, self._commands.refresh

    # TO DO - Carlos
    def setup_experiment(self) -> None:
        """<...>"""
        raise NotImplementedError

    # TO DO - Carlos
    def start_experiment(self) -> None:
        """<...>"""
        raise NotImplementedError

    # TO DO - Carlos
    def stop_experiment(self) -> None:
        """<...>"""
        raise NotImplementedError

    # TO DO - Carlos
    def layer_shutdown(self) -> None:
        """<...>"""
        raise NotImplementedError

    def get_status_flags(self) -> StatusFlags:
        """<...>"""
        return self._status

    def get_command_flags(self) -> CommandFlags:
        """<...>"""
        return self._commands
    
    # ----- Layer Specific Utils ----- #
    def _info(self) -> list:
        """<...>"""
        sub = [
            ("Control", "File Upload", str(self._file_upload)),
            ("Control", "Config Manager", str(self._config_manager)),
            ("Control", "Diagnostics Layer", str(self._diagnostics)),
        ]
        sub.extend(self._diagnostics._info())
        return sub
        
    
    def _load_all_subcomponents(self) -> dict:
        """<...>"""
        # load subcomponent modules
        file_upload_mod = self._load(self.file_upload_mod)
        config_manager_mod = self._load(self.config_manager_mod)

        # load subcomponent classes
        file_upload_cls = file_upload_mod.FileUpload
        config_manager_cls = config_manager_mod.ConfigManager

        # load lower layer
        diagnostics_layer_mod = self._load_mod(self.diagnostics_layer_mod)
        diagnostics_layer_cls = diagnostics_layer_mod.DiagnosticsLayer

        # pack and return subcomponents
        classes = {
            "file_upload": file_upload_cls,
            "config_manager": config_manager_cls,
            "diagnostics_layer": diagnostics_layer_cls
        }
        return classes
    
    def __make_printer(self):
        """<...>"""
        # create kill switch for PrinterThread
        kill = Event()
        kill.clear()

        # create output log file
        log_name = str(datetime.datetime.now()).replace(':', '_')
        log = open(f"run_logs/LOG_{log_name}.txt", 'a')

        # create and launch printer thread
        printer_output = [None, log]  # output to default stdout and log file
        printer = PrinterThread(kill=kill, text_out=printer_output)  # create thread
        printer.start()  # launch thread

        # get writer object and write log name to log file's header
        writer = printer.get_writer()
        writer(f"# {log_name}")

        return printer

    def __diagnostics_args(self):
        """<...>"""
        args = {
            "text_out": self._say_obj,
            "status_flags": self._status,
            "command_flags": self._commands,
            "results_buffer": self._results,
            "real_time_param": self._real_time_param,
            "debug": self.debug
        }
        return args
    
    # TO DO - add specific args
    def __file_upload_args(self):
        """<...>"""
        args = {
            "text_out": self._say_obj,
            "status_flags": self._status,
            "command_flags": self._commands
        }
        return args
    
    # TO DO - add specific args
    def __config_manager_args(self):
        """<...>"""
        args = {
            "text_out": self._say_obj,
            "status_flags": self._status,
            "command_flags": self._commands
        }
        return args
