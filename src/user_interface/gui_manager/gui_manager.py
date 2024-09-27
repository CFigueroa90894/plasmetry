import sys
import os

# ----- PATH HAMMER v3.0 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:
    """Resolve absolute imports by recursing into subdirs and appending them to python path."""
    # os delimeters
    win_delimeter, rpi_delimeter = "\\", "/"

    # locate project root
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    print(f"Path Hammer: {src_abs}")

    # select path delimeter
    if win_delimeter in src_abs: delimeter = win_delimeter
    elif rpi_delimeter in src_abs: delimeter = rpi_delimeter
    else: raise RuntimeError("Path Hammer could not determine path delimeter!")

    # validate correct top folder
    assert src_abs.split(delimeter)[-1*len(root_target):] == root_target
    
    # get subdirs, exclude unwanted
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split(delimeter)[-1] not in exclude]
    for dir in dirs: sys.path.append(dir)    # add all subdirectories to python path

if __name__ == "__main__":  # execute path hammer if this script is run directly
    path_hammer(2, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #

from PyQt5.QtWidgets import QApplication
from experiment_run import ExperimentRun
from user_settings import UserSettings
from experiment_setup import ExperimentSetup
from control_layer import ControlLayer

class GuiManager():
    """GuiManager acts as the main entry point of the application when initialized and properly set-up."""
    
    def __init__(self):
        """Gui manager constructor. Initializes the control layer."""                                                                                         
        # Initialize control layer
        self.control = ControlLayer()
        
        # Loading the config file data
        self.control.load_config_file()    
        
    def start_signals(self):
        """start_signals instantiates the GUI components, connects signal emissions for page switching, and defines the exit logic."""
        
        # Initializing the GUI
        app = QApplication(sys.argv)
        app.setStyle('Windows')
        
        # Initializing each window of the GUI
        settings_window= UserSettings
        run_window = ExperimentRun(self.control)
        setup_window = ExperimentSetup(self.control, run_window, settings_window)
        settings_window = UserSettings(self.control, setup_window)
        
        # Setting up logic for signal emission
        setup_window.switch_to_run.connect(lambda: (run_window.show(), setup_window.close()))
        setup_window.switch_to_settings.connect(lambda: (settings_window.show(), setup_window.close(), settings_window.set_widget_values()))
        run_window.back_btn_clicked.connect(lambda: (setup_window.show(), run_window.close()))
        settings_window.back_btn_clicked.connect(lambda: (setup_window.show(), settings_window.close()))
        
        # Showing the first page (Experiment setup page)
        setup_window.show()
        
        # Logic for when app is about to close, done so to properly clear all components
        app.aboutToQuit.connect(lambda: self.control.layer_shutdown())
        
        # App exit from execution
        sys.exit(app.exec_())
    
if __name__ == "__main__":
    
    """Gui manager instantiation and setup is performed here."""

    # Instantiating GuiManager object and the control components
    gui_manager = GuiManager()
    
    # Instantiation of GUI components
    gui_manager.start_signals()
   