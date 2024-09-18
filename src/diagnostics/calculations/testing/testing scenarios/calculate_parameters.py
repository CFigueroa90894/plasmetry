# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 13:43:38 2024

@author: ajco2
"""
#TODO: MUST UPDATE TO TAKE PARAMETERS DICTIONARY AS ARGUMENTS, ALSO TO USE EQS LIST


import slp_plasma_parameters as slp
from scipy import signal

    
def FilterSignal(rawSignal):
    """
    Filters a signal using a butterworth digital filter. 
    
    Inputs:
        rawSignal = an array of raw data captured by the sensor.
        
    Outputs:
        filteredSignal = signal after being processed by a butterworth digital filter.
    """
    
    sos = signal.butter(2, 0.03, output='sos')
    filteredSignal = signal.sosfiltfilt(sos, rawSignal)
    
    return filteredSignal

def get_sweeps_parameters(sweep_list):
    parameter_list = []
    for sweep in sweep_list: 
        current = sweep[0]
        bias = sweep[1]
        parameter_dictionary = {} 
        #filtering raw current, storing the output in a list
        filtered_current = FilterSignal(current)


        floating_potential, plasma_potential = slp.get_floating_and_plasma_potential(filtered_current, bias)

        parameter_dictionary['floating potential (V)']= floating_potential[1]

        parameter_dictionary['plasma potential (V)']= plasma_potential[1]

        electron_temperature_ev, electron_temperature_joules = slp.get_electron_temperature(floating_potential, plasma_potential, filtered_current, bias)

        parameter_dictionary['electron temperature (eV)']=  electron_temperature_ev
        parameter_dictionary['electron temperature (J)'] = electron_temperature_joules
        

        electron_saturation_current = slp.get_electron_saturation_current(filtered_current, plasma_potential[0])

        probe_area = 30.3858e-06

        electron_density= slp.get_electron_density(electron_saturation_current, electron_temperature_joules, probe_area)

        parameter_dictionary['Electron Density']= electron_density

        debye_length = slp.get_debye_length(electron_temperature_joules, electron_density)


        parameter_dictionary['Debye length (m)']= debye_length
        
        number_of_charged_particles = slp.get_number_of_electrons(debye_length, electron_density)

        parameter_dictionary['Number of charged particles in the Debye sphere (integer)']= number_of_charged_particles
        parameter_list.append(parameter_dictionary)
        
    return parameter_list
