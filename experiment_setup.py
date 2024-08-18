import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolButton, QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal, QRect
from numerical_keypad import NumericalKeypad 

class ExperimentSetup(QMainWindow):
    switch_to_run = pyqtSignal()  # Signal to switch to the experiment run window
    switch_to_settings = pyqtSignal()  # Signal to switch to the user settings window

    def __init__(self):
        super().__init__()
        loadUi('experiment_setup.ui', self)  # Load the .ui file directly

        # Add overlay buttons for each QDoubleSpinBox
        self.add_tool_buttons()

        # Connect the continue button to switch to the experiment run window
        self.continue_btn.clicked.connect(self.emit_switch_to_run_signal)

        # Connect the view settings button to switch to the user settings window
        self.view_settings_btn.clicked.connect(self.emit_switch_to_settings_signal)

        # Connect the QComboBox signal to the method that updates the QStackedWidget
        self.probe_selection_cb.currentIndexChanged.connect(self.update_main_view)

        # Connect the reset button to reset settings to default
        self.reset_btn.clicked.connect(self.reset_setup)

    def add_tool_buttons(self):
        # Target QDoubleSpinBoxes and add a tool button to each
        spinboxes = [
            self.slp_sweep_adjustment_min_input,
            self.slp_sweep_adjustment_max_input,
            self.slp_sample_sweep_input,
            self.slp_time_sweep_input,
        ]

        for spinbox in spinboxes:
            tool_button = QToolButton(self)
            tool_button.setText("...")
            tool_button.setFixedSize(40, spinbox.height())
            tool_button.clicked.connect(lambda _, s=spinbox: self.open_keypad_dialog(s))
            tool_button.setStyleSheet("background-color: #DDDDDD; border: none;")  # Adjust the style as needed

            # Calculate the position of the button relative to the spinbox
            spinbox_geometry = spinbox.geometry()
            x_pos = spinbox_geometry.right() - tool_button.width()
            y_pos = spinbox_geometry.top() + (spinbox_geometry.height() - tool_button.height()) // 2

            # Position the button
            tool_button.setParent(spinbox.parentWidget())
            tool_button.setGeometry(QRect(x_pos, y_pos, tool_button.width(), tool_button.height()))
            tool_button.raise_()  # Ensure the button appears above the spinbox

    def open_keypad_dialog(self, spinbox):
        keypad = NumericalKeypad(self)
        if keypad.exec_() == QDialog.Accepted:
            spinbox.setValue(keypad.get_value())

    def emit_switch_to_run_signal(self):
        self.switch_to_run.emit()  # Emit the signal to switch to the experiment run window

    def emit_switch_to_settings_signal(self):
        self.switch_to_settings.emit()  # Emit the signal to switch to the user settings window

    def update_main_view(self, index):
        # Update the QStackedWidget based on the selected index in the QComboBox
        self.main_view.setCurrentIndex(index)

    def reset_setup(self):
        print("Reset button clicked...waiting for implementation")


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
