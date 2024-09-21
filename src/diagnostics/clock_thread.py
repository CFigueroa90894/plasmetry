""" G3 - Plasma Devs
Layer 3 - Diagnostics
    Provides a simple BaseThread subclass that signals when the next data sample should be taken.

author: figueroa_90894@students.pupr.edu
status: DONE

classes:
    ClockThread - Controls synchronization for Probe Object thread's data sampling.
"""

# built-in imports
import sys
import os

from threading import Event, Timer

# ----- PATH HAMMER v2.7 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:
    """Resolve absolute imports by recusring into subdirs and appending them to python path."""
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    print(f"Path Hammer: {src_abs}")
    assert src_abs.split('\\')[-1*len(root_target):] == root_target   # validate correct top folder
    
    # get subdirs, exclude unwanted
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split('\\')[-1] not in exclude]
    for dir in dirs: sys.path.append(dir)    # add all subdirectories to python path

if __name__ == "__main__":  # execute path hammer if this script is run directly
    # hammer subdirs in plasmetry/src
    path_hammer(1, ['plasmetry', 'src'], ['__pycache__'])
# ----- END PATH HAMMER ----- #

# local imports
from base_thread import BaseThread


class ClockThread(BaseThread):
    """The ClockThread class provides a synchronization mechanism for Probe Objects.
    
    Attributes:
        + rate: float - ticks per second (Hz)
        + interval: float - time between ticks (seconds)
        + trigger: Event - signal to notify other threads an interval has passed
        + kill: Event - signal to stop the clock thread

    Methods
        + tick() - notify an interval passed, overriden at constructor
        # _debug_tick_() - print at every tick
        # _default_tick() - no prints during ticking
        ^+ run() - called when start() is invoked
        + pause() - starts a timer but does explicitly wait, redefines parent method
        # _THREAD_MAIN_() - main loop
        # _thread_setup_() - prepares clock thread
        # _thread_cleanup() - exit function
        ^+ say() - print out a message
    """
    def __init__(self, tick_rate:float, trigger:Event, kill:Event, debug=False, *args, **kwargs):
        """Initialize the ClockThread.
        
        Arguments:
            tick_rate: float - number of ticks per second (Hz)
            trigger: Event - mechanism to signal other threads an interval has passed
            kill: Event - mechanism to stop the ClockThread
            debug: bool - when set, clock prints at every tick
                default: False
        """
        super().__init__(*args, **kwargs)   # initialize inherited attributes
        self.rate = tick_rate       # ticks per second (Hz)
        self.interval = 1/tick_rate # seconds between ticks
        self.trigger = trigger      # tick notification mechanism
        self.kill = kill            # stop the clock thread

        # select tick method
        if debug:
            self.tick = self._debug_tick_
        else:
            self.tick = self._default_tick

    # ----- Tick Methods ----- #
    def tick(self):
        """Notifies other threads that an interval has passed. Overloaded in constructor."""
        raise NotImplementedError("Method tick() was not overloaded in the constructor!")

    def _debug_tick_(self):
        """Notifies other threads an interval has passed and print a 'tick' message."""
        self._default_tick()
        self.say("tick")

    def _default_tick(self):
        """Notifies other threads an interval has passed."""
        self.trigger.set()  # set the flag to notify the interval hass passed

    # ----- Thread Overloads ----- #
    def run(self):
        """Inherited from parent. Called by the threading framework when start() is called."""
        super().run()   # call parent run method

    # Redefines the inherited method
    def pause(self, sec):
        """Set the timer, but DO NOT wait. Call wait manually in other methods."""
        self.pause_sig.clear()
        Timer(sec, self._wake).start()

    def _THREAD_MAIN_(self):
        """The main loop for the ClockThread. Sets the trigger flag every tick."""
        while not self.kill.is_set():
            self.pause(self.interval)   # set interval timer
            self.tick()                 # notify interval has passed
            self.pause_sig.wait(timeout=self.interval+1)    # wait for interval to pass

    def _thread_setup_(self):
        """Clear the given trigger and invoke parent method."""
        self.trigger.clear()        # reset the trigger mechanism
        super()._thread_setup_()    # call parent setup

    def _thread_cleanup_(self):
        """Perform thread exit functions. Inherited from parent."""
        super()._thread_cleanup_()  # call parent cleanup

    def say(self, msg):
        """Print out messages, by default to the console. Inherited from parent."""
        super().say(msg)    # call parent print

