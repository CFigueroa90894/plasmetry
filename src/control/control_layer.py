""" G3 - Plasma Devs
Layer 2 - Control - Concrete Implementation
    Provides the main implementation for the Control Layer, assembling its subcomponents and
    exposing the layer's public functionality.

author: figueroa_90894@students.pupr.edu
status: WIP
    - add docstrings
    - add call to file upload in 'stop_experiment()'
    - update configuration file name in __init__()
    - decide if we should wait for file upload to complete before shutting down or it should be left
        running in the background (and add or remove its call in layer_shutdown())
    - integrate with config manager and file upload from separate branch 
    - verify names of subcomponent files and their classes
    - add specific args to components instantiation
    - validate with team

    - time permitting, implement rerouting of stderr to printer thread
"""

# built-in imports
import sys
import os

import datetime

from threading import Event, Thread
from queue import Queue, Empty

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
from abstract_control import AbstractControl
from system_flags import StatusFlags, CommandFlags
from protected_dictionary import ProtectedDictionary

from printer_thread import PrinterThread

# local config
RESULT_TIMEOUT = 10

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
        self._real_time_param = []  # thread-safe container for plasma parameters

        # ----- Assemble Control Layer ----- #
        sub = self._load_all_subcomponents()    # import subcompoenents, returns in a dict

        # instantiate lower layer
        self._diagnostics = sub["diagnostics_layer"](**self.__diagnostics_args())

        # instantiate subcomponents
        self._file_upload_cls = sub["file_upload"]
        self._config_manager = sub["config_manager"](**self.__config_manager_args())

        self.say(f"DEBUG - {self.debug}")
        self.say("control layer initialized...")

        # local state indicators
        self._ready = Event()
        self._terminated = Event()
        self._ready.clear()
        self._terminated.clear()

        # TO DO - UPDATE NAMES WHEN IMPLEMENTED
        self.__selected_probe = None
        self.__previous_config_pathname = "configuration_file.json"

        
    # ----- Config Manipulations ----- #
    # TO DO - Alberto
    def set_config(self, probe_id, key, value) -> Tuple[bool, str]:
        """Mutator function, edits the in memory configuration values."""
        self._config_manager.set_config(probe_id, key, value)

    # TO DO - Alberto
    def get_config(self, probe_id, key) -> any:
        """Accessor function, receives data from the in memory configuration values."""
        return self._config_manager.get_config(probe_id, key)

    # TO DO - Alberto
    def save_config_file(self) -> bool:
        """Config file writer."""
        self._config_manager.save_config_file()

    # TO DO - Alberto
    def load_config_file(self) -> None:
        """Config file loader."""
        self._config_manager.load_config_file()


    # ----- Control Object Getters ----- #
    def get_status_flags(self) -> StatusFlags:
        """<...>"""
        return self._status

    def get_command_flags(self) -> CommandFlags:
        """<...>"""
        return self._commands
    
    def get_real_time_container(self) -> Tuple[dict, Event]:
        """<...>"""
        return self._real_time_param, self._commands.refresh


    # ----- Experiment Control ----- #
    def setup_experiment(self, probe_id:str) -> None:
        """Called by upper layers to prepare the system for plasma diagnostic operations.

        Notifies lower layers to begin plasma diagnostic initializations. When ready, lower levels
        will wait until this interface's `start_experiment()` method is called before beginning
        plasma diagnostics.

        Arguments:
            probe_id - identifier for the selected probe, used to select which config dict will
                be passed to the 
        Exceptions:
            RuntimeError: `setup_experiment()` was called while:
                - plasma diagnostics are being performed, or
                - system shutdown is underway
        """
        # validate system is not performing diagnostics
        if self._status.operating.is_set() or self._commands.diagnose.is_set():
            raise RuntimeError("Cannot call 'setup_experiment()' while diagnostics are underway!")
        
        # validate system is not undergoing shutdown before proceeding
        elif self._commands.shutdown.is_set():
            raise RuntimeError("Cannot call 'setup_experiment()' while shutdown is underway!")
        
        # checks successful, proceed
        else:
            self.say("setting up experiment...")

            # save probe id to private attribute
            self.__selected_probe = probe_id

            # get probe specific config values
            sys_ref = self._config_manager.sys_ref[probe_id]
            config_ref = self._config_manager.config_ref[probe_id]

            # prepare diagnostics layer
            self._diagnostics.setup_diagnostics(sys_ref, config_ref)

            # confirm diagnostics is ready
            if self._diagnostics._ready.is_set():
                self._ready.set()
                self.say("READY")
                for eq in self._diagnostics._probe_op._probe.equations:
                    print(eq)
                    
                    
            else:
                raise RuntimeError("Could not set up diagnostics layer!")

    def start_experiment(self) -> None:
        """Called by upper layers to trigger plasma diagnostic operations in lower layers.

        Exceptions:
            RuntimeError: `start_experiment()` was called:
                - while system shutdown is underway, or
                - without first calling `setup_experiment()`, or
                - diagnostics layer is not ready to perform diagnostics, or
                - diagnostics are already underway
        """
        # validate system is not undergoing shutdown
        if self._commands.shutdown.is_set():
            raise RuntimeError("Cannot call 'start_experiment()' while shutdown is underway!")
        
        # validate control layer is ready for diagnostics
        elif not self._ready.is_set():
            raise RuntimeError("Cannot begin diagnostics before setup_experiment is called!")
        
        # validate diagnostics layer is ready to perform diagnostics
        elif not self._diagnostics._ready.is_set():
            raise RuntimeError("Diagnostics Layer is not ready for diagnostics!")
        
        # validate diagnostics are not already underway
        elif self._commands.diagnose.is_set() or self._status.operating.is_set():
            raise RuntimeError("Called 'start_experiment()' while diagnostics are underway!")
        
        # checks successful, proceed
        else:
            self.say("notifying diagnostics must start...")
            self._ready.clear()     # cannot be 'ready' for diagnostics once diagnostics start
            self._diagnostics.start_diagnostics()   # trigger diagnostics in lower layers

    # TO DO - CALL FILE UPLOAD
    def stop_experiment(self) -> None:
        """Called by upper layers to halt plasma diagnostic operations in lower layers.
        
        This layer will attempt to complete all pending operations. It will signal lower layers
        that they must halt diagnsotics, then await the results of the experiment returned by the
        diagnostic layer. These results will be formatted and stored by this layer, before
        returning to its idle state.

        Exceptions:
            RuntimeError: `stop_experiment()` was called while:
                - system was not performing plasma diagnostics, or
        """
        # validate diagnostics are being performed
        if not self._commands.diagnose.is_set() and not self._status.operating.is_set():
            raise RuntimeError("Called 'stop_experiment' but diagnostics are not being performed!")

        # checks successful, proceed
        else:
            self.say("stopping experiment...")
            self._diagnostics.stop_diagnostics()    # halt diagnostics in lower layers
            self.say("awaiting results...")

            # get results from lower layers
            try:
                results = self._results.get(timeout=RESULT_TIMEOUT)  # read results from buffer
                self.say("results obtained")

                # TEMPORARY - DELETE WHEN CALL TO FILE UPLOAD IS IMPLEMENTED
                self.say(results)

                # TO DO - CALL FILE UPLOAD
                # Make a single-use FileUpload object
                
                uploader = self._file_upload_cls(**self.__file_upload_args())
                Thread(target=uploader.new_data(results), daemon=False).start()

                self.__selected_probe = None    # clear probe selection

            # get results timed out 
            except Empty:
                self.say("could not obtain results!")

    # TO DO
    def layer_shutdown(self) -> None:
        """Called by upper layers to initiate a system-wide shutdown.
        
        Lower layers will attempt to complete pending operations, then terminate their processes.
        * NOTE: this call blocks until lower layers have terminated to prevent corruption.
        This layer should await until all buffered results are saved to files before terminating
        its subcomponents.
        """
        self.say("initiating system-wide shutdown...")
        self._commands.shutdown.set()   # notify all software components must begin shutdown

        # stop experiment
        if self._commands.diagnose.is_set() or self._status.operating.is_set():
            self.stop_experiment()
        else:
            self.say("experiment is already halted.")

        # TO DO - ADD WAITS UNTIL TRANSMISSION IS COMPLETE - or should it leave the upload running
        # in the background?
        # destroying file output and data formatting doesn't seem like a good idea
        # wait for file output to finish
        # <...wait for stuff...>

        self._diagnostics.layer_shutdown()  # terminate lower layers

        # validate diagnostics layer terminated
        if not self._diagnostics._terminated.is_set():
            raise RuntimeError("Diagnostics Layer did not shutdown correctly!")
        
        self.say("layer shutdown complete.")

        # shutdown printer thread if it exists
        if self._printer is not None:
            self.say("waiting for printer to exit...")
            self._printer.kill.set()    # stop printer thread
            self._printer.join()        # wait for printer thread to exit

            # TO DO - RESTORE STDERR - if it was overriden

        self._terminated.set()
    

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
        file_upload_mod = self._load_mod(self.file_upload_mod)
        config_manager_mod = self._load_mod(self.config_manager_mod)

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
            "command_flags": self._commands,
            "probe_type": self.__selected_probe,
            "local_path": self._config_manager.config_ref["local_path"],
            "credentials_path": self._config_manager.config_ref["credentials_path"]
        }
        return args
    
    # TO DO - add specific args
    def __config_manager_args(self):
        """<...>"""
        args = {
            "text_out": self._say_obj,
            "status_flags": self._status,
            "command_flags": self._commands,
            "path_name": 'configuration_file.json'
        }
        return args
