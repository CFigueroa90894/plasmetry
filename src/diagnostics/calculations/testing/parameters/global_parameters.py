import numpy as np

# Storing the charge of the electron particle, since it shall be used for calculation
ELECTRON_CHARGE = 1.60217657e-19

# Storing the permittivity of free space constant in F/m, since it shall be used for calculation
EPSILON_NAUGHT= 8.854e-12


def get_debye_length(parameters):
    
    """DLP and SLP Debye length is calculated from this function in meters."""
    
    # Acquiring Debye length
    parameters['Debye length'] = np.sqrt(2 * EPSILON_NAUGHT * \
                                         parameters['Electron temperature (Joules)'] / \
                                        (parameters['Electron density'] * ELECTRON_CHARGE **2))
    

def get_number_of_electrons(parameters):
    
    """DLP and SLP number of particles in the debye sphere is yielded from this function."""
    
    # Obtaining the number of electrons in the debye sphere 
    parameters['Number of electrons'] = 4/3 * np.pi * parameters['Debye length'] * parameters['Electron density']


def get_particle_density(parameters):
    
    """This function yields the electron  density for SLP, HEA,IEA in Kilograms per cubic meter.
    
    If SLP or HEA for electron parameters is used, must receive electron mass as particle mass.
    
    Otherwise, the particle mass should be the estimated ion mass of the ions in the plasma
    """
    
    if  'Electron saturation current' in parameters:
        parameters['Particle saturation current'] = parameters['Electron saturation current']
        parameters['Particle temperature (Joules)'] = parameters['Electron temperature (Joules)'] 

    # Acquiring electron density
    parameters['Particle density'] =  abs(parameters['Particle saturation current']/(ELECTRON_CHARGE * parameters['Probe area'] * np.sqrt(parameters['Particle temperature (Joules)'] / (2 * np.pi * parameters['Particle mass']))))
   
    if  'Electron saturation current' in parameters:
       parameters['Electron density'] = parameters['Particle density']
       del parameters['Particle density']
       del parameters['Particle temperature (Joules)']
       
def get_plasma_potential(parameters):
    
    """HEA and IEA plasma potential is yielded by the applied bias where dI/dV = 0"""
    
    # Storing I-V values
    filtered_current_list = parameters['Filtered current'] 
    voltage_list =  parameters['Bias']
    
    # Value closest to 0 is taken to yield the index, since the derivative may not be 0
    parameters['Plasma potential index'] = np.argmin(abs(np.gradient(filtered_current_list, voltage_list)))
    
    # Storing the plasma potential
    parameters['Plasma potential'] = voltage_list[parameters['Plasma potential index']]

    
def get_particle_temperature(parameters):
    
    """HEA and IEA particle temperature in both electron volts and  Joules is calculated by this function.
    
    Particle temperature in electron volts may be yielded from 1/ (d(ln(I))/dV) where  dI/dV = 0 (a.k.a.  plasma potential)
    """
    # Storing parameters used to calculate temperature
    plasma_potential = parameters['Plasma potential']
    filtered_current_list = parameters['Filtered current'] 
    voltage_list =  parameters['Bias']
    
    # Storing the derivative of the ln(I)-V values
    log_I_V_derivative=  np.gradient(np.log(abs(filtered_current_list)), voltage_list )
    
    # Storing the particle temperature in electron volts
    parameters['Particle temperature (eV)'] = 1/log_I_V_derivative[plasma_potential[0]]
    
    # Storing the particle temperature in Joules
    parameters['Particle temperature (Joules)']  = parameters['Particle temperature [eV]']  * ELECTRON_CHARGE
    

def get_equations():
    
    """This function returns a list of references for the equations used by both
    
    HEA implementations and the IEA implementation.
    """
    
    list_of_references = []
    list_of_references.append(get_plasma_potential)
    list_of_references.append(get_particle_temperature)
    list_of_references.append(get_particle_density)
    return list_of_references