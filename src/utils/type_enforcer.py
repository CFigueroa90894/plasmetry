# author: figueroa_90894@students.pupr

# built-in imports
from typing import get_type_hints as hint
import inspect


# METHOD DECORATOR - EXPERIMENTAL
def enforce_type(function):
    """Enforces type-checking at runtime by comparing a given argument's 
    type to the type hint specified in the decorated function's signature.
    Does not check default values when no arguments given. Does not support
    keyword arguments.
    """
    def wrap(*args, **kwargs):
        hint_tupes = hint(function) # THESE ARE THE TYPES TO ENFORCE, ARGS ARE THE VALUES        
        try:
            hint_tupes.pop('return')
        except KeyError:
            pass
        hint_list = list(hint_tupes.values()) # TARGET TYPES
        for i in range(0-len(hint_tupes), 0):
            if hint_list[i] != type(args[i]):
                raise TypeError(f"Expected {hint_list[i]} but received {type(args[i])}")
        result = function(*args, **kwargs)
        return result
    return wrap

# TEST - METHOD DECORATOR
def deco_test(function):
    def wrap(*args, **kwargs):
        print("pre func")
        result = function(*args, **kwargs)
        print("pos func")
        return result
    return wrap

# CLASS DECORATOR
def enforce_type_class(cls):
    return decorate_class(enforce_type, cls)

# GENERIC CLASS DECORATOR - EXPERIMENTAL
def decorate_class(decorator, cls=None):
    members = inspect.getmembers(cls)
    for mem in members:
        if (mem[0][0] != '_'):
            setattr(cls, mem[0], decorator(mem[1]))
    return cls

# GENERIC CLASS DECORATOR
def put_decorator_on_all_methods(decorator, cls=None):
    if cls is None:
        return lambda cls: put_decorator_on_all_methods(decorator, cls)
    class Decoratable(cls):
        def __init__(self, *args, **kargs):
            super().__init__(*args, **kargs)
        def __getattribute__(self, item):
            value = object.__getattribute__(self, item)
            if callable(value):
                return decorator(value)
            return value
    return Decoratable