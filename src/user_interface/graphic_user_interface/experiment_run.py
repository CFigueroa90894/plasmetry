from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QFrame, QVBoxLayout
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

        # Load the .ui file directly
        loadUi('../graphic_user_interface/experiment_run.ui', self)

        # Connect buttons to emit signals
        self.back_btn.clicked.connect(self.emit_back_signal)
        self.run_btn.clicked.connect(self.emit_run_signal)
        self.stop_btn.clicked.connect(self.emit_stop_signal)

        # Initialize a timer for updating parameters
        self.timer = QTimer()
        self.counter = 1
        self.timer.timeout.connect(self.update_parameters)
        
        self.params_container = self.control.get_real_time_container()[0]
        
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
        """Start the timer to update parameters every second."""
        print("Starting timer...")
        self.timer.start(1000)  # Update every second

    def stop_timer(self):
        """Stop the timer."""
        print("Stopping timer...")
        self.timer.stop()

    def load_probe_calculations(self, parameters):
        """Load and display calculations for the selected probe."""
        if parameters:
            print('Loading calculations...')

            self.keys = list(parameters.keys())
            half = (len(self.keys)) // 2  # Divide roughly in half

            # Clear existing layouts before adding new widgets
            self.clear_layout(self.frame_left.layout())
            self.clear_layout(self.frame_right.layout())

            # Add widgets to the left frame
            for key in self.keys[:half]:
                print(f"Adding {key}: {parameters[key]}")  # Debug statement
                self.add_calculation_to_frame(
                    self.frame_left.layout(), key, parameters[key])

            # Add widgets to the right frame
            for key in self.keys[half:]:
                print(f"Adding {key}: {parameters[key]}")  # Debug statement
                self.add_calculation_to_frame(
                    self.frame_right.layout(), key, parameters[key])

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
        print('updating parameters...')
        
       # parameter_values = self.params_container
       
        parameter_values = [i * self.counter for i in range(10)]
       
        self.counter = self.counter + 5
        
        for i in range(self.frame_left.layout().count()):
            item = self.frame_left.layout().itemAt(i)
            if item:
                widget = item.widget()
                if isinstance(widget, QFrame):
                    for j in range(widget.layout().count()):
                        inner_item = widget.layout().itemAt(j)
                        inner_widget = inner_item.widget()
                        if isinstance(inner_widget, QLineEdit):
                            if parameter_values:
                                new_value = str(parameter_values.pop(0))
                                inner_widget.setText(new_value)
            
        for i in range(self.frame_right.layout().count()):
            item = self.frame_right.layout().itemAt(i)
            if item:
                widget = item.widget()
                if isinstance(widget, QFrame):
                    for j in range(widget.layout().count()):
                        inner_item = widget.layout().itemAt(j)
                        inner_widget = inner_item.widget()
                        if isinstance(inner_widget, QLineEdit):
                            if parameter_values:
                                new_value = str(parameter_values.pop(0))
                                inner_widget.setText(new_value)
            

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