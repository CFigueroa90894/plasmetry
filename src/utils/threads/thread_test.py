# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - add docstrings


# built-in imports
import sys
import os

from threading import Event, Barrier
from queue import Queue, Empty
import time

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

from base_thread import BaseThread
from printer_thread import PrinterThread

class PrinterTestThread(PrinterThread):
    """<...>"""
    def __init__(self, *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)

    # ----- MAIN ----- #
    def _THREAD_MAIN_(self):
        """<...>"""
        while not self.kill.is_set() or not self.console_buff.empty():
            try:
                print(f"{self.console_buff.get(timeout=3)} : kill {self.kill.is_set()}")
            except Empty:
                pass


class SpammerThread(BaseThread):
    """<...>"""
    def __init__(self,
                 sleep_print=0,
                 msg:str=None,
                 kill:Event=None,
                 *args, **kwargs
        ):
        """<...>"""
        super().__init__(*args, **kwargs)
        self.sleep_print = sleep_print  # determines time to sleep run iterations
        self.msg = msg                  # message to print
        self.kill = kill                # shutdown signal
        self.count = 0

    # ----- MAIN ----- #
    def _THREAD_MAIN_(self):
        """<...>"""
        while not self.kill.is_set():
            self.say(self.msg)
            self.pause(self.sleep_print)

    def run(self):
        super().run()
    
    # ---- LIFE CYCLE ----- #
    def _setup(self):
        """<...>"""
        super()._setup()    # use parent implementation

    def _cleanup(self):
        """<...>"""
        super()._cleanup()  # use parent implementation

    # ----- PRINT UTILS ----- #
    def say(self, msg):
        """<...>"""
        self._whisper(f"{self.count} : {self.name} : {msg}")
        self.count += 1



class MainTestThread(BaseThread):
    def __init__(self, main_sleep=0, max_sleep=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_sleep = main_sleep
        self.max_sleep = max_sleep

    def run(self):
        """<...>"""
        super().run()

    def _setup(self):
        """<...>"""
        super()._setup()

    def _cleanup(self):
        """<...>"""
        super()._cleanup()

    def say(self, msg):
        super().say(msg)

    def _THREAD_MAIN_(self):
        """<...>"""
        self.say("init...")
        kill = Event()
        buff = Queue()
        barr = Barrier(2)
        self.console_buff = buff
        self._whisper = self._print_buff

        self.say("init children...")
        self.pause(self.main_sleep)

        printer = PrinterTestThread(
            console_buff=buff,
            daemon=True,
            name="Printer",
            kill=kill
        )
        alpha  = SpammerThread(
            start_barrier=barr,
            msg="HHHeeelllooo!!!",
            console_buff=buff,
            daemon=True,
            name="Alpha",
            kill=kill
        )
        beta  = SpammerThread(
            start_barrier=barr,
            msg="WWWooorrrlllddd!!!",
            console_buff=buff,
            daemon=True,
            name="Beta",
            kill=kill
        )
        self.say("starting printer...")
        printer.start()
        self.pause(self.main_sleep)

        self.say("starting children...")
        self.pause(self.main_sleep)
        beta.start()
        alpha.start()

        self.say(f"sleeping for {self.max_sleep}...")
        start = time.perf_counter()
        self.pause(self.max_sleep)
        end = time.perf_counter()

        self.say("awake...")
        self.say("send kill signal...")
        kill.set()

        alpha.join()
        beta.join()
        printer.join()

        self._whisper = self._print_stdout

        self.say("children joined")
        self.pause(self.main_sleep)

        self.say(f"slept for {end - start}")
        self.say("terminating...")
        self.pause(self.main_sleep)
        sys.exit(0)


if __name__ == "__main__":
    main = MainTestThread(
        name="MAIN",
        main_sleep = 0.5,
        max_sleep = 0.01
    )
    main.start()
    main.join()