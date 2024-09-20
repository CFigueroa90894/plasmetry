import sys
import os

# ----- PATH HAMMER v2.7 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:  # execute snippet if current script was run directly 
    """Resolve absolute imports by recusring into subdirectories and appending them to python path."""
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    assert src_abs.split('\\')[-1*len(root_target):] == root_target   # validate correct top folder
    
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split('\\')[-1] not in exclude] # get subdirs, exclude unwanted
    for dir in dirs: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: {src_abs}")

# Apply path hammer to append `abstract_layers` to Python path
if __name__ == "__main__":  # execute path hammer if this script is run directly
    path_hammer(3, ['plasmetry', 'src'], ['__pycache__'], suffix='/src')  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #

from PyQt5.QtWidgets import QApplication, QMessageBox
from experiment_run import ExperimentRun
from user_settings import UserSettings
from experiment_setup import ExperimentSetup
from control_layer import ControlLayer


class GuiManager():
    
    def __init__(self):
        # Initialize control layer
        self.control = ControlLayer()
        self.control.load_config_file()        
        
    def start_signals(self):
        app = QApplication(sys.argv)
        
       # sys.excepthook = self.global_exception_handler

        setup_window = ExperimentSetup(self.control, ExperimentRun, UserSettings)
        run_window = ExperimentRun(self.control)
        settings_window = UserSettings(self.control)

        setup_window.switch_to_run.connect(lambda: (run_window.show(), setup_window.close()))
        
        setup_window.switch_to_settings.connect(lambda: (settings_window.show(), setup_window.close()))
        run_window.back_btn_clicked.connect(lambda: (setup_window.show(), run_window.close()))
        settings_window.back_btn_clicked.connect(lambda: (setup_window.show(), settings_window.close()))

        setup_window.show()
        
        app.aboutToQuit.connect(lambda: self.control.layer_shutdown())
        
       
        sys.exit(app.exec_())
        
    def global_exception_handler(self, exctype, value, traceback):
        self.control.layer_shutdown()
       
if __name__ == "__main__":
    gui_manager = GuiManager()
    gui_manager.start_signals()
   