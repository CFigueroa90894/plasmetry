# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings


# built-in imports
import sys

from threading import Thread, Event, Timer, Barrier
from queue import Queue, Full
from abc import ABCMeta, abstractmethod

class BaseThread(Thread, metaclass=ABCMeta):
    """<...>
    <required override methods>
        _THREAD_MAIN_
        run
        _setup_
        _cleanup_
        say
    """
    
    def __init__(self,
                 start_delay:int|float=None,
                 start_barrier:Barrier=None,
                 console_buff:Queue=None,
                 daemon:bool=True,
                 *args, **kwargs
        ):
        """<...>"""
        super().__init__(*args, daemon=daemon, **kwargs)   # initialize attributes from parent
        
        # Define variable with custom setters and getters
        self._console_buff = None   # protected attribute to store mirrored public console_buff

        # Validate arguments
        assert_msg = f"Cannot instantiate with both: delay: {start_delay}, barrier: {start_barrier}"
        assert start_delay is None or start_barrier is None, assert_msg

        # Save Arguments
        self.delay = start_delay            # delay run() by specified amount of time
        self.barrier = start_barrier        # delay run() until all threads are at the barrier
        self.console_buff = console_buff    # select how to print, by default uses built-in print

        self.pause_sig = Event()            # local signal used to pause thread

    # console buffer definition and getter
    @property
    def console_buff(self):
        return self._console_buff
    
    # console buffer setter
    @console_buff.setter
    def console_buff(self, buff):
        """<...>"""
        # Overload say() with appropriate output
        # default value
        if buff is None:
            self._whisper = self._print_stdout
            self._console_buff = buff
            self.say(f"prints set to default for {self}")
        # PrinterThread buffer
        elif isinstance(buff, Queue):
            self._whisper = self._print_buff
            self._console_buff = buff
            self.say(f"prints set to buffer for {self}")
        # Error Handling
        else:
            raise AttributeError(f"{self.__class__}'s could not overload the __say() method.")


    # ----- MAIN ----- #
    @abstractmethod
    def _THREAD_MAIN_(self):
        """<...>
        <overload this one for plasmetry-specific threads>"""
        raise NotImplementedError("The thread's main() method is not implemented! Did you overload it correctly in subclasses?")

    @abstractmethod
    def run(self):
        """<...>
        <the method invoked when calling start()>"""
        self._thread_setup_()
        self._THREAD_MAIN_()
        self._thread_cleanup_()

    # ----- LIFE CYCLE UTILS ----- #
    @abstractmethod
    def _thread_setup_(self):
        """<...>"""
        # assumes constructor already validated that barrier and delay are not both specified for this instance
        if self.delay is not None:
            self._delay_start()
        if self.barrier is not None:
            self._barrier_wait()
        self.say("running...")

    @abstractmethod
    def _thread_cleanup_(self):
        """<...>"""
        self.say("exiting...")
        sys.exit(0)
    
    def _delay_start(self):
        """<...>"""
        self.say(f"delaying run by {self.delay} sec...")
        self.pause(self.delay)

    def _barrier_wait(self):
        """<...>"""
        self.say("waiting at barrier...")
        self.barrier.wait()

    # ----- SLEEP UTILS ----- #
    def pause(self, sec):
        """<...>"""
        self.pause_sig.clear()
        Timer(sec, self._wake).start()
        self.pause_sig.wait()

    def _wake(self):
        """<...>"""
        self.pause_sig.set()

    # ----- PRINT UTILS ----- #
    @abstractmethod
    def say(self, msg):
        """<...>"""
        self._whisper(f"{self.name} : {msg}")   # invoke overloaded say method

    def _whisper(self):   # Constructor overloads this method based on passed arguments
        """<...>"""
        raise NotImplementedError(f"{self.__class__} constructor did not correctly override the say() method.")

    def _print_stdout(self, msg):
        """<...>"""
        print(msg, flush=True)

    def _print_buff(self, msg):
        """<...>"""
        try:
            self.console_buff.put(msg)
        except Full:
            pass

