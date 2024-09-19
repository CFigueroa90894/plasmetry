
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
path_hammer(3, ['plasmetry', 'src'], ['__pycache__'], suffix='/src')  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #

from PyQt5.QtWidgets import QApplication
from experiment_run import ExperimentRun
from user_settings import UserSettings
from experiment_setup import ExperimentSetup
from control_layer import ControlLayer

class GuiManager():
    
    def __init__(self):
        # init control layer
        self.control = ControlLayer()
        
        self.control.load_config_file()        
        
    def start_signals(self):
        app = QApplication(sys.argv)

        setup_window = ExperimentSetup(self.control, ExperimentRun, UserSettings)
        
        run_window= ExperimentRun(self.control)
        
        settings_window = UserSettings()

        # Connect the signals for transitions between windows
        setup_window.switch_to_run.connect(run_window.show)

        setup_window.switch_to_settings.connect(settings_window.show)
        setup_window.switch_to_settings.connect(setup_window.close)

        # Back button in ExperimentRun should return to the setup window
        run_window.back_btn_clicked.connect(setup_window.show)
        run_window.back_btn_clicked.connect(run_window.close)

        # Back button in UserSettings should return to the setup window
        settings_window.back_btn_clicked.connect(setup_window.show)
        settings_window.back_btn_clicked.connect(settings_window.close)

        setup_window.show()
        
        sys.exit(app.exec_())
        
if __name__ == "__main__":
    gui_manager = GuiManager()
    gui_manager.start_signals()
   