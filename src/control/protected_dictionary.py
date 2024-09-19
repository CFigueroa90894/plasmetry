# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings

# built-in
from threading import RLock
import secrets


class ProtectedDictionary:
    """<...>
    <thread-safe>
    <virtual class of dict, some access methods excluded>"""
    def __init__(self, dict_ref:dict=None, readable:bool=True, writeable:bool=True):
        """<...>"""
        self.__thread_lock = RLock()            # enforce mutual exclusion
        self.__token = secrets.token_bytes(1)   # permission bypass token, can only be claimed once
        self.__token_claimed = False            # if set, token has already been claimed
        
        if isinstance(dict_ref, ProtectedDictionary):       # deep copy, inherit permissions
            self.__readable = dict_ref._get_readable()
            self.__writeable = dict_ref._get_writable()
            self.__dict = self.__deep_copy_dict(dict_ref)   # make deep copy from ProtectedDictionary

        elif isinstance(dict_ref, dict):    # deep copy, no permissions are inherited
            self.__readable = readable
            self.__writeable = writeable
            self.__dict = self.__deep_copy_dict(dict_ref)   # make deep copy from dict
        
        elif dict_ref is None:
            self.__dict = {}
            self.__readable = readable
            self.__writeable = writeable
        
        else:
            raise TypeError(f"Unsupported argument type for 'dict_ref': {type(dict_ref)}")

    # ----- Dictionary Overload ----- #
    def keys(self):
        """<...>
        <guarantees mutual exclusion>
        <usage: obj.keys()>"""
        with self.__thread_lock:
            self.__validate_readable()
            return self.__dict.keys()
        
    def values(self):
        """<...>
        <guarantees mutual exclusion>
        <usage: obj.values()>"""
        with self.__thread_lock:
            self.__validate_readable()
            return self.__dict.values()
    
    def copy(self):
        """<...>"""
        with self.__thread_lock:
            self.__validate_readable()
            return ProtectedDictionary(self)

    def update(self, dict_ref):
        """<...>"""
        assert isinstance(dict_ref, dict)
        with self.__thread_lock:
            self.__validate_writeable()
            for key in dict_ref.keys():
                self.__dict[key] = dict_ref[key]

    def __setitem__(self, key: str, value):
        """<...>
        <guarantees mutual exclusion>
        <usage: obj[key] = value>"""
        with self.__thread_lock:
            self.__validate_writeable()
            self.__dict[key] = value

    def __getitem__(self, key:str):
        """<...>
        <guarantees mutual exclusion>
        <usage: x = obj[key]>"""
        with self.__thread_lock:
            self.__validate_readable()
            return self.__dict[key]
        
    def __len__(self) -> int:
        """<...>
        <guarantees mutual exclusion>
        <usage: len(obj)>"""
        with self.__thread_lock:
            self.__validate_readable()
            return len(self.__dict)

    def __delitem__(self, key:str):
        """<...>
        <guarantees mutual exclusion>
        <usage: del obj[key]>"""
        with self.__thread_lock:
            self.__validate_writeable()
            del self.__dict[key]

    def __contains__(self, key:str) -> bool:
        """<...>
        <guarantees mutual exclusion>
        <usage: key in obj>"""
        with self.__thread_lock:
            self.__validate_readable()
            return key in self.__dict

    # ----- Internal Copy Methods ---- #
    def __deep_copy_dict(self, dict_ref) -> dict:
        """<...>
        <retains access permissions but resets the token>"""
        new = {}
        for key in dict_ref.keys():  # manually add each key-value pair to new dictionary, overriding existing values
            value = dict_ref[key]
            if isinstance(value, ProtectedDictionary):  # if the argument is a dictionary, recursively copy its contents
                value = ProtectedDictionary(value)
            elif isinstance(value, dict):
                value = self.__deep_copy_dict(value)
            new[key] = value
        return new
    
    def __dict__(self) -> dict:
        new = {}
        for key in self.__dict.keys():  # manually add each key-value pair to new dictionary, overriding existing values
            value = self.__dict[key]
            if isinstance(value, [ProtectedDictionary, dict]):  # if the argument is a dictionary, recursively copy its contents
                value = dict(value)
            new[key] = value
        return new


    # ----- Access Control ----- #
    def lock(self, token):
        """<...>"""
        with self.__thread_lock:
            self.__validate_token(token)
            self.__writeable = False

    def hide(self, token):
        """<...>"""
        with self.__thread_lock:
            self.__validate_token(token)
            self.__readable = False

    def reveal(self, token):
        """<...>"""
        with self.__thread_lock:
            self.__validate_token(token)
            self.__readable = True

    def unlock(self, token):
        """<...>"""
        with self.__thread_lock:
            self.__validate_token(token)
            self.__writeable = True

    def _get_readable(self) -> bool:
        """<...>"""
        with self.__thread_lock:
            return self.__readable
    
    def _get_writable(self) -> bool:
        """<...>"""
        with self.__thread_lock:
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
            raise PermissionError(f"This ProtectedDictionary instance is not writeable!")

    def __validate_writeable(self):
        """<...>"""
        if not self.__writeable:
            raise PermissionError(f"This ProtectedDictionary instance is not readable!")

    # ----- Permission Bypass ----- #
    def _bypass_set(self, key:str, value, token):
        """<...>"""
        with self.__thread_lock:
            if self.__validate_token(token):
                    self.__dict[key] = value
            else:
                raise PermissionError(f"Invalid bypass permissions")

    def _bypass__get(self, key: str, token):
        """<...>
        <guarantees mutual exclusion>"""
        with self.__thread_lock:
            if self.__validate_token(token):
                    return self.__dict[key]
            else:
                raise PermissionError(f"Invalid bypass permissions")
        
    # Single Use token getter
    def token(self):
        """<...>"""
        with self.__thread_lock:
            __token = self.__token
            if not self.__token_claimed:
                self.__token_claimed = True
                return __token
            else:
                raise RuntimeError("Token cannot be requested more than once per instance.")
        
    def __str__(self):
        """<...>"""
        with self.__thread_lock:
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
    pdict = ProtectedDictionary()
    print(pdict)
    token = pdict.token()
    print(pdict)
    pdict.lock(token)
    print(pdict)
    pdict.hide(token)
    print(pdict)
    pdict.unlock(token)
    print(pdict)
    pdict.reveal(token)
    print(pdict)

    pdict["a"] = "A"
    pdict["b"] = "B"
    pdict["c"] = "C"
    print(pdict["a"])
    print(pdict.keys())
    for key in pdict.keys():
        print(f"{key} : {pdict[key]}")


    