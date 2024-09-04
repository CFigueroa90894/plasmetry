import unittest
import sys 
import os
from BaseCase import BaseCase
sys.path.insert(0, os.path.abspath('parameters'))
import slp_plasma_parameters
import global_parameters

class SLPTestCases(BaseCase):    
    parameters = {}
        
    @classmethod
    def set_parameters(cls, raw_current, bias):
        SLPTestCases.parameters['config_ref'] = {'Probe area' : 30.3858e-06, 'Particle mass':  9.10938356e-31}
        SLPTestCases.parameters['Raw current'] = raw_current
        SLPTestCases.parameters['Bias'] = bias
    

    def test_1_filter_current(self):
        
        """Test the filter_current function"""
        slp_plasma_parameters.filter_current(SLPTestCases.parameters)
        self.assertIn('Filtered current', SLPTestCases.parameters)

    def test_2_get_floating_and_plasma_potential(self):
        """Test the get_floating_and_plasma_potential function"""
        
        slp_plasma_parameters.get_floating_and_plasma_potential(SLPTestCases.parameters)
        
        self.assertIn('Floating potential', SLPTestCases.parameters)
        self.assertIn('Floating potential index', SLPTestCases.parameters)
        self.assertIn('Plasma potential', SLPTestCases.parameters)
        self.assertIn('Plasma potential index', SLPTestCases.parameters)
       
        self.assertGreaterEqual(SLPTestCases.parameters['Plasma potential'], 0, "Plasma potential should be non-negative")
        
        self.assertTrue(0 <= SLPTestCases.parameters['Floating potential index'] <  SLPTestCases.parameters['Plasma potential index'])
        self.assertTrue(SLPTestCases.parameters['Floating potential index'] <= SLPTestCases.parameters['Plasma potential index'] < len(SLPTestCases.parameters['Bias']))

    def test_3_get_electron_saturation_current(self):
        
        """Test the get_electron_saturation_current function"""
        slp_plasma_parameters.get_electron_saturation_current(SLPTestCases.parameters)
        self.assertIn('Electron saturation current', SLPTestCases.parameters)
        self.assertEqual(SLPTestCases.parameters['Electron saturation current'], SLPTestCases.parameters['Filtered current'][SLPTestCases.parameters['Plasma potential index']])
        self.assertGreater(SLPTestCases.parameters['Electron saturation current'],0, "Electron saturation current should be positive.")

    def test_4_get_electron_temperature(self):
        """Test the get_electron_temperature function"""
        
        slp_plasma_parameters.get_electron_temperature(SLPTestCases.parameters)
        self.assertIn('Electron temperature (eV)', SLPTestCases.parameters)
        self.assertIn('Electron temperature (Joules)', SLPTestCases.parameters)
        self.assertGreater(SLPTestCases.parameters['Electron temperature (eV)'], 0, "Electron temperature (eV) should be positive")
        self.assertGreater(SLPTestCases.parameters['Electron temperature (Joules)'], 0, "Electron temperature (Joules) should be a positive value.")
    
    def test_5_get_particle_density(self):
        """Test the get_particle_density global function"""
       
        global_parameters.get_particle_density(SLPTestCases.parameters)
        self.assertIn('Electron density', SLPTestCases.parameters)
        self.assertGreater(SLPTestCases.parameters['Electron density'], 0, "Electron density should be a positive value.")
        
    def test_6_get_debye_length(self):
        
        print()
    def test_7_get_number_of_electrons(self):
        print()
        
if __name__ == '__main__':
    unittest.main(verbosity=2)