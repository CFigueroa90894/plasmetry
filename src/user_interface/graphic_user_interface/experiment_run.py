from PyQt5.QtWidgets import QMainWindow, QLabel, QDoubleSpinBox, QFrame, QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal
from sys_control_mockup import SystemControlMockup

class ExperimentRun(QMainWindow):
    close_signal = pyqtSignal() # Signal to notify GuiManager about the close request
    back_btn_clicked = pyqtSignal()  # Signal for when the back button is clicked
    run_btn_clicked = pyqtSignal()
    stop_btn_clicked = pyqtSignal()
    def __init__(self, control):
        super().__init__()
        self.control = control
        
        loadUi('../graphic_user_interface/experiment_run.ui', self)  # Load the .ui file directly
        # Attribute to store the selected probe
        self.selected_probe = None

        # Connect the back button to emit the signal
        self.back_btn.clicked.connect(self.emit_back_signal)
        
        self.run_btn.clicked.connect(self.emit_run_signal)
        
        self.stop_btn.clicked.connect(self.emit_stop_signal)

    def set_selected_probe(self, probe):
        self.selected_probe = probe
        print(f"Selected probe for experiment run: {self.selected_probe}")  # Debug statement

        # Get the calculations for the selected probe
        self.load_probe_calculations(self.selected_probe)

    def load_probe_calculations(self, probe_name):
        
        # Get parameters for the selected probe from sys_control_mockup
        parameters = SystemControlMockup().get_parameters_for_probe(probe_name)
        
        if parameters:
            # Divide the calculations between frame_left and frame_right
            param_items = list(parameters.items())[:10]  # Only take the first 10 calculations if more
            half = (len(param_items) + 1) // 2  # Divide roughly in half

            # Clear the layouts before adding new widgets
          #  self.clear_layout(self.frame_left.layout())
           # self.clear_layout(self.frame_right.layout())

            # Add widgets to the left frame
            for param, value in param_items[:half]:
                self.add_calculation_to_frame(self.frame_left.layout(), param, value)

            # Add widgets to the right frame
            for param, value in param_items[half:]:
                self.add_calculation_to_frame(self.frame_right.layout(), param, value)
        else:
            print(f"No parameters found for probe: {probe_name}")

    def add_calculation_to_frame(self, layout, param_name, param_value):
        # Create a frame for the parameter
        param_frame = QFrame()
        param_frame.setMinimumSize(400, 66)
        param_frame.setMaximumSize(400, 66)
        
        # Create a vertical layout for the frame
        vertical_layout = QVBoxLayout(param_frame)
        vertical_layout.setContentsMargins(0, 0, 0, 0)

        # Create a label for the parameter name
        label = QLabel(param_name)
        label.setMaximumSize(1000, 25)
        label.setStyleSheet("font-size: 20px; font-weight: bold;")
        vertical_layout.addWidget(label)

        # Create a QDoubleSpinBox for the parameter value
        spin_box = QDoubleSpinBox()
        spin_box.setMinimumSize(300, 35)
        spin_box.setMaximumSize(300, 35)
        spin_box.setStyleSheet("background-color: #FFFFFF; font-size: 20px;")
        spin_box.setButtonSymbols(QDoubleSpinBox.NoButtons)
        spin_box.setReadOnly(True)
        spin_box.setDecimals(3)  # Set decimals to 3 for better precision
        spin_box.setMinimum(-1e10)
        spin_box.setMaximum(1e10)
        spin_box.setValue(param_value)  # Set the spin box value
        vertical_layout.addWidget(spin_box)

        # Add the frame to the given layout
        layout.addWidget(param_frame)

    def clear_layout(self, layout):
        # Helper method to clear all widgets from a layout
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def emit_back_signal(self):
        self.back_btn_clicked.emit()  # Emit the signal when the back button is clicked
        
    def emit_run_signal(self):
        self.control.start_experiment()
        
    def emit_stop_signal(self):
        self.control.stop_experiment()
