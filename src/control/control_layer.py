""" G3 - Plasma Devs
Layer 2 - Control - Concrete Implementation
    Implements the interface specified by the AbstractControl class. Provides the main functionality
    of the Control Layer, assembling its subcomponents and, controlling the experiment, and managing
    data.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    ControlLayer

"""

# built-in imports
import sys
import os

from threading import Event, Thread     # threading framework
from queue import Queue, Empty          # data buffering 

from typing import Tuple                # used for type hints
import datetime                         # datetime stamp the log file

# ----- PATH HAMMER v3.0 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:
    """Resolve absolute imports by recursing into subdirs and appending them to python path."""
    # os delimeters
    win_delimeter, rpi_delimeter = "\\", "/"

    # locate project root
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    print(f"Path Hammer: {src_abs}")

    # select path delimeter
    if win_delimeter in src_abs: delimeter = win_delimeter
    elif rpi_delimeter in src_abs: delimeter = rpi_delimeter
    else: raise RuntimeError("Path Hammer could not determine path delimeter!")

    # validate correct top folder
    assert src_abs.split(delimeter)[-1*len(root_target):] == root_target
    
    # get subdirs, exclude unwanted
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split(delimeter)[-1] not in exclude]
    for dir in dirs: sys.path.append(dir)    # add all subdirectories to python path

if __name__ == "__main__":  # execute path hammer if this script is run directly
    path_hammer(1, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #

# local imports
from abstract_control import AbstractControl
from system_flags import StatusFlags, CommandFlags

from printer_thread import PrinterThread

# local config
RESULT_TIMEOUT = 10


class ControlLayer(AbstractControl):
    """This class implements the Control Layer's specified interface, providing the upper layers
    public access to its required functionality. It coordinates Plasmetry's operation at the top
    level. This includes controlling the experiment and lower layers, managing data and overall
    creating and control objects used by other layers. Data management encompases maintaining the
    the system's configuration, provided by the ConfigManager subcomponent, and handling experiment
    results, which is done by the FileUpload subcomponent.
    
    Public methods include setters/getters for config values, config file operations, 
    start/stop/setup functions for experiments, getters for control objects, and a 
    system-wide shutdown method.

    The Control Layer is instantiable without arguments. It includes optional arguments that may
    be used to define specialized behavior, otherwise it uses default values.

    Class Attributes:
        + file_upload_mod: str - module name of the file upload subcomponent
        + config_manager_mod: str - module name of the config manager subcomponent
        + diagnostics_layer_mod: str - module name of the lowe layer component

    Instance Attributes:
        + name: str - name identifying the layer for printing purposes
        + debug: bool - Defines printing behavior for the lower layers.
        + log_text: bool - Defines whether or not to output text to a log file.
        + config_pathname: str - Path and name for the config file.
        # _say_obj: SayWriter - text output object
        # _printer: PrinterThread - used to output buffered text, specified at the constructor.
        # _status: StatusFlags - control object consisting of system-wide state indicators.
        # _commands: CommandFlags - control object consisting of system-wide action triggers.
        # _results: Queue - thread-safe queue to receive experiment results from lower layers.
        # _real_time_param: list - reference to shared memory updated with display values for UI. 
        # _diagnostics: DiagnosticsLayer - instantiated lower layer object.
        # _file_upload_cls: uninstantiated FileUpload class, instantiated for every experiment.
        # _config_manager: ConfigManager - instantiated config manager subcomponent.
        # _ready: Event - local state indicator; set when the layer is ready for diagnostics.
        # _terminated: - indicates whether the layer has shutdown
        - __selected_probe: - Stores an ID for the probe selected to be used in the experiment.

    Methods:
        + __init__(): instantiates an object of the class

    Config Methods:
        + set_config(): save a config value to memory
        + get_config(): read a config value from memory
        + save_config_file(): write config values in memory to a config file
        + load_config_file(): load config values into memory from a config file
    
    System Actions:
        + setup_experiment(): begin initializations for plasma diagnostics
        + start_experiment(): perform plasma diagnostics
        + stop_experiment(): halt plasma diagnostics
        + layer_shutdown(): initiate system-wide shutdown

    Control Object Getters:
        + get_status_flags(): returns state indicators
        + get_command_flags(): returns action triggers
        + get_real_time_container(): returns object concurrently updated with new data

    Layer Utils:
        # _info(): returns information about a layer's subcomponents
        # _load_all_subcomponents(): returns uninstantiated classes of subcomponents
        - __make_printer(): instantiates, starts, and returns a PrinterThread
        - __diagnostics_args(): returns arguments needed to instantiate the DiagnosticsLayer class
        - __file_upload_args(): returns arguments needed to instantiate the FileUpload class
        - __config_manager_args(): returns arguments needed to instantiate the ConfigManager class
        ^+ say(): print messages to configured output
        ^# _load_mod(): returns a module for a subcomponent

    """
    # Default subcomponent module names
    file_upload_mod = 'file_upload'
    config_manager_mod = 'config_manager'

    # Default lower layer module name
    diagnostics_layer_mod = 'diagnostics_layer'


    def __init__(self,
                 name:str="CTRL",
                 debug:bool=False,
                 config_pathname="configuration_file.json",
                 buffer_text:bool=True,
                 log_text: bool=True,
                   *args, **kwargs):
        """The constructor for the ControlLayer class, all of its arguments are optional.
        
        Arguments:
            name: str - Label used for text output
                    default: 'CTRL'
            debug: bool - Defines printing behavior for diagnostic layer
                    default: False
            config_pathname: str - Path and name to the config file
                    default: 'configuration_file.json'
            buffer_text: bool - Defines all text output will be buffered for PrinterThread
                    default: True
            log_text: bool - Defines whether text output should be saved to a log file
                    default: True
        
        """
        # save arguments
        self.debug = debug
        self.log_text = log_text
        self.config_pathname = config_pathname
        
        # validate if a PrinterThread is needed
        if buffer_text:
            self._printer = self.__make_printer()  # create and launch printer thread
            writer = self._printer.get_writer()    # get text output object
        else:
            self._printer = None  # do not create printer thread
            writer = None         # use default text output

        # call parent constructor
        super().__init__(*args, name=name, text_out=writer, **kwargs)


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

        self.__selected_probe = None

        
    # ----- Config Manipulations ----- #
    def set_config(self, probe_id, key, value) -> Tuple[bool, str]:
        """Mutator function, edits the in memory configuration values."""
        self._config_manager.set_config(probe_id, key, value)

    def get_config(self, probe_id, key) -> any:
        """Accessor function, receives data from the in memory configuration values."""
        return self._config_manager.get_config(probe_id, key)

    def save_config_file(self) -> bool:
        """Config file writer."""
        self._config_manager.save_config_file()

    def load_config_file(self) -> None:
        """Config file loader."""
        self._config_manager.load_config_file()


    # ----- Control Object Getters ----- #
    def get_status_flags(self) -> StatusFlags:
        """Returns the status flag control object."""
        return self._status

    def get_command_flags(self) -> CommandFlags:
        """Returns the command flags control object."""
        return self._commands
    
    def get_real_time_container(self) -> Tuple[list, Event]:
        """Returns the real time parameter container and a flag that is set by lower layers when the
        container has been refreshed with new parameters for display. This only needs to be called
        once, if the caller stores the reference to the list, because it is updated in place.

        """
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
                    self.say(str(eq))     
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
            self.say("starting experiment...")
            self._ready.clear()     # cannot be 'ready' for diagnostics once diagnostics start
            self._diagnostics.start_diagnostics()   # trigger diagnostics in lower layers

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
                self.say(f"{len(results)} data-points obtained.")

                # Make a single-use FileUpload object
                uploader = self._file_upload_cls(**self.__file_upload_args())
                Thread(target=uploader.new_data, args=[results], daemon=False,).start()

                self.__selected_probe = None    # clear probe selection

            # get results timed out 
            except Empty:
                self.say("could not obtain results!")

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

        self._terminated.set()          # indicate layer has finished shutting down
    

    # ----- Layer Specific Utils ----- #
    def _info(self) -> list:
        """Return info about the instantiated layer's subcomponents, including lower layers.
        Used for debugging system integration.

        """
        sub = [
            ("Control", "File Upload", str(self._file_upload)),
            ("Control", "Config Manager", str(self._config_manager)),
            ("Control", "Diagnostics Layer", str(self._diagnostics)),
        ]
        sub.extend(self._diagnostics._info())
        return sub
        
    def _load_all_subcomponents(self) -> dict:
        """Returns a dictionary with all the subcomponent classes corresponding to this layer."""
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
        """Returns a running PrinterThread object. Creates a log file to and configures the 
        PrinterThread to output to stdout and the file. Instantiates and starts the PrinterThread.

        """
        # create kill switch for PrinterThread
        kill = Event()
        kill.clear()

        printer_output = [None]  # output to default stdout

        # create output log file
        if self.log_text:
            log_time = str(datetime.datetime.now()).replace(':', '_')
            src_path = os.path.dirname(__file__)

            log_fold = "../../run_logs"
            log_fold = os.path.abspath(f"{src_path}/{log_fold}")
            if not os.path.exists(log_fold):
                os.mkdir(log_fold)

            log_name = f"LOG_{log_time}.txt"
            log_path = os.path.abspath(f"{log_fold}/{log_name}")
            log = open(log_path, 'a')

            printer_output.append(log)

        # create and launch printer thread
        printer = PrinterThread(kill=kill, text_out=printer_output)  # create thread
        printer.start()  # launch thread

        # get writer object and write log name to log file's header
        writer = printer.get_writer()
        writer(f"# {log_name}")

        return printer

    def __diagnostics_args(self):
        """Returns a dictionary packed with arguments to instantiate the DiagnosticsLayer object."""
        args = {
            "text_out": self._say_obj,
            "status_flags": self._status,
            "command_flags": self._commands,
            "results_buffer": self._results,
            "real_time_param": self._real_time_param,
            "debug": self.debug
        }
        return args
    
    def __file_upload_args(self):
        """Returns a dictionary packed with arguments to instantiate the FileUpload object."""
        args = {
            "text_out": self._say_obj,
            "status_flags": self._status,
            "command_flags": self._commands,
            "probe_type": self.__selected_probe,
            "local_path": self._config_manager.config_ref["local_path"],
            "credentials_path": self._config_manager.config_ref["credentials_path"],
            "experiment_name": self._config_manager.config_ref["experiment_name"],
            "folder_id": self._config_manager.config_ref["folder_id"]

        }
        return args
    
    def __config_manager_args(self):
        """Returns a dictionary packed with arguments to instantiate the ConfigManager object."""
        args = {
            "text_out": self._say_obj,
            "status_flags": self._status,
            "command_flags": self._commands,
            "path_name": self.config_pathname
        }
        return args
