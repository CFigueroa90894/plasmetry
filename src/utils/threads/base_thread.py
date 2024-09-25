""" G3 - Plasma Devs
Utilities - Base Thread
    Provides a parent class that defines common behavior for Plasmetry's thread's, including
    life-cycle utils, text output, error handling, and sleep functions. Additionally, it specifies
    abstract methods for all Plasmetry's threads to ensure consistent behavior.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    BaseThread - subclass that extends the built-in Thread class from the threading module
"""

# built-in imports
import sys
import os
import traceback

from threading import Thread, Event, Timer, Barrier, BrokenBarrierError
from abc import ABCMeta, abstractmethod

# ----- PATH HAMMER v3.0 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:
    """Resolve absolute imports by recursing into subdirs and appending them to python path."""
    # os delimeters
    win_delimeter, rpi_delimeter = "\\", "/"

    # locate project root
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    print(f"Path Hammer: {src_abs}")

    # select path delimeter
    if win_delimeter in src_abs: delimeter = win_delimeter
    elif rpi_delimeter in src_abs: delimeter = rpi_delimeter
    else: raise RuntimeError("Path Hammer could not determine path delimeter!")

    # validate correct top folder
    assert src_abs.split(delimeter)[-1*len(root_target):] == root_target
    
    # get subdirs, exclude unwanted
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split(delimeter)[-1] not in exclude]
    for dir in dirs: sys.path.append(dir)    # add all subdirectories to python path

if __name__ == "__main__":  # execute path hammer if this script is run directly
    path_hammer(2, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #

# local imports
from say_writer import SayWriter


class BaseThread(Thread, metaclass=ABCMeta):
    """This base class extends the functionality of python's built-in Thread class.
    
    The traditional Thread class uses the run() method to define all of its threaded life-cycle;
    BaseThread enhances reusability by dividing a thread's life-cycle execution into three parts:
    setup, main loop, and cleanup. This allows safer recovery from exceptions by wrapping the main
    loop in a try/except statement; should errors occur, the thread can still proceed to the cleanup
    script, making error handling more robust. While this is possible without needing to write three
    different methods, it allows subclasses to reuse setup and cleanup scripts.
     
    Attributes:
        + delay: float - number of seconds that the thread should wait before entering its main loop
        + barrier: Barrier - synchronization primitive that prevents the thread from starting until
            a specified number of threads reach the barrier
        + pause_sig: Event - flag used locally to pause a threads execution
        # _say_obj: SayWriter - text output object used to write messages

    Methods:
        + __init__() - object constructor
        + run() - executes the threads three life-cycle methods, invoked by the threading framework
            when start() is called on the BaseThread object.
        + pause() - blocks the thread's execution for a specified time
        + say() - text output method, using the SayWriter
        # _THREAD_MAIN_() - the main loop of the thread
        # _thread_setup_() - performs preparations before the _THREAD_MAIN_() method is called
        # _thread_cleanup_() - performs exit actions before finally terminating the thread
        # _delay_start() - blocks the thread's startup until a specified time passes
        # _barrier_wait() - blocks the thread's startup until other threads are at the barrier
        # _wake() - callback function to wake up a paused thread
    """
    def __init__(self,
                 start_delay:int|float=None,
                 start_barrier:Barrier=None,
                 text_out:SayWriter=None,
                 daemon:bool=True,
                 *args, **kwargs
        ):
        """The BaseThread constructor. Must be called using keyword arguments.
        
        Arguments:
            start_delay: int|float - seconds thread must wait before starting
                default: None - thread starts immediately
            start_barrier: Barrier - prevents thread from starting until other threads are ready
                default: None - thread starts immediately
            text_out: SayWriter - object used to output text
                default: None - built in 'print()' method used to output text
            daemon: bool - sets a threads behavior to daemonic, see built-in threading module
                default: True - thread exits if no non-daemonic threads are alive

        * NOTE: A start delay and a start barrier cannot both be given simultaneously. This will
        raise an assertion error in order to protect the thread from unpredictable behavior.

        """
        super().__init__(*args, daemon=daemon, **kwargs)   # initialize attributes from parent
        
        # Validate console_out argument
        if text_out is None:
            text_out = SayWriter()   # default SayWriter objects use built-in 'print()'
        # Error handling
        elif not isinstance(text_out, SayWriter):
            raise TypeError(f"Console out must be SayWriter! Given {type(text_out)}")

        # Validate start_delay and start_barrier arguments
        assert_msg = f"Cannot instantiate with both: delay: {start_delay}, barrier: {start_barrier}"
        assert start_delay is None or start_barrier is None, assert_msg

        # Save Arguments
        self.delay = start_delay            # delay run() by specified amount of time
        self.barrier = start_barrier        # delay run() until all threads are at the barrier
        self._say_obj = text_out             # save print util, SaveWriter object

        # Create attributes
        self.pause_sig = Event()            # local signal used to pause thread

    # ----- MAIN ----- #
    @abstractmethod
    def _THREAD_MAIN_(self):
        """The main loop in a thread's life cycle."""
        raise NotImplementedError("The thread's main() method is not implemented! \
                                  Did you overload it correctly in subclasses?")

    @abstractmethod
    def run(self):
        """Invoked by the threading framework when the start() method is called on the thread.
        
        Calls the setup method, then the main loop, then finally the cleanup. The main loop is
        wrapped in a try/except clause to catch all errors that may occur in the loop without
        killing the thread. To avoid reraising the exception, its traceback is outputted through
        the SayWriter object.
        """
        self._thread_setup_()
        try:
            self._THREAD_MAIN_()
        except Exception as err:
            self.say(err)
            self.say(traceback.format_exc())
        self._thread_cleanup_()

    # ----- LIFE CYCLE UTILS ----- #
    @abstractmethod
    def _thread_setup_(self):
        """Prepares the thread for execution.

        Blocks the thread's execution on startup either with a timed delay or by waiting at the
        barrier object, depending on the initialization arguments.
        """
        # assumes constructor already validated that barrier and delay are not both specified
        try:
            if self.delay is not None:
                self._delay_start()
            if self.barrier is not None:
                self._barrier_wait()
            self.say("running...")
        except BrokenBarrierError:
            self.say("barrier broken, aborting...")
            self._thread_cleanup_()
            
    @abstractmethod
    def _thread_cleanup_(self):
        """Closes the output object stream and terminates the thread."""
        self._say_obj.close()
        self.say("exiting...")
        sys.exit(0)
    
    def _delay_start(self):
        """Blocks thread startup until the given time has passed."""
        self.say(f"delaying run by {self.delay} sec...")
        self.pause(self.delay)

    def _barrier_wait(self):
        """Blocks thread startup until the barrier is released."""
        self.say("waiting at barrier...")
        self.barrier.wait()

    # ----- SLEEP UTILS ----- #
    def pause(self, sec):
        """Pauses a thread's execution until a Timer object invokes the callback function."""
        self.pause_sig.clear()
        Timer(sec, self._wake).start()
        self.pause_sig.wait()

    def _wake(self):
        """Call back function that sets the pause signal to True."""
        self.pause_sig.set()

    # ----- PRINT UTILS ----- #
    @abstractmethod
    def say(self, msg):
        """Outputs formatted text prefixed with the thread name using a SayWriter object."""
        self._say_obj(f"{self.name} : {msg}")   # invoke SayWriter object as a callable