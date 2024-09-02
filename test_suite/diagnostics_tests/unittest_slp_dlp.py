# author: figueroa_90894@students.pupr.edu

# built-in imports
import sys
import os

from unittest import main as RUNTESTS, skip

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 2             # how many parent folders to reach /plasmetry/src

    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..') # absolute path to plasmetry/src
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__'] # get subdirs, exclude __pycache__
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #


from unittest_probe_factory import ProbeObj_TestTemplate
from probe_enum import PRB
from Langmuir_Probe import LangmuirProbe
from Sweeper_Probe import SweeperProbe
from Base_Probe import BaseProbe

test_ready = 'WIP'

class SLP_Obj_Test(ProbeObj_TestTemplate):
    def setUp(self):
        super().setUp()
        self.probe = self.factory.make(PRB.SLP)

    # SLP Inheritance
    def test_SLP_inheritance(self):
        """SLP instance inherits correctly."""
        parents = [LangmuirProbe, SweeperProbe, BaseProbe]
        self.check_inheritance(parents)

    # SLP Contents
    @skip("Test not implemented")
    def test_SLP_fresh_contents(self):
        """SLP instantiated with correct attributes."""
        pass


class DLP_Obj_Test(ProbeObj_TestTemplate):
    def setUp(self):
        super().setUp()
        self.probe = self.factory.make(PRB.DLP)

    # DLP Inheritance
    def test_DLP_inheritance(self):
        """DLP instance inherits correctly."""
        parents = [LangmuirProbe, SweeperProbe, BaseProbe]
        self.check_inheritance(parents)

    # DLP Contents
    @skip("Test not implemented")
    def test_DLP_fresh_contents(self):
        """DLP instantiated with correct attributes."""
        pass


if __name__ == "__main__":
    print("\n\nRUNNING SLP AND DLP TESTS\n")
    RUNTESTS(verbosity=2)