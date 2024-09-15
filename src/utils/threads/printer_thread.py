""" G3 - Plasma Devs
Utilities - Printer Thread
    Provides a class, PrinterThread, that provides thread-safe text output for objects and scripts.
    The PrinterThread reads text from a queue and outputs it so the specified object.

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

from threading import Event
from queue import Empty


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
        self._whisper = self._print_buff    # set the printing mode
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

