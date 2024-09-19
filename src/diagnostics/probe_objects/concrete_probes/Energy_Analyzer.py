# author: figueroa_90894@students.pupr.edu
# status: WIP

# built-in imports
import sys
import os

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 3             # how many parent folders to reach /plasmetry/src

    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..') # absolute path to plasmetry/src
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__'] # get subdirs, exclude __pycache__
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: subdirectories appended to python path")
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

    def __continue(self):
        """<...>"""
        conditionA = self.command_flags.diagnose.is_set()
        conditionB = not self.command_flags.shutdown.is_set()
        return conditionA and conditionB

    def _THREAD_MAIN_(self):
        """<...>"""
        self.say("starting data acquisition...")
        # Continuously acquire data samples until user halts the operation
        while self.__continue():
            samples = self.sweep()      # perform a voltage sweep and get the samples
            self.data_buff.put(samples) # return samples to ProbeOperation
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
