import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal

class ExperimentSetup(QMainWindow):
    switch_to_run = pyqtSignal()  # Signal to switch to the experiment run window
    switch_to_settings = pyqtSignal()  # Signal to switch to the user settings window

    def __init__(self):
        super().__init__()
        loadUi('experiment_setup.ui', self)  # Load the .ui file directly

        ############################## GENERAL SIGNALS ##############################

        # Connect the continue button to switch to the experiment run window
        self.continue_btn.clicked.connect(self.emit_switch_to_run_signal)

        # Connect the view settings button to switch to the user settings window
        self.view_settings_btn.clicked.connect(self.emit_switch_to_settings_signal)

        # Connect the QComboBox signal to the method that updates the QStackedWidget
        self.probe_selection_cb.currentIndexChanged.connect(self.update_main_view)

        # Connect the reset button to reset settings to default
        self.reset_btn.clicked.connect(self.reset_setup)

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

        self.tlp_c_up_collector_gain_minus.clicked.connect(lambda: self.adjust_value(self.tlp_c_up_collector_gain_input, -1))
        self.tlp_c_up_collector_gain_plus.clicked.connect(lambda: self.adjust_value(self.tlp_c_up_collector_gain_input, +1))

        self.tlp_c_up_amp_bias_minus.clicked.connect(lambda: self.adjust_value(self.tlp_c_up_amp_bias_input, -1))
        self.tlp_c_up_amp_bias_plus.clicked.connect(lambda: self.adjust_value(self.tlp_c_up_amp_bias_input, +1))

        self.tlp_c_low_collect_gain_minus.clicked.connect(lambda: self.adjust_value(self.tlp_c_low_collect_gain_input, -1))
        self.tlp_c_low_collect_gain_plus.clicked.connect(lambda: self.adjust_value(self.tlp_c_low_collect_gain_input, +1))

        self.tlp_c_low_amp_bias_minus.clicked.connect(lambda: self.adjust_value(self.tlp_c_low_amp_bias_input, -1))
        self.tlp_c_low_amp_bias_plus.clicked.connect(lambda: self.adjust_value(self.tlp_c_low_amp_bias_input, +1))

        ############################## TLP-V SIGNALS ##############################

        self.tlp_v_sampling_rate_minus.clicked.connect(lambda: self.adjust_value(self.tlp_v_sampling_rate_input, -1))
        self.tlp_v_sampling_rate_plus.clicked.connect(lambda: self.adjust_value(self.tlp_v_sampling_rate_input, +1))

        self.tlp_v_up_collector_gain_minus.clicked.connect(lambda: self.adjust_value(self.tlp_c_up_collector_gain_input, -1))
        self.tlp_v_up_collector_gain_plus.clicked.connect(lambda: self.adjust_value(self.tlp_c_up_collector_gain_input, +1))

        self.tlp_v_up_amp_bias_minus.clicked.connect(lambda: self.adjust_value(self.tlp_c_up_amp_bias_input, -1))
        self.tlp_v_up_amp_bias_plus.clicked.connect(lambda: self.adjust_value(self.tlp_c_up_amp_bias_input, +1))

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

    def update_main_view(self, index):
        # Update the QStackedWidget based on the selected index in the QComboBox
        self.main_view.setCurrentIndex(index)

    def reset_setup(self):
        print("Reset button clicked...waiting for implementation")

    # ############################## SLP SLOTS ##############################

    # def decrease_slp_volt_ramp_max(self):
    #     current_value = self.slp_volt_rampt_max_input.value()
    #     new_value = self.decrement_last_decimal(current_value)
    #     self.slp_volt_rampt_max_input.setValue(new_value)

    # def increase_slp_volt_ramp_max(self):
    #     current_value = self.slp_volt_rampt_max_input.value()
    #     new_value = self.increment_last_decimal(current_value)
    #     self.slp_volt_rampt_max_input.setValue(new_value)

    # def decrease_slp_volt_ramp_min(self):
    #     current_value = self.slp_volt_ramp_min_input.value()
    #     new_value = self.decrement_last_decimal(current_value)
    #     self.slp_volt_ramp_min_input.setValue(new_value)

    # def increase_slp_volt_ramp_min(self):
    #     current_value = self.slp_volt_ramp_min_input.value()
    #     new_value = self.increment_last_decimal(current_value)
    #     self.slp_volt_ramp_min_input.setValue(new_value)

    # def decrease_slp_sampling_rate(self):
    #     current_value = self.slp_sampling_rate_input.value()
    #     new_value = self.decrement_last_decimal(current_value)
    #     self.slp_sampling_rate_input.setValue(new_value)

    # def increase_slp_sampling_rate(self):
    #     current_value = self.slp_sampling_rate_input.value()
    #     new_value = self.increment_last_decimal(current_value)
    #     self.slp_sampling_rate_input.setValue(new_value)

    # def decrease_slp_num_measurements(self):
    #     current_value = self.slp_num_measurements_input.value()
    #     new_value = self.decrement_last_decimal(current_value)
    #     self.slp_num_measurements_input.setValue(new_value)

    # def increase_slp_num_measurements(self):
    #     current_value = self.slp_num_measurements_input.value()
    #     new_value = self.increment_last_decimal(current_value)
    #     self.slp_num_measurements_input.setValue(new_value)

    # ############################## DLP SLOTS ##############################

    # def decrease_dlp_volt_ramp_max(self):
    #     current_value = self.dlp_volt_rampt_max_input.value()
    #     new_value = self.decrement_last_decimal(current_value)
    #     self.dlp_volt_rampt_max_input.setValue(new_value)

    # def increase_dlp_volt_ramp_max(self):
    #     current_value = self.dlp_volt_rampt_max_input.value()
    #     new_value = self.increment_last_decimal(current_value)
    #     self.dlp_volt_rampt_max_input.setValue(new_value)

    # def decrease_dlp_volt_ramp_min(self):
    #     current_value = self.dlp_volt_ramp_min_input.value()
    #     new_value = self.decrement_last_decimal(current_value)
    #     self.dlp_volt_ramp_min_input.setValue(new_value)

    # def increase_dlp_volt_ramp_min(self):
    #     current_value = self.dlp_volt_ramp_min_input.value()
    #     new_value = self.increment_last_decimal(current_value)
    #     self.dlp_volt_ramp_min_input.setValue(new_value)

    # def decrease_dlp_sampling_rate(self):
    #     current_value = self.dlp_sampling_rate_input.value()
    #     new_value = self.decrement_last_decimal(current_value)
    #     self.dlp_sampling_rate_input.setValue(new_value)

    # def increase_dlp_sampling_rate(self):
    #     current_value = self.dlp_sampling_rate_input.value()
    #     new_value = self.increment_last_decimal(current_value)
    #     self.dlp_sampling_rate_input.setValue(new_value)

    # def decrease_dlp_num_measurements(self):
    #     current_value = self.dlp_num_measurements_input.value()
    #     new_value = self.decrement_last_decimal(current_value)
    #     self.dlp_num_measurements_input.setValue(new_value)

    # def increase_dlp_num_measurements(self):
    #     current_value = self.dlp_num_measurements_input.value()
    #     new_value = self.increment_last_decimal(current_value)
    #     self.dlp_num_measurements_input.setValue(new_value)


    ############################## TLP SLOTS ##############################



    ############################## IEA SLOTS ##############################

    ############################## HEA SLOTS ##############################

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