""" G3 - Plasma Devs
Utilities - Type Enforcer
    Provides a python decorator that validates that the type of arguments passed to a function
    match its specified type hints; it is particularly helpful for debugging and in type sensitive
    situations. Its main disadvantage is that an error will not be raised until runtime, when the
    decorated function is executed.

author: figueroa_90894@students.pupr.edu
status: DONE

Methods:
    enforce_type() - a python decorator to enforce explicit typing
"""

# built-in imports
from typing import get_type_hints as hint


# METHOD DECORATOR - EXPERIMENTAL
def enforce_type(function):
    """Enforces type-checking at runtime by comparing a given argument's 
    type to the type hint specified in the decorated function's signature.
    Does not check default values when no arguments given. Does not support
    keyword arguments.
    """
    def wrap(*args, **kwargs):
        """Local wrapper function, returned when the python interpreter invokes the decorator."""
        hint_tupes = hint(function)  # dict with kwarg names as keys, and type hints as values
        
        # remove type hint for return values, if it was specified
        try:
            hint_tupes.pop('return')
        except KeyError:
            pass

        # get a list of type hints from the type hint dict
        hint_list = list(hint_tupes.values())

        # validate each argument against its expected type
        for i in range(0-len(hint_tupes), 0):
            if not isinstance(args[i], hint_list[i]):
                raise TypeError(f"Expected {hint_list[i]} but received {type(args[i])}")
        
        # if no errors were raised, call original function
        result = function(*args, **kwargs) 
        return result   # return the results from the original function
    return wrap         # return the decorated function