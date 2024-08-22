import numpy as np

#storing the charge of the electron particle, since it shall be used for calculation
electron_charge = 1.60217657e-19
#storing the permittivity of free space constant in F/m, since it shall be used for calculation
epsilon_naught= 8.854e-12

def get_debye_length(parameters):
    
    '''
    DLP and SLP Debye length is returned from this function in meters.
    '''
    #acquiring Debye length
    parameters['Debye length'] = np.sqrt( 2 * epsilon_naught * parameters['Electron temperature (Joules)']/ (  parameters['Electron density'] * electron_charge * electron_charge) )
    



def get_number_of_electrons(debye_length, electron_density):
    
    '''
    DLP and SLP number of charged particles in the debye sphere is returned from this function.
    '''
    
    #obtaining the number of electrons in the debye sphere
    number_of_electrons = 4/3 * np.pi * debye_length * electron_density
    
    return int(number_of_electrons)


def get_plasma_potential(parameters):
    
    '''
    HEA and IEA plasma potential is yielded by the applied bias where dI/dV = 0
    '''
    filtered_current_list = parameters['Filtered current'] 
    voltage_list =  parameters['Bias']
    #value closest to 0 is taken, since the derivative may not be 0 ever
    parameters['Plasma potential index'] = np.argmin(abs(np.gradient(filtered_current_list, voltage_list)))
    
    parameters['Plasma potential'] = voltage_list[parameters['Plasma potential index']]

    
def get_particle_temperature(parameters):
    
    '''
    HEA and IEA particle temperature in both electron volts and  Joules is returned by this function.
    
    Particle temperature in electron volts may be yielded from 1/ (d(ln(I))/dV) where  dI/dV = 0 (a.k.a.  plasma potential)
    '''
    plasma_potential = parameters['Plasma potential']
    filtered_current_list = parameters['Filtered current'] 
    voltage_list =  parameters['Bias']

    log_I_V_derivative=  np.gradient(np.log(abs(filtered_current_list)), voltage_list )
    
    parameters['Particle temperature (eV)'] = 1/log_I_V_derivative[plasma_potential[0]]
    
    #multiplying the electron particle mass times the electron temperature in electron volts yields the electron temperature in Joules
    parameters['Particle temperature (Joules)']  = parameters['Particle temperature [eV]']  * electron_charge
    

   
def get_particle_density(parameters):
    
    '''
    This function returns the electron  density for SLP, HEA,IEA in Kilograms per cubic meter.
    
    If SLP or HEA for electron parameters is used, must receive electron mass as particle mass.
    
    Otherwise, the particle mass should be the estimated ion mass of the ions in the plasma
    '''
    if parameters['bias'][-1] >= 0 & parameters['Electron saturation current'] != None:
        parameters['Particle saturation current'] = ['Particle saturation current']
        
    #acquiring electron density
    parameters['Particle density'] =  abs(parameters['Particle saturation current']/(electron_charge * parameters['Probe area'] * np.sqrt(parameters['Particle temperature(Joules)'] / (2 * np.pi * parameters['Particle mass']))))
    if parameters['bias'][-1] >= 0 & parameters['Electron saturation current'] != None:
       parameters['Electron density'] = parameters['Particle density']
       del parameters['Particle density']
       
        
    

def get_equations():
    '''
    This function returns a list of references for the equations used by both  HEA implementations and the IEA implementation.
    '''
    list_of_references = []
    list_of_references.append(get_plasma_potential)
    list_of_references.append(get_particle_temperature)
    list_of_references.append(get_particle_density)
    return list_of_references