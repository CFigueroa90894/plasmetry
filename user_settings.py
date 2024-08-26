from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal
import sys_control_mockup

class UserSettings(QMainWindow):
    back_btn_clicked = pyqtSignal()  # Signal for when the back button is clicked

    def __init__(self):
        super().__init__()
        loadUi('user_settings.ui', self)  # Load the .ui file directly

        # Initialize an instance of SystemControlMockup
        self.sys_control = sys_control_mockup.SystemControlMockup()

        # Extract probe parameters from sys_control_mockup
        self.probe_parameters = self.sys_control.probe_parameters

        # Initialize attributes
        self.current_probe = self.probe_selection_cb.currentText()
        self.current_param_index = 0
        self.param_keys = list(self.probe_parameters[self.current_probe].keys())

        # Connect the back button to emit the signal
        self.back_btn.clicked.connect(self.emit_back_signal)

        # Connect the reset button to reset settings to default
        self.reset_btn.clicked.connect(self.reset_settings)

        # Connect the save button to save changes made to settings
        self.save_btn.clicked.connect(self.save_settings)

        self.probe_selection_cb.currentIndexChanged.connect(self.update_main_view)

        # Connect the previous parameter button ("<-") 
        self.previous_param_btn.clicked.connect(self.view_previous_param)

        # Connect the next parameter button ("->") 
        self.next_param_btn.clicked.connect(self.view_next_param)

        # Initial UI setup
        self.update_main_view()

    def update_main_view(self, index=0):
        # Get the selected probe and its parameters
        self.current_probe = self.probe_selection_cb.currentText()
        self.param_keys = list(self.probe_parameters[self.current_probe].keys())
        total_params = len(self.param_keys)

        if total_params > 0:
            # Update parameter count label
            self.param_count.setText(f"{self.current_param_index + 1}/{total_params}")

            # Update the title of the QGroupBox to display the current parameter name
            current_param_key = self.param_keys[self.current_param_index]
            self.param_edit_frame.setTitle(current_param_key)

            # Display the current parameter value in the QDoubleSpinBox
            current_param_value = self.probe_parameters[self.current_probe][current_param_key]
            self.param_input.setValue(current_param_value)

            # Update button states
            self.previous_param_btn.setEnabled(self.current_param_index > 0)
            self.next_param_btn.setEnabled(self.current_param_index < total_params - 1)
        else:
            self.param_count.setText("0/0")
            self.param_edit_frame.setTitle("N/A")
            self.alert_msg_label.setText("No Parameters")
            self.param_input.setValue(0.0)
            self.previous_param_btn.setEnabled(False)
            self.next_param_btn.setEnabled(False)

    def view_previous_param(self):
        if self.current_param_index > 0:
            self.current_param_index -= 1
            self.update_main_view()

    def view_next_param(self):
        if self.current_param_index < len(self.param_keys) - 1:
            self.current_param_index += 1
            self.update_main_view()

    def emit_back_signal(self):
        self.back_btn_clicked.emit() 

    def reset_settings(self):
        print("Reset button clicked...waiting for implementation")

    def save_settings(self):
        print("Save button clicked...waiting for implementation")
