# author: figueroa_90894@studnt.pupr.edu

from enum import Enum, unique

@unique # prevent duplicate values
class PRB(Enum):
    """An enumarator class to represent probe types."""
    ABS = 0     # abstract probe type
    SLP = 1     # Single Langmuir Probe
    DLP = 2     # Double Langmuir Probe
    HEA = 3     # Hyperbolic Energy Analyzer
    IEA = 4     # Ion Energy Analyzer
    TLC = 5     # Triple Langmuir Probe - Current Mode
    TLV = 6     # Triple Langmuir Probe - Voltage Mode