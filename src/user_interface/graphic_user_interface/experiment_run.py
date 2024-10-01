""" G3 - Plasma Devs
Layer 4 - User Interface - Experiment Run
    <...>

author: <-------------------------
author: <-------------------------

status: DONE

Classes:
    ExperimentRun

"""
# built-in imports
from pathlib import Path

# third-party imports
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QFrame, QVBoxLayout, QFileDialog
from PyQt5.QtCore import pyqtSignal, QTimer

# local imports
from run_parameters import RunParameters
from experiment_run_ui import Ui_experiment_run_view


class ExperimentRun(QMainWindow):
    """ExperimentRun is defined to interface with the ui components shown after the user
    clicks the'continue' button.
    
    Attributes:
        + close_signal: Class attribute
        + back_btn_clicked: Class attribute
        + run_btn_clicked: Class attribute
        + stop_btn_clicked: Class attribute
        + control
        + running
        + display_container
        + ran
        + ui
        + container
        + params_container
        + params_flag
        + selected_probe
        + keys

    Methods:
        + __init__()
        + initialize_experiment_name_view()
        + showEvent()
        + show_exp_path_name_frame()
        + switch_to_run_page()
        + handle_page_switch()
        + set_selected_probe()
        + start_timer()
        + stop_timer()
        + load_probe_calculations()
        + add_calculation_to_frame()
        + updated_parameters()
        + clear_layout()
        + update_run_status()
        + display_alert_message()
        + clear_alert_message()
        + emit_back_signal()
        + emit_run_signal()
        + emit_stop_signal()
        + open_file_dialog()

    """
    close_signal = pyqtSignal()  # Signal to notify GuiManager about the close request
    back_btn_clicked = pyqtSignal()  # Signal for when the back button is clicked
    run_btn_clicked = pyqtSignal()
    stop_btn_clicked = pyqtSignal()

    def __init__(self, control):
        
        """ExperimentRun constructor, initializes subcomponents."""
        
        super().__init__()
        
        # Storing control object reference
        self.control = control
        
        # Storing boolean value for logic
        self.running = False
        
        
        # Used to verify if an experiment has ran previously
        self.ran = False
        
        # Storing ui view
        self.ui = Ui_experiment_run_view() 
        
        # Invoking the setupUi function, setting up the visual components
        self.ui.setupUi(self) 

        # Disable stop_btn and enable run_btn initially
        self.ui.stop_btn.setEnabled(False)
        self.ui.run_btn.setEnabled(True)

        # Connect buttons to emit signals
        self.ui.back_btn.clicked.connect(self.emit_back_signal)
        self.ui.run_btn.clicked.connect(self.emit_run_signal)
        self.ui.stop_btn.clicked.connect(self.emit_stop_signal)

        # Sets the run_status_label to default stop color 
        self.update_run_status(0)

        # Initialize a timer for updating parameters
        self.ui.timer = QTimer()
        self.ui.timer.timeout.connect(self.update_parameters)
        

        self.container = self.control.get_real_time_container()
        self.params_container = self.container[0]
        self.params_flag = self.container[1]
        # Set up the page switching logic
        self.ui.main_view.currentChanged.connect(self.handle_page_switch)

        # Ensure window starts on experiment_name
        self.ui.main_view.setCurrentIndex(0)
        self.handle_page_switch()

        # Connect the query buttons in experiment_name page
        self.ui.query_no_btn.clicked.connect(self.show_exp_path_name_frame)
        self.ui.query_yes_btn.clicked.connect(self.switch_to_run_page)

        # Connect confirm button in exp_path_name_frame
        self.ui.confirm_to_run_btn.clicked.connect(self.switch_to_run_page)
        self.ui.exp_path_name_btn.clicked.connect(lambda: self.open_file_dialog(self.ui.exp_path_name_input))
        self.ui.default_exp_path_name_label.setText(Path(self.control.get_config(probe_id='', key='experiment_name')).name)
        
        
        
    def initialize_experiment_name_view(self):
        """Shows the query frame by default when switching to experiment_name page."""
        self.ui.default_exp_path_name_label.setText(Path(self.control.get_config(probe_id='', key='experiment_name')).name)
        self.ui.exp_path_name_query_frame.setVisible(True)
        self.ui.exp_path_name_frame.setVisible(False)

    def showEvent(self, event):
        """Called every time the window is shown. Reset the view to experiment_name page."""
        super().showEvent(event)
        
        # Set the current page to experiment_name (index 0)
        self.ui.main_view.setCurrentIndex(0)
        
        # Ensure buttons are correctly hidden or shown
        self.handle_page_switch()

    def show_exp_path_name_frame(self):
        """Shows exp_path_name_frame and hides exp_path_name_query_frame."""
        self.ui.exp_path_name_input.setText(Path(self.control.get_config(probe_id='', key='experiment_name')).name)
        self.ui.exp_path_name_query_frame.setVisible(False)
        self.ui.exp_path_name_frame.setVisible(True)

    def switch_to_run_page(self):
        """Switches to the run_page when the user confirms or clicks yes."""
        self.control.save_config_file()
        self.ui.main_view.setCurrentIndex(1)  # Assuming run_page is at index 1

    def handle_page_switch(self):
        """Handles hiding/showing buttons and initializing frames based on page switch."""
        current_index = self.ui.main_view.currentIndex()

        # Assuming experiment_name is at index 0 and run_page is at index 1
        if current_index == 0:  # Experiment Name page
            self.ui.run_btn.setVisible(False)
            self.ui.stop_btn.setVisible(False)
            self.initialize_experiment_name_view()

        elif current_index == 1:  # Run Page
            self.ui.run_btn.setVisible(True)
            self.ui.stop_btn.setVisible(True)

    def set_selected_probe(self, probe):
        
        """set_selected_probe loads the information of the parameters used for display"""
        self.selected_probe = probe
        params_lists = RunParameters()
        params = params_lists.get_parameters_for_probe(probe)


        if params:
            self.load_probe_calculations(params)
        else:
            print(f"No parameters found for probe: {probe}")

    def start_timer(self):
        """Start the timer to update parameters every second."""
        self.ui.timer.start(1000)  # Update every second

    def stop_timer(self):
        """Stop the timer."""
        self.ui.timer.stop()

    def load_probe_calculations(self, parameters):
        """Load and display calculations for the selected probe."""
        if parameters:
            print('Loading calculations...')

            self.keys = parameters
            half = (len(self.keys)) // 2  # Divide roughly in half

            # Clear existing layouts before adding new widgets
            self.clear_layout(self.ui.frame_left.layout())
            self.clear_layout(self.ui.frame_right.layout())

            # Add widgets to the left frame
            for key in self.keys[:half]:
                self.add_calculation_to_frame(
                    self.ui.frame_left.layout(), key)

            # Add widgets to the right frame
            for key in self.keys[half:]:
                self.add_calculation_to_frame(
                    self.ui.frame_right.layout(), key)

        else:
            print('No parameters provided.')

    def add_calculation_to_frame(self, layout, param_name):
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
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        vertical_layout.addWidget(label)

        # Create a QLineEdit for the parameter value as a non-editable field
        line_edit = QLineEdit()
        line_edit.setMinimumSize(300, 35)
        line_edit.setMaximumSize(300, 35)
        line_edit.setStyleSheet("background-color: #FFFFFF; font-size: 20px;")
        line_edit.setReadOnly(True)  # Make it read-only to prevent editing
        line_edit.setText(str(0.0))  # Set the line edit value as text
        vertical_layout.addWidget(line_edit)

        # Add the frame to the given layout
        layout.addWidget(param_frame)
        
    def update_parameters(self):
        
        """update_parameters updates the currently shown parameters with new ones."""
        
        # Verifying if new parameters, if so, rewriting the display_container object
        if self.params_flag.is_set():
            parameter_values = self.params_container.copy()
            self.params_flag.clear()
        
            
            # Going through each widget in the frame_left and identifying the Qline edits for rewrite
            for i in range(self.ui.frame_left.layout().count()):
                item = self.ui.frame_left.layout().itemAt(i)
                if item:
                    widget = item.widget()
                    if isinstance(widget, QFrame):
                        for j in range(widget.layout().count()):
                            inner_item = widget.layout().itemAt(j)
                            inner_widget = inner_item.widget()
                            if isinstance(inner_widget, QLineEdit):
                                if parameter_values:
                                    # Pop operation performed on the list, poping the first value
                                    new_value = str(parameter_values.pop(0))
                                    # Writing the new value
                                    inner_widget.setText(new_value)
                                    
            # Going through each widget in the frame_right and identifying the Qline edits for rewrite
            for i in range(self.ui.frame_right.layout().count()):
                item = self.ui.frame_right.layout().itemAt(i)
                if item:
                    widget = item.widget()
                    if isinstance(widget, QFrame):
                        for j in range(widget.layout().count()):
                            inner_item = widget.layout().itemAt(j)
                            inner_widget = inner_item.widget()
                            if isinstance(inner_widget, QLineEdit):
                                if parameter_values:
                                    # Pop operation performed on the list, poping the first value
                                    new_value = str(parameter_values.pop(0))
                                    # Writing the new value
                                    inner_widget.setText(new_value)
            

    def clear_layout(self, layout):
        """Helper method to clear all widgets from a layout."""
        
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def update_run_status(self, status):
        """
        Update the background color of the run_status_label based on the experiment status.
        
        :param status: 0 for stopped, 1 for paused, 2 for running
        """
        # Define color mappings for each status
        color_map = {
            0: "#F33A3A",  # Fully stopped
            1: "#FFBF00",  # Paused
            2: "#61F65D"   # Running
        }

        # Modify only the background-color part of the stylesheet
        new_stylesheet = f"""
        border: 4px solid black;
        border-radius: 30px;
        background-color: {color_map[status]};
        """

        # Set the new stylesheet for the label
        self.ui.run_status_label.setStyleSheet(new_stylesheet)

    def display_alert_message(self, message):
        """
        Display a message on alert_msg_label for 5 seconds, then clear the label.
        
        :param message: The message to display.
        """
        self.clear_alert_message()
        # Set the message in the alert_msg_label
        self.ui.alert_msg_label.setText(message)

        # Create a QTimer to clear the message after 5 seconds (5000 milliseconds)
        QTimer.singleShot(5000, lambda: self.clear_alert_message())

    def clear_alert_message(self):
        """
        Clear the message displayed on alert_msg_label.
        """
        self.ui.alert_msg_label.setText("")

    def emit_back_signal(self):
        """Emit signal when back button is clicked."""
        
        if self.running:
            self.running = False
            self.control.stop_experiment()
            self.stop_timer()

        self.ran = False
        self.back_btn_clicked.emit()  # Emit back signal
        

    def emit_run_signal(self):
        """Emit signal when run button is clicked."""
        
        if not self.running:  # Ensure it only triggers if not already running
        
            if self.ran:
                self.control.setup_experiment(self.selected_probe)
                
            self.running = True
            
            # Disable run_btn to prevent double clicking
            self.ui.run_btn.setEnabled(False)

            # Disable back_btn to prevent error in experiment run
            self.ui.back_btn.setEnabled(False)
            
            # Enable stop_btn to allow stopping the experiment
            self.ui.stop_btn.setEnabled(True)

            # Start the experiment and timer
            self.control.start_experiment()
            self.start_timer()
            self.ran = True

        # Setting the run_status_label to running
        self.update_run_status(2)
        self.display_alert_message("Experiment started")
        
    def open_file_dialog(self, line_edit):
        """open_file_dialog opens a file dialog for folder path identification."""
        # Storing the file dialog object
        dialog = QFileDialog(self)
        
        # Setting the initial directory as the root
        dialog.setDirectory(r'C:/')
        
        # Setting the mode fo the dialog to directory, only accepting directories.
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        
        # Listing the directories
        dialog.setViewMode(QFileDialog.ViewMode.List)
        
        # Selection completed logic
        if dialog.exec():
            # Storing the selected directories
            filenames = dialog.selectedFiles()
            
            # If a folder was selected, setting new path and experiment name 
            if filenames:
                self.control.set_config(probe_id='', key='local_path', value=str(Path(filenames[0])))                
                self.control.set_config(probe_id='', key='experiment_name', value=Path(filenames[0]).name)
                # Writing the new folder name
                line_edit.setText(Path(self.control.get_config(probe_id='', key='local_path')).name)


    def emit_stop_signal(self):
         """Emit signal when stop button is clicked."""
         if self.running:
            self.display_alert_message("Stopping experiment...")

            # Disable stop_btn 
            self.ui.stop_btn.setEnabled(False)
            # Re-enable run_btn & back_btn
            self.ui.run_btn.setEnabled(True)
            self.ui.back_btn.setEnabled(True)

            # Stop the experiment and timer
            self.control.stop_experiment()
            self.stop_timer()

            # Setting the run_status_label to stopped
            self.update_run_status(0)

            self.display_alert_message("Experiment stopped")
            self.running = False
