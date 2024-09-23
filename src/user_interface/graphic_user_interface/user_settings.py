from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal, QTimer
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
        self.cb_handler.setVisible(False)
        
        # Connect buttons to switch between pages
        self.data_upload_settings_btn.clicked.connect(self.show_data_upload_settings)
        self.probe_config_settings_btn.clicked.connect(self.probe_config_settings)

        # Connect QComboBox selection change to change pages in the probe_config_view
        self.probe_selection_cb.currentIndexChanged.connect(self.switch_probe_page)

        # Connect left and right buttons to change pages
        self.page_left_btn.clicked.connect(self.go_to_previous_page)
        self.page_right_btn.clicked.connect(self.go_to_next_page)

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

                                ################## SLP ##################

        # Connect Plus/Minus buttons for Area
        self.slp_area_minus.clicked.connect(lambda: self.adjust_value(self.slp_area_input, -1, 'Probe area'))
        self.slp_area_plus.clicked.connect(lambda: self.adjust_value(self.slp_area_input, +1 , 'Probe area'))
        
        # Connect Plus/Minus buttons for DAC MIN
        self.slp_dac_min_minus.clicked.connect(lambda: self.adjust_value(self.slp_dac_min_input, -1, 'dac_min'))
        self.slp_dac_min_plus.clicked.connect(lambda: self.adjust_value(self.slp_dac_min_input, +1, 'dac_min'))
        
        # Connect Plus/Minus buttons for DAC MAX
        self.slp_dac_max_minus.clicked.connect(lambda: self.adjust_value(self.slp_dac_max_input, -1, 'dac_max'))
        self.slp_dac_max_plus.clicked.connect(lambda: self.adjust_value(self.slp_dac_max_input, +1, 'dac_max'))
        
        # Connect Plus/Minus buttons for Sweep MIN
        self.slp_sweep_min_minus.clicked.connect(lambda: self.adjust_value(self.slp_sweep_min_input, -1, 'sweep_amp_min'))
        self.slp_sweep_min_plus.clicked.connect(lambda: self.adjust_value(self.slp_sweep_min_input, +1, 'sweep_amp_min'))
        
        # Connect Plus/Minus buttons for Sweep Max
        self.slp_sweep_max_minus.clicked.connect(lambda: self.adjust_value(self.slp_sweep_max_input, -1, 'sweep_amp_max'))
        self.slp_sweep_max_plus.clicked.connect(lambda: self.adjust_value(self.slp_sweep_max_input, +1, 'sweep_amp_max'))
        
        # Connect Plus/Minus buttons for Collector Gain
        self.slp_collector_gain_minus.clicked.connect(lambda: self.adjust_value(self.slp_collector_gain_input, -1, 'collector_gain'))
        self.slp_collector_gain_plus.clicked.connect(lambda: self.adjust_value(self.slp_collector_gain_input, +1, 'collector_gain'))

        # Connect Plus/Minus buttons for Collector Shunt Resistance
        #self.slp_collector_shunt_rest_minus.clicked.connect(lambda: self.adjust_value(self.slp_collector_shunt_rest_input, -1, ''))
        #self.slp_collector_shunt_rest_plus.clicked.connect(lambda: self.adjust_value(self.slp_collector_shunt_rest_input, +1, ''))
        
                                ################## DLP ##################

        # Connect Plus/Minus buttons for Area
        self.dlp_area_minus.clicked.connect(lambda: self.adjust_value(self.dlp_area_input, -1, 'Probe area'))
        self.dlp_area_plus.clicked.connect(lambda: self.adjust_value(self.dlp_area_input, +1 , 'Probe area'))

        # Connect Plus/Minus buttons for DAC MIN
        self.dlp_dac_min_minus.clicked.connect(lambda: self.adjust_value(self.dlp_dac_min_input, -1, 'dac_min'))
        self.dlp_dac_min_plus.clicked.connect(lambda: self.adjust_value(self.dlp_dac_min_input, +1, 'dac_min'))

        # Connect Plus/Minus buttons for DAC MAX
        self.dlp_dac_max_minus.clicked.connect(lambda: self.adjust_value(self.dlp_dac_max_input, -1, 'dac_max'))
        self.dlp_dac_max_plus.clicked.connect(lambda: self.adjust_value(self.dlp_dac_max_input, +1, 'dac_max'))

        # Connect Plus/Minus buttons for Sweep MIN
        self.dlp_sweep_min_minus.clicked.connect(lambda: self.adjust_value(self.dlp_sweep_min_input, -1, 'sweep_amp_min'))
        self.dlp_sweep_min_plus.clicked.connect(lambda: self.adjust_value(self.dlp_sweep_min_input, +1, 'sweep_amp_min'))

        # Connect Plus/Minus buttons for Sweep MAX
        self.dlp_sweep_max_minus.clicked.connect(lambda: self.adjust_value(self.dlp_sweep_max_input, -1, 'sweep_amp_max'))
        self.dlp_sweep_max_plus.clicked.connect(lambda: self.adjust_value(self.dlp_sweep_max_input, +1, 'sweep_amp_max'))

        # Connect Plus/Minus buttons for Collector Gain
        self.dlp_collector_gain_minus.clicked.connect(lambda: self.adjust_value(self.dlp_collector_gain_input, -1, 'collector_gain'))
        self.dlp_collector_gain_plus.clicked.connect(lambda: self.adjust_value(self.dlp_collector_gain_input, +1, 'collector_gain'))

        # Connect Plus/Minus buttons for Collector Shunt Resistance
        #self.dlp_collector_shunt_rest_minus.clicked.connect(lambda: self.adjust_value(self.dlp_collector_shunt_rest_input, -1, ''))
        #self.dlp_collector_shunt_rest_plus.clicked.connect(lambda: self.adjust_value(self.dlp_collector_shunt_rest_input, +1, ''))

                                ################## TLC ##################

        # Connect Plus/Minus buttons for DAC MIN
        self.tlc_dac_min_minus.clicked.connect(lambda: self.adjust_value(self.tlc_dac_min_input, -1, 'dac_min'))
        self.tlc_dac_min_plus.clicked.connect(lambda: self.adjust_value(self.tlc_dac_min_input, +1, 'dac_min'))

        # Connect Plus/Minus buttons for DAC MAX
        self.tlc_dac_max_minus.clicked.connect(lambda: self.adjust_value(self.tlc_dac_max_input, -1, 'dac_max'))
        self.tlc_dac_max_plus.clicked.connect(lambda: self.adjust_value(self.tlc_dac_max_input, +1, 'dac_max'))

        # Connect Plus/Minus buttons for Up Amp MIN
        self.tlc_up_amp_min_minus.clicked.connect(lambda: self.adjust_value(self.tlc_up_amp_min_input, -1, 'up_amp_min'))
        self.tlc_up_amp_min_plus.clicked.connect(lambda: self.adjust_value(self.tlc_up_amp_min_input, +1, 'up_amp_min'))

        # Connect Plus/Minus buttons for Up Amp MAX
        self.tlc_up_amp_max_minus.clicked.connect(lambda: self.adjust_value(self.tlc_up_amp_max_input, -1, 'up_amp_max'))
        self.tlc_up_amp_max_plus.clicked.connect(lambda: self.adjust_value(self.tlc_up_amp_max_input, +1, 'up_amp_max'))

        # Connect Plus/Minus buttons for Down Amp MIN
        self.tlc_down_amp_min_minus.clicked.connect(lambda: self.adjust_value(self.tlc_down_amp_min_input, -1, 'down_amp_min'))
        self.tlc_down_amp_min_plus.clicked.connect(lambda: self.adjust_value(self.tlc_down_amp_min_input, +1, 'down_amp_min'))

        # Connect Plus/Minus buttons for Down Amp MAX
        self.tlc_down_amp_max_minus.clicked.connect(lambda: self.adjust_value(self.tlc_down_amp_max_input, -1, 'down_amp_max'))
        self.tlc_down_amp_max_plus.clicked.connect(lambda: self.adjust_value(self.tlc_down_amp_max_input, +1, 'down_amp_max'))

        # Connect Plus/Minus buttons for Area
        self.tlc_area_minus.clicked.connect(lambda: self.adjust_value(self.tlc_area_input, -1, 'Probe area'))
        self.tlc_area_plus.clicked.connect(lambda: self.adjust_value(self.tlc_area_input, +1, 'Probe area'))

        # Connect Plus/Minus buttons for Up Collector Gain
        self.tlc_up_collector_gain_minus.clicked.connect(lambda: self.adjust_value(self.tlc_up_collector_gain_input, -1, 'up_collector_gain'))
        self.tlc_up_collector_gain_plus.clicked.connect(lambda: self.adjust_value(self.tlc_up_collector_gain_input, +1, 'up_collector_gain'))

        # Connect Plus/Minus buttons for Down Collector Gain
        self.tlc_down_collect_gain_minus.clicked.connect(lambda: self.adjust_value(self.tlc_down_collect_gain_input, -1, 'down_collector_gain'))
        self.tlc_down_collect_gain_plus.clicked.connect(lambda: self.adjust_value(self.tlc_down_collect_gain_input, +1, 'down_collector_gain'))

        # Connect Plus/Minus buttons for Up Collector Shunt Resistance
        #self.tlc_up_shunt_rest_minus.clicked.connect(lambda: self.adjust_value(self.tlc_up_shunt_rest_input, -1, ''))
        #self.tlc_up_shunt_rest_plus.clicked.connect(lambda: self.adjust_value(self.tlc_up_shunt_rest_input, +1, ''))

        # Connect Plus/Minus buttons for Down Collector Shunt Resistance
        #self.tlc_down_shunt_rest_minus.clicked.connect(lambda: self.adjust_value(self.tlc_down_shunt_rest_input, -1, ''))
        #self.tlc_down_shunt_rest_plus.clicked.connect(lambda: self.adjust_value(self.tlc_down_shunt_rest_input, +1, ''))

                                ################## TLV ##################

        # Connect Plus/Minus buttons for DAC MIN
        self.tlv_dac_min_minus.clicked.connect(lambda: self.adjust_value(self.tlv_dac_min_input, -1, 'dac_min'))
        self.tlv_dac_min_plus.clicked.connect(lambda: self.adjust_value(self.tlv_dac_min_input, +1, 'dac_min'))

        # Connect Plus/Minus buttons for DAC MAX
        self.tlv_dac_max_minus.clicked.connect(lambda: self.adjust_value(self.tlv_dac_max_input, -1, 'dac_max'))
        self.tlv_dac_max_plus.clicked.connect(lambda: self.adjust_value(self.tlv_dac_max_input, +1, 'dac_max'))

        # Connect Plus/Minus buttons for Up Amp MIN
        self.tlv_up_amp_min_minus.clicked.connect(lambda: self.adjust_value(self.tlv_up_amp_min_input, -1, 'up_amp_min'))
        self.tlv_up_amp_min_plus.clicked.connect(lambda: self.adjust_value(self.tlv_up_amp_min_input, +1, 'up_amp_min'))

        # Connect Plus/Minus buttons for Up Amp MAX
        self.tlv_up_amp_max_minus.clicked.connect(lambda: self.adjust_value(self.tlv_up_amp_max_input, -1, 'up_amp_max'))
        self.tlv_up_amp_max_plus.clicked.connect(lambda: self.adjust_value(self.tlv_up_amp_max_input, +1, 'up_amp_max'))
    
        # Connect Plus/Minus buttons for Area
        self.tlv_area_minus.clicked.connect(lambda: self.adjust_value(self.tlv_area_input, -1, 'Probe area'))
        self.tlv_area_plus.clicked.connect(lambda: self.adjust_value(self.tlv_area_input, +1, 'Probe area'))

        # Connect Plus/Minus buttons for Float Collector Gain
        self.tlv_float_collect_gain_minus.clicked.connect(lambda: self.adjust_value(self.tlv_float_collect_gain_input, -1, 'float_collector_gain'))
        self.tlv_float_collect_gain_plus.clicked.connect(lambda: self.adjust_value(self.tlv_float_collect_gain_input, +1, 'float_collector_gain'))

        # Connect Plus/Minus buttons for Up Collector Gain
        self.tlv_up_collector_gain_minus.clicked.connect(lambda: self.adjust_value(self.tlv_up_collector_gain_input, -1, 'up_collector_gain'))
        self.tlv_up_collector_gain_plus.clicked.connect(lambda: self.adjust_value(self.tlv_up_collector_gain_input, +1, 'up_collector_gain'))

        # Connect Plus/Minus buttons for Up Collector Shunt Resistance
        #self.tlv_up_shunt_rest_minus.clicked.connect(lambda: self.adjust_value(self.tlv_up_shunt_rest_input, -1, ''))
        #self.tlv_up_shunt_rest_plus.clicked.connect(lambda: self.adjust_value(self.tlv_up_shunt_rest_input, +1, ''))

                                ################## IEA ##################

        # Connect Plus/Minus buttons for DAC MIN
        self.iea_dac_min_minus.clicked.connect(lambda: self.adjust_value(self.iea_dac_min_input, -1, 'dac_min'))
        self.iea_dac_min_plus.clicked.connect(lambda: self.adjust_value(self.iea_dac_min_input, +1, 'dac_min'))

        # Connect Plus/Minus buttons for DAC MAX
        self.iea_dac_max_minus.clicked.connect(lambda: self.adjust_value(self.iea_dac_max_input, -1, 'dac_max'))
        self.iea_dac_max_plus.clicked.connect(lambda: self.adjust_value(self.iea_dac_max_input, +1, 'dac_max'))

        # Connect Plus/Minus buttons for Rejector MIN
        self.iea_reject_min_minus.clicked.connect(lambda: self.adjust_value(self.iea_reject_min_input, -1, 'rejector_min'))
        self.iea_reject_min_plus.clicked.connect(lambda: self.adjust_value(self.iea_reject_min_input, +1, 'rejector_min'))

        # Connect Plus/Minus buttons for Rejector MAX
        self.iea_reject_max_minus.clicked.connect(lambda: self.adjust_value(self.iea_reject_max_input, -1, 'rejector_max'))
        self.iea_reject_max_plus.clicked.connect(lambda: self.adjust_value(self.iea_reject_max_input, +1, 'rejector_max'))

        # Connect Plus/Minus buttons for Collector Bias MIN
        self.iea_collect_bias_min_minus.clicked.connect(lambda: self.adjust_value(self.iea_collect_bias_min_input, -1, 'collector_bias_min'))
        self.iea_collect_bias_min_plus.clicked.connect(lambda: self.adjust_value(self.iea_collect_bias_min_input, +1, 'collector_bias_min'))

        # Connect Plus/Minus buttons for Collector Bias MAX
        self.iea_collect_bias_max_minus.clicked.connect(lambda: self.adjust_value(self.iea_collect_bias_max_input, -1, 'collector_bias_max'))
        self.iea_collect_bias_max_plus.clicked.connect(lambda: self.adjust_value(self.iea_collect_bias_max_input, +1, 'collector_bias_max'))

        # Connect Plus/Minus buttons for Collector Probe Bias
        self.iea_collector_probe_minus.clicked.connect(lambda: self.adjust_value(self.iea_collector_probe_input, -1, 'collector_bias'))
        self.iea_collector_probe_plus.clicked.connect(lambda: self.adjust_value(self.iea_collector_probe_input, +1, 'collector_bias'))

        # Connect Plus/Minus buttons for Collector Gain
        self.iea_collector_gain_minus.clicked.connect(lambda: self.adjust_value(self.iea_collector_gain_input, -1, 'collector_gain'))
        self.iea_collector_gain_plus.clicked.connect(lambda: self.adjust_value(self.iea_collector_gain_input, +1, 'collector_gain'))

        # Connect Plus/Minus buttons for Sweep MIN
        self.iea_sweep_min_minus.clicked.connect(lambda: self.adjust_value(self.iea_sweep_min_input, -1, 'sweep_amp_min'))
        self.iea_sweep_min_plus.clicked.connect(lambda: self.adjust_value(self.iea_sweep_min_input, +1, 'sweep_amp_min'))

        # Connect Plus/Minus buttons for Sweep MAX
        self.iea_sweep_max_minus.clicked.connect(lambda: self.adjust_value(self.iea_sweep_max_input, -1, 'sweep_amp_max'))
        self.iea_sweep_max_plus.clicked.connect(lambda: self.adjust_value(self.iea_sweep_max_input, +1, 'sweep_amp_max'))

        # Connect Plus/Minus buttons for Area
        self.iea_area_minus.clicked.connect(lambda: self.adjust_value(self.iea_area_input, -1, 'Probe area'))
        self.iea_area_plus.clicked.connect(lambda: self.adjust_value(self.iea_area_input, +1, 'Probe area'))

        # Connect Plus/Minus buttons for Custom Gas
        self.iea_mass_minus.clicked.connect(lambda: self.adjust_value(self.iea_mass_input, -1, 'Probe area'))
        self.iea_mass_plus.clicked.connect(lambda: self.adjust_value(self.iea_mass_input, +1, 'Probe area'))

        # Connect Plus/Minus buttons for Collector Shunt Resistance
        #self.iea_collector_shunt_rest_minus.clicked.connect(lambda: self.adjust_value(self.iea_collector_shunt_rest_input, -1, ''))
        #self.iea_collector_shunt_rest_plus.clicked.connect(lambda: self.adjust_value(self.iea_collector_shunt_rest_input, +1, ''))

                                ################## HEA ##################

        # Connect Plus/Minus buttons for DAC MIN
        self.hea_dac_min_minus.clicked.connect(lambda: self.adjust_value(self.hea_dac_min_input, -1, 'dac_min'))
        self.hea_dac_min_plus.clicked.connect(lambda: self.adjust_value(self.hea_dac_min_input, +1, 'dac_min'))

        # Connect Plus/Minus buttons for DAC MAX
        self.hea_dac_max_minus.clicked.connect(lambda: self.adjust_value(self.hea_dac_max_input, -1, 'dac_max'))
        self.hea_dac_max_plus.clicked.connect(lambda: self.adjust_value(self.hea_dac_max_input, +1, 'dac_max'))

        # Connect Plus/Minus buttons for Collector Bias MIN
        self.hea_collect_bias_min_minus.clicked.connect(lambda: self.adjust_value(self.hea_collect_bias_min_input, -1, 'collector_bias_min'))
        self.hea_collect_bias_min_plus.clicked.connect(lambda: self.adjust_value(self.hea_collect_bias_min_input, +1, 'collector_bias_min'))

        # Connect Plus/Minus buttons for Collector Bias MAX
        self.hea_collect_bias_max_minus.clicked.connect(lambda: self.adjust_value(self.hea_collect_bias_max_input, -1, 'collector_bias_max'))
        self.hea_collect_bias_max_plus.clicked.connect(lambda: self.adjust_value(self.hea_collect_bias_max_input, +1, 'collector_bias_max'))

        # Connect Plus/Minus buttons for Sweep MIN
        self.hea_sweep_min_minus.clicked.connect(lambda: self.adjust_value(self.hea_sweep_min_input, -1, 'sweep_amp_min'))
        self.hea_sweep_min_plus.clicked.connect(lambda: self.adjust_value(self.hea_sweep_min_input, +1, 'sweep_amp_min'))

        # Connect Plus/Minus buttons for Sweep MAX
        self.hea_sweep_max_minus.clicked.connect(lambda: self.adjust_value(self.hea_sweep_max_input, -1, 'sweep_amp_max'))
        self.hea_sweep_max_plus.clicked.connect(lambda: self.adjust_value(self.hea_sweep_max_input, +1, 'sweep_amp_max'))

        # Connect Plus/Minus buttons for Collimator Bias
        self.hea_collimator_bias_minus.clicked.connect(lambda: self.adjust_value(self.hea_collimator_bias_input, -1, 'collimator_bias'))
        self.hea_collimator_bias_plus.clicked.connect(lambda: self.adjust_value(self.hea_collimator_bias_input, +1, 'collimator_bias'))

        # Connect Plus/Minus buttons for Collector Gain
        self.hea_collect_gain_minus.clicked.connect(lambda: self.adjust_value(self.hea_collect_gain_input, -1, 'collector_gain'))
        self.hea_collect_gain_plus.clicked.connect(lambda: self.adjust_value(self.hea_collect_gain_input, +1, 'collector_gain'))

        # Connect Plus/Minus buttons for Area
        self.hea_area_minus.clicked.connect(lambda: self.adjust_value(self.hea_area_output, -1, 'Probe area'))
        self.hea_area_plus.clicked.connect(lambda: self.adjust_value(self.hea_area_output, +1, 'Probe area'))

        # Connect Plus/Minus buttons for Collector Shunt Resistance
        #self.hea_collector_shunt_rest_minus.clicked.connect(lambda: self.adjust_value(self.hea_collector_shunt_rest_input, -1, ''))
        #self.hea_collector_shunt_rest_plus.clicked.connect(lambda: self.adjust_value(self.hea_collector_shunt_rest_input, +1, ''))

    def set_widget_values(self):
        
        self.credentials_path_input.setText(self.control.get_config(probe_id = '', key = 'credentials_path'))
        self.local_path_input.setText(self.control.get_config(probe_id = '', key = 'local_path'))

                ################## SLP ##################

        self.slp_area_input.setValue(self.control.get_config('slp', 'Probe area'))
        self.slp_dac_min_input.setValue(self.control.get_config('slp', 'dac_min'))
        self.slp_dac_max_input.setValue(self.control.get_config('slp', 'dac_max'))
        self.slp_sweep_min_input.setValue(self.control.get_config('slp', 'sweep_amp_min'))
        self.slp_sweep_max_input.setValue(self.control.get_config('slp', 'sweep_amp_max'))
        self.slp_collector_gain_input.setValue(self.control.get_config('slp', 'collector_gain'))
        #self.slp_collector_shunt_rest_input.setValue(self.control.get_config('slp', ''))
        
                ################## SLP ##################

        self.dlp_area_input.setValue(self.control.get_config('dlp', 'Probe area'))
        self.dlp_dac_min_input.setValue(self.control.get_config('dlp', 'dac_min'))
        self.dlp_dac_max_input.setValue(self.control.get_config('dlp', 'dac_max'))
        self.dlp_sweep_min_input.setValue(self.control.get_config('dlp', 'sweep_amp_min'))
        self.dlp_sweep_max_input.setValue(self.control.get_config('dlp', 'sweep_amp_max'))
        self.dlp_collector_gain_input.setValue(self.control.get_config('dlp', 'collector_gain'))
        #self.dlp_collector_shunt_rest_input.setValue(self.control.get_config('dlp', ''))

                ################## TLC ##################

        self.tlc_area_input.setValue(self.control.get_config('tlc', 'Probe area'))
        self.tlc_dac_min_input.setValue(self.control.get_config('tlc', 'dac_min'))
        self.tlc_dac_max_input.setValue(self.control.get_config('tlc', 'dac_max'))
        self.tlc_up_amp_min_input.setValue(self.control.get_config('tlc', 'up_amp_min'))
        self.tlc_up_amp_max_input.setValue(self.control.get_config('tlc', 'up_amp_max'))
        self.tlc_down_amp_min_input.setValue(self.control.get_config('tlc', 'down_amp_min'))
        self.tlc_down_amp_max_input.setValue(self.control.get_config('tlc', 'down_amp_max'))
        self.tlc_up_collector_gain_input.setValue(self.control.get_config('tlc', 'up_collector_gain'))
        self.tlc_down_collect_gain_input.setValue(self.control.get_config('tlc', 'down_collector_gain'))
        #self.tlc_up_shunt_rest_input.setValue(self.control.get_config('tlc', ''))
        #self.tlc_down_shunt_rest_input.setValue(self.control.get_config('tlc', ''))

                ################## TLV ##################

        self.tlv_area_input.setValue(self.control.get_config('tlv', 'Probe area'))
        self.tlv_dac_min_input.setValue(self.control.get_config('tlv', 'dac_min'))
        self.tlv_dac_max_input.setValue(self.control.get_config('tlv', 'dac_max'))
        self.tlv_up_amp_min_input.setValue(self.control.get_config('tlv', 'up_amp_min'))
        self.tlv_up_amp_max_input.setValue(self.control.get_config('tlv', 'up_amp_max'))
        self.tlv_float_collect_gain_input.setValue(self.control.get_config('tlv', 'float_collector_gain'))
        self.tlv_up_collector_gain_input.setValue(self.control.get_config('tlv', 'up_collector_gain'))
        #self.tlv_up_shunt_rest_input.setValue(self.control.get_config('tlv', ''))

                ################## IEA ##################

        self.iea_area_input.setValue(self.control.get_config('iea', 'Probe area'))
        #self.iea_mass_input.setValue(self.control.get_config('iea', 'custom_mass'))
        self.iea_dac_min_input.setValue(self.control.get_config('iea', 'dac_min'))
        self.iea_dac_max_input.setValue(self.control.get_config('iea', 'dac_max'))
        self.iea_reject_min_input.setValue(self.control.get_config('iea', 'rejector_min'))
        self.iea_reject_max_input.setValue(self.control.get_config('iea', 'rejector_max'))
        self.iea_collect_bias_min_input.setValue(self.control.get_config('iea', 'collector_bias_min'))
        self.iea_collect_bias_max_input.setValue(self.control.get_config('iea', 'collector_bias_max'))
        self.iea_collector_probe_input.setValue(self.control.get_config('iea', 'collector_bias'))
        self.iea_collector_gain_input.setValue(self.control.get_config('iea', 'collector_gain'))
        self.iea_sweep_min_input.setValue(self.control.get_config('iea', 'sweep_amp_min'))
        self.iea_sweep_max_input.setValue(self.control.get_config('iea', 'sweep_amp_max'))
        #self.iea_collector_shunt_rest_input.setValue(self.control.get_config('iea', ''))

                ################## HEA ##################
        self.hea_area_output.setValue(self.control.get_config('hea', 'Probe area'))
        self.hea_dac_min_input.setValue(self.control.get_config('hea', 'dac_min'))
        self.hea_dac_max_input.setValue(self.control.get_config('hea', 'dac_max'))
        self.hea_collect_bias_min_input.setValue(self.control.get_config('hea', 'collector_bias_min'))
        self.hea_collect_bias_max_input.setValue(self.control.get_config('hea', 'collector_bias_max'))
        self.hea_sweep_min_input.setValue(self.control.get_config('hea', 'sweep_amp_min'))
        self.hea_sweep_max_input.setValue(self.control.get_config('hea', 'sweep_amp_max'))
     #   self.hea_collimator_bias_input.setValue(self.control.get_config('hea', 'collimator_bias'))
        self.hea_collect_gain_input.setValue(self.control.get_config('hea', 'collector_gain'))
        #self.hea_collector_shunt_rest_input.setValue(self.control.get_config('hea', ''))

    def show_data_upload_settings(self):
        self.main_view.setCurrentWidget(self.data_upload_settings_page)
        self.cb_handler.setVisible(False)  # Hide the combobox when switching away

    def probe_config_settings(self):
        # Switch to the probe config page
        self.main_view.setCurrentWidget(self.probe_config_settings_page)
        self.cb_handler.setVisible(True)  # Show the probe selection combo box
        self.switch_probe_page(self.probe_selection_cb.currentIndex())  # Initialize the page view

    def switch_probe_page(self, index):
        """
        Switch pages in the probe_config_view based on the selected probe in the QComboBox.
        This dynamically calculates the number of pages for the selected probe.
        """
        # Extract the selected probe ID and reset page tracking
        self.selected_probe = self.probe_selection_cb.currentText()[-4:-1].lower()

        # Dynamically calculate the number of pages for the selected probe
        self.total_pages = self.count_probe_pages(self.selected_probe)
        self.current_page_index = 0

        if self.total_pages > 0:
            self.update_page_view()
        else:
            self.page_identifier_label.setText("No pages found")
            self.page_left_btn.setEnabled(False)
            self.page_right_btn.setEnabled(False)

    def count_probe_pages(self, probe_prefix):
        """
        Count the number of pages in the QStackedWidget that match the given probe prefix.
        Example: For 'dlp', it would count 'double_lang_probe_1', 'double_lang_probe_2', etc.
        """
        count = 0
        
        for i in range(self.probe_config_view.count()):
            widget = self.probe_config_view.widget(i)
            widget_name = widget.objectName()
            
            if widget_name.startswith(probe_prefix):
                count += 1
        return count

    def update_page_view(self):
        """
        Update the probe_config_view to display the current page and update the page identifier label.
        """        
        # Iterate through the pages in the probe_config_view
        for i in range(self.probe_config_view.count()):
            widget = self.probe_config_view.widget(i)
            widget_name = widget.objectName()

            # Check if the widget corresponds to the current probe and page index
            if widget_name == f"{self.selected_probe}_{self.current_page_index + 1}":
                self.probe_config_view.setCurrentWidget(widget)  # Set the current widget to the matching page
                break
        else:
            print("No matching widget found for the current probe and page index")

        # Update the label with the current page info
        self.page_identifier_label.setText(f"Page {self.current_page_index + 1}/{self.total_pages}")
        
        # Enable/Disable buttons based on the current page
        self.page_left_btn.setEnabled(self.current_page_index > 0)
        self.page_right_btn.setEnabled(self.current_page_index < self.total_pages - 1)

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
            if key =='credentials_path':
                dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
            else:
                dialog.setFileMode(QFileDialog.FileMode.Directory) 

            dialog.setViewMode(QFileDialog.ViewMode.List)
            if dialog.exec():
                filenames = dialog.selectedFiles()
                
                if filenames:
                    self.control.set_config(probe_id='', key=key, value=str(Path(filenames[0])))
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
            self.cb_handler.setVisible(False)  # Hide the combobox when switching away
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
        self.alert_msg_label.setText(message)

        # Create a QTimer to clear the message after 5 seconds (5000 milliseconds)
        QTimer.singleShot(5000, lambda: self.clear_alert_message())

    def clear_alert_message(self):
        """
        Clear the message displayed on alert_msg_label.
        """
        self.alert_msg_label.setText("")

    def emit_back_signal(self):
        self.back_btn_clicked.emit() 

    def reset_settings(self):
        self.display_alert_message("Resetting Values")
        # Receiving original config values
        self.control.load_config_file()
        # Reset values from config file
        self.set_widget_values()

    def save_settings(self):
        self.control.save_config_file()
