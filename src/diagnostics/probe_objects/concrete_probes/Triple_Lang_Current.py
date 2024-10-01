""" G3 - Plasma Devs
Layer 2 - Diagnostics - Triple Lang Current
    Provides a concrete class to operate a Triple Langmuir Probe, specifically in its Current Mode
    configuration. It inherits from the BaseTLP class.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    TripleLangCurrent

Triple Langmuir Probe - Current Mode
            - V1 +                          V1 - 'Raw Voltage 1'         (sampled across shunt_1)
    - |-------S1------- up probe            S1 - 'Shunt 1': up_shunt     (shunt resistor)
  B1  A1                                    A1 - Up Probe Amp            (up_amp)
    + |                                     B1 - 'Bias 1': up_amp_bias   (applied bias)
      |---------------- center probe        
    + |                                     B2 - 'Bias 2': down_amp_bias (applied bias)
  B2  A2                                    A2 - Down Probe Amp          (down_amp)
    - |-------S2------- down probe          S2 - 'Shunt 2': down_shunt   (shunt resistor)
            - V2 +                          V2 - 'Raw Voltage 2'         (sampled across shunt_2)
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
from Base_TLP import BaseTLP

# local config
RELAY_PAUSE = 3

class TripleLangCurrent(BaseTLP):
    """This class defines a concrete implementation of TLP-C (TLC), inheriting many of its
    attributes from the BaseTLP class. The TLP-Cs main characteristic is its two physical biasing
    amplifiers apply voltage differences from the upper and lower probes to the center probe. This
    allows the center probe to be used as a reference point when calculating currents through the
    upper and lower probes. The currents obtained by dividing the upper and lower probe's measured
    voltages by their respective shunt's resistance can be used to calculate the current through the
    center probe. The proportion of the difference in currents is then used to calculate plasma
    parameters.

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
        + down_amp_bias: float - desired HV amplifier output (Volts)
        + down_amp: HighVoltAmp - takes a desired bias and outputs it from the amplifier 
        + down_collector: VoltageSensor - voltage difference between the center and floating probe
        + down_shunt: float - resistance of the associated shunt
        + up_probe_window: list - retains recent samples for an averaging window
        + down_probe_window: list - retains recent samples for an averaging window
        ^+ up_amp: HighVoltAmp - hardware object to control the associated amplifier
        ^+ up_amp_bias: float - desired high voltage output for the upper probe amplifier (Volts)
        ^+ up_collector: VoltageSensor - obtains voltage measurements across its shunt
        ^+ up_shunt: float - shunt resistance to calculate current through the upper probe
        ^+ sampling_rate: int - samples to obtain per second (Hz)
        ^+ num_samples: int - number of measurements per averaging window
        ^+ relay_set: RelaySet - collection of relays to energize the amplifiers

    Methods:
        + __init__() - initialize the object, called by subclasses
        + preprocess_samples() - provides external threads formatting required by calculations
        # _THREAD_MAIN_() - the main loop of the thread
        # _thread_setup_() - performs preparations before the _THREAD_MAIN_() method is called
        # _thread_cleanup_() - performs exit actions before finally terminating the thread
        ^+ run() - executes the threads three life-cycle methods
        ^+ pause() - blocks the thread's execution for a specified time
        ^+ say() - text output method, using the SayWriter
        ^# _delay_start() - blocks the thread's startup until a specified time passes
        ^# _barrier_wait() - blocks the thread's startup until other threads are at the barrier
        ^# _wake() - callback function to wake up a paused thread
    
    """
    def __init__(self,
                 down_amp_bias:float,
                 down_amp,
                 down_collector,
                 down_shunt,
                 *args, **kwargs):
        """Constructor for TripleLangCurrent class. It accepts HighVoltAmp and VoltageSensor objects
        as well as their associated bias and shunt resistor.
        
        Instantiates two empty lists to track samples for an averaging window. The object's
        num_samples attribute determines how many samples are retained in each window.

        Arguments:
            down_amp_bias: float - desired HV amplifier output (Volts)
            down_amp: HighVoltAmp - takes a desired bias and outputs it from the amplifier
            down_collector: VoltageSensor - reads voltage samples across the collector shunt resistor
            down_shunt: float - resistance of the associated shunt

        """
        super().__init__(*args, **kwargs)

        # PROBE CONFIG
        self.down_amp_bias = down_amp_bias
        self.down_shunt = down_shunt
        
        # PROBE SUBCOMPONENTS
        self.down_amp = down_amp              # set applied voltage to lower source
        self.down_collector = down_collector  # obtain voltage to calculate current through probe

        # Averaging windows
        self.up_probe_window = []
        self.down_probe_window = []

    def run(self):
        """Calls the parent run() method. Called by the threading framework when start() is invoked
        on this object.
        
        """
        super().run() 

    def preprocess_samples(self, raw_samples:list):
        """Returns a packed dictionary with raw samples and config values identified by the standard
        keys that the calculations subcomponent uses to retrieve them.
        
        The raw_samples argument should be the unmodified value enqueued by the probe thread into
        the data buffer. This guarantees that the first index maps to the voltage measured across
        the upper-probe collector's shunt, and the second index maps to the voltage measured across
        the down-probe collector's shunt.

        Since TLP equations require only one data-point, (unlike sweeper probes), they do not
        require larger data. For every sample obtained, this method packs the previous 'n' samples
        into its return value. Thus, the calculations subcomponent can apply basic low-pass
        filtering with a simple moving average technique, while maintaining a significantly smaller
        data set than sweeper probes.
        
        This method should NOT be invoked by the probe's data acquisition thread. Instead, the
        ProbeOperation thread must collect the samples from the data buffer and call this method
        from a separate thread. This method solely exists to ensure the ProbeOperation thread and
        the calculations subcomponent are decoupled from specific probe implementations while still
        maintaining compatibility.

            raw_samples[0]: up collector sample
            raw_samples[1]: down collector sample

        """
        # append raw samples to windows
        self.up_probe_window.append(raw_samples[0])
        self.down_probe_window.append(raw_samples[1])

        # trim excess samples
        if len(self.up_probe_window) > self.num_samples:
            self.up_probe_window.pop(0)  # remove the first (oldest) sample
            
        if len(self.down_probe_window) > self.num_samples:
            self.down_probe_window.pop(0)  # remove the first (oldest) sample

        # pack sample dictionary
        samples = {
            "Raw voltage 1": self.up_probe_window[:],
            "Raw voltage 2": self.down_probe_window[:],
            "Shunt 1": self.up_shunt,
            "Shunt 2": self.down_shunt,
            "Bias 1": self.up_amp_bias,
            "Bias 2": self.down_amp_bias,
        }
        return samples

    def _THREAD_MAIN_(self):
        """The main thread loop for the 'Triple Langmuir Probe - Current Mode' (TLP-C | TLC) data
        acquisition process. It traps the thread's execution in a while loop until the user halts
        diagnostics. Every iteration blocks until the sample trigger flag is set; when released,
        the thread takes two voltage measures, one for each collector. Samples are placed in a two
        element list, which is enqueued in the data buffer as a single data point.
        
        """
        self.say("starting data acquisition...")  # log message to file
        # Continuously acquire data samples until user halts the operation
        while self.diagnose.is_set():
            self.sample_trig.wait()
            # get and return samples to ProbeOperation as two element list
            self.data_buff.put([self.up_collector.read(), self.down_collector.read()])
            self.sample_trig.clear()
        self.say("completed data acquisition")  # log message to file

    def _thread_setup_(self):
        """Called before _THREAD_MAIN_ by the run() method. Initially, it sets the operating status
        flag to true to indicate the high voltage amplifiers are energized. Next, it sets the two
        biasing amplifier's output to their values, and enables their relays. After pausing to allow
        the relays to close, the thread blocks in the parent's setup method until it synchronizes
        with the clock thread. Once it releases, the thread proceeds to its main loop.

        """
        # notify circuit is active
        self.say("enabling probe circuit...")   # log message to file
        self.status_flags.operating.set()       # set status indicator to True

        # set initial state of amplifiers
        self.up_amp.write(self.up_amp_bias)     # set fixed bias for up probe amp
        self.down_amp.write(self.down_amp_bias) # set fixed bias for down probe amp 

        # enable relays
        self.relay_set.set()        # set all DOUT channels to HIGH
        self.pause(RELAY_PAUSE)     # wait for relays to close

        # call parent setup to synchronize with clock
        super()._thread_setup_()

    def _thread_cleanup_(self):
        """Called after the thread exits the main loop when the user halts diagnostics or unhandled
        exceptions are raised in the main loop. This allows the thread to safely disable the probe
        circuit in the event of a system crash.

        This method sets the both biasing amplifier's output to 0 volts, then disables its relays.
        It blocks to allow the relays to open. Once the amplifiers are no longer energized, the
        thread resets its DAC outputs to 0 volts and clears the operating status flag. Finally, it
        invokes its parent's cleanup method to terminate.

        """
        self.say("disabling probe circuit...")  # log message to file

        # set amplifier outputs to zero
        self.up_amp.zero()
        self.down_amp.zero()

        # disable relays
        self.relay_set.clear()    # set all DOUT channel to LOW
        self.pause(RELAY_PAUSE)   # wait for relays to open

        # set all DAC outputs to zero once relays are disconnected
        self.up_amp._output.write(0)
        self.down_amp._output.write(0)

        self.status_flags.operating.clear() # notify circuit is inactive
        super()._thread_cleanup_()          # call parent cleanup