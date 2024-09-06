# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings


# built-in imports
import sys
import os

from threading import Event
from queue import Empty

# ----- PATH HAMMER v2.7 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:  # execute snippet if current script was run directly 
    """Resolve absolute imports by recusring into subdirectories and appending them to python path."""
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    print(f"Path Hammer: {src_abs}")
    assert src_abs.split('\\')[-1*len(root_target):] == root_target   # validate correct top folder
    
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split('\\')[-1] not in exclude] # get subdirs, exclude unwanted
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
        super()._setup()    # use parent implementation

    def _thread_cleanup_(self):
        """<...>"""
        self._whisper = self._print_stdout
        super()._cleanup()  # use parent implementation

    # ----- PRINT UTILS ----- #
    def say(self, msg):
        super().say(msg)