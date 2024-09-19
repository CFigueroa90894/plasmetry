# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add subcomponents once hardware interface is implemented
#   - implement sweep method

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

# TO DO
class SweeperProbe(BaseProbe):
    """<...>"""
    def __init__(self,
                 sweeper,
                 collector,
                 sweeper_shunt:float,
                 *args, **kwargs
                 ):
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
        """<...>
        <...in-place operation...>
        <...should not be called by probe thread loop, probe op instead...>"""
        samples = {
            "Bias 1": self._premap_bias,
            "Shunt 1":  self.config_ref["sweeper_shunt"],
            "Raw Voltage 1": raw_samples,
        }
        return samples

    def sweep(self) -> dict:
        """Performs a single voltage sweep on the sweeper object.
        Returns a dictionary consisting of applied biases and raw sampled voltages."""
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

