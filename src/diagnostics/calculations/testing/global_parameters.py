import numpy as np


def get_debye_length(electron_temperature_joules, electron_density):
    
    '''
    DLP and SLP Debye length is returned from this function in meters.
    '''
    
    #storing the charge of the electron particle, since it shall be used for calculation
    electron_charge = 1.60217657e-19
    
    #storing the permittivity of free space constant in F/m, since it shall be used for calculation
    epsilon_naught= 8.854e-12
    
    #acquiring Debye length
    debye_length = np.sqrt( (2* epsilon_naught * electron_temperature_joules) / ( electron_density * electron_charge * electron_charge) )
    
    return debye_length


def get_number_of_electrons(debye_length, electron_density):
    
    '''
    DLP and SLP number of charged particles in the debye sphere is returned from this function.
    '''
    
    #obtaining the number of electrons in the debye sphere
    number_of_electrons = 4/3 * np.pi * debye_length * electron_density
    
    return int(number_of_electrons)


def get_plasma_potential(filtered_current_list, voltage_list):
    
    '''
    HEA and IEA plasma potential is yielded by the applied bias where dI/dV = 0
    '''
    #value closest to 0 is taken, since the derivative may not be 0 ever
    plasma_potential_index = np.argmin(abs(np.gradient(filtered_current_list, voltage_list)))
    
    plasma_potential = voltage_list[plasma_potential_index]
    
    return plasma_potential, plasma_potential_index
    
    
def get_particle_temperature(plasma_potential, filtered_current_list, voltage_list):
    
    '''
    HEA and IEA particle temperature in both electron volts and  Joules is returned by this function.
    
    Particle temperature in electron volts may be yielded from 1/ (d(ln(I))/dV) where  dI/dV = 0 (a.k.a.  plasma potential)
    '''
    #storing the charge of the electron particle, since it shall be used for calculation
    electron_charge = 1.60217657e-19  
    
    log_I_V_derivative=  np.gradient(np.log(abs(filtered_current_list)), voltage_list )
    
    particle_temperature_ev = 1/log_I_V_derivative[plasma_potential[0]]
    
    #multiplying the electron particle mass times the electron temperature in electron volts yields the electron temperature in Joules
    particle_temperature_joules = particle_temperature_ev * electron_charge
    
    #could return the temperature in a list containing both ev and Joules values of electron temperature, need to review with team
    return particle_temperature_ev, particle_temperature_joules

   
def get_particle_density(electron_saturation_current, electron_temperature_joules, probe_area, particle_mass):
    
    '''
    This function returns the electron  density for SLP, HEA,IEA in Kilograms per cubic meter.
    
    If SLP or HEA for electron parameters is used, must receive electron mass as particle mass.
    
    Other wise, the particle mass should be the estimated ion mass of the ions in the plasma
    '''
    
    #storing the charge of the electron particle, since it shall be used for calculation
    electron_charge = 1.60217657e-19
    
    #acquiring electron density
    particle_density = electron_saturation_current/(electron_charge * probe_area * np.sqrt(electron_temperature_joules / (2 * np.pi * particle_mass)))
    
    return particle_density
