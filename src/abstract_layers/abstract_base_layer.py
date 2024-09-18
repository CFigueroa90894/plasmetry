"""G3 - Plasma Devs
Layer 0 - Abstract Base Layer
    Specifies the common methods that all of Plasmetry's layers must implement. In
    addition, it implements methods that do not need to be overriden by subclasses.

author: figueroa_90894@students.pupr.edu
status: WIP
    - add docstrings
    - validate with team

Architecture Initialization:
    It is recommended that each layer be instantiable without arguments, though this may not
    always be possible. Optional arguments may be specified for additional customization.

    Calls to initialize Plasmetry's architecture are intended to occur in a stack pattern, from
    top-to-bottom, where each layer's constructor attempts to initialize the lower layer.

Customizing Subcomponents:
    Each layer's concrete class must define individual class attributes that specify the module
    name of each subcomponent, including the lower layer's interface. A custom subcomponent is
    specified by assigning its corresponding class attribute with a module object.
    
    Once a layer is initialized, DO NOT reassign its subcomponents, this will have no effect since
    subcomponents are loaded and instantiated in the layer's constructor. They must be reassigned
    by calling the class attribute, before instantiation.

Impact of Customization:
    Customizing subcomponents will require deep understanding of the architecture, and should be
    done from an initialization script that provides external systems a single init call.
    Reassigning components in one layer will require changes in its parent layer. A customized
    layer MUST be reassigned in its parent layer's corresponding class attribute BEFORE the parent
    is initialized. This means that said parent layer is now a customized layer as well.

    To manage this impact, all layer's above the lowest customized layer will also need to be
    customized to account for changes. Despite this, each layer's implementation is agnostic to
    every other layer's internals.
        
Reasoning for this Customization Approach:
    1. Layers can be customized before initializing them and without modifying their source code.
    2. Default components don't need to be imported or even included in a deployment if unused.
    3. Customization scripts only need to import layer interfaces, not their subcomponents.
    4. Customization scripts only need to be aware of a custom component's module name.
    5. Customization scripts do not need to initialize layers nor subcomponents.
    6. Layer initialization calls can still occur from top-to-bottom.
    7. Layer's still retain the ability to self-assemble.
"""

# built-in imports
from abc import ABCMeta, abstractmethod
from inspect import ismodule

class AbstractBaseLayer(metaclass=ABCMeta):
    """This abstract class specifies functionality that all of layer's of the Plasmetry Software's
    Architecture must implement.

    Methods:
        + __init__() - instantiates an object of the class
        # _info() - returns information about a layer's subcomponents
        # _load_all_subcomponents() - returns uninstantiated classes of subcomponents
        # _load_mod() - returns a module for a subcomponent
    """

    @abstractmethod
    def __init__(self):
        """Constructor for the layer. Each layer must implement this method separately, to account
        for their specific subcomponents.
        
        The recommended order of operations follows:
            - use default values for optional arguments that were not specified
            - save necessary arguments to attributes
            - assemble the layer
                - get the current layer's subcomponent classes by calling _load_all_subcomponents()
                - unpack classes from returned dictionary
                - instantiate the lower layer's object
                - instantiate the the current layer's subcomponents
        """
        raise NotImplementedError("Method was not implemented in subclass!")
    
    @abstractmethod
    def _info(self):
        """Returns a list of tuples representing the layer's subcomponents. Each layer must
        implement this method separately, to account for their specific subcomponents.
        
        It is recommended that this method recursively calls the lower layer's method in order
        to obtain a complete system composition with a single call.
        """
        raise NotImplementedError("Method was not implemented in subclass!")
    
    @abstractmethod
    def _load_all_subcomponents(self):
        """Returns a dictionary of classes, each one corresponding to a subcomponent. 
        
        Each layer must implement this method separately, to account for its specific
        subcomponents. Use the _load_mod() method to simplify this one's implementation.

        Recommended order of operations:
            - load subcomponent modules specified in class attributes
            - get the known classes from each module
            - package all classes into dictionary
            - return dictionary
        """
        raise NotImplementedError("Method was not implemented in subclass!")
    
    def _load_mod(self, mod: str):
        """Returns a module specified by name of type string. If the argument is of
        type 'module', returns the module with no other operations.

        Arguments:
            mod: str | module - the module to import

        Exceptions:
            TypeError: if argument's type is not of type 'str' or 'module'
        """
        # check the module was specified as a string
        if isinstance(mod, str):
            mod = __import__(mod)   # import module by name, redefining mod
        
        # if it is not a string, mod MUST be an object of type 'module'
        elif not ismodule(mod):
            raise TypeError(f"Class attribute {mod} must be module or string! Given {type(mod)}")
        
        # all checks successful, return module
        return mod