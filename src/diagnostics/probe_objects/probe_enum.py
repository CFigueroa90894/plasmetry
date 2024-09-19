# author: figueroa_90894@students.pupr.edu
# status: DONE

# built-in imports
from enum import Enum, unique

# PROBE IDENTIFIERS
@unique # prevent duplicate values
class PRB(Enum):
    """An enumarator class to represent probe types."""
    SLP = 'slp'     # Single Langmuir Probe
    DLP = 'dlp'     # Double Langmuir Probe
    HEA = 'hea'     # Hyperbolic Energy Analyzer
    IEA = 'iea'     # Ion Energy Analyzer
    TLC = 'tlc'     # Triple Langmuir Probe - Current Mode
    TLV = 'tlv'     # Triple Langmuir Probe - Voltage Mode
