""" G3 - Plasma Devs
Utilities - Range Map
    Provides a method that scales down a large value to a smaller range. Both the large and small
    ranges may take negative values.


author: figueroa_90894@students.pupr.edu
status: DONE

Methods:
    high_to_low(): float - scales down a large value
"""

def high_to_low(high_val:float, low_min:float, low_max:float, high_min:float, high_max:float):
    """Returns the corresponding low-value mapped to a given high-value.
    
    Arguments:
        high_val: float - the value to scale down
        low_min: float - the minimum value of the smaller range
        low_max: float - the maximum value of the smaller range
        high_min: float - the minimum value of the larger range
        high_max: float - the maximum value of the larger range
    """
    return (high_val - high_min) / ((high_max - high_min) / (low_max - low_min))