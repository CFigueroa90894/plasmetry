""" G3 - Plasma Devs
Layer 2 - Control - Protected Dictionary
    Provides a partial, duck-typed implementation of a dictionary. Extends normal usage with thread
    safe mechanism to enforce mutual exclusion.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    ProtectedDictionary

"""

# built-in
from threading import RLock
import secrets


class ProtectedDictionary:
    """This class is partial, virtual class of Python's built-in dictionary. It leans on the concept
    of duck-typing, where it implements methods defined by the dictionary class without actually
    inheriting from it. Internally, its implementation merely stores a normal dictionary in its
    private attribute, and wraps calls to the dictionary with RLock objects from Python's built-in
    threading module in order to guarantee mutual exclusion.

    This class also provides safeguards by implementing configurable read/write permissions to its
    dictionary. Additionally, it includes copy-constructor functionality, capable of casting its 
    own instances and the built-in dictionary datatype to ProtectedDitionary instances. It also
    overloads the casting operator to convert ProtectedDictionary instances to regular dictionaries.
    Both the copy-constructor and cast-to-dict functionality works recursively, searching for other
    dictionaries internally to cast.
    
    Attributes:
        - __thread_lock: RLock - stores a reentrant lock to enforce mutual exclusion to all methods.
        - __token: Byte - randomized value, its owner may use it to bypass set permissions.
        - __token_claimed: bool - Set if the _token has been claimed.
        - __readable: bool - Defines whether this dictionary's entries may be read.
        - __writeable: bool - Defines whether this dictionary's entries may be modified.
        - __dict: dict - A built-in dictionary object, stores this class's entries.

    Methods:
        + __init__(): Constructor for this class.
        + keys(): Returns a view of all keys in the dictionary.
        + values(): Returns a view all key-value pairs in the dictionary.
        + copy(): Returns a new ProtectedDictionary with the same values.
        + update(): Accepts a dictionary and adds all its entries to this one.
        + lock(): Sets the 'write' permission to False.
        + hide(): Sets the 'read' permission to False.
        + reveal(): Sets the 'read' permission to True.
        + unlock(): Sets the 'write' permission to True.
        + token(): Claims the generated access token.
        # _get_readable(): Returns the __readable attribute.
        # _get_writable(): Returns the __writeable attribute. VALIDATE SPELLCHECK WONT BREAK SYSTEM
        # _bypass_set(): Verifies the passed token and modifies an entry regardless of permissions.
        # _bypass__get(): Verifies the passed token and returns an entry regardless of permissions.
        - __deep_copy_dict(): Recursively copies the given dictionary and returns it.
        - __validate_token(): Validates the passed argument is the bypass token.
        - __validate_readable(): Raise error if the dictionary is not readable.
        - __validate_writeable(): Raise error if the dictionary is not writeable.

    Overloaded Methods:
        + __setitem__(): Overloads the reassignment operator, 'D[key] = val'.
        + __getitem__(): Overloads the accessor operator, 'val = D[key]'.
        + __len__(): Overloads the 'len()' function.
        + __delitem(): Overloads the 'del' operator.
        + __contains__(): Overloads the 'in' operator.
        + __dict__(): Overloads the cast-to-dict function, 'dict(D)'.
        + __str__(): Overloads the cast-to-string function, 'str(D)'.

    
    """
    def __init__(self, dict_ref:dict=None, readable:bool=True, writeable:bool=True):
        """Constructor for this class. All arguments are optional."""
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

    # ----- Overload Methods ----- #
    def keys(self):
        """Returns a view of all keys in the dictionary."""
        with self.__thread_lock:
            self.__validate_readable()
            return self.__dict.keys()
        
    def values(self):
        """Returns a view all key-value pairs in the dictionary."""
        with self.__thread_lock:
            self.__validate_readable()
            return self.__dict.values()
    
    def copy(self):
        """Returns a new a ProtectedDictionary with the same values."""
        with self.__thread_lock:
            self.__validate_readable()
            return ProtectedDictionary(self)

    def update(self, dict_ref):
        """Accepts a dictionary and adds all its entries to this one."""
        assert isinstance(dict_ref, dict)
        with self.__thread_lock:
            self.__validate_writeable()
            for key in dict_ref.keys():
                self.__dict[key] = dict_ref[key]

    def __setitem__(self, key: str, value):
        """Overloads the reassignment operator, 'D[key] = val'."""
        with self.__thread_lock:
            self.__validate_writeable()
            self.__dict[key] = value

    def __getitem__(self, key:str):
        """Overloads the accessor operator, 'val = D[key]'."""
        with self.__thread_lock:
            self.__validate_readable()
            return self.__dict[key]
        
    def __len__(self) -> int:
        """Overloads the 'len()' function."""
        with self.__thread_lock:
            self.__validate_readable()
            return len(self.__dict)

    def __delitem__(self, key:str):
        """Overloads the 'del' operator."""
        with self.__thread_lock:
            self.__validate_writeable()
            del self.__dict[key]

    def __contains__(self, key:str) -> bool:
        """Overloads the 'in' operator."""
        with self.__thread_lock:
            self.__validate_readable()
            return key in self.__dict

    def __str__(self):
        """Overloads the cast-to-string function, 'str(D)'."""
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
            
            # return str with memory address and state
            out = f"{self.__repr__()} | {access} | {token_state}"
            return out

    # ----- Copy Methods ---- #
    def __deep_copy_dict(self, dict_ref) -> dict:
        """Recursively copies the given dictionary and returns it. Copy retains access the set
        permissions but resets the access token.
        
        """
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
        """Overloads the cast-to-dict function, 'dict(D)'. Recursively casts to dict."""
        new = {}
        for key in self.__dict.keys():  # manually add each key-value pair to new dictionary, overriding existing values
            value = self.__dict[key]
            if isinstance(value, [ProtectedDictionary, dict]):  # if the argument is a dictionary, recursively copy its contents
                value = dict(value)
            new[key] = value
        return new


    # ----- Access Control ----- #
    def lock(self, token):
        """Sets the 'write' permission to False. Requires the claimed access token."""
        with self.__thread_lock:
            self.__validate_token(token)
            self.__writeable = False

    def hide(self, token):
        """Sets the 'read' permission to False. Requires the claimed access token."""
        with self.__thread_lock:
            self.__validate_token(token)
            self.__readable = False

    def reveal(self, token):
        """Sets the 'read' permission to True. Requires the claimed access token."""
        with self.__thread_lock:
            self.__validate_token(token)
            self.__readable = True

    def unlock(self, token):
        """Sets the 'write' permissiont to True. Requires the claimed access token."""
        with self.__thread_lock:
            self.__validate_token(token)
            self.__writeable = True

    def _get_readable(self) -> bool:
        """Returns the boolean in the __readable attribute."""
        with self.__thread_lock:
            return self.__readable
    
    def _get_writable(self) -> bool:
        """Returns the boolean in the __writeable attribute."""
        with self.__thread_lock:
            return self.__writeable
    
    def __validate_token(self, token):
        """Validates the passed argument is the bypass token, otherwise raises an error."""
        if token == self.__token:
            return token == self.__token
        else:
            raise PermissionError(f"Invalid bypass token: {token}")
        
    def __validate_readable(self):
        """Raises an error if the dictionary is not readable."""
        if not self.__readable:
            raise PermissionError(f"This ProtectedDictionary instance is not writeable!")

    def __validate_writeable(self):
        """Raises an error if the dictionary is not writeable."""
        if not self.__writeable:
            raise PermissionError(f"This ProtectedDictionary instance is not readable!")

    # ----- Permission Bypass ----- #
    def _bypass_set(self, key:str, value, token):
        """Modifies an entry regardless of permissions. Requires the claimed access token."""
        with self.__thread_lock:
            if self.__validate_token(token):
                    self.__dict[key] = value
            else:
                raise PermissionError(f"Invalid bypass permissions")

    def _bypass__get(self, key: str, token):
        """Returns an entry regardless of permissions. Requires the claimed access token."""
        with self.__thread_lock:
            if self.__validate_token(token):
                    return self.__dict[key]
            else:
                raise PermissionError(f"Invalid bypass permissions")
        
    # Single Use token getter
    def token(self):
        """Claims and returns access token. Raises an error if it was already claimed.
        
        """
        with self.__thread_lock:
            __token = self.__token
            if not self.__token_claimed:
                self.__token_claimed = True
                return __token
            else:
                raise RuntimeError("Token cannot be requested more than once per instance.")


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


    