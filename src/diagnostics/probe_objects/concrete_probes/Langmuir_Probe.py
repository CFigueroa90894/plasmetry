""" G3 - Plasma Devs
Layer 3 - Diagnostics - Langmuir Probe
    Provides a concrete class for Langmuir Probes, for our current implementations this supports
    Single Langmuir Probes and Double Langmuir Probes. It inherits from the SweeperProbe class.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    LangmuirProbe

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
from Sweeper_Probe import SweeperProbe

# local config
RELAY_PAUSE = 3

class LangmuirProbe(SweeperProbe):
    """This class defines a concrete implementation for SLPs and DLPs, inheriting its sweep
    functionality directly from the SweeperProbe, and indirectly inheriting general attributes
    from BaseProbe. Though an SLP and DLP differ in physical makeup, their operation and components
    remain the same, their difference being the equations they use to calculate plasma paramaters.

    Note that all their attributes are inherited, as they are in simple sweeper probes, therefore,
    even its constructor is entirely inherited. However, this class does in fact redefine the thread
    life-cycle methods that make up their data acquisition functionality, as they are specific to
    SLPs and DLPs.

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
        ^+ sweeper_shunt: float - shunt resistance to obtain current through the probe
        ^+ sweeper: VoltageSweeper - outputs premapped voltage steps from the associated amplifier
        ^# _premap_bias: list - precalculated DAC outputs that produce desired HV output at the amp
        ^+ sampling_rate: int - samples to obtain per second (Hz)
        ^+ relay_set: RelaySet - collection of relays to energize the amplifiers

    Methods:
        ^+ __init__() - initialize the object, called by subclasses
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
    def __init__(self, *args, **kwargs):
        """The constructor for the LangmuirProbe class, it is directly inherited from its parent."""
        super().__init__(*args, **kwargs)   # initialize attributes inherited from parent

    def run(self):
        """The method invoked by the threading framework when start() is called on this object."""
        super().run() 

    def _THREAD_MAIN_(self):
        """The main loop of the LangmuirProbe data acquisition process. It traps the thread's
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
        """Called before _THREAD_MAIN_ by the run() method. Initially, it sets the operating status
        flag to true to indicate the high voltage amplifiers are energized. Next, it sets the
        sweeper amplifier's output to 0 volts, and enables its relays. After pausing to allow the
        relays to close, the thread blocks in the parent's setup method until it synchronizes with
        the clock thread. Once it releases, the thread proceeds to its main loop.

        """
        # notify circuit is active
        self.say("enabling probe circuit...")   # log message to file
        self.status_flags.operating.set()       # set status indicator to True

        # set initial state of amplifiers
        self.sweeper.zero()  # set sweeper amp output to zero

        # enable relays
        self.relay_set.set()        # set all DOUT channels to HIGH
        self.pause(RELAY_PAUSE)     # wait for relays to close

        # call parent setup to synchronize with clock
        super()._thread_setup_()

    def _thread_cleanup_(self):
        """Called after the thread exits the main loop when the user halts diagnostics or unhandled
        exceptions are raised in the main loop. This allows the thread to safely disable the probe
        circuit in the event of a system crash.

        This method sets the sweeper amplifier's output to 0 volts, then disables its relays. It
        blocks to allow the relays to open. Once the amplifiers are no longer energized, the thread
        resets its DAC output to 0 volts and clears the operating status flag. Finally, it invokes
        its parent's cleanup method to terminate.

        """
        self.say("disabling probe circuit...")  # log message to file

        # set amplifier outputs to zero
        self.sweeper.zero()

        # disable relays
        self.relay_set.clear()              # set all DOUT channel to LOW
        self.pause(RELAY_PAUSE)             # wait for relays to open

        # set all DAC outputs to zero once relays are disconnected
        self.sweeper._output.write(0)

        self.status_flags.operating.clear() # notify circuit is inactive
        super()._thread_cleanup_()          # call parent cleanup

