# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings
#   - add hardware interface objects
#   - implement run
"""
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

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 3             # how many parent folders to reach /plasmetry/src

    # absolute path to plasmetry/src
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..')
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    # get subdirs, exclude __pycache__
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__'] 
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #

# local imports
from Base_TLP import BaseTLP

# local config
RELAY_PAUSE = 3

class TripleLangCurrent(BaseTLP):
    "<...>"
    def __init__(self,
                 down_amp_bias:float,
                 down_amp,
                 down_collector,
                 down_shunt,
                 *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

        # PROBE CONFIG
        self.down_amp_bias = down_amp_bias
        self.down_shunt = down_shunt
        
        # PROBE SUBCOMPONENTS
        self.down_amp = down_amp              # set applied voltage to lower source
        self.down_collector = down_collector  # obtain voltage to calculate current through probe

    def __continue(self):
        """<...>"""
        conditionA = self.command_flags.diagnose.is_set()
        conditionB = not self.command_flags.shutdown.is_set()
        return conditionA and conditionB

    def _THREAD_MAIN_(self):
        """<...>"""
        self.say("starting data acquisition...")  # log message to file

        # get initial samples for dummy averaging window
        first_up_probe_sample = self.up_collector.read()
        first_float_probe_sample = self.float_collector.read()

        # pregen averaging windows from initial samples - list elements duplicated n times, len n
        up_probe_window = [first_up_probe_sample]*self.num_samples
        down_probe_window = [first_float_probe_sample]*self.num_samples

        # Continuously acquire data samples until user halts the operation
        while self.__continue():
            
            # get voltage samples
            up_volt = self.up_collector.read()
            down_volt = self.float_collector.read()

            # slice old window to create new list (needed since list operations are in place)
            # exclude first element by slicing and append new sample
            up_probe_window = up_probe_window[1:].append(up_volt)
            down_probe_window = down_probe_window[1:].append(down_volt)

            # pack samples to pass to ProbeOperation
            samples = {
                "Raw Voltage 1": up_probe_window,
                "Raw Voltage 2": down_probe_window,
                "Bias 1": self.up_amp_bias,
                "Bias 2": self.down_amp_bias,
            }
            self.data_buff.put(samples) # return samples to ProbeOperation
        self.say("completed data acquisition")  # log message to file

    def _thread_setup_(self):
        """<...>"""
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
        """<...>"""
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