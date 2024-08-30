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
from Base_TLP import BaseTLP
from Triple_Lang_Voltage import TripleLangVoltage
from Triple_Lang_Current import TripleLangCurrent

class TLV_Obj_Test(ProbeObj_TestTemplate):
    def setUp(self):
        super().setUp()
        self.probe = self.factory.make(PRB.TLV)

    #TLP-V Inheritance
    def test_TLV_inheritance(self):
        """TLV instance inherits correctly."""
        parents = [TripleLangVoltage, BaseTLP, BaseProbe]
        self.check_inheritance(parents)

    #TLP-V Contents
    @skip("Test not implemented")
    def test_TLV_fresh_contents(self):
        """TLV instantiated with correct attributes."""
        pass

class TLC_Obj_Test(ProbeObj_TestTemplate):
    def setUp(self):
        super().setUp()
        self.probe = self.factory.make(PRB.TLC)

    # TLC Inheritance
    def test_TLC_inheritance(self):
        """TLC instance inherits correctly."""
        parents = [TripleLangCurrent, BaseTLP, BaseProbe]
        self.check_inheritance(parents)

    # TLC Contents
    @skip("Test not implemented")
    def test_TLC_fresh_contents(self):
        """TLC instantiated with correct attributes."""
        pass


if __name__ == "__main__":
    print("\n\nRUNNING TLP-C AND TLP-V TESTS\n")
    RUNTESTS(verbosity=2)