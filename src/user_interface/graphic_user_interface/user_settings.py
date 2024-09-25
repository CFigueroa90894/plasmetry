from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSignal, QTimer
from virtual_keyboard import VirtualKeyboard
from pathlib import Path
from user_settings_ui import Ui_user_settings_view


class UserSettings(QMainWindow):
    close_signal = pyqtSignal()  # Signal to notify GuiManager about the close request
    back_btn_clicked = pyqtSignal()  # Signal for when the back button is clicked

    def __init__(self, control, setup_window):
        super().__init__()
   
        self.setup_window = setup_window
        self.control = control
        self.ui = Ui_user_settings_view() 
        self.ui.setupUi(self) 
        
        # Hide the probe_selection_cb by default
        self.ui.cb_handler.setVisible(False)

        # Connect buttons to switch between pages
        self.ui.data_upload_settings_btn.clicked.connect(
            self.show_data_upload_settings)
        self.ui.probe_config_settings_btn.clicked.connect(
            self.probe_config_settings)

        # Connect QComboBox selection change to change pages in the probe_config_view
        self.ui.probe_selection_cb.currentIndexChanged.connect(
            self.switch_probe_page)

        # Set up the page switching logic
        self.ui.main_view.currentChanged.connect(self.handle_page_switch)

        # Ensure window starts on experiment_name
        self.ui.main_view.setCurrentIndex(0)
        self.handle_page_switch()

        # Connect left and right buttons to change pages
        self.ui.page_left_btn.clicked.connect(self.go_to_previous_page)
        self.ui.page_right_btn.clicked.connect(self.go_to_next_page)

        # Connect the back button to emit the signal
        self.ui.back_btn.clicked.connect(self.handle_back_button)

        # Connect the reset button to reset settings to default
        self.ui.reset_btn.clicked.connect(self.reset_settings)

        # Connect the save button to save changes made to settings
        self.ui.save_btn.clicked.connect(self.save_settings)

        ############################## DATA UPLOAD SIGNALS ##############################

        # Connect QToolButton clicks to open the virtual keyboard
        self.ui.credentials_path_btn.clicked.connect(lambda: self.open_file_dialog(
            self.ui.credentials_path_input, 'credentials_path'))
        self.ui.local_path_btn.clicked.connect(
            lambda: self.open_file_dialog(self.ui.local_path_input, 'local_path'))
    

        ############################## PROBE CONFIG SETTINGS SIGNALS ##############################
        self.set_widget_values()
        self.ui.gas_select_cb.currentIndexChanged.connect(lambda: self.set_selected_gas(self.ui.gas_select_cb.currentText()))
        
        self.ui.button_adjust_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.button_adjust_input, -1, 'button_adjust'))
        
        self.ui.button_adjust_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.button_adjust_input, +1,'button_adjust'))    
        
        self.selected_probe = self.ui.probe_selection_cb.currentText()[-4:-1].lower()

        ################## SLP ##################
        self.ui.slp_area_units_cb.currentIndexChanged.connect(lambda: self.set_area_units('slp', self.ui.slp_area_units_cb))
            

        # Connect Plus/Minus buttons for Area
        self.ui.slp_area_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.slp_area_input, -1, {"area_units":"display_value"}))
        self.ui.slp_area_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.slp_area_input, +1, {"area_units":"display_value"}))

        # Connect Plus/Minus buttons for DAC MIN
        self.ui.slp_dac_min_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.slp_dac_min_input, -1, 'dac_min'))
        self.ui.slp_dac_min_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.slp_dac_min_input, +1, 'dac_min'))

        # Connect Plus/Minus buttons for DAC MAX
        self.ui.slp_dac_max_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.slp_dac_max_input, -1, 'dac_max'))
        self.ui.slp_dac_max_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.slp_dac_max_input, +1, 'dac_max'))

        # Connect Plus/Minus buttons for Sweep MIN
        self.ui.slp_sweep_min_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.slp_sweep_min_input, -1, 'sweep_amp_min'))
        self.ui.slp_sweep_min_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.slp_sweep_min_input, +1, 'sweep_amp_min'))

        # Connect Plus/Minus buttons for Sweep Max
        self.ui.slp_sweep_max_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.slp_sweep_max_input, -1, 'sweep_amp_max'))
        self.ui.slp_sweep_max_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.slp_sweep_max_input, +1, 'sweep_amp_max'))

        # Connect Plus/Minus buttons for Collector Gain
        self.ui.slp_collector_gain_minus.clicked.connect(lambda: self.adjust_value(
            self.ui.slp_collector_gain_input, -1, 'collector_gain'))
        self.ui.slp_collector_gain_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.slp_collector_gain_input, +1, 'collector_gain'))

        # Connect Plus/Minus buttons for Collector Shunt Resistance
        self.ui.slp_collector_shunt_rest_minus.clicked.connect(lambda: self.adjust_value(
            self.ui.slp_collector_shunt_rest_input, -1, 'sweeper_shunt'))
        self.ui.slp_collector_shunt_rest_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.slp_collector_shunt_rest_input, +1, 'sweeper_shunt'))

        ################## DLP ##################
        self.ui.dlp_area_units_cb.currentIndexChanged.connect(lambda: self.set_area_units('dlp', self.ui.dlp_area_units_cb))

        # Connect Plus/Minus buttons for Area
        self.ui.dlp_area_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.dlp_area_input, -1, {"area_units":"display_value"}))
        self.ui.dlp_area_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.dlp_area_input, +1, {"area_units":"display_value"}))
        

        # Connect Plus/Minus buttons for DAC MIN
        self.ui.dlp_dac_min_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.dlp_dac_min_input, -1, 'dac_min'))
        self.ui.dlp_dac_min_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.dlp_dac_min_input, +1, 'dac_min'))

        # Connect Plus/Minus buttons for DAC MAX
        self.ui.dlp_dac_max_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.dlp_dac_max_input, -1, 'dac_max'))
        self.ui.dlp_dac_max_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.dlp_dac_max_input, +1, 'dac_max'))

        # Connect Plus/Minus buttons for Sweep MIN
        self.ui.dlp_sweep_min_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.dlp_sweep_min_input, -1, 'sweep_amp_min'))
        self.ui.dlp_sweep_min_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.dlp_sweep_min_input, +1, 'sweep_amp_min'))

        # Connect Plus/Minus buttons for Sweep MAX
        self.ui.dlp_sweep_max_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.dlp_sweep_max_input, -1, 'sweep_amp_max'))
        self.ui.dlp_sweep_max_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.dlp_sweep_max_input, +1, 'sweep_amp_max'))

        # Connect Plus/Minus buttons for Collector Gain
        self.ui.dlp_collector_gain_minus.clicked.connect(lambda: self.adjust_value(
            self.ui.dlp_collector_gain_input, -1, 'collector_gain'))
        self.ui.dlp_collector_gain_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.dlp_collector_gain_input, +1, 'collector_gain'))

        # Connect Plus/Minus buttons for Collector Shunt Resistance
        self.ui.dlp_collector_shunt_rest_minus.clicked.connect(lambda: self.adjust_value(
            self.ui.dlp_collector_shunt_rest_input, -1, 'sweeper_shunt'))
        self.ui.dlp_collector_shunt_rest_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.dlp_collector_shunt_rest_input, +1, 'sweeper_shunt'))

        ################## TLC ##################
        self.ui.tlc_area_units_cb.currentIndexChanged.connect(lambda: self.set_area_units('tlc', self.ui.tlc_area_units_cb))
        
        # Connect Plus/Minus buttons for DAC MIN
        self.ui.tlc_dac_min_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlc_dac_min_input, -1, 'dac_min'))
        self.ui.tlc_dac_min_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlc_dac_min_input, +1, 'dac_min'))

        # Connect Plus/Minus buttons for DAC MAX
        self.ui.tlc_dac_max_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlc_dac_max_input, -1, 'dac_max'))
        self.ui.tlc_dac_max_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlc_dac_max_input, +1, 'dac_max'))

        # Connect Plus/Minus buttons for Up Amp MIN
        self.ui.tlc_up_amp_min_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlc_up_amp_min_input, -1, 'up_amp_min'))
        self.ui.tlc_up_amp_min_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlc_up_amp_min_input, +1, 'up_amp_min'))

        # Connect Plus/Minus buttons for Up Amp MAX
        self.ui.tlc_up_amp_max_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlc_up_amp_max_input, -1, 'up_amp_max'))
        self.ui.tlc_up_amp_max_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlc_up_amp_max_input, +1, 'up_amp_max'))

        # Connect Plus/Minus buttons for Down Amp MIN
        self.ui.tlc_down_amp_min_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlc_down_amp_min_input, -1, 'down_amp_min'))
        self.ui.tlc_down_amp_min_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlc_down_amp_min_input, +1, 'down_amp_min'))

        # Connect Plus/Minus buttons for Down Amp MAX
        self.ui.tlc_down_amp_max_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlc_down_amp_max_input, -1, 'down_amp_max'))
        self.ui.tlc_down_amp_max_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlc_down_amp_max_input, +1, 'down_amp_max'))

        # Connect Plus/Minus buttons for Area
        self.ui.tlc_area_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlc_area_input, -1, {"area_units":"display_value"}))
        self.ui.tlc_area_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlc_area_input, +1, {"area_units":"display_value"}))


        # Connect Plus/Minus buttons for Up Collector Gain
        self.ui.tlc_up_collector_gain_minus.clicked.connect(lambda: self.adjust_value(
            self.ui.tlc_up_collector_gain_input, -1, 'up_collector_gain'))
        self.ui.tlc_up_collector_gain_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.tlc_up_collector_gain_input, +1, 'up_collector_gain'))

        # Connect Plus/Minus buttons for Down Collector Gain
        self.ui.tlc_down_collect_gain_minus.clicked.connect(lambda: self.adjust_value(
            self.ui.tlc_down_collect_gain_input, -1, 'down_collector_gain'))
        self.ui.tlc_down_collect_gain_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.tlc_down_collect_gain_input, +1, 'down_collector_gain'))

        # Connect Plus/Minus buttons for Up Collector Shunt Resistance
        self.ui.tlc_up_shunt_rest_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlc_up_shunt_rest_input, -1, 'up_shunt'))
        self.ui.tlc_up_shunt_rest_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlc_up_shunt_rest_input, +1, 'up_shunt'))

        # Connect Plus/Minus buttons for Down Collector Shunt Resistance
        self.ui.tlc_down_shunt_rest_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlc_down_shunt_rest_input, -1, 'down_shunt'))
        self.ui.tlc_down_shunt_rest_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlc_down_shunt_rest_input, +1, 'down_shunt'))

        ################## TLV ##################
        
        self.ui.tlv_area_units_cb.currentIndexChanged.connect(lambda: self.set_area_units('tlv', self.ui.tlv_area_units_cb))

        # Connect Plus/Minus buttons for DAC MIN
        self.ui.tlv_dac_min_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlv_dac_min_input, -1, 'dac_min'))
        self.ui.tlv_dac_min_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlv_dac_min_input, +1, 'dac_min'))

        # Connect Plus/Minus buttons for DAC MAX
        self.ui.tlv_dac_max_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlv_dac_max_input, -1, 'dac_max'))
        self.ui.tlv_dac_max_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlv_dac_max_input, +1, 'dac_max'))

        # Connect Plus/Minus buttons for Up Amp MIN
        self.ui.tlv_up_amp_min_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlv_up_amp_min_input, -1, 'up_amp_min'))
        self.ui.tlv_up_amp_min_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlv_up_amp_min_input, +1, 'up_amp_min'))

        # Connect Plus/Minus buttons for Up Amp MAX
        self.ui.tlv_up_amp_max_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlv_up_amp_max_input, -1, 'up_amp_max'))
        self.ui.tlv_up_amp_max_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlv_up_amp_max_input, +1, 'up_amp_max'))

        # Connect Plus/Minus buttons for Area
        self.ui.tlv_area_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlv_area_input, -1, {"area_units":"display_value"}))
        self.ui.tlv_area_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlv_area_input, +1, {"area_units":"display_value"}))


        # Connect Plus/Minus buttons for Float Collector Gain
        self.ui.tlv_float_collect_gain_minus.clicked.connect(lambda: self.adjust_value(
            self.ui.tlv_float_collect_gain_input, -1, 'float_collector_gain'))
        self.ui.tlv_float_collect_gain_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.tlv_float_collect_gain_input, +1, 'float_collector_gain'))

        # Connect Plus/Minus buttons for Up Collector Gain
        self.ui.tlv_up_collector_gain_minus.clicked.connect(lambda: self.adjust_value(
            self.ui.tlv_up_collector_gain_input, -1, 'up_collector_gain'))
        self.ui.tlv_up_collector_gain_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.tlv_up_collector_gain_input, +1, 'up_collector_gain'))

        # Connect Plus/Minus buttons for Up Collector Shunt Resistance
        self.ui.tlv_up_shunt_rest_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlv_up_shunt_rest_input, -1, 'up_shunt'))
        self.ui.tlv_up_shunt_rest_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.tlv_up_shunt_rest_input, +1, 'up_shunt'))

        ################## IEA ##################
        self.ui.iea_area_units_cb.currentIndexChanged.connect(lambda: self.set_area_units('iea', self.ui.iea_area_units_cb))


        # Connect Plus/Minus buttons for DAC MIN
        self.ui.iea_dac_min_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.iea_dac_min_input, -1, 'dac_min'))
        self.ui.iea_dac_min_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.iea_dac_min_input, +1, 'dac_min'))

        # Connect Plus/Minus buttons for DAC MAX
        self.ui.iea_dac_max_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.iea_dac_max_input, -1, 'dac_max'))
        self.ui.iea_dac_max_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.iea_dac_max_input, +1, 'dac_max'))

        # Connect Plus/Minus buttons for Rejector MIN
        self.ui.iea_reject_min_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.iea_reject_min_input, -1, 'rejector_min'))
        self.ui.iea_reject_min_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.iea_reject_min_input, +1, 'rejector_min'))

        # Connect Plus/Minus buttons for Rejector MAX
        self.ui.iea_reject_max_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.iea_reject_max_input, -1, 'rejector_max'))
        self.ui.iea_reject_max_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.iea_reject_max_input, +1, 'rejector_max'))

        # Connect Plus/Minus buttons for Collector Bias MIN
        self.ui.iea_collect_bias_min_minus.clicked.connect(lambda: self.adjust_value(
            self.ui.iea_collect_bias_min_input, -1, 'collector_bias_min'))
        self.ui.iea_collect_bias_min_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.iea_collect_bias_min_input, +1, 'collector_bias_min'))

        # Connect Plus/Minus buttons for Collector Bias MAX
        self.ui.iea_collect_bias_max_minus.clicked.connect(lambda: self.adjust_value(
            self.ui.iea_collect_bias_max_input, -1, 'collector_bias_max'))
        self.ui.iea_collect_bias_max_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.iea_collect_bias_max_input, +1, 'collector_bias_max'))

        # Connect Plus/Minus buttons for Collector Gain
        self.ui.iea_collector_gain_minus.clicked.connect(lambda: self.adjust_value(
            self.ui.iea_collector_gain_input, -1, 'collector_gain'))
        self.ui.iea_collector_gain_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.iea_collector_gain_input, +1, 'collector_gain'))

        # Connect Plus/Minus buttons for Sweep MIN
        self.ui.iea_sweep_min_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.iea_sweep_min_input, -1, 'sweep_amp_min'))
        self.ui.iea_sweep_min_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.iea_sweep_min_input, +1, 'sweep_amp_min'))

        # Connect Plus/Minus buttons for Sweep MAX
        self.ui.iea_sweep_max_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.iea_sweep_max_input, -1, 'sweep_amp_max'))
        self.ui.iea_sweep_max_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.iea_sweep_max_input, +1, 'sweep_amp_max'))

        # Connect Plus/Minus buttons for Area
        self.ui.iea_area_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.iea_area_input, -1, {"area_units":"display_value"}))
        self.ui.iea_area_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.iea_area_input, +1, {"area_units":"display_value"}))
        
        # Connect Plus/Minus buttons for Collector Shunt Resistance
        self.ui.iea_collector_shunt_rest_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.iea_collector_shunt_rest_input, -1, 'sweeper_shunt'))
        self.ui.iea_collector_shunt_rest_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.iea_collector_shunt_rest_input, +1, 'sweeper_shunt'))

        ################## HEA ##################
        self.ui.hea_area_units_cb.currentIndexChanged.connect(lambda: self.set_area_units('hea', self.ui.hea_area_units_cb))


        # Connect Plus/Minus buttons for DAC MIN
        self.ui.hea_dac_min_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.hea_dac_min_input, -1, 'dac_min'))
        self.ui.hea_dac_min_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.hea_dac_min_input, +1, 'dac_min'))

        # Connect Plus/Minus buttons for DAC MAX
        self.ui.hea_dac_max_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.hea_dac_max_input, -1, 'dac_max'))
        self.ui.hea_dac_max_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.hea_dac_max_input, +1, 'dac_max'))

        # Connect Plus/Minus buttons for Collector Bias MIN
        self.ui.hea_collect_bias_min_minus.clicked.connect(lambda: self.adjust_value(
            self.ui.hea_collect_bias_min_input, -1, 'collector_bias_min'))
        self.ui.hea_collect_bias_min_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.hea_collect_bias_min_input, +1, 'collector_bias_min'))

        # Connect Plus/Minus buttons for Collector Bias MAX
        self.ui.hea_collect_bias_max_minus.clicked.connect(lambda: self.adjust_value(
            self.ui.hea_collect_bias_max_input, -1, 'collector_bias_max'))
        self.ui.hea_collect_bias_max_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.hea_collect_bias_max_input, +1, 'collector_bias_max'))
        
        # Connect Plus/Minus buttons for Collimator Bias min
        self.ui.hea_collimator_bias_min_minus.clicked.connect(lambda: self.adjust_value(
            self.ui.hea_collimator_bias_min_input, -1, 'rejector_min'))
        self.ui.hea_collimator_bias_min_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.hea_collimator_bias_min_input, +1, 'rejector_min'))
        
        # Connect Plus/Minus buttons for Collimator Bias MIN
        self.ui.hea_collimator_bias_max_minus.clicked.connect(lambda: self.adjust_value(
            self.ui.hea_collimator_bias_max_input, -1, 'rejector_max'))
        self.ui.hea_collimator_bias_max_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.hea_collimator_bias_max_input, +1, 'rejector_max'))
        

        # Connect Plus/Minus buttons for Sweep MIN
        self.ui.hea_sweep_min_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.hea_sweep_min_input, -1, 'sweep_amp_min'))
        self.ui.hea_sweep_min_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.hea_sweep_min_input, +1, 'sweep_amp_min'))

        # Connect Plus/Minus buttons for Sweep MAX
        self.ui.hea_sweep_max_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.hea_sweep_max_input, -1, 'sweep_amp_max'))
        self.ui.hea_sweep_max_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.hea_sweep_max_input, +1, 'sweep_amp_max'))

   

        # Connect Plus/Minus buttons for Collector Gain
        self.ui.hea_collect_gain_minus.clicked.connect(lambda: self.adjust_value(
            self.ui.hea_collect_gain_input, -1, 'collector_gain'))
        self.ui.hea_collect_gain_plus.clicked.connect(lambda: self.adjust_value(
            self.ui.hea_collect_gain_input, +1, 'collector_gain'))

        # Connect Plus/Minus buttons for Area
        self.ui.hea_area_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.hea_area_input, -1, {"area_units":"display_value"}))
        self.ui.hea_area_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.hea_area_input, +1, {"area_units":"display_value"}))


        # Connect Plus/Minus buttons for Collector Shunt Resistance
        self.ui.hea_collector_shunt_rest_minus.clicked.connect(
            lambda: self.adjust_value(self.ui.hea_collector_shunt_rest_input, -1, 'sweeper_shunt'))
        self.ui.hea_collector_shunt_rest_plus.clicked.connect(
            lambda: self.adjust_value(self.ui.hea_collector_shunt_rest_input, +1, 'sweeper_shunt'))

    def showEvent(self, event):
        """Called every time the window is shown. Reset the view to experiment_name page."""
        super().showEvent(event)

        # Set the current page to experiment_name (index 0)
        self.ui.main_view.setCurrentIndex(0)

        # Ensure buttons are correctly hidden or shown
        self.handle_page_switch()

    def handle_page_switch(self):
        """Handles hiding/showing buttons and initializing frames based on page switch."""
        self.ui.reset_btn.setVisible(True)
        self.ui.save_btn.setVisible(True)

    def set_widget_values(self):

        self.ui.credentials_path_input.setText(
            Path(self.control.get_config(probe_id='', key='credentials_path')).name)
        self.ui.local_path_input.setText(
            Path(self.control.get_config(probe_id='', key='experiment_name')).name)
        
        self.ui.button_adjust_input.setValue(
            self.control.get_config(probe_id='', key='button_adjust'))
        
        self.ui.gas_select_cb.setCurrentText(self.control.get_config(probe_id='', key='selected_gas'))
        
        
        ################## SLP ##################
         
        self.ui.slp_area_input.setValue(
            self.control.get_config('slp', {'area_units':'display_value'}))
        self.ui.slp_dac_min_input.setValue(
            self.control.get_config('slp', 'dac_min'))
        self.ui.slp_dac_max_input.setValue(
            self.control.get_config('slp', 'dac_max'))
        self.ui.slp_sweep_min_input.setValue(
            self.control.get_config('slp', 'sweep_amp_min'))
        self.ui.slp_sweep_max_input.setValue(
            self.control.get_config('slp', 'sweep_amp_max'))
        self.ui.slp_collector_gain_input.setValue(
            self.control.get_config('slp', 'collector_gain'))
        self.ui.slp_collector_shunt_rest_input.setValue(
            self.control.get_config('slp', 'sweeper_shunt'))
        self.ui.slp_area_units_cb.setCurrentText(self.control.get_config(probe_id='slp', key={'area_units':'unit'}))


        ################## SLP ##################

        self.ui.dlp_area_input.setValue(
            self.control.get_config('dlp', {'area_units':'display_value'}))
        self.ui.dlp_dac_min_input.setValue(
            self.control.get_config('dlp', 'dac_min'))
        self.ui.dlp_dac_max_input.setValue(
            self.control.get_config('dlp', 'dac_max'))
        self.ui.dlp_sweep_min_input.setValue(
            self.control.get_config('dlp', 'sweep_amp_min'))
        self.ui.dlp_sweep_max_input.setValue(
            self.control.get_config('dlp', 'sweep_amp_max'))
        self.ui.dlp_collector_gain_input.setValue(
            self.control.get_config('dlp', 'collector_gain'))
        self.ui.dlp_collector_shunt_rest_input.setValue(
            self.control.get_config('dlp', 'sweeper_shunt'))
        self.ui.dlp_area_units_cb.setCurrentText(self.control.get_config(probe_id='dlp', key={'area_units':'unit'}))

        ################## TLC ##################

        self.ui.tlc_area_input.setValue(
            self.control.get_config('tlc', {'area_units':'display_value'}))
        self.ui.tlc_dac_min_input.setValue(
            self.control.get_config('tlc', 'dac_min'))
        self.ui.tlc_dac_max_input.setValue(
            self.control.get_config('tlc', 'dac_max'))
        self.ui.tlc_up_amp_min_input.setValue(
            self.control.get_config('tlc', 'up_amp_min'))
        self.ui.tlc_up_amp_max_input.setValue(
            self.control.get_config('tlc', 'up_amp_max'))
        self.ui.tlc_down_amp_min_input.setValue(
            self.control.get_config('tlc', 'down_amp_min'))
        self.ui.tlc_down_amp_max_input.setValue(
            self.control.get_config('tlc', 'down_amp_max'))
        self.ui.tlc_up_collector_gain_input.setValue(
            self.control.get_config('tlc', 'up_collector_gain'))
        self.ui.tlc_down_collect_gain_input.setValue(
            self.control.get_config('tlc', 'down_collector_gain'))
        self.ui.tlc_up_shunt_rest_input.setValue(
            self.control.get_config('tlc', 'up_shunt'))
        self.ui.tlc_down_shunt_rest_input.setValue(
            self.control.get_config('tlc', 'down_shunt'))
        self.ui.tlc_area_units_cb.setCurrentText(self.control.get_config(probe_id='tlc', key={'area_units':'unit'}))


        ################## TLV ##################

        self.ui.tlv_area_input.setValue(
            self.control.get_config('tlv', {'area_units':'display_value'}))
        self.ui.tlv_dac_min_input.setValue(
            self.control.get_config('tlv', 'dac_min'))
        self.ui.tlv_dac_max_input.setValue(
            self.control.get_config('tlv', 'dac_max'))
        self.ui.tlv_up_amp_min_input.setValue(
            self.control.get_config('tlv', 'up_amp_min'))
        self.ui.tlv_up_amp_max_input.setValue(
            self.control.get_config('tlv', 'up_amp_max'))
        self.ui.tlv_float_collect_gain_input.setValue(
            self.control.get_config('tlv', 'float_collector_gain'))
        self.ui.tlv_up_collector_gain_input.setValue(
            self.control.get_config('tlv', 'up_collector_gain'))
        self.ui.tlv_up_shunt_rest_input.setValue(
            self.control.get_config('tlv', 'up_shunt'))
        self.ui.tlv_area_units_cb.setCurrentText(self.control.get_config(probe_id='tlv', key={'area_units':'unit'}))


        ################## IEA ##################
        

        self.ui.iea_area_input.setValue(
            self.control.get_config('iea', {'area_units':'display_value'}))
        self.ui.iea_dac_min_input.setValue(
            self.control.get_config('iea', 'dac_min'))
        self.ui.iea_dac_max_input.setValue(
            self.control.get_config('iea', 'dac_max'))
        self.ui.iea_reject_min_input.setValue(
            self.control.get_config('iea', 'rejector_min'))
        self.ui.iea_reject_max_input.setValue(
            self.control.get_config('iea', 'rejector_max'))
        self.ui.iea_collect_bias_min_input.setValue(
            self.control.get_config('iea', 'collector_bias_min'))
        self.ui.iea_collect_bias_max_input.setValue(
            self.control.get_config('iea', 'collector_bias_max'))
        self.ui.iea_collector_gain_input.setValue(
            self.control.get_config('iea', 'collector_gain'))
        self.ui.iea_sweep_min_input.setValue(
            self.control.get_config('iea', 'sweep_amp_min'))
        self.ui.iea_sweep_max_input.setValue(
            self.control.get_config('iea', 'sweep_amp_max'))
        self.ui.iea_collector_shunt_rest_input.setValue(
            self.control.get_config('iea', 'sweeper_shunt'))
        self.ui.iea_area_units_cb.setCurrentText(self.control.get_config(probe_id='iea', key={'area_units':'unit'}))


        ################## HEA ##################
        
        
        self.ui.hea_area_input.setValue(
            self.control.get_config('hea', {'area_units':'display_value'}))
        self.ui.hea_dac_min_input.setValue(
            self.control.get_config('hea', 'dac_min'))
        self.ui.hea_dac_max_input.setValue(
            self.control.get_config('hea', 'dac_max'))
        self.ui.hea_collimator_bias_min_input.setValue(
            self.control.get_config('hea', 'rejector_min'))
        self.ui.hea_collimator_bias_max_input.setValue(
            self.control.get_config('hea', 'rejector_max'))
        self.ui.hea_collect_bias_min_input.setValue(
            self.control.get_config('hea', 'collector_bias_min'))
        self.ui.hea_collect_bias_max_input.setValue(
            self.control.get_config('hea', 'collector_bias_max'))
        self.ui.hea_sweep_min_input.setValue(
            self.control.get_config('hea', 'sweep_amp_min'))
        self.ui.hea_sweep_max_input.setValue(
            self.control.get_config('hea', 'sweep_amp_max'))
        self.ui.hea_collect_gain_input.setValue(
            self.control.get_config('hea', 'collector_gain'))
        self.ui.hea_collect_gain_input.setValue(
            self.control.get_config('hea', 'collector_gain'))
        self.ui.hea_collector_shunt_rest_input.setValue(
            self.control.get_config('hea', 'sweeper_shunt'))
        self.ui.hea_area_units_cb.setCurrentText(self.control.get_config(probe_id='hea', key={'area_units':'unit'}))


    def show_data_upload_settings(self):
        self.ui.main_view.setCurrentWidget(self.ui.data_upload_settings_page)
        # Hide the combobox when switching away
        self.ui.cb_handler.setVisible(False)

    def probe_config_settings(self):
        # Switch to the probe config page
        self.ui.main_view.setCurrentWidget(self.ui.probe_config_settings_page)
        self.ui.cb_handler.setVisible(True)  # Show the probe selection combo box
        # Initialize the page view
        self.switch_probe_page(self.ui.probe_selection_cb.currentIndex())
        
    def set_selected_gas(self, current_gas):
        
        self.control.set_config(probe_id = '', key='selected_gas', value=current_gas.lower())
        
    def set_area_units(self, probe_id, combo_box):
         
        self.control.set_config(probe_id = probe_id, key={'area_units':'unit'}, value=combo_box.currentText())
        
    def switch_probe_page(self, index):
        """
        Switch pages in the probe_config_view based on the selected probe in the QComboBox.
        This dynamically calculates the number of pages for the selected probe.
        """
        # Extract the selected probe ID and reset page tracking
        self.selected_probe = self.ui.probe_selection_cb.currentText(
        )[-4:-1].lower()

        # Dynamically calculate the number of pages for the selected probe
        self.total_pages = self.count_probe_pages(self.selected_probe)
        self.current_page_index = 0

        if self.total_pages > 0:
            self.update_page_view()
        else:
            self.ui.page_identifier_label.setText("No pages found")
            self.ui.page_left_btn.setEnabled(False)
            self.ui.page_right_btn.setEnabled(False)

    def count_probe_pages(self, probe_prefix):
        """
        Count the number of pages in the QStackedWidget that match the given probe prefix.
        Example: For 'dlp', it would count 'double_lang_probe_1', 'double_lang_probe_2', etc.
        """
        count = 0

        for i in range(self.ui.probe_config_view.count()):
            widget = self.ui.probe_config_view.widget(i)
            widget_name = widget.objectName()

            if widget_name.startswith(probe_prefix):
                count += 1
        return count

    def update_page_view(self):
        """
        Update the probe_config_view to display the current page and update the page identifier label.
        """
        # Iterate through the pages in the probe_config_view
        for i in range(self.ui.probe_config_view.count()):
            widget = self.ui.probe_config_view.widget(i)
            widget_name = widget.objectName()

            # Check if the widget corresponds to the current probe and page index
            if widget_name == f"{self.selected_probe}_{self.current_page_index + 1}":
                # Set the current widget to the matching page
                self.ui.probe_config_view.setCurrentWidget(widget)
                break
        else:
            print("No matching widget found for the current probe and page index")

        # Update the label with the current page info
        self.ui.page_identifier_label.setText(
            f"Page {self.current_page_index + 1}/{self.total_pages}")

        # Enable/Disable buttons based on the current page
        self.ui.page_left_btn.setEnabled(self.current_page_index > 0)
        self.ui.page_right_btn.setEnabled(
            self.current_page_index < self.total_pages - 1)

    def go_to_next_page(self):
        """
        Navigate to the next page of the selected probe.
        """
        if self.current_page_index < self.total_pages - 1:
            self.current_page_index += 1
            self.update_page_view()  # Update the view
        else:
            print("Already on the last page")

    def go_to_previous_page(self):
        """
        Navigate to the previous page of the selected probe.
        """
        if self.current_page_index > 0:
            self.current_page_index -= 1
            self.update_page_view()  # Update the view
        else:
            print("Already on the first page")

    def open_file_dialog(self, line_edit, key):
        dialog = QFileDialog(self)
        dialog.setDirectory(r'C:/')
        if key == 'credentials_path':
            dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        else:
            dialog.setFileMode(QFileDialog.FileMode.Directory)

        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()

            if filenames:
                self.control.set_config(
                    probe_id='', key=key, value=str(Path(filenames[0])))
                line_edit.setText(
                    Path(self.control.get_config(probe_id='', key=key)).name)

    def adjust_value(self, spinbox, direction, config_key):
        """
        Adjust the value of a QDoubleSpinBox.

        :param spinbox: The QDoubleSpinBox to update.
        :param direction: 1 for increment, -1 for decrement.
        """
    
        current_value = spinbox.value()
        scale = 1
        if config_key!='button_adjust':
            new_value = self.increment(current_value) if direction == 1 else self.decrement(current_value)

            #Converting areas into meter
            if 'area' in config_key:
                scale = 1000
            elif 'bias' in config_key and abs(new_value) < 0.01:
                
                new_value = current_value * -1 
                    
                
            
            # Invoking mutator function of in memory config dictionary
            # Validations are also executed during the call stack of this method
            self.control.set_config(self.selected_probe, config_key, new_value/scale)
            probe= self.selected_probe
            
        else:
            new_value= self.new_adjust_scale(current_value, direction)
            self.control.set_config(probe_id='',key=config_key, value=new_value)
            probe=''
        # If the result is valid, a new value is set in the spinbox
        # Otherwise, previous value set
        spinbox.setValue(self.control.get_config(probe, config_key)*scale)
        
    def new_adjust_scale(self, current_value, direction):
        current_value = current_value * pow(10, direction)
        if current_value>= 0.01:
            return current_value
        else:
            return 0.01
    
    def increment(self, value):
        
        return value + self.control.get_config(probe_id='',key='button_adjust')

    def decrement(self, value):
        return value - self.control.get_config(probe_id='',key='button_adjust')
    
    def change_title(self):
        
        self.ui.slp_area_gb.setTitle(self.ui.slp_area_gb.title())
        self.ui.dlp_area_gb.setTitle(self.ui.dlp_area_gb.title())
        self.ui.tlv_area_gb.setTitle(self.ui.tlv_area_gb.title())
        self.ui.tlc_area_gb.setTitle(self.ui.tlc_area_gb.title())
        self.ui.hea_area_gb.setTitle(self.ui.hea_area_gb.title())
        self.ui.iea_area_gb.setTitle(self.ui.iea_area_gb.title())

    def handle_back_button(self):
        # Check if the current page is not the settings_select_page
        if self.ui.main_view.currentWidget() != self.ui.settings_select_page:
            # Jump to the settings_select_page
            self.ui.main_view.setCurrentWidget(self.ui.settings_select_page)
            # Hide the combobox when switching away
            self.ui.cb_handler.setVisible(False)
        else:
            # If already on settings_select_page, emit the back button signal
            self.emit_back_signal()

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
        self.back_btn_clicked.emit()
        self.setup_window.set_widget_values()

    def reset_settings(self):
        self.display_alert_message("Resetting Values")
        # Receiving original config values
        self.control.load_config_file()
        # Reset values from config file
        self.set_widget_values()

    def save_settings(self):
        self.control.save_config_file()
        self.setup_window.set_widget_values()
