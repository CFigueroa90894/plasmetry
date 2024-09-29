""" G3 - Plasma Devs
Layer 2 - Control - System Flags
    Provides two classes to quickly instantiate sets of flags used system-wide to coordinates all
    layers of the Plasmetry Software Architecture.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    StatusFlags
    CommandFlags

"""

# built-in imports
from threading import Event


class StatusFlags:
    """This class consists of seven Event flags from Python's built-in threading module. This set
    of flags is used to throughout the layers to indicate different states they may be in.
    
    Attributes:
        + operating: Indicates the physical probe circuit is enabled.
        + calculating: Indicates plasma parameters are being calculated.
        + connecting: Indicates a connection to the remote storage is being established.
        + transmitting: Indicates experiment results are being uploaded to the remote storage.
        + formatting: Indicates experiment results are being processed.
        + loading_config_file: Indicates the config file is being read and committed to memory.
        + writing_config_file: Indicates config values memory are being written to the config file.

    Method:
        + __init__(): Constructor for this class; generates a new set of flags.

    """
    def __init__(self):
        """The constructor for StatusFlags, it takes no arguments. Every StatusFlags object that is
        instantiated creates a complete new set of flags.
        
        """
        # Probe Operations
        self.operating = Event()    # High voltage amps are operating
        self.calculating = Event()  # Calculating plasma parameters
        
        # Remote Storage
        self.connecting = Event()   # establishing connection to remote storage
        self.transmitting = Event() # uploading results to remote storage
        
        # Data management
        self.formatting = Event()   # results are being formatted
        self.loading_config_file = Event()  # config is being read from file
        self.writing_config_file = Event()  # config is being written to file


class CommandFlags:
    """This class consists of three Event flags from Python's built-in threading module. This set
    of flags is used to throughout the layers to trigger different behaviors in its subsystems.
    
    Attributes:
        + shutdown: Begins process of terminating the entire system.
        + diagnose: System continues to perform data acquisition while set.
        + refresh: Set to indicate new values for display are available. Cleared when they are read.

    Method:
        + __init__(): Constructor for this class; generates a new set of flags.

    """
    def __init__(self):
        """The constructor for CommandFlags, it takes no arguments. Every CommandFlags object that
        is instantiated creates a complete new set of flags.
        
        """
        self.shutdown = Event()     # complete pending operations then terminate
        self.diagnose = Event()     # perform diagnostics
        self.refresh = Event()      # new plasma parameters to display

