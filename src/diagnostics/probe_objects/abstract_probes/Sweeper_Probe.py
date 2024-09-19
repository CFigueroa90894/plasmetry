# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add subcomponents once hardware interface is implemented
#   - implement sweep method

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

    def preprocess_samples(self, samples: dict):
        """<...>
        <...in-place operation...>"""
        samples["Bias 1"] = self._premap_bias   # add list of applied biases to samples dictionary
        samples["Shunt 1"] = self.config_ref["sweeper_shunt"]

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

