# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings

# built-in
from threading import Lock

class ConfigStruct:
    """<...>
    <thread-safe>"""
    def __init__(self, config_dict={}):
        """<...>"""
        self.__config = config_dict     # mangled; only modify with public functions
        self.lock = Lock()              # enforce mutual exclusion

    def set(self, key: str, value):
        """<...>
        <guarantees mutual exclusion>"""
        with self.lock:
            self.__config[key] = value

    def get(self, key: str):
        """<...>"""
        with self.lock:
            return self.__config[key]


    