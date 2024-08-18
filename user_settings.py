from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal

class UserSettings(QMainWindow):
    back_btn_clicked = pyqtSignal()  # Signal for when the back button is clicked

    def __init__(self):
        super().__init__()
        loadUi('user_settings.ui', self)  # Load the .ui file directly

        # Connect the back button to emit the signal
        self.back_btn.clicked.connect(self.emit_back_signal)

        # Connect the reset button to reset settings to default
        self.reset_btn.clicked.connect(self.reset_settings)

        # Connect the save button to save changes made to settings
        self.save_btn.clicked.connect(self.save_settings)

        # Connect the QComboBox signal to the method that updates the QStackedWidget
        self.probe_selection_cb.currentIndexChanged.connect(self.update_main_view)

    def update_main_view(self, index):
         # Update the QStackedWidget based on the selected index in the QComboBox
        self.main_view.setCurrentIndex(index)

    def emit_back_signal(self):
        self.back_btn_clicked.emit() 

    def reset_settings(self):
        print("Reset button clicked...waiting for implementation")

    def save_settings(self):
        print("Save button clicked...waiting for implementation")
