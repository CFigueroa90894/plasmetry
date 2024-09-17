from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal
from virtual_keyboard import VirtualKeyboard

class UserSettings(QMainWindow):
    back_btn_clicked = pyqtSignal()  # Signal for when the back button is clicked

    def __init__(self):
        super().__init__()
        loadUi('user_settings.ui', self)  # Load the .ui file directly

        # Hide the probe_selection_cb by default
        self.probe_selection_cb.setVisible(False)

        # Connect buttons to switch between pages
        self.data_upload_settings_btn.clicked.connect(self.show_data_upload_settings)
        self.probe_config_settings_btn.clicked.connect(self.probe_config_settings)
        self.plasma_param_settings_btn.clicked.connect(self.show_plasma_param_settings)

        # Connect QComboBox selection change to change pages in the probe_config_view
        self.probe_selection_cb.currentIndexChanged.connect(self.switch_probe_page)

        # Connect the back button to emit the signal
        self.back_btn.clicked.connect(self.handle_back_button)

        # Connect the reset button to reset settings to default
        self.reset_btn.clicked.connect(self.reset_settings)

        # Connect the save button to save changes made to settings
        self.save_btn.clicked.connect(self.save_settings)

        ############################## DATA UPLOAD SIGNALS ##############################

        # Connect QToolButton clicks to open the virtual keyboard
        self.bucket_name_btn.clicked.connect(lambda: self.open_keyboard(self.bucket_name_output))
        self.access_key_id_btn.clicked.connect(lambda: self.open_keyboard(self.access_key_id_output))
        self.secret_access_key_btn.clicked.connect(lambda: self.open_keyboard(self.secret_access_key_output))

        ############################## PROBE CONFIG SETTINGS SIGNALS ##############################

        # Connect Plus/Minus buttons for Min Voltage Ramp
        self.slp_area_minus_btn.clicked.connect(lambda: self.adjust_value(self.slp_area_output, -1))
        self.slp_area_plus_btn.clicked.connect(lambda: self.adjust_value(self.slp_area_output, +1))

        # Connect Plus/Minus buttons for Min Voltage Ramp
        self.dlp_area_minus_btn.clicked.connect(lambda: self.adjust_value(self.dlp_area_output, -1))
        self.dlp_area_btn.clicked.connect(lambda: self.adjust_value(self.dlp_area_output, +1))

        # Connect Plus/Minus buttons for Min Voltage Ramp
        self.iea_area_minus_btn.clicked.connect(lambda: self.adjust_value(self.iea_area_output, -1))
        self.iea_area_plus_btn.clicked.connect(lambda: self.adjust_value(self.iea_area_output, +1))

        # Connect Plus/Minus buttons for Min Voltage Ramp
        self.iea_mass_minus_btn.clicked.connect(lambda: self.adjust_value(self.iea_mass_output, -1))
        self.iea_mass_plus_btn.clicked.connect(lambda: self.adjust_value(self.iea_mass_output, +1))

        # Connect Plus/Minus buttons for Min Voltage Ramp
        self.tlp_area_minus_btn.clicked.connect(lambda: self.adjust_value(self.tlp_area_output, -1))
        self.tlp_area_plus_btn.clicked.connect(lambda: self.adjust_value(self.tlp_area_output, +1))

        # Connect Plus/Minus buttons for Min Voltage Ramp
        self.hea_area_minus_btn.clicked.connect(lambda: self.adjust_value(self.hea_area_output, -1))
        self.hea_area_plus_btn.clicked.connect(lambda: self.adjust_value(self.hea_area_output, +1))

        ############################## PLASMA PARAMETER SETTINGS SIGNALS ##############################


    def show_data_upload_settings(self):
        self.main_view.setCurrentWidget(self.data_upload_settings_page)
        self.probe_selection_cb.setVisible(False)  # Hide the combobox when switching away

    def probe_config_settings(self):
        self.main_view.setCurrentWidget(self.probe_config_settings_page)
        self.probe_selection_cb.setVisible(True)  # Hide the combobox when switching away

    def show_plasma_param_settings(self):
        self.main_view.setCurrentWidget(self.plasma_param_settings_page)
        self.probe_selection_cb.setVisible(False)  # Hide the combobox when switching away

    def switch_probe_page(self, index):
        """
        Switch pages in the probe_config_view based on the current index of probe_selection_cb.
        """
        # Map the QComboBox index to the correct page in probe_config_view
        if index == 0:
            self.probe_config_view.setCurrentWidget(self.single_lang_probe)
        elif index == 1:
            self.probe_config_view.setCurrentWidget(self.double_lang_probe)
        elif index == 2:
            self.probe_config_view.setCurrentWidget(self.triple_lang_c_probe)
        elif index == 3:
            self.probe_config_view.setCurrentWidget(self.triple_lang_v_probe)
        elif index == 4:
            self.probe_config_view.setCurrentWidget(self.ion_energy_analyzer)
        elif index == 5:
            self.probe_config_view.setCurrentWidget(self.hyper_energy_analyzer)

    def open_keyboard(self, line_edit):
        keyboard = VirtualKeyboard(self)
        
        # Show the keyboard dialog
        if keyboard.exec_() == QDialog.Accepted:
            # Get the input text and set it in the line edit
            input_text = keyboard.get_input_text()
            line_edit.setText(input_text)

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

    def handle_back_button(self):
        # Check if the current page is not the settings_select_page
        if self.main_view.currentWidget() != self.settings_select_page:
            # Jump to the settings_select_page
            self.main_view.setCurrentWidget(self.settings_select_page)
            self.probe_selection_cb.setVisible(False)  # Hide the combobox when switching away
        else:
            # If already on settings_select_page, emit the back button signal
            self.emit_back_signal()

    def emit_back_signal(self):
        self.back_btn_clicked.emit() 

    def reset_settings(self):
        print("Reset button clicked...waiting for implementation")

    def save_settings(self):
        print("Save button clicked...waiting for implementation")
