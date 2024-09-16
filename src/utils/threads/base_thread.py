# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings


# built-in imports
import sys
import os
import traceback

from threading import Thread, Event, Timer, Barrier, BrokenBarrierError
from abc import ABCMeta, abstractmethod

# ----- PATH HAMMER v2.7 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:
    """Resolve absolute imports by recursing into subdirs and appending them to python path."""
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    assert src_abs.split('\\')[-1*len(root_target):] == root_target   # validate correct top folder
    
    # get subdirs, exclude unwanted
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split('\\')[-1] not in exclude]
    for dir in dirs: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: {src_abs}")

if __name__ == "__main__":  # execute path hammer if this script is run directly
    path_hammer(2, ['plasmetry', 'src'], ['__pycache__'])
# ----- END PATH HAMMER ----- #

# local imports
from say_writer import SayWriter

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
                 text_out:SayWriter=None,
                 daemon:bool=True,
                 *args, **kwargs
        ):
        """<...>"""
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
        """<...>
        <overload this one for plasmetry-specific threads>"""
        raise NotImplementedError("The thread's main() method is not implemented! \
                                  Did you overload it correctly in subclasses?")

    @abstractmethod
    def run(self):
        """<...>
        <the method invoked when calling start()>"""
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
        """<...>"""
        # assumes constructor already validated that barrier and delay are not both specified for this instance
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
        """<...>"""
        self._say_obj.close()
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
        self._say_obj(f"{self.name} : {msg}")   # invoke SayWriter object as a callable

