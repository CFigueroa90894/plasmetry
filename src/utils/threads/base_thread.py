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
        _setup
        _cleanup
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
        super().__init__(*args, **kwargs)   # initialize attributes inherited from parent
        assert start_delay is None or start_barrier is None, f"Cannot instantiate with both: delay: {start_delay}, barrier: {start_barrier}"     # validate start conditions

        self.delay = start_delay            # delay run() by specified amount of time
        self.barrier = start_barrier        # delay run() until all threads are waiting at the barrier
        self.console_buff = console_buff        # select how to print console messages, by default uses built-in print
        self.dameon = daemon                # if set, forcibly terminate thread if main thread exits

        self.pause_sig = Event()            # local signal used to pause thread

        # Overload say() with appropriate output
        # default value
        if self.console_buff is None:
            self._whisper = self._print_stdout
        # PrinterThread buffer
        elif isinstance(console_buff, Queue):
            self._whisper = self._print_buff
        # Error Handling
        else:
            raise AttributeError(f"{self.__class__}'s constructor could not overload the __say() instance method.")


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
        self._setup()
        self._THREAD_MAIN_()
        self._cleanup()

    # ----- LIFE CYCLE UTILS ----- #
    @abstractmethod
    def _setup(self):
        """<...>"""
        # assumes constructor already validated that barrier and delay are not both specified for this instance
        if self.delay is not None:
            self._delay_start()
        if self.barrier is not None:
            self._barrier_wait()
        self.say("running...")

    @abstractmethod
    def _cleanup(self):
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

