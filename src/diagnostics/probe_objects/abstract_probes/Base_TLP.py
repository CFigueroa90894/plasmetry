""" G3 - Plasma Devs
Layer 3 - Diagnostics - Base TLP
    Provides a base class for concrete TLP probe classes, implementing the attributes they share.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    BaseTLP
"""

# built-in imports
import sys
import os

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
    path_hammer(3, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #

# local imports
from Base_Probe import BaseProbe

class BaseTLP(BaseProbe):
    """This class defines a base parent for Triple Langmuir Probe objects (TLP), inheriting
    general attributes from the BaseProbe class.

    Attributes (Config and Control):
        ^+ probe_id - identifier for the probe's type
        ^+ sys_ref: dict - reference to system settings
        ^+ config_ref: dict - reference to user settings
        ^+ status_flags - state indicators
        ^+ command_flags - action triggers
        ^+ data_buff: Queue - buffer to return data samples
        ^+ delay: float - seconds that the thread should wait before entering its main loop
        ^+ barrier: Barrier - synchronization primitive, blocks until other threads are ready
        ^+ pause_sig: Event - flag used locally to pause a threads execution
        ^# _say_obj: SayWriter - text output object used to write messages
    
    Attributes (Data Acquisition)
        + up_amp: HighVoltAmp - hardware object to control the associated amplifier
        + up_amp_bias: float - desired high voltage output for the upper probe amplifier (Volts)
        + up_collector: VoltageSensor - obtains voltage measurements
        + up_shunt: float - shunt resistance to calculate current through the upper probe
        ^+ sampling_rate: int - samples to obtain per second (Hz)
        ^+ num_samples: int - number of measurements per averaging window
        ^+ relay_set: RelaySet - collection of relays to energize the amplifiers

    Methods:
        + __init__() - initialize the object, called by subclasses
        ^+ run() - perform data acquistion, override in subclasses
        ^+ preprocess_samples() - provides external threads formatting required by calculations
        ^+ run() - executes the threads three life-cycle methods
        ^+ pause() - blocks the thread's execution for a specified time
        ^+ say() - text output method, using the SayWriter
        ^# _THREAD_MAIN_() - the main loop of the thread
        ^# _thread_setup_() - performs preparations before the _THREAD_MAIN_() method is called
        ^# _thread_cleanup_() - performs exit actions before finally terminating the thread
        ^# _delay_start() - blocks the thread's startup until a specified time passes
        ^# _barrier_wait() - blocks the thread's startup until other threads are at the barrier
        ^# _wake() - callback function to wake up a paused thread
    
    """
    def __init__(self,
                 up_amp_bias: float,
                 up_amp,
                 up_collector,
                 up_shunt:float,
                 *args, **kwargs):
        """Constructor for the BaseTLP class, accepts arguments associated with the upper probe.
        
        Arguments:
            up_amp_bias: float - desired HV amplifier output (Volts)
            up_amp: HighVoltAmp - takes a desired bias and outputs it from the amplifier
            up_collector: VoltageSensor - reads voltage samples across the collector shunt resistor
            up_shunt: float - resistance of the associated shunt

        """
        super().__init__(*args, **kwargs)

        # PROBE CONFIG
        self.up_amp_bias = up_amp_bias  # fixed voltage bias applied to the upper probe
        self.up_shunt = up_shunt

        # PROBE SUBCOMPONENTS
        self.up_amp = up_amp               # Set voltage source output
        self.up_collector = up_collector   # Obtain voltage samples to calculate probe current.

    def run(self):
        """Invokes the parent run() method; called by the threading library when start() is called
        on this object.

        """
        super().run()