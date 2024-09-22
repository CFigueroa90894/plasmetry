""" G3 - Plasma Devs
Layer 3 - Diagnostics - Sweeper Probe
    Provides a parent class for concrete probe classes that require voltage sweeps. This class
    specifies required methods and implements common functionality.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    SweeperProbe

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
from Base_Probe import BaseProbe        # parent class


class SweeperProbe(BaseProbe):
    """This class defines a base parent for any probe type that requires voltage sweeps. For
    our current implementation, this includes Single Langmuir Probes, Double Langmuir Probes,
    Hyperbolic Energy Analyzers, and Ion Energy Analyzers. It inherits general attributes from
    BaseProbe. Sweeper probes in general apply a biasing voltage in incremental steps. The measured
    voltages are used to calculate current through the sweeper probe. This current can be plotted
    against the applied voltage steps, yielding a plot known as Current-Voltage Curve (I-V curve).
    This plot is analyzed to obtain several plasma parameters, which turn allow us to calculate
    more plasma parameters.

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
        + sweeper_shunt: float - shunt resistance to calculate current through the probe
        + sweeper: VoltageSweeper - outputs premapped voltage steps from the associated amplifier
        # _premap_bias: list - precalculated DAC outputs that produce desired HV output at the amp
        ^+ sampling_rate: int - samples to obtain per second (Hz)
        ^+ num_samples: int - number of measurements per voltage sweep
        ^+ relay_set: RelaySet - collection of relays to energize the amplifiers

    Methods:
        + __init__() - initialize the object, called by subclasses
        + sweep() - performs one voltage sweep, applying one voltage when sample trigger is set
        + preprocess_samples() - formats data samples and adds config data required by calculations
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
                 sweeper,
                 collector,
                 sweeper_shunt:float,
                 *args, **kwargs
                 ):
        """Constructor for the SweeperProbe class, accepts arguments related with the voltage
        sweeper amplifier and its associated collector.

        Arguments:
            sweeper: VoltageSweeper - outputs premapped voltage steps from its associated amplifier
            collector: VoltageSensor - reads voltage samples across the collector shunt resistor
            sweeper_shunt: float - resistance of the associated shunt

        """
        super().__init__(*args, **kwargs)   # initialize attributes inherited from parent

        # PROBE INFO
        self.sweeper_shunt = sweeper_shunt

        # PROBE SUBCOMPONENTS
        self.sweeper = sweeper      # output voltages to sweeper source
        self.collector = collector  # obtain voltage samples to calculate probe current

        # pre-mapped sweep steps
        self._premap_bias = []
        for pair in self.sweeper._premap:
            self._premap_bias.append(pair[1])  # make list of desired high voltage bias

    def preprocess_samples(self, raw_samples: list):
        """Returns a packed dictionary with raw samples and config values identified by the standard
        keys that the calculations subcomponent uses to retrieve them.

        The raw_samples argument should be the unmodified value enqueued by the sweep() method into
        the data buffer. This guarantees that for any 'n-th' step in the sweep, indexing both the
        self._premap_bias list and the raw_samples argument list by 'n' will yield the premapped
        applied-bias that produced the measured raw-voltage response from the plasma:
            i.e. 'n' maps applied biases to measured voltages.

        Sweeper probe equations use "<...analytic methods...>" to obtain initial values for
        the sequentially applied equations. Therefore, they require a complete data set in order to 
        obtain plasma parameters. In this case, a complete data set corresponds to a full sweep.
        
        This method should NOT be invoked by the probe's data acquisition thread. Instead, the
        ProbeOperation thread must collect the samples from the data buffer and call this method
        from a separate thread. This method solely exists to ensure the ProbeOperation thread and
        the calculations subcomponent are decoupled from specific probe implementations while still
        maintaining compatibility.

        """
        samples = {
            "Bias 1": self._premap_bias,
            "Shunt 1":  self.config_ref["sweeper_shunt"],
            "Raw Voltage 1": raw_samples,
        }
        return samples

    def sweep(self):
        """Performs a single voltage sweep using the sweeper object. Returns a list of measured
        voltages acquired for each sweep step.
        
        """
        # setup
        volt_samps = []   # list of measured voltages

        # iterate through premapped voltage steps 
        for index in range(self.num_samples):
            self.sample_trig.wait()             # wait for 'get sample' signal

            # get sample
            self.sweeper.write(index)  # output the voltage step in the given index
            volt_samps.append(self.collector.read())  # read and save voltage sample
            
            # reset the signal
            self.sample_trig.clear()

        return volt_samps

