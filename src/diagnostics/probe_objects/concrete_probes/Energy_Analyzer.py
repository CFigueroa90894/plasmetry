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
    """<...>"""
    def __init__(self,
                 rejector_bias:float,
                 collector_bias:float,
                 rejector_amp,
                 collector_amp,
                 *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

        # PROBE CONFIG
        self.rejector_bias = rejector_bias      # fixed voltage bias applied to particle rejector
        self.collector_bias = collector_bias    # fixed voltage bias applied to particle collector

        # PROBE SUBCOMPONENTS
        self.rejector_amp = rejector_amp    # set voltage to reject particles at outer subcomponent
        self.collector_amp = collector_amp  # set voltage to attract particles at innermost subcomponent

    def run(self):
        """<...>"""
        super().run()

    def _THREAD_MAIN_(self):
        """<...>"""
        self.say("starting data acquisition...")
        # Continuously acquire data samples until user halts the operation
        while self.diagnose.is_set():
            # sweep method traps loop until samples are acquired (desired to prevent corruption)
            self.data_buff.put(self.sweep()) # perform sweep and return samples to ProbeOperation
        self.say("completed data acquisition")

    def _thread_setup_(self):
        """<...>"""
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
        """<...>"""
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
