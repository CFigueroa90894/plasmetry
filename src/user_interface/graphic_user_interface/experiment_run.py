from PyQt5.QtWidgets import QMainWindow, QLabel, QDoubleSpinBox, QFrame, QVBoxLayout, QLineEdit
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal, QTimer
from run_parameters import RunParameters

class ExperimentRun(QMainWindow):
    close_signal = pyqtSignal()  # Signal to notify GuiManager about the close request
    back_btn_clicked = pyqtSignal()  # Signal for when the back button is clicked
    run_btn_clicked = pyqtSignal()
    stop_btn_clicked = pyqtSignal()

    def __init__(self, control):
        super().__init__()
        self.control = control
        self.running = False
        
        loadUi('../graphic_user_interface/experiment_run.ui', self)  # Load the .ui file directly
        
        # Connect buttons to emit signals
        self.back_btn.clicked.connect(self.emit_back_signal)
        self.run_btn.clicked.connect(self.emit_run_signal)
        self.stop_btn.clicked.connect(self.emit_stop_signal)
        
        self.timer = QTimer() 
        self.timer.timeout.connect(self.update_parameters)
        self.parameters = self.control.get_real_time_container()[0]
        

    def set_selected_probe(self, probe):
        params_dictionaries = RunParameters()
        params = params_dictionaries.get_parameters_for_probe(probe)
        
        print(f"Parameters for {probe}: {params}")  # Debug statement
        
        if params:
            self.load_probe_calculations(params)
            print(f"Selected probe for experiment run: {probe}")  # Debug statement
        else:
            print(f"No parameters found for probe: {probe}")

    def start_timer(self):
        self.timer.start(1000)

    def stop_timer(self):
        self.timer.stop()

    def load_probe_calculations(self, parameters):
        """Load and display calculations for the selected probe."""
        if parameters:
            print('Loading calculations...')
            
            self.keys = list(parameters.keys())
            half = (len(self.keys )) // 2  # Divide roughly in half
            
            # Clear existing layouts before adding new widgets
            self.clear_layout(self.frame_left.layout())
            self.clear_layout(self.frame_right.layout())

            # Add widgets to the left frame
            for key in self.keys[:half]:
                print(parameters[key])
                self.add_calculation_to_frame(self.frame_left.layout(), key, parameters[key])

            # Add widgets to the right frame
            for key in self.keys[half:]:
                print(parameters[key])
                self.add_calculation_to_frame(self.frame_right.layout(), key, parameters[key])
                
            print("Calculations loaded into frames.")
        else:
            print('No parameters provided.')

    def add_calculation_to_frame(self, layout, param_name, param_value):
        
        """Add a parameter's calculation display to a specified layout."""
        
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
        label.setStyleSheet("font-size: 14px; font-weight: bold;")
        vertical_layout.addWidget(label)

        # Create a QLineEdit for the parameter value as a non-editable field
        line_edit = QLineEdit()
        line_edit.setMinimumSize(300, 35)
        line_edit.setMaximumSize(300, 35)
        line_edit.setStyleSheet("background-color: #FFFFFF; font-size: 20px;")
        line_edit.setReadOnly(True)  # Make it read-only to prevent editing
        line_edit.setText(str(param_value))  # Set the line edit value as text
        vertical_layout.addWidget(line_edit)

        # Add the frame to the given layout
        layout.addWidget(param_frame)
        
    def update_parameters(self):
        
        parameter_values = self.parameters
        print(parameter_values)
        for i in range(self.frame_left.layout().count()):
            items = self.frame_left.layout().itemAt(i)
            if items is not None:
               parameters = items.widget()
               if isinstance(parameters, QLineEdit):
                   parameters.setText(str(parameter_values.pop(0)))
                   parameter_values.pop()
        print(f'\n\n\n\n\n adoadokdoao \n\n\n\n\n {parameter_values}')
        for i in range(self.frame_right.layout().count()):
            items = self.frame_right.layout().itemAt(i)
            if items is not None:
               parameters = items.widget()
               if isinstance(parameters, QLineEdit):
                   parameters.setText(str(parameter_values.pop(0)))
                   
             
               
        
    def clear_layout(self, layout):
        """Helper method to clear all widgets from a layout."""
        
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def emit_back_signal(self):
        """Emit signal when back button is clicked."""
        
        if self.running:
            self.control.stop_experiment()
            self.stop_timer()
            
        self.back_btn_clicked.emit()  # Emit back signal
        
    def emit_run_signal(self):
        """Emit signal when run button is clicked."""
        
        self.running = True
        
        self.control.start_experiment()
        self.start_timer()
        print("Experiment started.")
        
    def emit_stop_signal(self):
        """Emit signal when stop button is clicked."""
        
        if self.running:
            self.control.stop_experiment()
            self.stop_timer() 
            
            print("Experiment stopped.")