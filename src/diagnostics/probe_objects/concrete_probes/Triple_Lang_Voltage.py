# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings
#   - add hardware interface objects
#   - implement run
"""
Triple Langmuir Probe - Voltage Mode
            - V1 +                          V1 - 'Raw Voltage 1'       (sampled across shunt_1)
    - |-------S1------- up probe            S1 - 'Shunt 1': up_shunt   (shunt resistor)
  B1  A1                                    A1 - Up Probe Amp          (up_amp)
    + |                                     B1 - 'Bias 1': up_amp_bias (applied bias)
      |---------------- center probe        
          +                                 V2 - 'Raw Voltage 2'       (sampled center to floating)
          - V2
       ---------------- floating probe
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

class TripleLangVoltage(BaseTLP):
    "<...>"
    def __init__(self,
                 float_collector,
                 *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

        # PROBE SUBCOMPONENTS
        self.float_collector = float_collector     # get voltage difference from center probe down to floating probe

        # Averaging windows
        self.up_probe_window = []
        self.float_probe_window = []

    def run(self):
        """<...>"""
        super().run() 

    def preprocess_samples(self, raw_samples:list):
        """<...>
        <...in-place operation...>
        raw_samples[0]: up collector sample,
        raw_samples[1]: float collector sample
        """
        # append raw samples to windows
        self.up_probe_window.append(raw_samples[0])
        self.float_probe_window.append(raw_samples[1])

        # trim excess samples
        if len(self.up_probe_window) > self.num_samples:
            self.up_probe_window.pop(0)  # remove the first (oldest) sample
            
        if len(self.float_probe_window) > self.num_samples:
            self.float_probe_window.pop(0)  # remove the first (oldest) sample

        # pack sample dictionary
        samples = {
            "Raw voltage 1": self.up_probe_window[:],
            "Raw voltage 2": self.float_probe_window[:],
            "Shunt 1": self.up_shunt,
            "Bias 1": self.up_amp_bias,
        }
        return samples

    def _THREAD_MAIN_(self):
        """<...>"""
        self.say("starting data acquisition...")  # log message to file
        # Continuously acquire data samples until user halts the operation
        while self.diagnose.is_set():
             # get and return samples to ProbeOperation as two element list
            self.data_buff.put([self.up_collector.read(), self.float_collector.read()])
        self.say("completed data acquisition")  # log message to file

    def _thread_setup_(self):
        """<...>"""
        # notify circuit is active
        self.say("enabling probe circuit...")   # log message to file
        self.status_flags.operating.set()       # set status indicator to True

        # set initial state of amplifiers
        self.up_amp.write(self.up_amp_bias)     # set fixed bias output for upper probe amp

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

        # disable relays
        self.relay_set.clear()              # set all DOUT channel to LOW
        self.pause(RELAY_PAUSE)             # wait for relays to open

        # set all DAC outputs to zero once relays are disconnected
        self.up_amp._output.write(0)

        self.status_flags.operating.clear() # notify circuit is inactive
        super()._thread_cleanup_()          # call parent cleanup

