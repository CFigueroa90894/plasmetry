# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings
#   - implement run()

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

class LangmuirProbe(SweeperProbe):
    """<...>"""
    def __init__(self, *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)   # initialize attributes inherited from parent

    def run(self):
        """<...>"""
        super().run() 

    def __continue(self):
        """<...>"""
        condition = self.command_flags.diagnose.is_set()
        condition = condition and not self.command_flags.shutdown.is_set()
        return condition

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
        self.say("enabling probe circuit...")
        self.status_flags.operating.set()   # notify circuit is active are enabled
        self.sweeper.zero()                 # set sweeper amp output to zero
        self.relay_set.set()                # enable relays
        self.pause(RELAY_PAUSE)             # wait for relays to close
        super()._thread_setup_()            # call parent setup

    def _thread_cleanup_(self):
        """<...>"""
        self.say("disabling probe circuit...")
        self.sweeper.zero()                 # set sweeper amp output to zero
        self.relay_set.clear()              # disable the relays
        self.pause(RELAY_PAUSE)             # wait for relays to open
        self.sweeper._output.write(0)       # set DAC output to zero
        self.status_flags.operating.clear() # notify circuit is inactive
        super()._thread_cleanup_()          # call parent cleanup


