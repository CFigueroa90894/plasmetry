# author: figueroa_90894@students.pupr.edu
# status: DONE

# built-in imports
from enum import Enum, unique

# PROBE IDENTIFIERS
@unique # prevent duplicate values
class PRB(Enum):
    """An enumarator class to represent probe types."""
    SLP = 0     # Single Langmuir Probe
    DLP = 1     # Double Langmuir Probe
    HEA = 2     # Hyperbolic Energy Analyzer
    IEA = 3     # Ion Energy Analyzer
    TLC = 4     # Triple Langmuir Probe - Current Mode
    TLV = 5     # Triple Langmuir Probe - Voltage Mode