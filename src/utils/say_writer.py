""" G3 - Plasma Devs
Utilities - Say Writer
    Provides printing a utility class, capable of outputting text to various I/O objects, as well
    as well as Queue objects from the built-in queue module.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    SayWriter - object to provide thread-safe printing functionality
"""

# built-in imports
from io import TextIOWrapper
from queue import Queue
from typing import Tuple

class SayWriter:
    """A basic printing object that abstracts away the need for other objects to manually track
    which output they should print to.

    The SayWriter object overloads the python magic method __call__, meaning that instantiated
    objects of the class can be invoked as if they were functions. Doing so invokes the __call__
    method, which calls printing method defined by the object's mode.

    Usage Example:
        say = SayWriter()   # instantiate the object
        say("Hello World!") # call the object as a function
    
    Attributes:
        + end - terminator for Text I/O outputs (default: newline)
        - __buffer: Queue | TextIOWrapper - object to output text
        - __mode: str - string identifying the objects write mode
    
    Mehtods:
        + __init__() - object constructor
        + set_buffer() - changes the printing mode of object
        + __call__() - method called when a SayWriter object is invoked as callable object
        + close() - close the writers output stream
        + get_mode() - returns the current mode and used buffer
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
    
    def close(self):
        """Close the buffer if it is an instance of TextIOWrapper."""
        if isinstance(self.__buffer, TextIOWrapper):
            self.__buffer.close()

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
        """Writes text to a Text I/O stream."""
        self.__buffer.write(f"{msg}{self.end}")    # write to the Text I/O object
        self.__buffer.flush()       # flush the TextI/O object's buffer

    def __queue_msg(self, msg) -> None:
        """Places the text in a thread-safe queue for buffering."""
        self.__buffer.put(msg)      # enqueue text

    def __whisper(self, msg) -> None:
        """Method invoked to print text in the __call__ method. Overriden by the object
        with the corresponding print method depending on the object's mode
        """
        raise NotImplementedError("The __whisper() method was not overriden in the constructor!")