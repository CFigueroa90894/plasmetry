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
from Base_Probe import BaseProbe
from Sweeper_Probe import SweeperProbe
from Energy_Analyzer import EnergyAnalyzer

class HEA_Obj_Test(ProbeObj_TestTemplate):
    def setUp(self):
        super().setUp()
        self.probe = self.factory.make(PRB.HEA)

    # HEA Inheritance
    def test_HEA_inheritance(self):
        """HEA instance inherits correctly."""
        parents = [EnergyAnalyzer, SweeperProbe, BaseProbe]
        self.check_inheritance(parents)

    @skip("Test not implemented")
    def test_HEA_fresh_contents(self):
        """HEA instantiated with correct attributes."""
        pass


class IEA_Obj_Test(ProbeObj_TestTemplate):
    def setUp(self):
        super().setUp()
        self.probe = self.factory.make(PRB.IEA)

    # IEA Inheritance
    def test_IEA_inheritance(self):
        """IEA instance inherits correctly."""
        parents = [EnergyAnalyzer, SweeperProbe, BaseProbe]
        self.check_inheritance(parents)

    @skip("Test not implemented")
    def test_IEA_fresh_contents(self):
        """SLP instantiated with correct attributes."""
        pass


if __name__ == "__main__":
    print("\n\nRUNNING HEA AND IEA TESTS\n")
    RUNTESTS(verbosity=2)