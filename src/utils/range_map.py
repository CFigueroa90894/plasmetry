# author: figueroa_90894@students.pupr

def high_to_low(high_val:float, low_min:float, low_max:float, high_min:float, high_max:float):
    """Returns the corresponding low-value mapped to a given high-value.
    
    Arguments:
        high_val: high-value for which we wish to obtain the corresponding low value
        low_min: minimum of the low-value's range
        low_max: maximum of the low-value's range
        high_min: minimum of the high-value's range
        high_max: maximum of the high-value's range
    """
    return (high_val - high_min) / ((high_max - high_min) / (low_max - low_min))