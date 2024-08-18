from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal

class ExperimentRun(QMainWindow):
    back_btn_clicked = pyqtSignal()  # Signal for when the back button is clicked

    def __init__(self):
        super().__init__()
        loadUi('experiment_run.ui', self)  # Load the .ui file directly

        # Connect the back button to emit the signal
        self.back_btn.clicked.connect(self.emit_back_signal)

    def emit_back_signal(self):
        self.back_btn_clicked.emit()  # Emit the signal when the back button is clicked
