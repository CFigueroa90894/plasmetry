# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings

# built-in
from threading import Event


class StatusFlags:
    """<...>"""
    def __init__(self):
        """<...>"""
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
    """<...>"""
    def __init__(self):
        """<...>"""
        self.shutdown = Event()     # complete pending operations then terminate
        self.diagnose = Event()     # perform diagnostics
        self.refresh = Event()      # new plasma parameters to display
