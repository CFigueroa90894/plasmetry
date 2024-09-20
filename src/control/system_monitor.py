# built-in imports
import sys
import os
import traceback

from threading import Event, current_thread
from queue import Queue, Empty
from io import TextIOWrapper

from typing import Tuple

import time

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

class SystemMonitor(BaseThread):
    def __init__(self, 
                 kill:Event,
                 daemon=False,
                 name="SYSMON",
                 parent_thread=None,
                 shutdown_callback=None,
                 *args, **kwargs):

        if parent_thread is None:
            parent_thread = current_thread()

        self._shutdown = shutdown_callback

        # Save Arguments
        self.kill = kill        # signal to terminate thread
        self._parent = parent_thread
        
        # Initialize parent attributes
        super().__init__(*args, name=name, daemon=daemon, **kwargs)

            
    # ----- THREAD MAIN ----- #
    def _THREAD_MAIN_(self):

        while not self.kill.is_set():
                if not self._parent.is_alive():
                    self.kill.set()
                    self.say("SYSTEM CRASH DETECTED")
                    self.say("TERMINATING")
                    self._shutdown()
                time.sleep(5)
    
    # ---- THREAD LIFE CYCLE ----- #
    def run(self):
        """Call the run() method inherited from parent class."""
        super().run()

    def _thread_setup_(self):
        """Call the _thread_setup_() method inherited from parent class."""
        super()._thread_setup_()    # use parent implementation

    def _thread_cleanup_(self):
        """Perform all thread cleanup functions. Writes the last PrinterThread message then
        closes all writers before finally terminating the thread.
        """
        self.say("exiting...")
        self._say_obj.close()       # close personal writer
        sys.exit(0)

    # ----- PRINT UTILS ----- #
    def say(self, msg):
        """Prints a message to the output buffer."""
        super().say(msg)    # call method inherited from parent

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


