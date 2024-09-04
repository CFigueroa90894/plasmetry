# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings

# built-in
from threading import Lock
from typing import overload 
import secrets

# TO DO
class ConfigStruct:
    """<...>
    <thread-safe>
    <virtual class of dict, some access methods excluded>"""
    def __init__(self, config_ref:dict=None, readable:bool=True, writeable:bool=True):
        """<...>"""
        self.__thread_lock = Lock()                  # enforce mutual exclusion
        self.__token = secrets.token_bytes(1)        # permission bypass token, can only be claimed once
        self.__token_claimed = False                 # if set, token has already been claimed
        
        if isinstance(config_ref, ConfigStruct):   # deep copy, inherit permissions
            self.__readable = config_ref._get_readable()
            self.__writeable = config_ref._get_writable()
            self.__config = self.__copy_struct(config_ref)  # make deep copy from ConfigStruct

        elif isinstance(config_ref, dict):      # deep copy, no permissions are inherited
            self.__readable = readable
            self.__writeable = writeable
            self.__config = self.__copy_dict(config_ref)    # make deep copy from dict
        
        elif config_ref is None:
            self.__config = {}
            self.__readable = readable
            self.__writeable = writeable
        
        else:
            raise TypeError(f"Unsupported argument type for 'config_ref': {type(config_ref)}")


    # ----- Copy Methods ---- #
    # TO DO
    def __copy_dict(self, config_ref):
        """<...>"""
        raise NotImplementedError("THIS FUNCTION IS STILL A TO DO")
        assert type(config_ref) == dict
        return None

    # TO DO
    def __copy_struct(self, config_ref):
        """<...>"""
        raise NotImplementedError("THIS FUNCTION IS STILL A TO DO")
        assert type(config_ref) == ConfigStruct
        return None


    # ----- Access Control ----- #
    def lock(self, token):
        """<...>"""
        self.__validate_token(token)
        self.__writeable = False

    def hide(self, token):
        """<...>"""
        self.__validate_token(token)
        self.__readable = False

    def reveal(self, token):
        """<...>"""
        self.__validate_token(token)
        self.__readable = True

    def unlock(self, token):
        """<...>"""
        self.__validate_token(token)
        self.__writeable = True

    def _get_readable(self) -> bool:
        """<...>"""
        return self.__readable
    
    def _get_writable(self) -> bool:
        """<...>"""
        return self.__writeable
    
    def __validate_token(self, token):
        """<...>"""
        if token == self.__token:
            return token == self.__token
        else:
            raise PermissionError(f"Invalid bypass token: {token}")
        
    def __validate_readable(self):
        """<...>"""
        if not self.__readable:
            raise PermissionError(f"ConfigStruct is not writeable!")

    def __validate_writeable(self):
        """<...>"""
        if not self.__writeable:
            raise PermissionError(f"ConfigStruct is not readable!")


    # ----- Dictionary Overload ----- #
    def keys(self):
        """<...>
        <guarantees mutual exclusion>"""
        self.__validate_readable()
        with self.__thread_lock:
            return self.__config.keys()

    def __setitem__(self, key: str, value):
        """<...>
        <guarantees mutual exclusion>"""
        self.__validate_writeable()
        with self.__thread_lock:
            self.__config[key] = value

    def __getitem__(self, key:str):
        """<...>
        <guarantees mutual exclusion>"""
        self.__validate_readable()
        with self.__thread_lock:
            return self.__config[key]
        
    def __len__(self):
        """<...>
        <guarantees mutual exclusion>"""
        self.__validate_readable()
        with self.__thread_lock:
            return len(self.__config)

    def __delitem__(self, key:str):
        """<...>
        <guarantees mutual exclusion>"""
        self.__validate_writeable()
        with self.__thread_lock:
            del self.__config[key]

    def __contains__(self, key:str):
        """<...>
        <guarantees mutual exclusion>"""
        self.__validate_readable()
        with self.__thread_lock:
            return key in self.__config


    # ----- Permission Bypass ----- #
    def _bypass_set(self, key:str, value, token):
        """<...>"""
        if self.__validate_token(token):
            with self.__thread_lock:
                self.__config[key] = value
        else:
            raise PermissionError(f"Invalid bypass permissions")

    def _bypass__get(self, key: str, token):
        """<...>
        <guarantees mutual exclusion>"""
        if self.__validate_token(token):
            with self.__thread_lock:
                return self.__config[key]
        else:
            raise PermissionError(f"Invalid bypass permissions")
        
    # Single Use token getter
    def token(self):
        """<...>"""
        __token = self.__token
        if not self.__token_claimed:
            self.__token_claimed = True
            return __token
        else:
            raise RuntimeError("Token cannot be requested more than once per instance.")
        
    def __str__(self):
        # Permissions
        access = ""
        if self.__readable:
            access += "R"
        if self.__writeable:
            access += "W"
        if access == "":
            access = "None"
        
        # Token
        if self.__token_claimed:
            token_state = "claimed"
        else:
            token_state = "available"
        
        out = f"{self.__repr__()} | {access} | {token_state}"   # return str with memory address and state
        return out
    
# ----- BASIC TESTS ----- #
if __name__ == "__main__":
    config = ConfigStruct()
    print(config)
    token = config.token()
    print(config)
    config.lock(token)
    print(config)
    config.hide(token)
    print(config)
    config.unlock(token)
    print(config)
    config.reveal(token)
    print(config)

    config["a"] = "a"
    print(config["a"])


    