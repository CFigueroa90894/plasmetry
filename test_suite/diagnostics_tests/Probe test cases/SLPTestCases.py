from BaseCase import BaseCase
import sys 
import os
sys.path.insert(0, os.path.abspath('parameters'))

import slp_plasma_parameters

import unittest

class SLPTestCases(BaseCase):

    def test_filter_current(self):
        """Test the filter_current function"""
        slp_plasma_parameters.filter_current(self.parameters)
        self.assertIn('Filtered current', self.parameters)
      
    def test_get_particle_density(self):
        print('aaa')

    def test_get_floating_and_plasma_potential(self):
        """Test the get_floating_and_plasma_potential function"""
        
        slp_plasma_parameters.filter_current(self.parameters)
        slp_plasma_parameters.get_floating_and_plasma_potential(self.parameters)
        
        self.assertIn('Floating potential', self.parameters)
        self.assertIn('Floating potential index', self.parameters)
        self.assertIn('Plasma potential', self.parameters)
        self.assertIn('Plasma potential index', self.parameters)
        
        self.assertGreaterEqual(self.parameters['Plasma potential'], 0, "Plasma potential should be non-negative")
        
        self.assertTrue(0 <= self.parameters['Floating potential index'] <  self.parameters['Plasma potential index'])
        self.assertTrue(self.parameters['Floating potential index'] <= self.parameters['Plasma potential index'] < len(self.parameters['Bias']))

    def test_get_electron_saturation_current(self):
        """Test the get_electron_saturation_current function"""
        slp_plasma_parameters.filter_current(self.parameters)
        slp_plasma_parameters.get_floating_and_plasma_potential(self.parameters)
        slp_plasma_parameters.get_electron_saturation_current(self.parameters)
        self.assertIn('Electron saturation current', self.parameters)
        self.assertEqual(self.parameters['Electron saturation current'], self.parameters['Filtered current'][self.parameters['Plasma potential index']])
        self.assertGreaterEqual(self.parameters['Electron saturation current'], 0, "Electron saturation current should be non-negative")

    def test_get_electron_temperature(self):
        """Test the get_electron_temperature function"""
        slp_plasma_parameters.filter_current(self.parameters)
        slp_plasma_parameters.get_floating_and_plasma_potential(self.parameters)
        slp_plasma_parameters.get_electron_saturation_current(self.parameters)
        slp_plasma_parameters.get_electron_temperature(self.parameters)
        self.assertIn('Electron temperature (eV)', self.parameters)
        self.assertIn('Electron temperature (Joules)', self.parameters)
        self.assertGreater(self.parameters['Electron temperature (eV)'], 0, "Electron temperature (eV) should be positive")
        self.assertGreater(self.parameters['Electron temperature (Joules)'], 0, "Electron temperature (Joules) should be positive")
        
    def test_get_debye_length(self):
        print('aaa')
        
    def test_get_number_of_electrons(self):
        print('aaa')
        
if __name__ == '__main__':
    unittest.main(verbosity=2)