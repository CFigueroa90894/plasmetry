import unittest
from BaseCase import BaseCase

class GlobalTestCases(BaseCase):    
    
    parameters = {}
    probe_equations = []
    
    @classmethod
    def set_parameters(cls, parameters):
        GlobalTestCases.parameters = parameters
        
    @classmethod
    def set_probe_type(cls, equations):
        GlobalTestCases.probe_equations = equations

    def test_1_filter_current(self):
        
        """Test the filter_current function"""
        for equation in GlobalTestCases.probe_equations:
            if 'filter_current' == equation.__name__:
                equation(GlobalTestCases.parameters)
                self.assertIn('Filtered current', GlobalTestCases.parameters)
                break

    def test_2_get_floating_and_plasma_potential(self):
        """Test the get_floating_and_plasma_potential function"""
        for equation in GlobalTestCases.probe_equations:
            if 'get_floating_and_plasma_potential' == equation.__name__:
                equation(GlobalTestCases.parameters)
                
                self.assertIn('Floating potential', GlobalTestCases.parameters)
                self.assertIn('Floating potential index', GlobalTestCases.parameters)
                self.assertIn('Plasma potential', GlobalTestCases.parameters)
                self.assertIn('Plasma potential index', GlobalTestCases.parameters)
        
                self.assertGreaterEqual(GlobalTestCases.parameters['Plasma potential'], 0, "Plasma potential should be non-negative")
                
                self.assertTrue(0 <= GlobalTestCases.parameters['Floating potential index'] <  GlobalTestCases.parameters['Plasma potential index'])
                self.assertTrue(GlobalTestCases.parameters['Floating potential index'] <= GlobalTestCases.parameters['Plasma potential index'] < len(GlobalTestCases.parameters['Bias']))
                break
            
    def test_3_get_electron_saturation_current(self):
        """Test the get_electron_saturation_current function"""

        for equation in GlobalTestCases.probe_equations:
            if 'get_electron_saturation_current' == equation.__name__:
                equation(GlobalTestCases.parameters)
                self.assertIn('Electron saturation current', GlobalTestCases.parameters)
                self.assertEqual(GlobalTestCases.parameters['Electron saturation current'], GlobalTestCases.parameters['Filtered current'][GlobalTestCases.parameters['Plasma potential index']])
                self.assertGreater(GlobalTestCases.parameters['Electron saturation current'],0, "Electron saturation current should be positive.")
                break
                
    def test_4_get_ion_saturation_current(self):
        """Test the get_electron_saturation_current function"""

        for equation in GlobalTestCases.probe_equations:
            if 'get_ion_saturation_current' == equation.__name__:
                equation(GlobalTestCases.parameters)
                self.assertIn('Ion saturation current', GlobalTestCases.parameters)
                self.assertLess(GlobalTestCases.parameters['Ion saturation current'],0, "Electron saturation current should be positive.")
                
    def test_5_get_electron_temperature(self):
        """Test the get_electron_temperature function"""
        for equation in GlobalTestCases.probe_equations:
            if 'get_electron_temperature' == equation.__name__:
                equation(GlobalTestCases.parameters)
                self.assertIn('Electron temperature (eV)', GlobalTestCases.parameters)
                self.assertIn('Electron temperature (Joules)', GlobalTestCases.parameters)
                self.assertGreater(GlobalTestCases.parameters['Electron temperature (eV)'], 0, "Electron temperature (eV) should be positive")
                self.assertGreater(GlobalTestCases.parameters['Electron temperature (Joules)'], 0, "Electron temperature (Joules) should be a positive value.")
                break
       
    def test_6_get_particle_density(self):
        """Test the get_particle_density global function"""
        for equation in GlobalTestCases.probe_equations:
            if 'get_particle_density' == equation.__name__:
                equation(GlobalTestCases.parameters)
                self.assertIn('Electron density', GlobalTestCases.parameters)
                self.assertGreater(GlobalTestCases.parameters['Electron density'], 0, "Electron density should be a positive value.")
                break
       
    def test_7_get_debye_length(self):
        print()
        
        
    def test_8_get_number_of_electrons(self):
        print()
        
if __name__ == '__main__':
    unittest.main(verbosity=2)