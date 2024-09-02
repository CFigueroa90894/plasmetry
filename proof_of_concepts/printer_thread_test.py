# author: figueroa_90894@students.pupr.edu
# status: DONE
#
# Testing asynchronous prints with a PrinterThread


# built-in imports
import sys

from threading import Thread, Event, Timer, Barrier
from queue import Queue, Full, Empty

import time

# ----- PATH HAMMER v2.7 ----- resolve absolute imports ----- #
# def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:  # execute snippet if current script was run directly 
#     """Resolve absolute imports by recusring into subdirectories and appending them to python path."""
#     src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
#     print(f"Path Hammer: {src_abs}")
#     assert src_abs.split('\\')[-1*len(root_target):] == root_target   # validate correct top folder
    
#     dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split('\\')[-1] not in exclude] # get subdirs, exclude unwanted
#     for dir in dirs: sys.path.append(dir)    # add all subdirectories to python path

# if __name__ == "__main__":  # execute path hammer if this script is run directly
#     path_hammer(1, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #


class BaseThread(Thread):
    """<...>"""
    
    def __init__(self, start_barrier:Barrier=None, daemon:bool=True, start_delay=0, sleep_print=None, msg:str=None, kill:Event=None, print_buff:Queue=None, *args, **kwargs):
        """<...>"""
        super().__init__(*args, **kwargs)
        self.sleep_print = sleep_print  # determines time to sleep run iterations
        self.msg = msg                  # message to print
        self.kill = kill                # shutdown signal
        self.print_buff = print_buff    # console output buffer
        self.count = 0
        self.delay = start_delay
        self.dameon = daemon
        self.start_barrier = start_barrier

        self.pause_sig = Event()

        # overload say() with appropriate message
        if self.print_buff is None:
            self._say = self._say_print
        elif isinstance(print_buff, Queue):
            self._say = self._say_buff
        else:
            raise AttributeError(f"{self.__class__}'s constructor could overload the __say() instance method.")

    def say(self, msg):
        """<...>"""
        self._say(f"{self.count} : {self.name} : {msg}")
        self.count += 1

    def _say(self, msg):   # Constructor overloads this method based on passed arguments
        """<...>"""
        raise NotImplementedError(f"{self.__class__} constructor did not correctly override the say() method.")

    def _say_print(self, msg):
        """<...>"""
        print(msg, flush=True)

    def _say_buff(self, msg):
        """<...>"""
        try:
            self.print_buff.put(msg)
        except Full:
            pass
        
    def _cleanup(self):
        """<...>"""
        self.say("exiting...")

    def _wake(self):
        self.pause_sig.set()


    def pause(self, sec):
        self.pause_sig.clear()
        Timer(sec, self._wake).start()
        self.pause_sig.wait()
        

    def run(self):
        """<...>"""
        # self.pause(self.delay)
        self.start_barrier.wait()
        while not self.kill.is_set():
            self.say(self.msg)
        self._cleanup()
        sys.exit(0)


class PrinterThread(BaseThread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._say = self._say_print

    def _cleanup(self):
        self.say("exiting...")
    
    def run(self):
        self.pause(self.delay)
        self.say("running...")
        while not self.kill.is_set() or not self.print_buff.empty():
            try:
                print(f"{self.print_buff.get(timeout=3)} : kill {self.kill.is_set()}")
            except Empty:
                pass
        self._cleanup()
        sys.exit(0)

class MainThread(BaseThread):
    def __init__(self, main_sleep=0, max_sleep=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_sleep = main_sleep
        self.max_sleep = max_sleep

    def run(self):
        self.main()

    def main(self):
        self.say("init...")
        kill = Event()
        buff = Queue()
        barr = Barrier(2)

        self.say("init children...")
        start_delay = 1
        self.pause(self.main_sleep)

        printer = PrinterThread(
            print_buff=buff,
            daemon=True,
            name="Printer",
            kill=kill
        )
        alpha  = BaseThread(
            start_barrier=barr,
            start_delay = start_delay,
            sleep_print=0.5, 
            msg="HHHeeelllooo!!!",
            print_buff=buff,
            daemon=True,
            name="Alpha",
            kill=kill
        )
        beta  = BaseThread(
            start_barrier=barr,
            start_delay = start_delay,
            sleep_print=0.8,
            msg="WWWooorrrlllddd!!!",
            print_buff=buff,
            daemon=True,
            name="Beta",
            kill=kill
        )
        self.say("starting printer...")
        printer.start()
        self.pause(self.main_sleep)

        self.say("starting children...")
        beta.start()
        alpha.start()

        self.say(f"sleeping for {self.max_sleep}...")
        start = time.perf_counter()
        self.pause(self.max_sleep)
        end = time.perf_counter()

        self.say("awake...")
        self.say("send kill signal...")
        kill.set()
        self.pause(self.main_sleep)

        self.say("awaiting children...")
        alpha.join()
        beta.join()
        printer.join()

        self.say("children joined")
        self.pause(self.main_sleep)

        self.say(f"slept for {end - start}")
        self.say("terminating...")
        self.pause(self.main_sleep)
        sys.exit(0)


if __name__ == "__main__":
    main = MainThread(
        name="MAIN",
        main_sleep = 2,
        max_sleep = 0.5
    )
    main.start()
    main.join()

