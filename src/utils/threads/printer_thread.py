""" G3 - Plasma Devs
Utilities - Printer Thread
    Provides printing utilities, including a printer thread and a writer object. 
    
    The sole responsibility of the PrinterThread is outputting buffered in a thread-safe manner.
    The SayWriter object provides functionality to output text to various I/O objects, as well
    as well as outputting text to the PrinterThreads buffer.

author: figueroa_90894@students.pupr.edu
status: WIP
    - modify PrinterThread to use SayWriter objects
    - add docstrings to PrinterThread

classes:
    PrinterThread - reads from a buffer and print to the given output.
    SayWriter - object to provide thread-safe printing functionality
"""

# built-in imports
import sys
import os

from io import TextIOWrapper

from threading import Event
from queue import Queue, Empty

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


class PrinterThread(BaseThread):
    """<...>"""
    def __init__(self, kill:Event, *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)
        self._whisper = self._print_buff
        self.kill = kill                    # signal to terminate thread

    # ----- MAIN ----- #
    def _THREAD_MAIN_(self):
        """<...>"""
        while not self.kill.is_set() or not self.console_buff.empty():
            try:
                print(self.console_buff.get(timeout=3))
            except Empty:
                pass
    
    def run(self):
        """<...>"""
        super().run()

    # ---- LIFE CYCLE ----- #
    def _thread_setup_(self):
        """<...>"""
        super()._thread_setup_()    # use parent implementation

    def _thread_cleanup_(self):
        """<...>"""
        self._whisper = self._print_stdout
        super()._thread_cleanup_()  # use parent implementation

    # ----- PRINT UTILS ----- #
    def say(self, msg):
        """<...>"""
        super().say(msg)


class SayWriter:
    """A basic printing object.
    
    Abstracts away the need for other objects to manually track which output they should print to. 
    It is primarily intended to be instantiated by a PrinterThread object, though in its absence
    the parent script should instantiate the SayWriter object. The SayWriter object should be passed
    down the stack so all of Plasmetry's subcomponents can access it.

    The SayWriter object overloads the python magic method __call__, meaning that instantiated
    objects of the class can be invoked as if they were functions. Doing so invokes the __call__
    method, which calls printing method defined by the object's mode.

    Usage Example:
        say = SayWriter()   # instantiate the object
        say("Hello World!") # call the object as a function
    
    Attributes:
        + end - terminator for Text I/O outputs (default '\\n')
        - __buffer: Queue | TextIOWrapper - object to output text
    
    Mehtods:
        + set_buffer() - changes the printing mode of object
        + __call__() - method called when a SayWriter object is invoked as callable object
        + get_mode() - returns the current mode andused buffer
        - __default() - the default printing method, uses built-in 'print()'
        - __io_write() - write text to the Text I/O object
        - __queue_msg() - enqueue text to the Queue buffer
        - __whisper() - method redefined based on printing mode
    """
    # ----- INITILIZATION ----- #
    def __init__(self, buffer:Queue | TextIOWrapper=None):
        """Constructor for the SayWriter class."""
        self.set_buffer(buffer)  # validate argument and set output mode
        self.end = '\n'          # set line terminator, default '\n'

    def set_buffer(self, buffer:Queue | TextIOWrapper=None):
        """Sets the SayWriter object's output mode based on given arguments.
        
        buffer: Queue | TextIOWrapper - output buffer object
            None (default) - sets output mode to use the built-in 'print()' method
            Queue - sets output mode to enqueue messages in the given Queue object
            TextIOWrapper - sets mode to write to the given I/O object
        """
        # Use given Queue object to enqueue text to print
        if isinstance(buffer, Queue):
            self.__mode = "Queue"               # used when returning mode info
            self.__whisper = self.__queue_msg   # redefine printing method to Queue version
        
        # Use the given Text I/O object
        elif isinstance(buffer, TextIOWrapper):
            self.__mode = "Text I/O"            # used when returning mode info
            self.__whisper = self.__io_write    # redefine printing method to Text I/O version

        # Use default if no buffer was specified (or it is an unsupported type)
        elif buffer is None:
            self.__mode = "Default"             # returned for mode info
            self.__whisper = self.__default     # redefine printing method to default version

        # Error handling
        else:
            raise TypeError(f"Argument type {type(buffer)} is not supported!")
        
        # Save argument
        self.__buffer = buffer
        
    # ----- PUBLIC UTILS ----- #
    def __call__(self, msg) -> None:
        """Outputs text using the method defined by the object's mode. Allows SayWriter
        objects to be called as if they were a function. See the class docstring for usage.
        """
        self.__whisper(msg)
    
    def get_mode(self) -> Tuple[str, object]:
        """Returns a tuple with the object's mode and its buffer."""
        return (self.__mode, self.__buffer)
    
    # ----- PRIVATE UTILS ----- #
    def __default(self, msg) -> None:
        """Prints text directly to the python interpreter's output. By default, the python
        interpreter wraps stdout with the built-in print() method.
        """
        print(msg, flush=True)      # default built-in method

    def __io_write(self, msg) -> None:
        """<...>"""
        self.__buffer.write(f"{msg}{self.end}")    # write to the Text I/O object
        self.__buffer.flush()       # flush the TextI/O object's buffer

    def __queue_msg(self, msg) -> None:
        """Places the text in a thread-safe queue for the PrinterThread."""
        self.__buffer.put(msg)      # enqueue text

    def __whisper(self, msg) -> None:
        """Method invoked to print text in the __call__ method. Overriden by the object
        with the corresponding print method depending on the object's mode
        """
        raise NotImplementedError("The __whisper() method was not overriden in the constructor!")

# if __name__ == "__main__":
#     import time
#     f = open(file='test.txt', mode='w')
#     # print('stdout', type(sys.stdout))
#     # print('stderr', type(sys.stderr))
#     # print('file  ', type(f))

#     buff = Queue()
#     kill = Event()
#     kill.clear()

#     # say = SayWriter()
#     # say = SayWriter(sys.stdout)
#     # say = SayWriter(sys.stderr)
#     say = SayWriter(f)

#     # say = SayWriter(buff)

#     printer = PrinterThread(
#         console_buff=buff,
#         name="PRINTER",
#         kill=kill
#     )
#     # printer.start()
#     for i in range(30):
#         say(f"Hello World! {i}")
#     kill.set()
#     # printer.join()
#     f.close()

