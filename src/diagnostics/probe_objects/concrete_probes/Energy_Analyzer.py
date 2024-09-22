""" G3 - Plasma Devs
Layer 3 - Diagnostics - Energy Analyzer
    Provides a concrete class for Energy Analyzers, a specialized type of sweeper probes. Currently,
    our implementations supports Hyperbolic Energy Analyzers and Ion energy Analyzers. The equations
    provided by the calculations factory allow them to obtain either electron parameters, or ion
    parameters, depending on the polarity of the biases applied to the rejector and collector.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    EnergyAnalyzer

"""

# author: figueroa_90894@students.pupr.edu
# status: WIP

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
from Sweeper_Probe import SweeperProbe


# local config
RELAY_PAUSE = 3

class EnergyAnalyzer(SweeperProbe):
    """This class defines a concrete implementation for HEA and IEA probes, inheriting its sweep
    functionality from SweeperProbe, and extending it to operate the fixed biases on the particle
    rejector and collector. The difference between HEAs and IEAs in physical construction is almost
    negligible, and most their equations are shared. Thus, the software can operate both types of
    probes in the same manner. However, the minor details in the construction of their rejector and
    collector subcomponents may cause the equations to yield different values for a body of plasma
    under the same conditions.
    
    In addition to the attributes that distuinguish this implementation from simple sweeper probes,
    this class also redefines the threaded life-cycle methods that make up its data acquisition
    functionality, as it is specific to HEAs and IEAs.

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
        + rejector_bias: float - fixed voltage bias applied to the particle rejector
        + collector_bias: float - fixed voltage bias applied to the particle collector
        + rejector_amp: HighVoltAmp - controls the amplifier that biases the particle rejector
        + collector_amp: HighVoltAmp - controls the amplifier that biases the particle collector
        ^+ sweeper_shunt: float - shunt resistance to calculate current through the probe
        ^+ sweeper: VoltageSweeper - outputs premapped voltage steps from the associated amplifier
        ^# _premap_bias: list - precalculated DAC outputs that produce desired HV output at the amp
        ^+ sampling_rate: int - samples to obtain per second (Hz)
        ^+ num_samples: int - number of measurements per voltage sweep
        ^+ relay_set: RelaySet - collection of relays to energize the amplifiers

    Methods:
        + __init__() - initialize the object, called by subclasses
        # _THREAD_MAIN_() - the main loop of the thread, repeatedly invokes the sweep() method
        # _thread_setup_() - zeros and enables the probe circuit
        # _thread_cleanup_() - zeros and disables the probe circuit, then resets the DAC output
        ^+ sweep() - performs one voltage sweep, applying one voltage when sample trigger is set
        ^+ preprocess_samples() - formats data samples and adds config data required by calculations
        ^+ run() - perform data acquistion, override in subclasses
        ^+ preprocess_samples() - provides external threads formatting required by calculations
        ^+ run() - executes the threads three life-cycle methods
        ^+ pause() - blocks the thread's execution for a specified time
        ^+ say() - text output method, using the SayWriter
        ^# _delay_start() - blocks the thread's startup until a specified time passes
        ^# _barrier_wait() - blocks the thread's startup until other threads are at the barrier
        ^# _wake() - callback function to wake up a paused thread

    """
    def __init__(self,
                 rejector_bias:float,
                 collector_bias:float,
                 rejector_amp,
                 collector_amp,
                 *args, **kwargs):
        """The constructor for the EnergyAnalyzer class, it sets the attributes associated to
        this specialized type of probe that is lacking in simple sweeper probes.
        
        Arguments:
            rejector_bias: float - the desired high voltage bias that is applied to the rejector
            collector_bias: float - the desired high voltage bias that is applied to the collector
            rejector_amp: HighVoltAmp - controls the amplifier that biases the rejector
            collector_amp: HighVoltAmp - controls the amplifier that biases the collector
        """
        super().__init__(*args, **kwargs)

        # PROBE CONFIG
        self.rejector_bias = rejector_bias      # fixed bias applied to particle rejector
        self.collector_bias = collector_bias    # fixed bias applied to particle collector

        # PROBE SUBCOMPONENTS
        self.rejector_amp = rejector_amp    # sets to reject particles at outer subcomponent
        self.collector_amp = collector_amp  # sets to attract particles at innermost subcomponent

    def run(self):
        """Calls the parent run method."""
        super().run()

    def _THREAD_MAIN_(self):
        """The main loop of the EnergyAnalyzer data acquisition process. It traps the thread's
        execution in a while loop until the user halts diagnostics. Every iteration blocks until
        a full voltage sweep is performed, and places the obtained samples a in thread-safe queue.
        
        """
        self.say("starting data acquisition...")
        # Continuously acquire data samples until user halts the operation
        while self.diagnose.is_set():
            # sweep method traps loop until samples are acquired (desired to prevent corruption)
            self.data_buff.put(self.sweep()) # perform sweep and return samples to ProbeOperation
        self.say("completed data acquisition")

    def _thread_setup_(self):
        """Called before _THREAD_MAIN_ by the run() method. It first sets the operating status flag
        to indicate the high voltage amplifiers are energized. Next, it sets the sweeper amplifier's
        output to 0 volts, and the collector and rejector amplifiers to their fixed biases. It then
        all enables all relays for its amplifiers. After pausing to allow the relays to close, the
        thread blocks in parent method until it synchronizes with the clock thread. When it does,
        the thread proceeds to its main loop.

        """
        # notify circuit is active
        self.say("enabling probe circuit...")   # log message to file
        self.status_flags.operating.set()       # set status indicator to True

        # set initial state of amplifiers
        self.sweeper.zero()                             # set sweeper amp output to zero
        self.rejector_amp.write(self.rejector_bias)     # set rejector fixed bias
        self.collector_amp.write(self.collector_bias)   # set collector fixed bias

        # enable relays
        self.relay_set.set()        # set all DOUT channels to HIGH
        self.pause(RELAY_PAUSE)     # wait for relays to close

        # call parent setup to synchronize with clock
        super()._thread_setup_()

    def _thread_cleanup_(self):
        """Called after the thread exits the main loop when the user halts diagnostics or unhandled
        exceptions are raised in the main loop. This allows the thread to safely disable the probe
        circuit in the event of a system crash.

        This method sets all amplifier outputs to 0 volts, then disables their relays. It blocks to
        allow the relays to open. Once the amplifiers are no longer energized, the thread resets its
        DAC outputs to 0 volts and clears the operating status flag. Lastly, it invokes its parent's
        cleanup method to terminate.
        
        """
        self.say("disabling probe circuit...")  # log message to file

        # set amplifier outputs to zero
        self.sweeper.zero()
        self.rejector_amp.zero()
        self.collector_amp.zero()

        # disable relays
        self.relay_set.clear()              # set all DOUT channel to LOW
        self.pause(RELAY_PAUSE)             # wait for relays to open

        # set all DAC outputs to zero once relays are disconnected
        self.sweeper._output.write(0)
        self.rejector_amp._output.write(0)
        self.collector_amp._output.write(0)

        self.status_flags.operating.clear() # notify circuit is inactive
        super()._thread_cleanup_()          # call parent cleanup
