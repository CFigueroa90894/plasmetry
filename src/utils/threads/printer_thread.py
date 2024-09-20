""" G3 - Plasma Devs
Utilities - Printer Thread
    Provides a class, PrinterThread, that provides thread-safe text output for objects and scripts.
    The PrinterThread reads text from a queue and outputs it so the specified object.

author: figueroa_90894@students.pupr.edu
status: DONE

classes:
    PrinterThread - reads from a buffer and print to the given output.
    SayWriter - object to provide thread-safe printing functionality
"""

# built-in imports
import sys
import os
import traceback

from threading import Event, current_thread
from queue import Queue, Empty
from io import TextIOWrapper

from typing import Tuple

# ----- PATH HAMMER v2.7 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:  
    """Resolve absolute imports by recursing into subdirs and appending them to python path."""
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    print(f"Path Hammer: {src_abs}")
    assert src_abs.split('\\')[-1*len(root_target):] == root_target   # validate correct top folder
    
    # get subdirs, exclude unwanted
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split('\\')[-1] not in exclude] 
    for dir in dirs: sys.path.append(dir)    # add all subdirectories to python path

if __name__ == "__main__":  # execute path hammer if this script is run directly
    path_hammer(2, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #

# local imports
from base_thread import BaseThread
from say_writer import SayWriter

# local config
BUFF_TIMEOUT = 3    # timeout value in seconds for read operation on input buffer

class PrinterThread(BaseThread):
    """The PrinterThread class provides a thread-safe mechanism for text output.
    
    Text output is a relatively time consuming operation. In addition to thread-safe printing, the
    PrinterThread outsources this workload from other threads (or objects), to save resources.
    
    Others may use the public SayWriter generated by the PrinterThread to push items to be written
    to an output stream (file, stdout, etc). PrinterThread objects continually read from their input
    buffer, pushing each item to all of its output writers.

    PrinterThread objects accept SayWriter or TextIOWrapper objects to be used as outputs. These may
    be passed as one argument or a list. Where none are given, the class creates a default SayWriter
    object. In addition to the generated public SayWriter, PrinterThreads use private SayWriters to
    write text to output streams.

    * NOTE: Since outputting text is time consuming, the rate at which the PrinterThread outputs
    should NOT be used to diagnose time-sensitive behavior. It is preferable to include timestamps
    on messages pushed to the PrinterThread, and more so to set its output to a file that can be
    analyzed after runtime.

    Attributes:
        + kill: Event - signaling mechanism to stop the thread
        # _input: Queue - input queue from the thread reads items it must output
        # _output: List[SayWriter] - all output writers

    Methods:
        + __init__() - constructor
        + get_writer() - returns a SayWriter object configured to push items to the PrinterThread
        + say() - inherited from BaseThread, in PrinterThread's case, pushes to its own input queue
        + run() - method invoked by the threading framework when start() is called on the object
        # _THREAD_MAIN_() - the main loop of the PrinterThread, called by run()
        # _thread_setup_() - prepares the thread for execution, called before _THREAD_MAIN_()
        # _thread_cleanup_() - closes all output streams, called after _THREAD_MAIN_() exits
        - __make_writer() - creates on SayWriter for output
        - __make__all_writers() - creates all output SayWriters
        - __write() - writes an item to all output streams
    """
    def __init__(self, 
                 kill:Event,
                 go,
                 text_in:Queue=None,
                 text_out:SayWriter|TextIOWrapper|Tuple[SayWriter|TextIOWrapper]=None,
                 daemon=False,
                 name="PRINTR",
                 *args, **kwargs):
        """Constructor for the PrinterThread class.

        The first object in text_out is treated as the PrinterThread's own _say_obj attribute.
        If daemon is set to True, PrinterThread may not exit correctly and corrupt all output text.
        Please, only set daemon to True if you know what you're doing.

        Arguments:
            kill: Event - signaling mechanism to stop the PrinterThread
            text_in: Queue - input queue of text to print
                default: None (generates a new queue in cosntructor)
            text_out: object or list of objects of output streams to associate with writers
                default: None (creates a single default SayWriter object)
            daemon: bool - sets the thread to daemonic behavior (see built-in threading module)
        """
        # Validate if text_in was not specified
        if text_in is None:
            text_in = Queue()

        self.go = go

        # Generate a public writer for other objects to send text to the PrinterThread
        public_writer = SayWriter(text_in)

        # Save Arguments
        self.kill = kill        # signal to terminate thread
        self._input = text_in   # thread-safe queue to recieve messages to output

        # Private Writers that PrinterThread must write recieved messages to
        self._output = self.__make_all_writers(text_out)    # generate private set of writers
        
        # Initialize parent attributes
        super().__init__(*args, name=name, daemon=daemon, text_out=public_writer, **kwargs)

    # ----- PUBLIC METHODS ----- #        
    def get_writer(self):
        """Returns the public writer generated by the PrinterThread constructor."""
        return self._say_obj
            
    # ----- THREAD MAIN ----- #
    def _THREAD_MAIN_(self):
        """Write text received through the input queue to the output writers. This method will loop
        until the kill flag is set, but will attempt to empty the buffer before terminating.
        """
        # Loop while theres content in buffer, until the kill flag is set
        while not self.kill.is_set() or not self._input.empty():
            try:
                # Attempt to write to all output writers
                self.__write(self.read())
            # Catch the exception and continue looping
            except Empty:
                pass
    
    # ---- THREAD LIFE CYCLE ----- #
    def run(self):
        """Call the run() method inherited from parent class."""
        super().run()

    def _thread_setup_(self):
        """Call the _thread_setup_() method inherited from parent class."""
        self.go.wait()
        super()._thread_setup_()    # use parent implementation

    def _thread_cleanup_(self):
        """Perform all thread cleanup functions. Writes the last PrinterThread message then
        closes all writers before finally terminating the thread.
        """
        self.__write(f"{self.name}: exiting...")  # print final PrinterThread message
        self._say_obj.close()       # close personal writer
        for writer in self._output: # close all output writers
            writer.close()
        sys.exit(0) # terminate PrinterThread

    # ----- PRIVATE UTILS ----- #
    def __make_writer(self, output):
        """Returns a SayWriter object created with the given output argument."""
        # Verify if argument is SayWriter
        if isinstance(output, SayWriter):
            return output
        # Otherwise create writer, SayWriter constructor will raise error if invalid type was given
        else:
            return SayWriter(output)

    def __make_all_writers(self, out_list):
        """Returns a list of SayWriter objects created from the arguments in the list."""
        writers = []    # list to be returned
        
        # validate input is an iterable
        if not isinstance(out_list, (list, tuple)):
            out_list = [out_list]   # make a one element list

        # Iterate over items in list and generate a writer for each one
        for out in out_list:
            writers.append(self.__make_writer(out))
        return writers

    # ----- PRINT UTILS ----- #
    def say(self, msg):
        """Prints a message to the output buffer."""
        super().say(msg)    # call method inherited from parent

    def __write(self, msg):
        """Outputs text to all the private writers."""
        for writer in self._output:
            writer(msg)

    def read(self):
        return self._input.get(timeout=BUFF_TIMEOUT)

# # Basic Tests
# if __name__ == "__main__":

#     # create kill switch
#     kill = Event()
#     kill.clear()

#     # create output streams
#     f = open(file='test.txt', mode='a')
#     out_stream = [f, sys.stdout, sys.stderr]

#     # create printer thread
#     printer = PrinterThread(
#         text_out=out_stream,
#         name="PRINTER",
#         kill=kill
#     )

#     # get public writer from printer thread
#     say = printer.get_writer()

#     printer.start()

#     for i in range(10):
#         say(f"Hello World! {i}")

#     for i in range(3):
#         say(f"Ahoy! {i}")

#     kill.set()
#     printer.join()


