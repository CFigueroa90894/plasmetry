import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal, QTimer
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
# if __name__ == "__main__":  # execute path hammer if this script is run directly
#     path_hammer(2, ['plasmetry', 'src'], ['__pycache__'], suffix='/src')  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #

from control_layer import ControlLayer
from probe_enum import PRB
from experiment_setup_ui import Ui_experiment_setup_view
class ExperimentSetup(QMainWindow):
    
    """ExperimentSetup is defined to interface with the ui components shown at start-up and defines their logic."""
    
    close_signal = pyqtSignal() # Signal to notify GuiManager about the close request
    switch_to_run = pyqtSignal()  # Signal to switch to the experiment run window
    switch_to_settings = pyqtSignal()  # Signal to switch to the user settings window

    def __init__(self, control, run_window, settings_window):
        super().__init__()
        
        # Storing control object reference
        self.control= control
        
        # Storing reference to the other windows
        self.run_window_ref = run_window
        self.settings_window_ref = settings_window
        
        # Storing ui view
        self.ui = Ui_experiment_setup_view() 
        
        # Invoking the setupUi function, setting up the visual components
        self.ui.setupUi(self) 

        ############################## GENERAL SIGNALS ##############################


        # Initialize the view based on the QComboBox selection
        self.initialize_view()

        # Connect the continue button to switch to the experiment run window
        self.ui.continue_btn.clicked.connect(self.emit_switch_to_run_signal)

        # Connect the view settings button to switch to the user settings window
        self.ui.view_settings_btn.clicked.connect(self.emit_switch_to_settings_signal)
        
        # Connect the reset button to reset settings to default
        self.ui.reset_btn.clicked.connect(self.reset_setup)
        
        self.ui.probe_selection_cb.currentIndexChanged.connect(self.update_main_view)  
        self.selected_probe = self.ui.probe_selection_cb.currentText()[-4:-1].lower()
        
        
        # Set values from config file
        self.set_widget_values()
        
        ############################## SLP SIGNALS ##############################
      
        # Connect Plus/Minus buttons for Min Voltage Ramp
        self.ui.slp_volt_ramp_min_minus.clicked.connect(lambda: self.adjust_value(self.ui.slp_volt_ramp_min_input, -1, 'sweep_min'))
        self.ui.slp_volt_ramp_min_plus.clicked.connect(lambda: self.adjust_value(self.ui.slp_volt_ramp_min_input, +1, 'sweep_min'))

        # Connect Plus/Minus buttons for Max Voltage Ramp
        self.ui.slp_volt_ramp_max_minus.clicked.connect(lambda: self.adjust_value(self.ui.slp_volt_rampt_max_input, -1, 'sweep_max'))
        self.ui.slp_volt_ramp_max_plus.clicked.connect(lambda: self.adjust_value(self.ui.slp_volt_rampt_max_input, +1, 'sweep_max'))

        # Connect Plus/Minus buttons for Sampling Rate
        self.ui.slp_sampling_rate_minus.clicked.connect(lambda: self.adjust_value(self.ui.slp_sampling_rate_input, -1, 'sampling_rate'))
        self.ui.slp_sampling_rate_plus.clicked.connect(lambda: self.adjust_value(self.ui.slp_sampling_rate_input, +1, 'sampling_rate'))

        # Connect Plus/Minus buttons for Number of Measurements 
        self.ui.slp_num_measurements_minus.clicked.connect(lambda: self.adjust_value(self.ui.slp_num_measurements_input, -1, 'num_samples'))
        self.ui.slp_num_measurements_plus.clicked.connect(lambda: self.adjust_value(self.ui.slp_num_measurements_input, +1, 'num_samples'))

        ############################## DLP SIGNALS ##############################

        # Connect Plus/Minus buttons for Min Voltage Ramp
        self.ui.dlp_volt_ramp_min_minus.clicked.connect(lambda: self.adjust_value(self.ui.dlp_volt_ramp_min_input, -1, 'sweep_min'))
        self.ui.dlp_volt_ramp_min_plus.clicked.connect(lambda: self.adjust_value(self.ui.dlp_volt_ramp_min_input, +1, 'sweep_min'))

        # Connect Plus/Minus buttons for Max Voltage Ramp
        self.ui.dlp_volt_ramp_max_minus.clicked.connect(lambda: self.adjust_value(self.ui.dlp_volt_rampt_max_input, -1, 'sweep_max'))
        self.ui.dlp_volt_ramp_max_plus.clicked.connect(lambda: self.adjust_value(self.ui.dlp_volt_rampt_max_input, +1, 'sweep_max'))

        # Connect Plus/Minus buttons for Sampling Rate
        self.ui.dlp_sampling_rate_minus.clicked.connect(lambda: self.adjust_value(self.ui.dlp_sampling_rate_input, -1, 'sampling_rate'))
        self.ui.dlp_sampling_rate_plus.clicked.connect(lambda: self.adjust_value(self.ui.dlp_sampling_rate_input, +1, 'sampling_rate'))

        # Connect Plus/Minus buttons for Number of Measurements 
        self.ui.dlp_num_measurements_minus.clicked.connect(lambda: self.adjust_value(self.ui.dlp_num_measurements_input, -1, 'num_samples'))
        self.ui.dlp_num_measurements_plus.clicked.connect(lambda: self.adjust_value(self.ui.dlp_num_measurements_input, +1, 'num_samples'))

        

        ############################## TLP-C SIGNALS ##############################        
        self.ui.tlc_sampling_rate_minus.clicked.connect(lambda: self.adjust_value(self.ui.tlc_sampling_rate_input, -1, 'sampling_rate'))
        self.ui.tlc_sampling_rate_plus.clicked.connect(lambda: self.adjust_value(self.ui.tlc_sampling_rate_input, +1, 'sampling_rate'))

        self.ui.tlc_up_amp_bias_minus.clicked.connect(lambda: self.adjust_value(self.ui.tlc_up_amp_bias_input, -1, 'up_amp_bias'))
        self.ui.tlc_up_amp_bias_plus.clicked.connect(lambda: self.adjust_value(self.ui.tlc_up_amp_bias_input, +1, 'up_amp_bias'))

        self.ui.tlc_down_amp_bias_minus.clicked.connect(lambda: self.adjust_value(self.ui.tlc_down_amp_bias_input, -1, 'down_amp_bias'))
        self.ui.tlc_down_amp_bias_plus.clicked.connect(lambda: self.adjust_value(self.ui.tlc_down_amp_bias_input, +1, 'down_amp_bias'))

        self.ui.tlc_avg_window_minus.clicked.connect(lambda: self.adjust_value(self.ui.tlc_avg_window_input, -1,'num_samples'))
        self.ui.tlc_avg_window_plus.clicked.connect(lambda: self.adjust_value(self.ui.tlc_avg_window_input, +1,'num_samples'))

        ############################## TLP-V SIGNALS ##############################


        self.ui.tlv_sampling_rate_minus.clicked.connect(lambda: self.adjust_value(self.ui.tlv_sampling_rate_input, -1,'sampling_rate'))
        self.ui.tlv_sampling_rate_plus.clicked.connect(lambda: self.adjust_value(self.ui.tlv_sampling_rate_input, +1, 'sampling_rate'))

        self.ui.tlv_up_amp_bias_minus.clicked.connect(lambda: self.adjust_value(self.ui.tlv_up_amp_bias_input, -1, 'up_amp_bias'))
        self.ui.tlv_up_amp_bias_plus.clicked.connect(lambda: self.adjust_value(self.ui.tlv_up_amp_bias_input, +1, 'up_amp_bias'))

        self.ui.tlv_avg_window_minus.clicked.connect(lambda: self.adjust_value(self.ui.tlv_avg_window_input, -1,'num_samples'))
        self.ui.tlv_avg_window_plus.clicked.connect(lambda: self.adjust_value(self.ui.tlv_avg_window_input, +1,'num_samples'))

        

        ############################## IEA SIGNALS ##############################
        self.ui.iea_volt_ramp_min_minus.clicked.connect(lambda: self.adjust_value(self.ui.iea_volt_ramp_min_input, -1, 'sweep_min'))
        self.ui.iea_volt_ramp_min_plus.clicked.connect(lambda: self.adjust_value(self.ui.iea_volt_ramp_min_input, +1, 'sweep_min'))

        self.ui.iea_volt_ramp_max_minus.clicked.connect(lambda: self.adjust_value(self.ui.iea_volt_rampt_max_input, -1, 'sweep_max'))
        self.ui.iea_volt_ramp_max_plus.clicked.connect(lambda: self.adjust_value(self.ui.iea_volt_rampt_max_input, +1, 'sweep_max'))

        self.ui.iea_sampling_rate_minus.clicked.connect(lambda: self.adjust_value(self.ui.iea_sampling_rate_input, -1,'sampling_rate'))
        self.ui.iea_sampling_rate_plus.clicked.connect(lambda: self.adjust_value(self.ui.iea_sampling_rate_input, +1, 'sampling_rate'))

        self.ui.iea_num_measurements_minus.clicked.connect(lambda: self.adjust_value(self.ui.iea_num_measurements_input, -1,'num_samples'))
        self.ui.iea_num_measurements_plus.clicked.connect(lambda: self.adjust_value(self.ui.iea_num_measurements_input, +1,'num_samples'))

        self.ui.iea_rejector_mesh_bias_minus.clicked.connect(lambda: self.adjust_value(self.ui.iea_rejector_mesh_bias_input, -1, 'rejector_bias'))
        self.ui.iea_rejector_mesh_bias_plus.clicked.connect(lambda: self.adjust_value(self.ui.iea_rejector_mesh_bias_input, +1, 'rejector_bias'))
        
        # Connect Plus/Minus buttons for Collector Probe Bias
        self.ui.iea_collector_probe_minus.clicked.connect(lambda: self.adjust_value(self.ui.iea_collector_probe_input, -1, 'collector_bias'))
        self.ui.iea_collector_probe_plus.clicked.connect(lambda: self.adjust_value(self.ui.iea_collector_probe_input, +1, 'collector_bias'))
        
        ############################## HEA SIGNALS ##############################
        self.ui.hea_volt_ramp_min_minus.clicked.connect(lambda: self.adjust_value(self.ui.hea_volt_ramp_min_input, -1, 'sweep_min'))
        self.ui.hea_volt_ramp_min_plus.clicked.connect(lambda: self.adjust_value(self.ui.hea_volt_ramp_min_input, +1, 'sweep_min'))
        
        self.ui.hea_volt_ramp_max_minus.clicked.connect(lambda: self.adjust_value(self.ui.hea_volt_rampt_max_input, -1, 'sweep_max'))
        self.ui.hea_volt_ramp_max_plus.clicked.connect(lambda: self.adjust_value(self.ui.hea_volt_rampt_max_input, +1, 'sweep_max'))

        self.ui.hea_sampling_rate_minus.clicked.connect(lambda: self.adjust_value(self.ui.hea_sampling_rate_input, -1,'sampling_rate'))
        self.ui.hea_sampling_rate_plus.clicked.connect(lambda: self.adjust_value(self.ui.hea_sampling_rate_input, +1,'sampling_rate'))

        self.ui.hea_num_measurements_minus.clicked.connect(lambda: self.adjust_value(self.ui.hea_num_measurements_input, -1,'num_samples'))
        self.ui.hea_num_measurements_plus.clicked.connect(lambda: self.adjust_value(self.ui.hea_num_measurements_input, +1, 'num_samples'))

        self.ui.hea_faraday_cup_bias_minus.clicked.connect(lambda: self.adjust_value(self.ui.hea_faraday_cup_bias_input, -1,'collector_bias'))
        self.ui.hea_faraday_cup_bias_plus.clicked.connect(lambda: self.adjust_value(self.ui.hea_faraday_cup_bias_input, +1,'collector_bias'))
        
        self.ui.hea_collimator_bias_minus.clicked.connect(lambda: self.adjust_value(self.ui.hea_collimator_bias_input, -1,'rejector_bias'))
        self.ui.hea_collimator_bias_plus.clicked.connect(lambda: self.adjust_value(self.ui.hea_collimator_bias_input, +1,'rejector_bias'))


    ############################## GENERAL SLOTS ##############################
    
    def set_widget_values(self):
        
        """set_widget_values initializes the values demonstrated by the UI."""

        ################## SLP ##################

        self.ui.slp_volt_ramp_min_input.setValue(self.control.get_config('slp', 'sweep_min'))
        self.ui.slp_volt_rampt_max_input.setValue(self.control.get_config('slp', 'sweep_max'))
        self.ui.slp_sampling_rate_input.setValue(self.control.get_config('slp', 'sampling_rate'))
        self.ui.slp_num_measurements_input.setValue(self.control.get_config('slp', 'num_samples'))
        
        ################## DLP ##################

        self.ui.dlp_volt_ramp_min_input.setValue(self.control.get_config('dlp', 'sweep_min'))
        self.ui.dlp_volt_rampt_max_input.setValue(self.control.get_config('dlp', 'sweep_max'))
        self.ui.dlp_sampling_rate_input.setValue(self.control.get_config('dlp', 'sampling_rate'))
        self.ui.dlp_num_measurements_input.setValue(self.control.get_config('dlp', 'num_samples'))
        
        ################## TLC ##################

        self.ui.tlc_sampling_rate_input.setValue(self.control.get_config('tlc', 'sampling_rate'))
        self.ui.tlc_up_amp_bias_input.setValue(self.control.get_config('tlc', 'up_amp_bias'))
        self.ui.tlc_down_amp_bias_input.setValue(self.control.get_config('tlc', 'down_amp_bias'))
        self.ui.tlc_avg_window_input.setValue(self.control.get_config('tlc', 'num_samples'))

        ################## TLV ##################

        self.ui.tlv_sampling_rate_input.setValue(self.control.get_config('tlv', 'sampling_rate'))
        self.ui.tlv_up_amp_bias_input.setValue(self.control.get_config('tlv', 'up_amp_bias'))
        self.ui.tlv_avg_window_input.setValue(self.control.get_config('tlv', 'num_samples'))

        ################## IEA ##################

        self.ui.iea_volt_ramp_min_input.setValue(self.control.get_config('iea', 'sweep_min'))
        self.ui.iea_volt_rampt_max_input.setValue(self.control.get_config('iea', 'sweep_max'))
        self.ui.iea_sampling_rate_input.setValue(self.control.get_config('iea', 'sampling_rate'))
        self.ui.iea_num_measurements_input.setValue(self.control.get_config('iea', 'num_samples'))
        self.ui.iea_collector_probe_input.setValue(self.control.get_config('iea', 'collector_bias'))
        self.ui.iea_rejector_mesh_bias_input.setValue(self.control.get_config('iea', 'rejector_bias'))
        
        ################## HEA ##################

        self.ui.hea_volt_ramp_min_input.setValue(self.control.get_config('hea', 'sweep_min'))
        self.ui.hea_volt_rampt_max_input.setValue(self.control.get_config('hea', 'sweep_max'))
        self.ui.hea_sampling_rate_input.setValue(self.control.get_config('hea', 'sampling_rate'))
        self.ui.hea_num_measurements_input.setValue(self.control.get_config('hea', 'num_samples'))
        self.ui.hea_faraday_cup_bias_input.setValue(self.control.get_config('hea', 'collector_bias'))
        self.ui.hea_collimator_bias_input.setValue(self.control.get_config('hea', 'rejector_bias'))


    def initialize_view(self):
        
        """initialize_view selects the probe first in display (currently SLP)"""

        # Initialize the view to display the correct page based on QComboBox selection.
        # Get the current index of the probe_selection_cb combobox
        current_index = self.ui.probe_selection_cb.currentIndex()
        
        # Extracting the probe identifier for config file
        self.selected_probe = self.ui.probe_selection_cb.currentText()[-4:-1].lower()
        
        
        # Update the main view based on the current index
        self.update_main_view(current_index)
        

    def update_main_view(self, index):
        """
        Switch pages in the probe_config_view based on the current index of probe_selection_cb.
        """
        
        self.selected_probe = self.ui.probe_selection_cb.currentText()[-4:-1].lower()
        

        # Map the QComboBox index to the correct page in main_view
        if index == 0:
            self.ui.main_view.setCurrentWidget(self.ui.single_lang_probe)

        elif index == 1:
            self.ui.main_view.setCurrentWidget(self.ui.double_lang_probe)

        elif index == 2:
            self.ui.main_view.setCurrentWidget(self.ui.triple_lang_c_probe)

        elif index == 3:
            self.ui.main_view.setCurrentWidget(self.ui.triple_lang_v_probe)

        elif index == 4:
            self.ui.main_view.setCurrentWidget(self.ui.ion_energy_analyzer)
            
        elif index == 5:
            self.ui.main_view.setCurrentWidget(self.ui.hyper_energy_analyzer)
            

    def emit_switch_to_run_signal(self, run_window):
        
        """emit_switch_to_run_signal defines the logic executed when the continue button is clicked."""
        
        # Disables all interactables to prevent erros while system prepares for experiment run
        self.disable_all()

        # Get the selected probe from the QComboBox
        # Set the selected probe in the experiment run window
        self.control.set_config(self.selected_probe, 'probe_id', self.selected_probe)
        
        self.control.setup_experiment(self.selected_probe)
        
        # Emit the signal to switch to the experiment run window
        self.switch_to_run.emit()
        self.run_window_ref.set_selected_probe(self.selected_probe)
        
        # Restores all interactables as enables
        self.enable_all()

        
       
    def emit_switch_to_settings_signal(self):
        
        """emit_switch_to_settings_signal defines the logic executed when the settings button is clicked."""
        
        # Emit the signal to switch to the user settings window
        self.switch_to_settings.emit() 


    def reset_setup(self):
        
        """reset_setup defines the logic executed when the reset button is clicked."""

        self.display_alert_message("Resetting Values")
        # Receiving original config values
        self.control.load_config_file()
        # Reset values from config file
        self.set_widget_values()

    ############################## Other Functions ##############################

    def adjust_value(self, spinbox, direction, config_key):
        """
        Adjust the value of a QDoubleSpinBox.
        
        :param spinbox: The QDoubleSpinBox to update.
        :param direction: 1 for increment, -1 for decrement.
        """
        
        current_value = spinbox.value()
        new_value = self.increment(current_value) if direction == 1 else self.decrement(current_value)
        
        if 'bias' in config_key and abs(new_value) < 0.01:
            new_value = current_value * -1 

        # Invoking mutator function of in memory config dictionary
        # Validations are also executed during the call stack of this method
        self.control.set_config(self.selected_probe, config_key, new_value)
        
        # If the result is valid, a new value is set in the spinbox
        # Otherwise, previous value set
        spinbox.setValue(self.control.get_config(self.selected_probe, config_key))

    def display_alert_message(self, message):
        """
        Display a message on alert_msg_label for 5 seconds, then clear the label.
        
        :param message: The message to display.
        """
        self.clear_alert_message()
        # Set the message in the alert_msg_label
        self.ui.alert_msg_label.setText(message)

        # Create a QTimer to clear the message after 5 seconds (5000 milliseconds)
        QTimer.singleShot(5000, lambda: self.clear_alert_message())

    def clear_alert_message(self):
        """clear_alert_message clears the message displayed on alert_msg_label when executed."""
        self.ui.alert_msg_label.setText("")

    def disable_all(self):
        """disable_all disables all interaction in the main window."""
        self.setEnabled(False)

    def enable_all(self):
        """enable_all enables all interaction in the main window."""
        self.setEnabled(True)

    def increment(self, value):
        """increment function executed to adjust according to the button_adjust value in config"""
        return value + self.control.get_config(probe_id='',key='button_adjust')

    def decrement(self, value):
        """decrement function executed to adjust according to the button_adjust value in config"""
        return value - self.control.get_config(probe_id='',key='button_adjust')

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
