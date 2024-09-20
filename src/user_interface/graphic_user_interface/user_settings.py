from PyQt5.QtWidgets import QMainWindow, QDialog, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal
from virtual_keyboard import VirtualKeyboard
from pathlib import Path

class UserSettings(QMainWindow):
    close_signal = pyqtSignal() # Signal to notify GuiManager about the close request
    back_btn_clicked = pyqtSignal()  # Signal for when the back button is clicked

    def __init__(self, control):
        super().__init__()
        loadUi('../graphic_user_interface/user_settings.ui', self)  # Load the .ui file directly
        
        self.control = control
        # Hide the probe_selection_cb by default
        self.probe_selection_cb.setVisible(False)
        
        # Connect buttons to switch between pages
        self.data_upload_settings_btn.clicked.connect(self.show_data_upload_settings)
        self.probe_config_settings_btn.clicked.connect(self.probe_config_settings)

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
        self.credentials_path_btn.clicked.connect(lambda: self.open_file_dialog(self.credentials_path_input, 'credentials_path'))
        self.local_path_btn.clicked.connect(lambda: self.open_file_dialog(self.local_path_input, 'local_path'))

        ############################## PROBE CONFIG SETTINGS SIGNALS ##############################
        self.set_widget_values()

        # SLP

            # ... to do: Jahn

        self.slp_area_minus.clicked.connect(lambda: self.adjust_value(self.slp_area_input, -1, 'Probe area'))
        self.slp_area_plus.clicked.connect(lambda: self.adjust_value(self.slp_area_input, +1 , 'Probe area'))
        
        self.slp_dac_min_minus.clicked.connect(lambda: self.adjust_value(self.slp_dac_min_input, -1, 'dac_min'))
        self.slp_dac_min_plus.clicked.connect(lambda: self.adjust_value(self.slp_dac_min_input, +1, 'dac_min'))
        
        self.slp_dac_max_minus.clicked.connect(lambda: self.adjust_value(self.slp_dac_max_input, -1, 'dac_max'))
        self.slp_dac_max_plus.clicked.connect(lambda: self.adjust_value(self.slp_dac_max_input, +1, 'dac_max'))
        
        self.slp_sweep_min_minus.clicked.connect(lambda: self.adjust_value(self.slp_sweep_min_input, -1, 'sweep_amp_min'))
        self.slp_sweep_min_plus.clicked.connect(lambda: self.adjust_value(self.slp_sweep_min_input, +1, 'sweep_amp_min'))
        
        self.slp_sweep_max_minus.clicked.connect(lambda: self.adjust_value(self.slp_sweep_max_input, -1, 'sweep_amp_max'))
        self.slp_sweep_max_plus.clicked.connect(lambda: self.adjust_value(self.slp_sweep_max_input, +1, 'sweep_amp_max'))
        
        self.slp_collector_gain_minus.clicked.connect(lambda: self.adjust_value(self.slp_collector_gain_input, -1, 'collector_gain'))
        self.slp_collector_gain_plus.clicked.connect(lambda: self.adjust_value(self.slp_collector_gain_input, +1, 'collector_gain'))
        
        
        # DLP

            # ... to do: Jahn

        self.dlp_area_minus.clicked.connect(lambda: self.adjust_value(self.dlp_area_input, -1, 'Probe area'))
        self.dlp_area_plus.clicked.connect(lambda: self.adjust_value(self.dlp_area_input, +1, 'Probe area'))

        # TLC

            # ... to do: Jahn

        # TLC

            # ... to do: Jahn

        # IEA

            # ... to do: Jahn

        self.iea_area_minus.clicked.connect(lambda: self.adjust_value(self.iea_area_input, -1, 'Probe area'))
        self.iea_area_plus.clicked.connect(lambda: self.adjust_value(self.iea_area_input, +1, 'Probe area'))

        self.iea_mass_minus.clicked.connect(lambda: self.adjust_value(self.iea_mass_output, -1, 'Probe area'))
        self.iea_mass_plus.clicked.connect(lambda: self.adjust_value(self.iea_mass_output, +1, 'Probe area'))

        # HEA

            # ... to do: Jahn

        self.tlc_area_minus.clicked.connect(lambda: self.adjust_value(self.tlc_area_output, -1, 'Probe area'))
        self.tlc_area_plus.clicked.connect(lambda: self.adjust_value(self.tlc_area_output, +1, 'Probe area'))
        self.tlv_area_minus.clicked.connect(lambda: self.adjust_value(self.tlv_area_output, -1, 'Probe area'))
        self.tlv_area_plus.clicked.connect(lambda: self.adjust_value(self.tlv_area_output, +1, 'Probe area'))

        self.hea_area_minus.clicked.connect(lambda: self.adjust_value(self.hea_area_output, -1, 'Probe area'))
        self.hea_area_plus.clicked.connect(lambda: self.adjust_value(self.hea_area_output, +1, 'Probe area'))

    def set_widget_values(self):
        
        self.credentials_path_input.setText(self.control.get_config(probe_id = '', key = 'credentials_path'))
        self.local_path_input.setText(self.control.get_config(probe_id = '', key = 'local_path'))

        
        self.slp_area_input.setValue(self.control.get_config('slp', 'Probe area'))
        self.slp_dac_min_input.setValue(self.control.get_config('slp', 'dac_min'))
        self.slp_dac_max_input.setValue(self.control.get_config('slp', 'dac_max'))
        
        self.slp_sweep_min_input.setValue(self.control.get_config('slp', 'sweep_amp_min'))

        self.slp_sweep_max_input.setValue(self.control.get_config('slp', 'sweep_amp_max'))


        self.slp_collector_gain_input.setValue(self.control.get_config('slp', 'collector_gain'))

    def show_data_upload_settings(self):
        self.main_view.setCurrentWidget(self.data_upload_settings_page)
        self.probe_selection_cb.setVisible(False)  # Hide the combobox when switching away

    def probe_config_settings(self):
        
        self.main_view.setCurrentWidget(self.probe_config_settings_page)
        self.probe_selection_cb.setVisible(True)  # Hide the combobox when switching away
        self.selected_probe = self.probe_selection_cb.currentText()[-4:-1].lower()

    def switch_probe_page(self, index):
        """
        Switch pages in the probe_config_view based on the current index of probe_selection_cb.
        """
        self.selected_probe = self.probe_selection_cb.currentText()[-4:-1].lower()

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


            
    def open_file_dialog(self, line_edit, key):
            dialog = QFileDialog(self)
            dialog.setDirectory(r'C:/')
            if key =='credentials_path':
                dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
            else:
                dialog.setFileMode(QFileDialog.FileMode.Directory) 

            dialog.setViewMode(QFileDialog.ViewMode.List)
            if dialog.exec():
                filenames = dialog.selectedFiles()
                
                if filenames:
                    self.control.set_config(probe_id='', key=key, value = str(Path(filenames[0])))
                    line_edit.setText(self.control.get_config(probe_id='',key=key))
                    
    def adjust_value(self, spinbox, direction, config_key):
        """
        Adjust the value of a QDoubleSpinBox.
        
        :param spinbox: The QDoubleSpinBox to update.
        :param direction: 1 for increment, -1 for decrement.
        """
        
        current_value = spinbox.value()
        new_value = self.increment_last_decimal(current_value) if direction == 1 else self.decrement_last_decimal(current_value)

        # Invoking mutator function of in memory config dictionary
        # Validations are also executed during the call stack of this method
        self.control.set_config(self.selected_probe, config_key, new_value)
        
        # If the result is valid, a new value is set in the spinbox
        # Otherwise, previous value set
        spinbox.setValue(self.control.get_config(self.selected_probe, config_key))


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
        
        self.control.save_config_file()

    def closeEvent(self, event):
        # Emit the signal to notify GuiManager about the close request
        self.close_signal.emit()
        event.ignore()  # Ignore the default close event; GuiManager will handle it
