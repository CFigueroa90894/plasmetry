import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal
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
path_hammer(2, ['plasmetry', 'src'], ['__pycache__'], suffix='/src')  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #

# Now you can import from abstract_layers
from control_layer import ControlLayer

import hardware_layer
import diagnostics_layer
from config_manager import ConfigManager

class ExperimentSetup(QMainWindow):
    switch_to_run = pyqtSignal()  # Signal to switch to the experiment run window
    switch_to_settings = pyqtSignal()  # Signal to switch to the user settings window

    def __init__(self):
        super().__init__()


        # init control layer
        self.control = ControlLayer()
        
        
        self.control.load_config_file()
        
        loadUi('experiment_setup.ui', self)  # Load the .ui file directly

        ############################## GENERAL SIGNALS ##############################

        # Initialize the view based on the QComboBox selection
        self.initialize_view()

        # Connect the continue button to switch to the experiment run window
        self.continue_btn.clicked.connect(self.emit_switch_to_run_signal)

        # Connect the view settings button to switch to the user settings window
        self.view_settings_btn.clicked.connect(self.emit_switch_to_settings_signal)

        # Connect the QComboBox signal to the method that updates the QStackedWidget
        self.probe_selection_cb.currentIndexChanged.connect(self.update_main_view)

        # Connect the reset button to reset settings to default
        self.reset_btn.clicked.connect(self.reset_setup)
        
        # Set values from config file
        self.set_widget_values()
        ############################## SLP SIGNALS ##############################

        # Connect Plus/Minus buttons for Min Voltage Ramp
        self.slp_volt_ramp_min_minus.clicked.connect(lambda: self.adjust_value(self.slp_volt_ramp_min_input, -1))
        self.slp_volt_ramp_min_plus.clicked.connect(lambda: self.adjust_value(self.slp_volt_ramp_min_input, +1))

        # Connect Plus/Minus buttons for Max Voltage Ramp
        self.slp_volt_ramp_max_minus.clicked.connect(lambda: self.adjust_value(self.slp_volt_rampt_max_input, -1))
        self.slp_volt_ramp_max_plus.clicked.connect(lambda: self.adjust_value(self.slp_volt_rampt_max_input, +1))

        # Connect Plus/Minus buttons for Sampling Rate
        self.slp_sampling_rate_minus.clicked.connect(lambda: self.adjust_value(self.slp_sampling_rate_input, -1))
        self.slp_sampling_rate_plus.clicked.connect(lambda: self.adjust_value(self.slp_sampling_rate_input, +1))

        # Connect Plus/Minus buttons for Number of Measurements 
        self.slp_num_measurements_minus.clicked.connect(lambda: self.adjust_value(self.slp_num_measurements_input, -1))
        self.slp_num_measurements_plus.clicked.connect(lambda: self.adjust_value(self.slp_num_measurements_input, +1))

        ############################## DLP SIGNALS ##############################

        # Connect Plus/Minus buttons for Min Voltage Ramp
        self.dlp_volt_ramp_min_minus.clicked.connect(lambda: self.adjust_value(self.dlp_volt_ramp_min_input, -1))
        self.dlp_volt_ramp_min_plus.clicked.connect(lambda: self.adjust_value(self.dlp_volt_ramp_min_input, +1))

        # Connect Plus/Minus buttons for Max Voltage Ramp
        self.dlp_volt_ramp_max_minus.clicked.connect(lambda: self.adjust_value(self.dlp_volt_rampt_max_input, -1))
        self.dlp_volt_ramp_max_plus.clicked.connect(lambda: self.adjust_value(self.dlp_volt_rampt_max_input, +1))

        # Connect Plus/Minus buttons for Sampling Rate
        self.dlp_sampling_rate_minus.clicked.connect(lambda: self.adjust_value(self.dlp_sampling_rate_input, -1))
        self.dlp_sampling_rate_plus.clicked.connect(lambda: self.adjust_value(self.dlp_sampling_rate_input, +1))

        # Connect Plus/Minus buttons for Number of Measurements 
        self.dlp_num_measurements_minus.clicked.connect(lambda: self.adjust_value(self.dlp_num_measurements_input, -1))
        self.dlp_num_measurements_plus.clicked.connect(lambda: self.adjust_value(self.dlp_num_measurements_input, +1))

        ############################## TLP-C SIGNALS ##############################

        self.tlp_c_sampling_rate_minus.clicked.connect(lambda: self.adjust_value(self.tlp_c_sampling_rate_input, -1))
        self.tlp_c_sampling_rate_plus.clicked.connect(lambda: self.adjust_value(self.tlp_c_sampling_rate_input, +1))

        self.tlp_c_positive_collector_gain_minus.clicked.connect(lambda: self.adjust_value(self.tlp_c_positive_collector_gain_input, -1))
        self.tlp_c_positive_collector_gain_plus.clicked.connect(lambda: self.adjust_value(self.tlp_c_positive_collector_gain_input, +1))

        self.tlp_c_positive_amp_bias_minus.clicked.connect(lambda: self.adjust_value(self.tlp_c_positive_amp_bias_input, -1))
        self.tlp_c_positive_amp_bias_plus.clicked.connect(lambda: self.adjust_value(self.tlp_c_positive_amp_bias_input, +1))

        self.tlp_c_negative_collect_gain_minus.clicked.connect(lambda: self.adjust_value(self.tlp_c_negative_collect_gain_input, -1))
        self.tlp_c_negative_collect_gain_plus.clicked.connect(lambda: self.adjust_value(self.tlp_c_negative_collect_gain_input, +1))

        self.tlp_c_negative_amp_bias_minus.clicked.connect(lambda: self.adjust_value(self.tlp_c_negative_amp_bias_input, -1))
        self.tlp_c_negative_amp_bias_plus.clicked.connect(lambda: self.adjust_value(self.tlp_c_negative_amp_bias_input, +1))

        ############################## TLP-V SIGNALS ##############################

        self.tlp_v_sampling_rate_minus.clicked.connect(lambda: self.adjust_value(self.tlp_v_sampling_rate_input, -1))
        self.tlp_v_sampling_rate_plus.clicked.connect(lambda: self.adjust_value(self.tlp_v_sampling_rate_input, +1))

        self.tlp_v_positive_collector_gain_minus.clicked.connect(lambda: self.adjust_value(self.tlp_v_positive_collector_gain_input, -1))
        self.tlp_v_positive_collector_gain_plus.clicked.connect(lambda: self.adjust_value(self.tlp_v_positive_collector_gain_input, +1))

        self.tlp_v_positive_amp_bias_minus.clicked.connect(lambda: self.adjust_value(self.tlp_v_positive_amp_bias_input, -1))
        self.tlp_v_positive_amp_bias_plus.clicked.connect(lambda: self.adjust_value(self.tlp_v_positive_amp_bias_input, +1))

        self.tlp_v_float_collect_gain_minus.clicked.connect(lambda: self.adjust_value(self.tlp_v_float_collect_gain_input, -1))
        self.tlp_v_float_collect_gain_plus.clicked.connect(lambda: self.adjust_value(self.tlp_v_float_collect_gain_input, +1))

        ############################## IEA SIGNALS ##############################

        self.iea_volt_ramp_min_minus.clicked.connect(lambda: self.adjust_value(self.iea_volt_ramp_min_input, -1))
        self.iea_volt_ramp_min_plus.clicked.connect(lambda: self.adjust_value(self.iea_volt_ramp_min_input, +1))

        self.iea_volt_ramp_max_minus.clicked.connect(lambda: self.adjust_value(self.iea_volt_rampt_max_input, -1))
        self.iea_volt_ramp_max_plus.clicked.connect(lambda: self.adjust_value(self.iea_volt_rampt_max_input, +1))

        self.iea_sampling_rate_minus.clicked.connect(lambda: self.adjust_value(self.iea_sampling_rate_input, -1))
        self.iea_sampling_rate_plus.clicked.connect(lambda: self.adjust_value(self.iea_sampling_rate_input, +1))

        self.iea_num_measurements_minus.clicked.connect(lambda: self.adjust_value(self.iea_num_measurements_input, -1))
        self.iea_num_measurements_plus.clicked.connect(lambda: self.adjust_value(self.iea_num_measurements_input, +1))

        self.iea_collector_probe_minus.clicked.connect(lambda: self.adjust_value(self.iea_collector_probe_input, -1))
        self.iea_collector_probe_plus.clicked.connect(lambda: self.adjust_value(self.iea_collector_probe_input, +1))

        self.iea_rejector_mesh_bias_minus.clicked.connect(lambda: self.adjust_value(self.iea_rejector_mesh_bias_input, -1))
        self.iea_rejector_mesh_bias_plus.clicked.connect(lambda: self.adjust_value(self.iea_rejector_mesh_bias_input, +1))

        ############################## HEA SIGNALS ##############################

        self.hea_volt_ramp_min_minus.clicked.connect(lambda: self.adjust_value(self.hea_volt_ramp_min_input, -1))
        self.hea_volt_ramp_min_plus.clicked.connect(lambda: self.adjust_value(self.hea_volt_ramp_min_input, +1))

        self.hea_volt_ramp_max_minus.clicked.connect(lambda: self.adjust_value(self.hea_volt_rampt_max_input, -1))
        self.hea_volt_ramp_max_plus.clicked.connect(lambda: self.adjust_value(self.hea_volt_rampt_max_input, +1))

        self.hea_sampling_rate_minus.clicked.connect(lambda: self.adjust_value(self.hea_sampling_rate_input, -1))
        self.hea_sampling_rate_plus.clicked.connect(lambda: self.adjust_value(self.hea_sampling_rate_input, +1))

        self.hea_num_measurements_minus.clicked.connect(lambda: self.adjust_value(self.hea_num_measurements_input, -1))
        self.hea_num_measurements_plus.clicked.connect(lambda: self.adjust_value(self.hea_num_measurements_input, +1))

        self.hea_faraday_cup_bias_minus.clicked.connect(lambda: self.adjust_value(self.hea_faraday_cup_bias_input, -1))
        self.hea_faraday_cup_bias_plus.clicked.connect(lambda: self.adjust_value(self.hea_faraday_cup_bias_input, +1))

        self.hea_cullinator_cup_minus.clicked.connect(lambda: self.adjust_value(self.hea_cullinator_cup_input, -1))
        self.hea_cullinator_cup_plus.clicked.connect(lambda: self.adjust_value(self.hea_cullinator_cup_input, +1))

    ############################## GENERAL SLOTS ##############################
    
    def set_widget_values(self):
        
        self.slp_volt_ramp_min_input.setValue(self.control.get_config('slp', 'sweep_min'))
        self.slp_volt_rampt_max_input.setValue(self.control.get_config('slp', 'sweep_max'))
        self.slp_sampling_rate_input.setValue(self.control.get_config('slp', 'sampling_rate'))
        self.slp_num_measurements_input.setValue(self.control.get_config('slp', 'num_samples'))
        
        self.dlp_volt_ramp_min_input.setValue(self.control.get_config('dlp', 'sweep_min'))
        self.dlp_volt_rampt_max_input.setValue(self.control.get_config('dlp', 'sweep_max'))
        self.dlp_sampling_rate_input.setValue(self.control.get_config('dlp', 'sampling_rate'))
        self.dlp_num_measurements_input.setValue(self.control.get_config('dlp', 'num_samples'))

    def initialize_view(self):
        # Initialize the view to display the correct page based on QComboBox selection.
        # Get the current index of the probe_selection_cb combobox
        current_index = self.probe_selection_cb.currentIndex()

        # Update the main view based on the current index
        self.update_main_view(current_index)

    def update_main_view(self, index):
        """
        Switch pages in the probe_config_view based on the current index of probe_selection_cb.
        """

        # Map the QComboBox index to the correct page in main_view
        if index == 0:
            self.main_view.setCurrentWidget(self.single_lang_probe)
        elif index == 1:
            self.main_view.setCurrentWidget(self.double_lang_probe)
        elif index == 2:
            self.main_view.setCurrentWidget(self.triple_lang_c_probe)
        elif index == 3:
            self.main_view.setCurrentWidget(self.triple_lang_v_probe)
        elif index == 4:
            self.main_view.setCurrentWidget(self.ion_energy_analyzer)
        elif index == 5:
            self.main_view.setCurrentWidget(self.hyper_energy_analyzer)

    def emit_switch_to_run_signal(self):
        # Get the selected probe from the QComboBox
        selected_probe = self.probe_selection_cb.currentText()

        # Emit the signal to switch to the experiment run window
        self.switch_to_run.emit()

        # Set the selected probe in the experiment run window
        run_window.set_selected_probe(selected_probe)

    def emit_switch_to_settings_signal(self):
        # Emit the signal to switch to the user settings window
        self.switch_to_settings.emit() 

    def reset_setup(self):
        print("Reset button clicked...waiting for implementation")

    ############################## Other Functions ##############################

    def adjust_value(self, spinbox, direction):
        """
        Adjust the value of a QDoubleSpinBox.
        
        :param spinbox: The QDoubleSpinBox to update.
        :param direction: 1 for increment, -1 for decrement.
        """
        current_value = spinbox.value()
        new_value = self.increment_last_decimal(current_value) if direction == 1 else self.decrement_last_decimal(current_value)
        
        spinbox.setValue(new_value)

    def increment_last_decimal(self, value):
        return round(value + 0.01, 2)

    def decrement_last_decimal(self, value):
        return round(value - 0.01, 2)

if __name__ == "__main__":
    from experiment_run import ExperimentRun
    from user_settings import UserSettings

    app = QApplication(sys.argv)

    setup_window = ExperimentSetup()
    run_window = ExperimentRun()
    settings_window = UserSettings()

    # Connect the signals for transitions between windows
    setup_window.switch_to_run.connect(run_window.show)
    setup_window.switch_to_run.connect(setup_window.close)

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
